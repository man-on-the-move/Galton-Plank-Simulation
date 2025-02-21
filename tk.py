import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import Tk, Button, Label, Frame, ttk, Entry, StringVar, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Arbre:
    def __init__(self,niveau):
        self.niveau=niveau
        self.arbre=self.creer_arbre(niveau)

    def creer_arbre(self,niveau):
        """Construit un arbre binaire de profondeur donnée avec des feuilles
        initialisées à 0."""
        if niveau==0:
            return [0,[],[]]
        return [None,Arbre(niveau-1),Arbre(niveau-1)]

    def est_vide(self):
        """Vérifie si un arbres est vide."""
        return self.niveau==0

    def est_feuille(self,arbre):
        """Vérifie si un nœud est une feuille."""
        return arbre==[]

    def inserer_bille(self,niveaux,position,distribution={}):
        """Fait tomber une bille dans l'arbre jusqu'à une feuille en respectant
         la loi binomiale. Cette fonction est dépendante de la fonction
         laisser_tomber_n_bille(self,nb_billes)"""
        if self.niveau==0:
            distribution[position]+=1
            return
        if random.random() < 0.5:
            self.arbre[1].inserer_bille( niveaux-1, position, distribution)
        else:
            self.arbre[2].inserer_bille( niveaux-1, position+1, distribution)

    def laisser_tomber_n_billes(self,nb_billes):
        """Simule la chute d'un nombre de billes dans l'arbre en les
        répartissant correctement. Cette fonction est dépendante de la fonction
        inserer_bille(self,niveaux,position,distribution={})"""

        distribution={}
        for i in range(0,self.niveau+1):
            distribution[i]=0
        for _ in range(nb_billes):
            self.inserer_bille(self.niveau,0,distribution)

        return distribution


class MyWindow(Tk):

    def __init__(self):
        # On appelle le constructeur parent
        super().__init__()
        
        self.nb_billes = StringVar()
        self.nb_colonnes = StringVar()
        self.figure = None 
        self.canva = None
        
        
        left_frame = Frame(self, bg='#FFFFFF', width = 200)
        left_frame.pack(side='left', fill='y')
        left_frame.pack_propagate(False)

        
        label = Label(self, text='Simulation de la planche de Galton',fg='black', bg='#0caded',justify='center')
        label.pack(side='top', fill='x')
    
        billes = Label(left_frame,text='Entrez le nombre de billes :')
        billes.pack(side = 'top', fill = 'x')
        self.nb_billes_entry = Entry(left_frame, textvariable = self.nb_billes)
        self.nb_billes_entry.pack(side='top')
        
        colonnes = Label(left_frame,text='Entrez le nombre de colonnes :')
        colonnes.pack(fill='x')
        self.nb_colonnes_entry = Entry(left_frame, textvariable = self.nb_colonnes)
        self.nb_colonnes_entry.pack(side='top')
        
        button = Button(left_frame, text='Valider',bg = '#0caded', command=self.run_simulation)
        button.pack(fill='x')
        
        self.billes_label = Label(left_frame, text="Nombre de billes : 0", fg="black")  # Label pour afficher le résultat
        self.billes_label.pack(fill='x')
        self.colonnes_label = Label(left_frame,text='Nombre de colonnes:0',fg='black')
        self.colonnes_label.pack(fill='x')
        
        self.graph_frame = Frame(self, bg='#f0f0f0')
        self.graph_frame.pack(side='right', expand=True, fill='both')
        
        self.geometry('900x600')
        self.title('Simulation planche de Galton')
        
        
        def afficher_graphe(self,distribution,n,nb_bille):
            # supression du graphique existant le cas échéant 
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            
            x=list(distribution.keys())
            y=list(distribution.values())

            n = max(x)
            nb_billes = sum(y)
            mu = n/2
            sigma = np.sqrt(n)/2

            x_gauss = np.linspace(min(x),max(x),100)
            y_gauss = (nb_billes/(sigma*np.sqrt(2*np.pi)))*np.exp(-((x_gauss - mu) ** 2) / (2 * sigma ** 2))

            self.figure, ax = plt.subplots(figsize=(6, 4))

            ax.bar(x, y, color='blue', alpha=0.6, label='Répartition des billes')
            ax.plot(x_gauss, y_gauss, color='red', linewidth=2, label='Courbe de Gauss')
            ax.xlabel('colonnes')
            ax.ylabel('Nombres de billes')
            ax.title('Simulation de la planche de galton')
            ax.legend()

            # Intégration du graphe dans Tkinter
            self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
            
    def run_simulation(self):     # gestionnaire d'événement
        try :
            # On récupère les entrées de l'utilisateur
            nb_billes = int(self.nb_billes.get().strip())
            nb_colonnes = int(self.nb_colonnes.get().strip())

            if nb_billes <= 0 :
                messagebox.showerror("Erreur", "Le nombre de billes doit être un entier positif.")
                return 
            if nb_colonnes <= 0:
                messagebox.showerror("Erreur", "Le nombre de colonnes doit être un entier positif.")
                return
            print('Nombre de billes :',nb_billes)
            
            # Mise à jour des labels
            self.billes_label.config(text=f"Nombre de billes : {nb_billes}")
            self.colonnes_label.config(text=f'Nombre de colonnes : {nb_colonnes}')
            
            arbre = Arbre(nb_colonnes - 1)  # On soustrait 1 car l'arbre a n-1 niveaux
            distribution = arbre.laisser_tomber_n_billes(nb_billes)

            self.afficher_graphe(distribution, nb_colonnes, nb_billes)
            
            self.nb_billes.set('')
            self.nb_colonnes.set('')
            
        except ValueError:
                    # Gestion des erreurs avec une boîte de message
                    messagebox.showerror("Erreur", "Veuillez entrer un nombre entier valide dans chaque champs avant de valider.")



# On crée notre fenêtre et on l'affiche
if __name__ == "__main__" :
    window = MyWindow()
    window.mainloop()

