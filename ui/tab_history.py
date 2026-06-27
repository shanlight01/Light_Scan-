import tkinter as tk
from tkinter import ttk
from ui.theme import *
from database.models import get_all_scans

class TabHistory(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MAIN)
        self._build_ui()
        # Actualiser la liste chaque fois que l'onglet est affiché
        self.bind("<Visibility>", self._refresh_history)

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(fill="x", padx=PAD_L, pady=PAD_L)
        
        tk.Label(header, text="Historique des Scans (MySQL)", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_PRIMARY).pack(side="left")
        
        btn_refresh = tk.Button(header, text="Actualiser", bg=BG_CARD, fg=TEXT_PRIMARY, font=FONT_BODY, command=self._refresh_history)
        btn_refresh.pack(side="right")
        
        # Tableau pour afficher l'historique
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Cible", "Statut"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date du Scan")
        self.tree.heading("Cible", text="Cible")
        self.tree.heading("Statut", text="Statut / Résultat")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=150)
        self.tree.column("Cible", width=150)
        self.tree.column("Statut", width=300)
        
        self.tree.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))

    def _refresh_history(self, event=None):
        """Récupère les données depuis MySQL et met à jour le tableau"""
        # On vide le tableau actuel
        self.tree.delete(*self.tree.get_children())
        
        # On récupère depuis la BDD
        scans = get_all_scans()
        
        # On insère les nouvelles lignes
        for s in scans:
            self.tree.insert("", "end", values=(s.get('id', ''), s.get('scan_date', ''), s.get('target', ''), s.get('status', '')))
