import tkinter as tk
from ui.theme import *

class TabDashboard(tk.Frame):
    def __init__(self, parent, scan_data):
        super().__init__(parent, bg=BG_MAIN)
        self.scan_data = scan_data
        self._build_ui()
        self.bind("<Visibility>", self._refresh_dashboard)

    def _build_ui(self):
        # En-tête
        header = tk.Frame(self, bg=BG_MAIN)
        header.pack(fill="x", padx=PAD_L, pady=PAD_L)
        tk.Label(header, text="Tableau de Bord Global", font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_PRIMARY).pack(side="left")
        
        btn_refresh = tk.Button(header, text="Actualiser", font=FONT_BODY, command=self._refresh_dashboard)
        btn_refresh.pack(side="right")

        # Cartes compteurs
        cards_frame = tk.Frame(self, bg=BG_MAIN)
        cards_frame.pack(fill="x", padx=PAD_L)

        self.val_hosts = tk.StringVar(value="0")
        self.val_ports = tk.StringVar(value="0")
        self.val_vulns = tk.StringVar(value="0")

        self._create_card(cards_frame, "Hôtes Actifs", self.val_hosts).pack(side="left", expand=True, fill="both", padx=PAD_S)
        self._create_card(cards_frame, "Ports Ouverts", self.val_ports).pack(side="left", expand=True, fill="both", padx=PAD_S)
        self._create_card(cards_frame, "Vulnérabilités", self.val_vulns).pack(side="left", expand=True, fill="both", padx=PAD_S)

        # Graphiques (Canvas)
        graphs_frame = tk.Frame(self, bg=BG_MAIN)
        graphs_frame.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        self.canvas_os = tk.Canvas(graphs_frame, bg=BG_CARD, bd=1, relief="solid", highlightthickness=0)
        self.canvas_os.pack(side="left", expand=True, fill="both", padx=PAD_S)

        self.canvas_ports = tk.Canvas(graphs_frame, bg=BG_CARD, bd=1, relief="solid", highlightthickness=0)
        self.canvas_ports.pack(side="left", expand=True, fill="both", padx=PAD_S)

    def _create_card(self, parent, title, text_var):
        frame = tk.Frame(parent, bg=BG_CARD, bd=1, relief="solid")
        tk.Label(frame, text=title, font=FONT_SUBTITLE, bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(PAD_M, 0))
        tk.Label(frame, textvariable=text_var, font=FONT_BIG_STAT, bg=BG_CARD, fg=GREEN).pack(pady=(0, PAD_M))
        return frame

    def _refresh_dashboard(self, event=None):
        hosts_count = len([h for h in self.scan_data.get("hosts", []) if h.get("state") == "up"])
        ports_count = len([p for p in self.scan_data.get("services", {}).get("ports", []) if p.get("state") == "open"])
        vulns_count = len(self.scan_data.get("services", {}).get("vulns", []))

        self.val_hosts.set(str(hosts_count))
        self.val_ports.set(str(ports_count))
        self.val_vulns.set(str(vulns_count))

        self._draw_os_chart()
        self._draw_ports_chart()

    def _draw_os_chart(self):
        c = self.canvas_os
        c.delete("all")
        c.create_text(20, 20, text="Répartition des OS", font=FONT_SUBTITLE, anchor="nw", fill=TEXT_PRIMARY)
        
        os_results = self.scan_data.get("os_results", [])
        if not os_results:
            c.create_text(150, 150, text="Aucune donnée", fill=TEXT_SECONDARY)
            return

        counts = {}
        for r in os_results:
            name = r.get("os", "Inconnu")
            counts[name] = counts.get(name, 0) + 1

        total = sum(counts.values())
        start_angle = 0
        colors = ["#4caf50", "#2196f3", "#ff9800", "#e91e63", "#9c27b0", "#00bcd4"]
        
        y_legend = 50
        for i, (name, count) in enumerate(counts.items()):
            extent = (count / total) * 360
            color = colors[i % len(colors)]
            c.create_arc(50, 60, 250, 260, start=start_angle, extent=extent, fill=color, outline="white")
            
            # Legende
            c.create_rectangle(270, y_legend, 285, y_legend+15, fill=color, outline="white")
            c.create_text(295, y_legend+7, text=f"{name} ({count})", anchor="w", font=FONT_BODY, fill=TEXT_PRIMARY)
            
            start_angle += extent
            y_legend += 25

    def _draw_ports_chart(self):
        c = self.canvas_ports
        c.delete("all")
        c.create_text(20, 20, text="Ports ouverts", font=FONT_SUBTITLE, anchor="nw", fill=TEXT_PRIMARY)

        ports = [p for p in self.scan_data.get("services", {}).get("ports", []) if p.get("state") == "open"]
        if not ports:
            c.create_text(150, 150, text="Aucune donnée", fill=TEXT_SECONDARY)
            return

        # Très basique : dessine des barres pour la proportion des protocoles ou liste les ports
        # Comme on n'a peut-être pas plusieurs hosts dans services, on va juste lister
        c.create_text(20, 60, text="Liste des ports détectés :", font=FONT_BODY, anchor="nw", fill=TEXT_PRIMARY)
        y = 90
        for p in ports:
            c.create_text(30, y, text=f"• Port {p['port']}/{p['protocol']} - {p['service']}", font=FONT_DATA, anchor="nw", fill=TEXT_PRIMARY)
            y += 20
