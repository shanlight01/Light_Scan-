# =============================================================================
#  LIGHT_SCAN — Moteur de scan réseau
#  Appelle Nmap via subprocess et parse la sortie XML
# =============================================================================

import subprocess
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)


class NetworkScanner:
    """Wrapper autour de Nmap utilisant subprocess + XML."""

    def _run_nmap(self, args: list) -> ET.Element | None:
        """Exécute nmap avec les arguments donnés et retourne l'arbre XML."""
        cmd = ["nmap"] + args + ["-oX", "-"]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )
            if result.returncode != 0 and not result.stdout:
                logging.error(f"Nmap stderr: {result.stderr}")
                return None
            return ET.fromstring(result.stdout)
        except FileNotFoundError:
            logging.error("Nmap n'est pas installé ou introuvable dans le PATH.")
            return None
        except subprocess.TimeoutExpired:
            logging.error("Le scan a dépassé le délai de 5 minutes.")
            return None
        except ET.ParseError as e:
            logging.error(f"Erreur de parsing XML: {e}")
            return None

    # -----------------------------------------------------------------
    #  F1 — Inventaire des hôtes (Ping Sweep)
    # -----------------------------------------------------------------
    def host_discovery(self, target: str) -> list:
        """Scan -sn (ping sweep) pour lister les hôtes actifs."""
        root = self._run_nmap(["-sn", target])
        if root is None:
            return []

        hosts = []
        for host_el in root.findall("host"):
            state = host_el.find("status").get("state", "down")
            ip = ""
            mac = ""
            hostname = ""

            for addr in host_el.findall("address"):
                if addr.get("addrtype") == "ipv4":
                    ip = addr.get("addr", "")
                elif addr.get("addrtype") == "mac":
                    mac = addr.get("addr", "")

            hostnames_el = host_el.find("hostnames")
            if hostnames_el is not None:
                hn = hostnames_el.find("hostname")
                if hn is not None:
                    hostname = hn.get("name", "")

            hosts.append({
                "ip": ip,
                "hostname": hostname,
                "mac": mac,
                "state": state,
            })
        return hosts

    # -----------------------------------------------------------------
    #  F2 — OS Fingerprinting
    # -----------------------------------------------------------------
    def os_fingerprint(self, target: str) -> list:
        """Scan -O --osscan-guess pour identifier les OS."""
        root = self._run_nmap(["-O", "--osscan-guess", target])
        if root is None:
            return []

        results = []
        for host_el in root.findall("host"):
            ip = ""
            for addr in host_el.findall("address"):
                if addr.get("addrtype") == "ipv4":
                    ip = addr.get("addr", "")

            os_el = host_el.find("os")
            if os_el is None:
                results.append({"ip": ip, "os": "Inconnu", "accuracy": "0", "cpe": ""})
                continue

            match = os_el.find("osmatch")
            if match is not None:
                cpe = ""
                osclass = match.find("osclass")
                if osclass is not None:
                    cpe_el = osclass.find("cpe")
                    if cpe_el is not None:
                        cpe = cpe_el.text or ""
                results.append({
                    "ip": ip,
                    "os": match.get("name", "Inconnu"),
                    "accuracy": match.get("accuracy", "0"),
                    "cpe": cpe,
                })
            else:
                results.append({"ip": ip, "os": "Inconnu", "accuracy": "0", "cpe": ""})

        return results

    # -----------------------------------------------------------------
    #  F3 — Audit des Services & Vulnérabilités
    # -----------------------------------------------------------------
    def service_audit(self, target: str, vuln_scripts: bool = False) -> dict:
        """Scan -sV (+ --script=vuln si demandé)."""
        args = ["-sV", target]
        if vuln_scripts:
            args.insert(1, "--script=vuln")

        root = self._run_nmap(args)
        if root is None:
            return {"ports": [], "vulns": []}

        ports = []
        vulns = []

        for host_el in root.findall("host"):
            ports_el = host_el.find("ports")
            if ports_el is None:
                continue
            for port_el in ports_el.findall("port"):
                port_num = port_el.get("portid", "")
                protocol = port_el.get("protocol", "")
                state_el = port_el.find("state")
                state = state_el.get("state", "") if state_el is not None else ""
                service_el = port_el.find("service")
                service = ""
                version = ""
                product = ""
                if service_el is not None:
                    service = service_el.get("name", "")
                    product = service_el.get("product", "")
                    version = service_el.get("version", "")

                ports.append({
                    "port": port_num,
                    "protocol": protocol,
                    "state": state,
                    "service": service,
                    "product": product,
                    "version": version,
                })

                # Scripts de vulnérabilité
                for script_el in port_el.findall("script"):
                    vulns.append({
                        "port": port_num,
                        "script": script_el.get("id", ""),
                        "output": script_el.get("output", ""),
                    })

        return {"ports": ports, "vulns": vulns}
