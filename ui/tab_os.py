import tkinter as tk
from tkinter import ttk
import threading
from ui.theme import *
from core.scanner import NetworkScanner

class TabOS(tk.Frame):
    def __init__(self, parent, scan_data):
        super().__init__(parent, bg=BG_MAIN)
        self.scan_data = scan_data
        self.scanner = NetworkScanner()
        self._build_ui()

    def _build_ui(self):
        ctrl_frame = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid")
        ctrl_frame.pack(fill="x", padx=PAD_L, pady=PAD_L)
        
        tk.Label(ctrl_frame, text="Cible IP :", bg=BG_CARD, fg=TEXT_PRIMARY, font=FONT_BODY).pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.entry_target = tk.Entry(ctrl_frame, font=FONT_BODY, width=30)
        self.entry_target.insert(0, "127.0.0.1")
        self.entry_target.pack(side="left", padx=PAD_M)
        
        self.btn_scan = tk.Button(ctrl_frame, text="Identifier OS", bg=GREEN, fg="white", font=FONT_BODY, command=self._start_scan)
        self.btn_scan.pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.lbl_status = tk.Label(ctrl_frame, text="Prêt.", bg=BG_CARD, fg=TEXT_SECONDARY, font=FONT_BODY)
        self.lbl_status.pack(side="left", padx=PAD_L)
        
        self.tree = ttk.Treeview(self, columns=("IP", "OS", "Précision", "CPE"), show="headings")
        self.tree.heading("IP", text="Adresse IP")
        self.tree.heading("OS", text="Système d'Exploitation")
        self.tree.heading("Précision", text="Précision (%)")
        self.tree.heading("CPE", text="CPE")
        self.tree.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))

    def _start_scan(self):
        target = self.entry_target.get().strip()
        if not target: return
        
        self.btn_scan.config(state="disabled")
        self.lbl_status.config(text="Analyse OS en cours (peut être long)...", fg=TEXT_PRIMARY)
        self.tree.delete(*self.tree.get_children())
        
        t = threading.Thread(target=self._run_scan, args=(target,))
        t.daemon = True
        t.start()

    def _run_scan(self, target):
        results = self.scanner.os_fingerprint(target)
        self.after(0, self._on_scan_complete, results)

    def _on_scan_complete(self, results):
        self.btn_scan.config(state="normal")
        self.lbl_status.config(text=f"Terminé. {len(results)} résultat(s).", fg=GREEN)
        
        # Ajout aux données globales
        self.scan_data["os_results"].extend(results)
        
        for r in results:
            self.tree.insert("", "end", values=(r['ip'], r['os'], r['accuracy'], r['cpe']))
