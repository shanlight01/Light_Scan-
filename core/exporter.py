# =============================================================================
#  LIGHT_SCAN — Module d'export (JSON / CSV)
#  Utilise uniquement les modules standard Python
# =============================================================================

import json
import csv
import os
from datetime import datetime


def _timestamp() -> str:
    """Retourne un horodatage au format YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_json(data: dict, directory: str) -> str:
    """Exporte les données de scan au format JSON.
    
    Args:
        data: Dictionnaire contenant les résultats de scan.
        directory: Dossier de destination.
    
    Returns:
        Le chemin du fichier créé.
    """
    os.makedirs(directory, exist_ok=True)
    filename = f"rapport_{_timestamp()}.json"
    filepath = os.path.join(directory, filename)

    export_data = {
        "outil": "LIGHT_SCAN",
        "date": datetime.now().isoformat(),
        "resultats": data,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    return filepath


def export_csv(data: dict, directory: str) -> str:
    """Exporte les données de scan au format CSV.
    
    Args:
        data: Dictionnaire contenant les résultats de scan.
        directory: Dossier de destination.
    
    Returns:
        Le chemin du fichier créé.
    """
    os.makedirs(directory, exist_ok=True)
    filename = f"rapport_{_timestamp()}.csv"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # --- Hôtes ---
        if "hosts" in data and data["hosts"]:
            writer.writerow(["=== INVENTAIRE DES HÔTES ==="])
            writer.writerow(["IP", "Hostname", "MAC", "État"])
            for h in data["hosts"]:
                writer.writerow([h.get("ip"), h.get("hostname"), h.get("mac"), h.get("state")])
            writer.writerow([])

        # --- OS ---
        if "os_results" in data and data["os_results"]:
            writer.writerow(["=== IDENTIFICATION OS ==="])
            writer.writerow(["IP", "OS", "Précision (%)", "CPE"])
            for o in data["os_results"]:
                writer.writerow([o.get("ip"), o.get("os"), o.get("accuracy"), o.get("cpe")])
            writer.writerow([])

        # --- Ports / Services ---
        if "services" in data:
            if data["services"].get("ports"):
                writer.writerow(["=== SERVICES & PORTS ==="])
                writer.writerow(["Port", "Protocole", "État", "Service", "Produit", "Version"])
                for p in data["services"]["ports"]:
                    writer.writerow([
                        p.get("port"), p.get("protocol"), p.get("state"),
                        p.get("service"), p.get("product"), p.get("version"),
                    ])
                writer.writerow([])

            if data["services"].get("vulns"):
                writer.writerow(["=== VULNÉRABILITÉS ==="])
                writer.writerow(["Port", "Script", "Résultat"])
                for v in data["services"]["vulns"]:
                    writer.writerow([v.get("port"), v.get("script"), v.get("output")])

    return filepath


def export_html(data: dict, directory: str) -> str:
    """Exporte les données de scan au format HTML (Rapport moderne)."""
    os.makedirs(directory, exist_ok=True)
    filename = f"rapport_{_timestamp()}.html"
    filepath = os.path.join(directory, filename)

    nb_hosts = len(data.get("hosts", []))
    nb_ports = len(data.get("services", {}).get("ports", []))
    nb_vulns = len(data.get("services", {}).get("vulns", []))
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport d'Audit - Light Scan</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 30px; }}
        .summary {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .card {{ background: #ecf0f1; padding: 20px; border-radius: 6px; flex: 1; text-align: center; }}
        .card h3 {{ margin: 0 0 10px 0; color: #7f8c8d; font-size: 14px; text-transform: uppercase; }}
        .card .value {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
        .vuln-val {{ color: #e74c3c !important; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: #fff; font-weight: 600; }}
        tr:hover {{ background-color: #f1f2f6; }}
        .footer {{ margin-top: 40px; text-align: center; color: #95a5a6; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Rapport d'Audit - Light Scan</h1>
        <p>Généré le : <strong>{date_str}</strong></p>
        
        <div class="summary">
            <div class="card"><h3>Hôtes Actifs</h3><div class="value">{nb_hosts}</div></div>
            <div class="card"><h3>Ports Ouverts</h3><div class="value">{nb_ports}</div></div>
            <div class="card"><h3>Vulnérabilités</h3><div class="value vuln-val">{nb_vulns}</div></div>
        </div>
"""

    if data.get("hosts"):
        html += "<h2>1. Inventaire des Hôtes</h2><table><tr><th>IP</th><th>Hostname</th><th>MAC</th><th>État</th></tr>"
        for h in data["hosts"]:
            html += f"<tr><td>{h.get('ip','')}</td><td>{h.get('hostname','')}</td><td>{h.get('mac','')}</td><td>{h.get('state','')}</td></tr>"
        html += "</table>"

    if data.get("os_results"):
        html += "<h2>2. Identification OS</h2><table><tr><th>IP</th><th>Système d'Exploitation</th><th>Précision</th></tr>"
        for o in data["os_results"]:
            html += f"<tr><td>{o.get('ip','')}</td><td>{o.get('os','')}</td><td>{o.get('accuracy','')}%</td></tr>"
        html += "</table>"

    if data.get("services", {}).get("ports"):
        html += "<h2>3. Services & Ports</h2><table><tr><th>Port</th><th>Proto</th><th>État</th><th>Service</th><th>Produit</th><th>Version</th></tr>"
        for p in data["services"]["ports"]:
            html += f"<tr><td>{p.get('port','')}</td><td>{p.get('protocol','')}</td><td>{p.get('state','')}</td><td>{p.get('service','')}</td><td>{p.get('product','')}</td><td>{p.get('version','')}</td></tr>"
        html += "</table>"

    if data.get("services", {}).get("vulns"):
        html += "<h2>4. Vulnérabilités Détectées</h2><table><tr><th>Port</th><th>Script</th><th>Résultat</th></tr>"
        for v in data["services"]["vulns"]:
            output = v.get('output', '').replace('\n', '<br>')
            html += f"<tr><td>{v.get('port','')}</td><td>{v.get('script','')}</td><td><pre style='margin:0;font-family:inherit;'>{output}</pre></td></tr>"
        html += "</table>"

    html += """
        <div class="footer">
            Rapport généré automatiquement par le scanner réseau Light Scan.
        </div>
    </div>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath
