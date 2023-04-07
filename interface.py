#Importation des modules requis
from tkinter import *
from tkinter import ttk
from database import *

# ------INTERFACE GRAPHIQUE------

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Boutique en ligne")
        self.geometry("800x600")

        #Frame principal qui contiendra les boutons pour ajouter, supprimer, modifier des produits
        frame1 = Frame(self, bg='white')

        #------MISE EN PLACE DES CHAMPS DE TEXTE ET DES BOUTONS D'ACTION------

        label_name = Label(frame1, text='Veuillez entrer un nom de produit :', bg="white", font=('Verdana', 10))
        entry_name = Entry(frame1, bg="white", font=('Verdana', 10))
        
        label_description = Label(frame1, text='Veuillez entrer une description :', bg="White", font=('Verdana', 10))
        entry_description = Entry(frame1, bg="White", font=('Verdana', 10))

        label_price = Label(frame1, text='Veuillez entrer un prix :', bg="White", font=('Verdana', 10))
        entry_price = Entry(frame1, bg="White", font=('Verdana', 10))

        label_quantity = Label(frame1, text='Veuillez entrer une quantité :', bg="White", font=('Verdana', 10))
        entry_quantity = Entry(frame1, bg="White", font=('Verdana', 10))

            #Je rajoute une méthode pour ajouter des produits
        def add_product(self):
            #Je récupère les champs d'entrée et les stock dans des variables
            name = self.entry_name.get()
            description = self.entry_description.get()
            price = self.entry_price.get()
            quantity = self.entry_quantity.get()

            boutique.cursor.execute("INSERT INTO 'produit'('nom', 'description', 'prix', 'quantité') \
            VALUES (%s, %s, %s, %s)", (name, description, price, quantity))
            boutique.my_db.commit()     

            # Ajouter les valeurs au TreeView
            product = (name, description, price, quantity)
            tableau.insert('', 'end', values=product)

        button_add = Button(frame1, text='Ajouter', font=('Verdana', 12), bg='green', command=add_product)

        

        button_delete = Button(frame1, text='Supprimer', font=('Verdana', 12), bg='blue')
        button_update = Button(frame1, text='Modifier', font=('Verdana', 12), bg='red')

        
        # ------PLACEMENT DES CHAMPS DE TEXTE ET DES BOUTONS------
        
        label_name.grid(row=0, column=0, sticky='e')
        entry_name.grid(row=0, column=1, pady=10, padx=10)

        label_description.grid(row=1, column=0, sticky='e')
        entry_description.grid(row=1, column=1, pady=10, padx=10)

        label_price.grid(row=2, column=0, sticky='e')
        entry_price.grid(row=2, column=1, pady=10, padx=10)

        label_quantity.grid(row=3, column=0, sticky='e')
        entry_quantity.grid(row=3, column=1, pady=10, padx=10)

        button_add.grid(row=4, column=0, pady=20, padx=20,)
        button_delete.grid(row=4, column=1, pady=20, padx=20, sticky='w')
        button_update.grid(row=4, column=2, pady=20, padx=20, sticky='e')

        #Placement de ma première frame dans mon interface graphique
        frame1.grid(row=0, column=0, padx=30, pady=30)

        #frame secondaire, qui contiendra l'affichage de la table produit
        frame2 = Frame(self, bg='white')

        #Création du tableau d'affichage de ma table produit
        tableau = ttk.Treeview(frame2, columns=("nom", "description", "prix", "quantité", "catégorie"))
        tableau.heading("#0", text="ID")
        tableau.column("#0", width=50)
        tableau.heading("nom", text="Nom")
        tableau.column("nom", width=150)
        tableau.heading("description", text="Description")
        tableau.column("description", width=200)
        tableau.heading("prix", text="Prix")
        tableau.column("prix", width=100)
        tableau.heading("quantité", text="Quantité")
        tableau.column("quantité", width=100)
        tableau.heading("catégorie", text= "Catégorie")
        tableau.column("catégorie", width=100)

        #Je me connecte à ma base de donnée
        boutique.connexion('boutique')

        #Je récupère les données de la table produit et je réalise une jointure avec la table categeorie
        cursor = boutique.cursor
        cursor.execute("SELECT * FROM produit")
        result = cursor.fetchall()

        #Pour chaque donnée dans le resultat de la requête, je les insère dans le tableau
        for data in result:
            tableau.insert("", "end", text=data[0], values=(data[1], data[2], data[3], data[4], data[5]))

        #positionnement du tableau dans la Frame
        tableau.pack(fill="both", expand=True)

        #Placement de la deuxième frame dans mon interface
        frame2.grid(row=1, column=0, padx=60, pady=30)

    
    







