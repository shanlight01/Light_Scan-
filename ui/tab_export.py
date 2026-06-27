import tkinter as tk
from tkinter import messagebox, filedialog
from ui.theme import *
from core.exporter import export_json, export_csv, export_html

class TabExport(tk.Frame):
    def __init__(self, parent, scan_data):
        super().__init__(parent, bg=BG_MAIN)
        self.scan_data = scan_data
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Rapport et Export", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_PRIMARY).pack(pady=PAD_L)
        tk.Label(self, text="Sauvegardez les données accumulées en mémoire.", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_SECONDARY).pack()

        frame_btns = tk.Frame(self, bg=BG_MAIN)
        frame_btns.pack(pady=PAD_XL)

        btn_json = tk.Button(frame_btns, text="Exporter en JSON", font=FONT_BODY, bg=GREEN, fg="white", width=20, command=self._export_json)
        btn_json.pack(side="left", padx=PAD_M)

        btn_csv = tk.Button(frame_btns, text="Exporter en CSV", font=FONT_BODY, bg=GREEN, fg="white", width=20, command=self._export_csv)
        btn_csv.pack(side="left", padx=PAD_M)

        btn_html = tk.Button(frame_btns, text="Rapport HTML (Nouveau)", font=FONT_BODY, bg="#2980b9", fg="white", width=20, command=self._export_html)
        btn_html.pack(side="left", padx=PAD_M)
        
        self.lbl_info = tk.Label(self, text="", font=FONT_BODY, bg=BG_MAIN, fg=TEXT_PRIMARY)
        self.lbl_info.pack(pady=PAD_M)

    def _export_json(self):
        directory = filedialog.askdirectory(title="Choisir le dossier de destination")
        if directory:
            try:
                filepath = export_json(self.scan_data, directory)
                self.lbl_info.config(text=f"Export JSON réussi :\n{filepath}", fg=GREEN)
            except Exception as e:
                messagebox.showerror("Erreur d'export", str(e))

    def _export_csv(self):
        directory = filedialog.askdirectory(title="Choisir le dossier de destination")
        if directory:
            try:
                filepath = export_csv(self.scan_data, directory)
                self.lbl_info.config(text=f"Export CSV réussi :\n{filepath}", fg=GREEN)
            except Exception as e:
                messagebox.showerror("Erreur d'export", str(e))

    def _export_html(self):
        directory = filedialog.askdirectory(title="Choisir le dossier de destination")
        if directory:
            try:
                filepath = export_html(self.scan_data, directory)
                self.lbl_info.config(text=f"Rapport HTML généré avec succès :\n{filepath}", fg="#2980b9")
            except Exception as e:
                messagebox.showerror("Erreur d'export", str(e))
