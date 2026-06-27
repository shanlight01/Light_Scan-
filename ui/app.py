import tkinter as tk
from tkinter import ttk
from ui.theme import *
from ui.tab_hosts import TabHosts
from ui.tab_os import TabOS
from ui.tab_services import TabServices
from ui.tab_export import TabExport
from ui.tab_dashboard import TabDashboard
from ui.tab_history import TabHistory

class App(tk.Tk):
    # Constructeur de la classe App, appelé lors de l'instanciation
    def __init__(self):
        super().__init__()
        # Titre de la fenêtre principale
        self.title("LIGHT_SCAN - Audit Réseau")
        # Dimensions de la fenêtre (largeur x hauteur)
        self.geometry("1000x700")
        # Couleur de fond principale
        self.configure(bg=BG_MAIN)

        
        # Données partagées en mémoire (pas de BDD externe)
        # Ces données seront alimentées par les différents onglets de scan
        self.scan_data = {
            "hosts": [],
            "os_results": [],
            "services": {
                "ports": [],
                "vulns": []
            }
        }
        
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_HEADER, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🛡️ LIGHT_SCAN", font=FONT_TITLE, bg=BG_HEADER, fg=TEXT_PRIMARY).pack(side="left", padx=PAD_L)
        tk.Label(header, text="Audit & Test d'Intrusion Réseau", font=FONT_BODY, bg=BG_HEADER, fg=TEXT_SECONDARY).pack(side="right", padx=PAD_L)

        # Notebook (Onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=PAD_M, pady=PAD_M)
        
        # Initialisation des onglets
        self.tab_hosts = TabHosts(self.notebook, self.scan_data)
        self.tab_os = TabOS(self.notebook, self.scan_data)
        self.tab_services = TabServices(self.notebook, self.scan_data)
        self.tab_export = TabExport(self.notebook, self.scan_data)
        self.tab_dashboard = TabDashboard(self.notebook, self.scan_data)
        self.tab_history = TabHistory(self.notebook)
        
        self.notebook.add(self.tab_hosts, text="📍 Inventaire (Hosts)")
        self.notebook.add(self.tab_os, text="💻 OS Fingerprint")
        self.notebook.add(self.tab_services, text="🔍 Services & Vulns")
        self.notebook.add(self.tab_history, text="🗄️ Historique MySQL")
        self.notebook.add(self.tab_export, text="💾 Rapport & Export")
        self.notebook.add(self.tab_dashboard, text="📊 Tableau de Bord")
