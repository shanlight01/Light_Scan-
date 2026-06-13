import tkinter as tk
from tkinter import ttk
import threading
from ui.theme import *
from core.scanner import NetworkScanner

class TabHosts(tk.Frame):
    def __init__(self, parent, scan_data):
        super().__init__(parent, bg=BG_MAIN)
        self.scan_data = scan_data
        self.scanner = NetworkScanner()
        self._build_ui()

    def _build_ui(self):
        # Top panel pour les contrôles
        ctrl_frame = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid")
        ctrl_frame.pack(fill="x", padx=PAD_L, pady=PAD_L)
        
        tk.Label(ctrl_frame, text="Cible (ex: 192.168.1.0/24) :", bg=BG_CARD, fg=TEXT_PRIMARY, font=FONT_BODY).pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.entry_target = tk.Entry(ctrl_frame, font=FONT_BODY, width=30)
        self.entry_target.insert(0, "127.0.0.1")
        self.entry_target.pack(side="left", padx=PAD_M)
        
        self.btn_scan = tk.Button(ctrl_frame, text="Lancer le Scan", bg=GREEN, fg="white", font=FONT_BODY, command=self._start_scan)
        self.btn_scan.pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.lbl_status = tk.Label(ctrl_frame, text="Prêt.", bg=BG_CARD, fg=TEXT_SECONDARY, font=FONT_BODY)
        self.lbl_status.pack(side="left", padx=PAD_L)
        
        # Tableau des résultats
        self.tree = ttk.Treeview(self, columns=("IP", "Hostname", "MAC", "Statut"), show="headings")
        self.tree.heading("IP", text="Adresse IP")
        self.tree.heading("Hostname", text="Nom d'hôte")
        self.tree.heading("MAC", text="Adresse MAC")
        self.tree.heading("Statut", text="Statut")
        self.tree.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))

    def _start_scan(self):
        target = self.entry_target.get().strip()
        if not target: return
        
        self.btn_scan.config(state="disabled")
        self.lbl_status.config(text="Scan en cours...", fg=TEXT_PRIMARY)
        self.tree.delete(*self.tree.get_children())
        
        t = threading.Thread(target=self._run_scan, args=(target,))
        t.daemon = True
        t.start()

    def _run_scan(self, target):
        results = self.scanner.host_discovery(target)
        self.after(0, self._on_scan_complete, results)

    def _on_scan_complete(self, results):
        self.btn_scan.config(state="normal")
        self.lbl_status.config(text=f"Terminé. {len(results)} hôte(s) trouvé(s).", fg=GREEN)
        
        # Mise à jour des données globales
        self.scan_data["hosts"] = results
        
        for h in results:
            self.tree.insert("", "end", values=(h['ip'], h['hostname'], h['mac'], h['state']))
