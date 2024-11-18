import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Fichiers CSV
zones_file = "zones.csv"
data_file = "logistique.csv"

# Vérifie si le fichier des zones existe, sinon le crée avec des zones par défaut
if not os.path.exists(zones_file):
    with open(zones_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Zone"])
        default_zones = [
            "A - 1", "A - 2", "A - 3", "A - 4", "A - 5",
            "B - 1", "B - 2", "B - 3", "B - 4", "B - 5",
            "C - 1", "C - 2", "C - 3", "C - 4", "C - 5"
        ]
        for zone in default_zones:
            writer.writerow([zone])

# Vérifie si le fichier des affectations existe, sinon le crée avec des en-têtes
if not os.path.exists(data_file):
    with open(data_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Zone", "Element"])

# Fonctions de gestion des données
def ajouter_zone(zone):
    """Ajoute une nouvelle zone au fichier zones.csv"""
    if zone_existe(zone):
        messagebox.showerror("Erreur", f"La zone {zone} existe déjà.")
        return
    with open(zones_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([zone])
    messagebox.showinfo("Succès", f"La zone {zone} a été ajoutée.")
    charger_zones()

def ajouter_element(zone, element):
    """Ajoute un élément à une zone de rangement"""
    if not zone_existe(zone):
        messagebox.showerror("Erreur", f"La zone {zone} n'existe pas.")
        return
    with open(data_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([zone, element])
    messagebox.showinfo("Succès", f"Ajouté : {element} à la zone {zone}.")
    charger_elements()

def zone_existe(zone):
    """Vérifie si une zone existe dans le fichier zones.csv"""
    with open(zones_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        return any(row[0] == zone for row in reader)

def charger_zones():
    """Charge les zones dans la liste déroulante"""
    zone_list.delete(0, tk.END)
    with open(zones_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            zone_list.insert(tk.END, row[0])

def charger_elements():
    """Charge les éléments dans la vue"""
    for item in elements_tree.get_children():
        elements_tree.delete(item)
    with open(data_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            elements_tree.insert("", tk.END, values=row)

# Interface graphique
root = tk.Tk()
root.title("Gestion des zones de rangement")
root.geometry("800x600")

# Zone d'ajout d'une nouvelle zone
zone_frame = tk.Frame(root, padx=10, pady=10)
zone_frame.pack(fill="x", pady=5)
tk.Label(zone_frame, text="Nouvelle zone :").pack(side="left")
zone_entry = tk.Entry(zone_frame)
zone_entry.pack(side="left", padx=5)
tk.Button(zone_frame, text="Ajouter Zone", command=lambda: ajouter_zone(zone_entry.get())).pack(side="left", padx=5)

# Zone de sélection et ajout d'éléments
element_frame = tk.Frame(root, padx=10, pady=10)
element_frame.pack(fill="x", pady=5)
tk.Label(element_frame, text="Zone :").pack(side="left")
zone_list = tk.Listbox(element_frame, height=5, width=20)
zone_list.pack(side="left", padx=5)
tk.Label(element_frame, text="Élément :").pack(side="left")
element_entry = tk.Entry(element_frame)
element_entry.pack(side="left", padx=5)
tk.Button(element_frame, text="Ajouter Élément", command=lambda: ajouter_element(zone_list.get(tk.ACTIVE), element_entry.get())).pack(side="left", padx=5)

# Affichage des éléments
elements_frame = tk.Frame(root, padx=10, pady=10)
elements_frame.pack(fill="both", expand=True)
tk.Label(elements_frame, text="Contenu des zones :").pack(anchor="w")
columns = ("Zone", "Élément")
elements_tree = ttk.Treeview(elements_frame, columns=columns, show="headings")
elements_tree.heading("Zone", text="Zone")
elements_tree.heading("Élément", text="Élément")
elements_tree.pack(fill="both", expand=True)

# Charger les données au démarrage
charger_zones()
charger_elements()

# Lancer l'application
root.mainloop()
