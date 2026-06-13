import tkinter as tk
from tkinter import ttk
import threading
from ui.theme import *
from core.scanner import NetworkScanner

class TabServices(tk.Frame):
    def __init__(self, parent, scan_data):
        super().__init__(parent, bg=BG_MAIN)
        self.scan_data = scan_data
        self.scanner = NetworkScanner()
        self._build_ui()

    def _build_ui(self):
        ctrl_frame = tk.Frame(self, bg=BG_CARD, bd=1, relief="solid")
        ctrl_frame.pack(fill="x", padx=PAD_L, pady=PAD_L)
        
        tk.Label(ctrl_frame, text="Cible :", bg=BG_CARD, fg=TEXT_PRIMARY, font=FONT_BODY).pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.entry_target = tk.Entry(ctrl_frame, font=FONT_BODY, width=30)
        self.entry_target.insert(0, "127.0.0.1")
        self.entry_target.pack(side="left", padx=PAD_M)
        
        self.var_vuln = tk.BooleanVar()
        tk.Checkbutton(ctrl_frame, text="Scripts Vulnérabilités", variable=self.var_vuln, bg=BG_CARD, font=FONT_BODY).pack(side="left", padx=PAD_M)
        
        self.btn_scan = tk.Button(ctrl_frame, text="Auditer Services", bg=GREEN, fg="white", font=FONT_BODY, command=self._start_scan)
        self.btn_scan.pack(side="left", padx=PAD_M, pady=PAD_M)
        
        self.lbl_status = tk.Label(ctrl_frame, text="Prêt.", bg=BG_CARD, fg=TEXT_SECONDARY, font=FONT_BODY)
        self.lbl_status.pack(side="left", padx=PAD_L)
        
        # Split horizontal
        paned = tk.PanedWindow(self, orient="vertical", bg=BORDER)
        paned.pack(fill="both", expand=True, padx=PAD_L, pady=(0, PAD_L))
        
        # Haut: Ports
        frame_top = tk.Frame(paned, bg=BG_MAIN)
        paned.add(frame_top, minsize=150)
        
        tk.Label(frame_top, text="Services & Ports ouverts", font=FONT_SUBTITLE, bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=PAD_S)
        self.tree = ttk.Treeview(frame_top, columns=("Port", "Proto", "État", "Service", "Version"), show="headings")
        self.tree.heading("Port", text="Port")
        self.tree.heading("Proto", text="Protocole")
        self.tree.heading("État", text="État")
        self.tree.heading("Service", text="Service")
        self.tree.heading("Version", text="Produit / Version")
        self.tree.pack(fill="both", expand=True)
        
        # Bas: Vulnérabilités
        frame_bot = tk.Frame(paned, bg=BG_MAIN)
        paned.add(frame_bot, minsize=150)
        
        tk.Label(frame_bot, text="Résultats des scripts Nmap (Vulnérabilités)", font=FONT_SUBTITLE, bg=BG_MAIN, fg=TEXT_PRIMARY).pack(anchor="w", pady=PAD_S)
        self.txt_vuln = tk.Text(frame_bot, font=FONT_DATA, bg="white", fg=TEXT_PRIMARY, height=10)
        self.txt_vuln.pack(fill="both", expand=True)

    def _start_scan(self):
        target = self.entry_target.get().strip()
        if not target: return
        
        self.btn_scan.config(state="disabled")
        self.lbl_status.config(text="Audit en cours...", fg=TEXT_PRIMARY)
        self.tree.delete(*self.tree.get_children())
        self.txt_vuln.delete("1.0", tk.END)
        
        t = threading.Thread(target=self._run_scan, args=(target, self.var_vuln.get()))
        t.daemon = True
        t.start()

    def _run_scan(self, target, vuln):
        results = self.scanner.service_audit(target, vuln_scripts=vuln)
        self.after(0, self._on_scan_complete, results)

    def _on_scan_complete(self, results):
        self.btn_scan.config(state="normal")
        self.lbl_status.config(text="Audit terminé.", fg=GREEN)
        
        # Maj des données partagées
        self.scan_data["services"] = results
        
        for p in results.get("ports", []):
            version_str = f"{p['product']} {p['version']}".strip()
            self.tree.insert("", "end", values=(p['port'], p['protocol'], p['state'], p['service'], version_str))
            
        for v in results.get("vulns", []):
            self.txt_vuln.insert(tk.END, f"=== PORT {v['port']} | SCRIPT: {v['script']} ===\n")
            self.txt_vuln.insert(tk.END, f"{v['output']}\n\n")
