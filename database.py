#Importation des modules requis
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

        try: #Tentative de jointure entre les deux tables.
            self.cursor.execute("SELECT p.nom, p.description, p.prix, p.quantité, c.nom \
            FROM produit p \
            INNER JOIN categorie c ON p.id_catégorie = c.id")
            products = self.cursor.fetchall()
            return products
        except mysql.connector.Error as error:
            print("Erreur lors de la récupération des produits avec leur catégorie : {}".format(error))
         
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
        self.my_db.close()
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