import os

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

class HostsBlock:
    @staticmethod
    def get_clean_hosts():
        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            return [l.rstrip("\n") for l in f.readlines()]

    @staticmethod
    def write_hosts(lines):
        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    @staticmethod
    def block_domain(domain):
        domain = domain.strip().lower().replace("https://","").replace("http://","").replace("www.","")
        if "/" in domain:
            domain = domain.split("/")[0]
        lines = HostsBlock.get_clean_hosts()
        new_lines = [l for l in lines if domain not in l]
        new_lines.append(f"127.0.0.1 {domain}")
        new_lines.append(f"127.0.0.1 www.{domain}")
        HostsBlock.write_hosts(new_lines)
        os.system("ipconfig /flushdns >nul 2>&1")

    @staticmethod
    def unblock_domain(domain):
        lines = HostsBlock.get_clean_hosts()
        new_lines = [l for l in lines if domain not in l]
        HostsBlock.write_hosts(new_lines)
        os.system("ipconfig /flushdns >nul 2>&1")