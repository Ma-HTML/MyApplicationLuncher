import os
import threading
import tkinter as tk
from tkinter import scrolledtext

def search_executable(executable_name):
    # Cachons les boutons et affichons le message "Démarrage du logiciel..."
    for widget in button_frame.winfo_children():
        widget.pack_forget()  # Cache les boutons
    status_label.config(text="Démarrage du logiciel...", fg="#f39c12")
    
    log_area.delete('1.0', tk.END)
    log_area.insert(tk.END, f"Recherche de {executable_name}...\n")
    
    found_path = None
    
    # Dossiers prioritaires à explorer
    priority_folders = [
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]
    
    # Fonction pour explorer un répertoire et ses sous-dossiers
    def explore_directory(directory):
        nonlocal found_path
        if found_path:  # Si le fichier est déjà trouvé, on arrête la recherche
            return
        for root, dirs, files in os.walk(directory):
            log_area.insert(tk.END, f"Vérification: {root}\n")
            log_area.yview(tk.END)
            app.update()  # Force la mise à jour de l'interface
            files_verified.insert(tk.END, f"Vérification: {root}\n")  # Affiche dans la zone de texte
            # Privilégier les fichiers .exe
            if executable_name.lower() in [file.lower() for file in files if file.endswith('.exe')]:
                found_path = os.path.join(root, executable_name)
                break

    # Prioriser les dossiers "Program Files"
    for folder in priority_folders:
        if found_path:
            break
        if os.path.exists(folder):
            explore_directory(folder)
    
    # Si le programme n'a pas été trouvé dans les dossiers prioritaires, on explore le reste du système
    if not found_path:
        for root, dirs, files in os.walk("C:\\"):
            files_verified.insert(tk.END, f"Vérification: {root}\n")  # Affiche dans la zone de texte
            # Privilégier les fichiers .exe
            if executable_name.lower() in [file.lower() for file in files if file.endswith('.exe')]:
                found_path = os.path.join(root, executable_name)
                break
    
    if found_path:
        log_area.insert(tk.END, f"\nTrouvé: {found_path}\nLancement...\n")
        status_label.config(text="Lancement en cours...", fg="#f39c12")
        app.update()  # Mise à jour de l'interface avant de lancer l'application
        
        print(f"Lancement de {found_path}")  # Pour vérifier si le chemin est correct
        os.startfile(found_path)
        
        # Attente que l'application s'ouvre (cela peut être optimisé, ici on attend simplement)
        log_area.insert(tk.END, "Application lancée\n")
        log_area.yview(tk.END)
        
        # Retour à la page d'accueil après un délai de quelques secondes
        app.after(3000, show_home_page)  # Retour à la page d'accueil après 3 secondes
    else:
        log_area.insert(tk.END, "Application introuvable\n")
    
def show_home_page():
    # Réafficher les boutons et réinitialiser l'état
    for widget in button_frame.winfo_children():
        widget.pack_forget()  # Cache les boutons
    status_label.config(text="Prêt à démarrer", fg="white")
    # Réafficher les boutons
    for app_name in apps:
        btn = tk.Button(button_frame, text=f"Lancer {app_name}", command=lambda a=app_name: launch_search(a), **button_style)
        btn.pack(pady=10)

    # Réinitialiser les zones de logs
    log_area.delete('1.0', tk.END)
    files_verified.delete('1.0', tk.END)
    
    restart_button.pack_forget()  # Masque le bouton de redémarrage

def launch_search(executable_name):
    print(f"Recherche de {executable_name} lancée...")  # Vérification
    threading.Thread(target=search_executable, args=(executable_name,), daemon=True).start()

# Configuration de l'interface Tkinter
app = tk.Tk()
app.title("Launcher d'Applications")
app.geometry("500x500")  # Taille fixe de la fenêtre
app.config(bg="#2c3e50")  # Couleur de fond moderne (gris foncé)

# Style des boutons
button_style = {
    "bg": "#3498db",  # Bleu clair
    "fg": "white",  # Texte blanc
    "font": ("Helvetica", 12, "bold"),
    "relief": "flat",
    "padx": 20,
    "pady": 10,
    "width": 20
}

# Frame pour les boutons avec espacement et alignement
button_frame = tk.Frame(app, bg="#2c3e50")
button_frame.pack(pady=20)

# Liste des applications à lancer
apps = ["brave.exe", "Discord.exe", "Spotify.exe", "Code.exe", "TLauncher.exe"]
for app_name in apps:
    btn = tk.Button(button_frame, text=f"Lancer {app_name}", command=lambda a=app_name: launch_search(a), **button_style)
    btn.pack(pady=10)

# Zone de texte pour afficher les logs, avec style moderne
log_area = scrolledtext.ScrolledText(app, height=10, width=60, font=("Helvetica", 10), bg="#34495e", fg="white", insertbackground="white", bd=0)
log_area.pack(padx=20, pady=10)

# Zone de texte pour afficher les fichiers vérifiés
files_verified = tk.Text(app, height=10, width=60, font=("Helvetica", 10), bg="white", fg="black", bd=0)
files_verified.pack(padx=20, pady=10)

# Ajouter un titre en haut de la fenêtre
title_label = tk.Label(app, text="Launcher d'Applications", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white")
title_label.pack(pady=20)

# Label pour afficher le statut du démarrage
status_label = tk.Label(app, text="Prêt à démarrer", font=("Helvetica", 14), bg="#2c3e50", fg="white")
status_label.pack(pady=10)

# Bouton pour relancer la recherche
restart_button = tk.Button(app, text="Relancer la recherche", command=lambda: app.quit(), **button_style)

# Démarrer l'interface graphique
app.mainloop()
