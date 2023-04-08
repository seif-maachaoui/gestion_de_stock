#Importation des modules requis
from tkinter import *
from tkinter import ttk, messagebox
from database import *

# ------INTERFACE GRAPHIQUE------

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Boutique en ligne")
        self.geometry("800x600")

    #Une méthode pour créer un tableau treeview
    def create_treeview(self):  
        frame1 = Frame(self, bg='white')

        self.tableau = ttk.Treeview(frame1, columns=("nom", "description", "prix", "quantité", "catégorie"))
        self.tableau.heading("#0", text="ID")
        self.tableau.column("#0", width=50)
        self.tableau.heading("nom", text="Nom")
        self.tableau.column("nom", width=150)
        self.tableau.heading("description", text="Description")
        self.tableau.column("description", width=200)
        self.tableau.heading("prix", text="Prix")
        self.tableau.column("prix", width=100)
        self.tableau.heading("quantité", text="Quantité")
        self.tableau.column("quantité", width=100)
        self.tableau.heading("catégorie", text= "Catégorie")
        self.tableau.column("catégorie", width=100)

        #Je me connecte à ma base de donnée
        boutique.connexion('boutique')


        #Je récupère les données de la table produit
        cursor = boutique.cursor
        cursor.execute("SELECT * FROM produit")
        result = cursor.fetchall()

        #Pour chaque donnée dans le resultat de la requête, je les insère dans le tableau
        for data in result:
            self.tableau.insert("", "end", text=data[0], values=(data[1], data[2], data[3], data[4], data[5]))

        #positionnement du tableau dans la Frame
        self.tableau.pack(fill="both", expand=True)

        #affichage de la frame principale
        frame1.grid(row=0, column=0, padx=60, pady=30)

    #Une méthode pour les widgets
    def widgets(self):
        
        frame2 = Frame(self, bg='white')

        self.label_name = Label(frame2, text='Veuillez entrer un nom de produit :', bg="white", font=('Verdana', 10))
        self.entry_name = Entry(frame2, bg="white", font=('Verdana', 10))
        self.label_description = Label(frame2, text='Veuillez entrer une description :', bg="White", font=('Verdana', 10))
        self.entry_description = Entry(frame2, bg="White", font=('Verdana', 10))
        self.label_price = Label(frame2, text='Veuillez entrer un prix :', bg="White", font=('Verdana', 10))
        self.entry_price = Entry(frame2, bg="White", font=('Verdana', 10))
        self.label_quantity = Label(frame2, text='Veuillez entrer une quantité :', bg="White", font=('Verdana', 10))
        self.entry_quantity = Entry(frame2, bg="White", font=('Verdana', 10))

        self.label_name.grid(row=0, column=0, sticky='e')
        self.entry_name.grid(row=0, column=1, pady=10, padx=10)
        self.label_description.grid(row=1, column=0, sticky='e')
        self.entry_description.grid(row=1, column=1, pady=10, padx=10)
        self.label_price.grid(row=2, column=0, sticky='e')
        self.entry_price.grid(row=2, column=1, pady=10, padx=10)
        self.label_quantity.grid(row=3, column=0, sticky='e')
        self.entry_quantity.grid(row=3, column=1, pady=10, padx=10)
        

        button_add = Button(frame2, text='Ajouter', font=('Verdana', 12), bg='green', command=self.add_product)
        button_update = Button(frame2, text='Modifier', font=('Verdana', 12), bg='red', command=self.update_product)
        button_delete = Button(frame2, text='Supprimer', font=('Verdana', 12), bg='blue', command=self.delete_product)

        button_add.grid(row=4, column=0, pady=20, padx=20,)
        button_update.grid(row=4, column=1, pady=10, padx=20, sticky='w')
        button_delete.grid(row=4, column=2, pady=10, padx=20, sticky='e')

        #affichage de la frame principale
        frame2.grid(row=1, column=0, padx=60, pady=30)

    #Une méthode pour ajouter des produits 
    def add_product(self):
        name = self.entry_name.get()
        description = self.entry_description.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        if not name or not description or not price or not quantity:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")

        else:
            try:
                price = float(price)
                quantity = int(quantity)
                cursor = boutique.cursor
                cursor.execute("INSERT INTO produit (nom, description, prix, quantité) VALUES (%s, %s, %s, %s)", (name, description, price, quantity))
                boutique.my_db.commit()

                self.tableau.insert("", "end", values=(name, description, price, quantity, ""), text=cursor.lastrowid)
                self.entry_name.delete(0, END)
                self.entry_description.delete(0, END)
                self.entry_price.delete(0, END)
                self.entry_quantity.delete(0, END)

            except ValueError:
                messagebox.showerror("Erreur", "Le prix doit être un nombre.")

    #Une méthode pour mettre à jour des produits
    def update_product(self):
        # Je sélectionne un élément dans le Treeview
        selected_item = self.tableau.focus()
    
        # Je vérifie si un produit est sélectionné
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit.")
            return
        
        # Je récupére les informations du produit sélectionné
        item = self.tableau.item(selected_item)
        item_id = item["text"]
        item_values = item["values"]
        
        #Je récupére les nouvelles valeurs des champs d'entrée
        name = self.entry_name.get()
        description = self.entry_description.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        # Je vérifie si tous les champs sont remplis
        if not name or not description or not price or not quantity:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return

        # Je souhaite convertir le prix et la quantité en nombre
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Attention", "Le prix et la quantité doivent être des nombres.")
            return

        # J'éxécute la requête SQL pour mettre à jour les données
        cursor = boutique.cursor
        cursor.execute("UPDATE produit SET nom = %s, description = %s, prix = %s, quantité = %s WHERE id = %s",
                    (name, description, price, quantity, item_id))
        boutique.my_db.commit()

        # Je mets à jour les donnée dans le treeview
        self.tableau.item(selected_item, text=item_id, values=(name, description, price, quantity, item_values[4]))
  
    def delete_product(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit.")
        else:
            id = self.tableau.item(selection[0], 'text')
            cursor = boutique.cursor
            cursor.execute("DELETE FROM produit WHERE id=%s", (id,))
            boutique.my_db.commit()
            self.tableau.delete(selection)

    #je ferme la connexion à la base de données
    boutique.my_db.close()

                

            