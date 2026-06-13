# LIGHT_SCAN - Outil d'Audit et de Test d'Intrusion Réseau

LIGHT_SCAN est un logiciel d'audit réseau doté d'une interface graphique simple et épurée, codé entièrement en Python avec `tkinter`. Il n'utilise aucune dépendance externe Python autre que les bibliothèques standards.

---

## ⚙️ Explication du Fonctionnement (Sous le capot)

LIGHT_SCAN n'envoie pas les paquets réseau par lui-même. Il agit comme un **wrapper (une surcouche graphique)** pour l'outil de référence mondial : **Nmap**.

1. **Interface Utilisateur (`tkinter`)** : Gère les interactions et la présentation des données dans différents onglets.
2. **Moteur d'exécution (`core/scanner.py`)** : Lorsqu'un scan est lancé, le logiciel crée un processus en arrière-plan via la bibliothèque `subprocess` qui appelle le binaire `nmap` installé sur la machine.
3. **Parsing XML** : LIGHT_SCAN demande à Nmap de retourner ses résultats sous format XML (`-oX -`). Le logiciel analyse (parse) ensuite ce XML en temps réel à l'aide de `xml.etree.ElementTree`.
4. **Multithreading** : Pour éviter que l'interface graphique ne gèle (freeze) pendant les scans qui peuvent durer longtemps, chaque appel à Nmap est exécuté dans un Thread (processus léger) séparé.
5. **Stockage en mémoire** : Au fur et à mesure que les scans se terminent, les données extraites sont stockées temporairement dans la mémoire vive (`app.py -> self.scan_data`) et rendues disponibles pour les autres vues (comme le Dashboard et l'Export).

---

## 📖 Mode d'Emploi

### 1. Lancement de l'Application
Ouvrez un terminal ou un invite de commande dans le dossier `light_scan` et exécutez la commande suivante :
```bash
python main.py
```
*(Note: Sur certaines machines, cela peut être `python3 main.py`)*

### 2. Navigation et Utilisation
L'application est divisée en plusieurs onglets thématiques :

* **📍 Inventaire (Hosts)** : 
   * **But** : Trouver toutes les machines connectées et allumées sur votre réseau local.
   * **Action** : Entrez une plage réseau (ex: `192.168.1.0/24`) et cliquez sur "Lancer le Scan" (utilise un "Ping Sweep" `-sn`).
* **💻 OS Fingerprint** : 
   * **But** : Deviner le système d'exploitation d'une cible précise.
   * **Action** : Saisissez l'adresse IP de la cible trouvée précédemment et lancez l'identification (utilise `-O --osscan-guess`).
* **🔍 Services & Vulns** : 
   * **But** : Lister les ports ouverts sur une machine cible, identifier les services (ex: Apache, SSH), et optionnellement, scanner la cible pour des failles connues avec les scripts de vulnérabilité de Nmap.
   * **Action** : Entrez l'IP cible, cochez (ou non) la case "Inclure scripts vuln" et lancez l'audit (utilise `-sV` et `--script=vuln`).
* **📊 Tableau de Bord** : 
   * **But** : Regrouper visuellement les résultats accumulés par les différents scans. Fournit des indicateurs globaux.
* **💾 Rapport & Export** : 
   * **But** : Sauvegarder votre audit avant de quitter le logiciel.
   * **Action** : Cliquez sur Exporter en JSON ou CSV. Les fichiers seront générés dans un sous-dossier de votre ordinateur.

---


