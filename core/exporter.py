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
