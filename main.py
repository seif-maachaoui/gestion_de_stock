#Importation des modules requis
from tkinter import *
from tkinter import ttk
import mysql.connector

#Je commence par créer une classe Boutique
class Boutique:
    #fonction constructeur
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.my_db = None
        self.cursor = None

    #Méthode de création de base de donnée
    def create_database(self):
        cursor = self.my_db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS boutique")
        cursor.close()
        print("La base de données a été créée avec succès.")

    #Méthode de connexion à la base de donnée boutique
    def connexion(self, database):
        self.my_db = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=database
        )
        self.cursor = self.my_db.cursor()

    #Méthode pour la création des tables produit & categorie
    def create_tables(self):
    
        try: #Tentative de création de la table produit
            self.cursor.execute("CREATE TABLE IF NOT EXISTS produit(id INT AUTO_INCREMENT PRIMARY KEY,\
            nom VARCHAR(255),\
            description TEXT,\
            prix INT,\
            quantité INT,\
            id_catégorie INT)")
        except mysql.connector.errors.ProgrammingError: #Si la table existe déjà, alors...
            print("La table produit existe déjà")

        try: #Tentative de création de la table catégorie
            self.cursor.execute("CREATE TABLE IF NOT EXISTS categorie(id INT AUTO_INCREMENT PRIMARY KEY,\
            nom VARCHAR(255))")
        except mysql.connector.errors.ProgrammingError: #Si la table existe déjà, alors...
            print("La table categorie existe déjà")
    
        #Une méthode pour insérer des produits au sein de ma table produit.
    def insert_products(self):
        self.cursor.execute("SELECT * FROM produit")
        products = self.cursor.fetchall()

        #Si il n'y a pas de produits alors...
        if not products:
            #Si le contenu des colonnes affiché est vide, alors...
            self.cursor.execute("INSERT INTO produit(id, nom, description, prix, quantité, id_catégorie) \
            VALUES (NULL, 'Samsung Galaxy S22 Ultra', 'Un smartphone haut de gamme', 1259, 50, 1), \
            (NULL, 'Samsung Galaxy S22', 'Un bon rapport qualité prix', 749, 100, 1), \
            (NULL, 'Galaxy Book3 Ultra', 'Une puissance à couper le souffle', 3299, 20, 2), \
            (NULL, 'TV OLED 4K', 'Des couleurs intenses', 2399, 80, 3)")
            print("Ajout des nouveaux produits")
        else:
            print("Les produits existent déjà")
        
        self.my_db.commit() #Sauvegarde de la base de donnée

    #Une méthode pour insérer des catégories au sein de ma table catégorie
    def insert_categories(self):
        self.cursor.execute("SELECT * FROM categorie")
        categories = self.cursor.fetchall()

        # Si il n'y a pas de catégories, alors...
        if not categories:
            self.cursor.execute("INSERT INTO categorie(id, nom) VALUES \
            (1, 'Smartphone'), \
            (2, 'Ordinateur portable'), \
            (3, 'Téléviseurs')")
            print("Ajout des nouvelles catégories")
        else:
            print('Il existe déjà des catégories de produits')

        self.my_db.commit() #Sauvegarde de la base de donnée

        
#Création d'un objet Boutique
boutique = Boutique("localhost", "seifeddine", "Cyberpunk2077*")

#Connexion à la base de données boutique
boutique.connexion("boutique")

#Création des tables produit et categorie au sein de la base de donnée boutique
boutique.create_tables()

#Ajout de nouveaux produits
boutique.insert_products()

#Ajout des nouvelles catégories
boutique.insert_categories()

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
        label_name_entry = Entry(frame1, bg="white", font=('Verdana', 10))
        
        label_description = Label(frame1, text='Veuillez entrer une description :', bg="White", font=('Verdana', 10))
        label_description_entry = Entry(frame1, bg="White", font=('Verdana', 10))

        label_price = Label(frame1, text='Veuillez entrer un prix :', bg="White", font=('Verdana', 10))
        label_price_entry = Entry(frame1, bg="White", font=('Verdana', 10))

        label_quantity = Label(frame1, text='Veuillez entrer une quantité :', bg="White", font=('Verdana', 10))
        label_quantity_entry = Entry(frame1, bg="White", font=('Verdana', 10))

        button_add = Button(frame1, text='Ajouter', font=('Verdana', 12))
        button_delete = Button(frame1, text='Supprimer', font=('Verdana', 12))
        button_update = Button(frame1, text='Modifier', font=('Verdana', 12))

        
        # ------PLACEMENT DES CHAMPS DE TEXTE ET DES BOUTONS------
        
        label_name.grid(row=0, column=0, sticky='e')
        label_name_entry.grid(row=0, column=1, pady=10, padx=10)

        label_description.grid(row=1, column=0, sticky='e')
        label_description_entry.grid(row=1, column=1, pady=10, padx=10)

        label_price.grid(row=2, column=0, sticky='e')
        label_price_entry.grid(row=2, column=1, pady=10, padx=10)

        label_quantity.grid(row=3, column=0, sticky='e')
        label_quantity_entry.grid(row=3, column=1, pady=10, padx=10)

        label_price.grid(row=4, column=0, sticky='e')
        label_price_entry.grid(row=4, column=1, pady=10, padx=10)

        button_add.grid(row=5, column=0, pady=20, padx=20,)
        button_delete.grid(row=5, column=1, pady=20, padx=20, sticky='w')
        button_update.grid(row=5, column=2, pady=20, padx=20, sticky='e')

        #Placement de ma première frame dans mon interface graphique
        frame1.grid(row=0, column=0, padx=30, pady=30)

        #frame secondaire, qui contiendra l'affichage de la table produit
        frame2 = Frame(self, bg='white')

        #Création du tableau d'affichage de ma table produit
        tableau = ttk.Treeview(frame2, columns=("nom", "description", "prix", "quantité"))
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

        #Connexion à ma base de donnée Boutique
        boutique.connexion("boutique")

        #positionnement du tableau dans la Frame
        tableau.pack(fill="both", expand=True)

        #Placement de la deuxième frame dans mon interface
        frame2.grid(row=1, column=0, padx=100, pady=30)


#Appel de l'interface
window = Interface()
window.mainloop()






