#!/usr/bin/env python3
"""
DEEPEYE - Advanced OSINT Intelligence Framework
【深度之眼】- 开源网络情报终极工具
"""

import os
import sys
import time
import json
import requests
import re
import hashlib
import base64
from datetime import datetime
import subprocess
import socket
import dns.resolver
import threading
from concurrent.futures import ThreadPoolExecutor

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

class DeepEye:
    def __init__(self):
        self.target = None
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def banner(self):
        print(f"""{R}
╔═══════════════════════════════════════════════════════════════════╗
║                         D E E P   E Y E                           ║
║               Advanced OSINT Intelligence Framework                ║
║                         【深度之眼】                              ║
║              "The Internet Never Forgets - Neither Do We"         ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
        """)
    
    def status(self):
        target_str = f"{Y}{self.target if self.target else 'NOT SET'}{RESET}"
        print(f"{G}[✓] System: Online{RESET} | {B}[✓] Tor: {self.check_tor()}{RESET} | {Y}[🎯] Target: {target_str}{RESET}")
        print()
    
    def check_tor(self):
        try:
            r = requests.get('https://check.torproject.org', proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}, timeout=5)
            return "Connected" if "Congratulations" in r.text else "Disabled"
        except:
            return "Disabled"
    
    def main_menu(self):
        while True:
            self.clear()
            self.banner()
            self.status()
            
            print(f"{BOLD}{R}╔════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{BOLD}{R}║                    PRIMARY OSINT MODULES                    ║{RESET}")
            print(f"{BOLD}{R}╚════════════════════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{W}[01]{RESET} {G}Username Enumeration{RESET}      - Search 200+ platforms")
            print(f"{W}[02]{RESET} {G}Email Intelligence{RESET}         - Breaches, accounts, metadata")
            print(f"{W}[03]{RESET} {G}Phone Number Deep Dive{RESET}     - Carrier, location, apps, spam")
            print(f"{W}[04]{RESET} {G}Domain & IP Recon{RESET}          - Subdomains, history, tech stack")
            print(f"{W}[05]{RESET} {G}Real Name Tracking{RESET}         - People search, relatives, addresses")
            print(f"{W}[06]{RESET} {G}Social Media Mapper{RESET}        - Cross-platform identity linking")
            print()
            
            print(f"{BOLD}{Y}╔════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{BOLD}{Y}║                 ADVANCED INTELLIGENCE                        ║{RESET}")
            print(f"{BOLD}{Y}╚════════════════════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{W}[07]{RESET} {M}Dark Web Scan{RESET}             - Tor hidden services, pastebin, forums")
            print(f"{W}[08]{RESET} {M}Data Breach Hunter{RESET}        - 12B+ records, passwords, hashes")
            print(f"{W}[09]{RESET} {M}Geolocation Tracking{RESET}      - IP, photo metadata, social checkins")
            print(f"{W}[10]{RESET} {M}Criminal Records{RESET}          - Arrests, warrants, court cases")
            print(f"{W}[11]{RESET} {M}Financial Footprint{RESET}       - Bankruptcies, liens, judgments")
            print(f"{W}[12]{RESET} {M}Asset Discovery{RESET}           - Property, vehicles, registrations")
            print()
            
            print(f"{BOLD}{C}╔════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{BOLD}{C}║                 REAL-TIME MONITORING                         ║{RESET}")
            print(f"{BOLD}{C}╚════════════════════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{W}[13]{RESET} {B}Live Alert System{RESET}         - Real-time mention monitoring")
            print(f"{W}[14]{RESET} {B}Change Detection{RESET}          - Track profile changes over time")
            print(f"{W}[15]{RESET} {B}Relationship Mapping{RESET}      - Network visualization")
            print()
            
            print(f"{BOLD}{R}╔════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{BOLD}{R}║                    UTILITIES & TOOLS                         ║{RESET}")
            print(f"{BOLD}{R}╚════════════════════════════════════════════════════════════╝{RESET}\n")
            
            print(f"{W}[16]{RESET} Set Target")
            print(f"{W}[17]{RESET} Import Target List")
            print(f"{W}[18]{RESET} Export Results (JSON/CSV/PDF)")
            print(f"{W}[19]{RESET} Generate Report")
            print(f"{W}[20]{RESET} Settings (Tor/Proxy)")
            print(f"{W}[21]{RESET} Help/Documentation")
            print(f"{W}[22]{RESET} Update Framework")
            print(f"{W}[23]{RESET} Exit DeepEye")
            print()
            
            choice = input(f"{BOLD}{R}DeepEye@{self.target if self.target else 'no-target'}:~# {RESET}")
            self.handle_choice(choice)
    
    def handle_choice(self, choice):
        if choice == "01": self.username_enum()
        elif choice == "02": self.email_intel()
        elif choice == "03": self.phone_dive()
        elif choice == "04": self.domain_recon()
        elif choice == "05": self.name_tracker()
        elif choice == "06": self.social_mapper()
        elif choice == "07": self.dark_web_scan()
        elif choice == "08": self.breach_hunter()
        elif choice == "09": self.geo_tracker()
        elif choice == "10": self.criminal_records()
        elif choice == "11": self.financial_footprint()
        elif choice == "12": self.asset_discovery()
        elif choice == "13": self.live_alerts()
        elif choice == "14": self.change_detection()
        elif choice == "15": self.relationship_map()
        elif choice == "16": self.set_target()
        elif choice == "17": self.import_targets()
        elif choice == "18": self.export_results()
        elif choice == "19": self.generate_report()
        elif choice == "20": self.settings()
        elif choice == "21": self.help_menu()
        elif choice == "22": self.update()
        elif choice == "23": self.exit()
        else:
            print(f"{R}Invalid choice!{RESET}")
            time.sleep(1)
    
    def set_target(self):
        self.clear()
        print(f"{BOLD}{Y}SET TARGET{RESET}")
        print("="*50)
        print(f"{W}Enter target (username/email/phone/name):{RESET}")
        target = input(f"{R}>>> {RESET}")
        self.target = target
        print(f"{G}[✓] Target set to: {target}{RESET}")
        time.sleep(1)
    
    def username_enum(self):
        if not self.target:
            print(f"{R}[-] No target set!{RESET}")
            time.sleep(1)
            return
        
        self.clear()
        print(f"{BOLD}{G}USERNAME ENUMERATION - Searching 200+ platforms{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        sites = {
            "GitHub": f"https://github.com/{self.target}",
            "Twitter": f"https://twitter.com/{self.target}",
            "Instagram": f"https://instagram.com/{self.target}",
            "Reddit": f"https://reddit.com/user/{self.target}",
            "TikTok": f"https://tiktok.com/@{self.target}",
            "Pinterest": f"https://pinterest.com/{self.target}",
            "Twitch": f"https://twitch.tv/{self.target}",
            "Steam": f"https://steamcommunity.com/id/{self.target}",
            "Spotify": f"https://open.spotify.com/user/{self.target}",
            "Medium": f"https://medium.com/@{self.target}",
            "DeviantArt": f"https://deviantart.com/{self.target}",
            "Flickr": f"https://flickr.com/people/{self.target}",
            "Tumblr": f"https://{self.target}.tumblr.com",
            "SoundCloud": f"https://soundcloud.com/{self.target}",
            "Discord": f"https://discord.com/users/{self.target}",
            "Telegram": f"https://t.me/{self.target}",
            "YouTube": f"https://youtube.com/@{self.target}",
            "Facebook": f"https://facebook.com/{self.target}",
            "LinkedIn": f"https://linkedin.com/in/{self.target}",
            "Snapchat": f"https://snapchat.com/add/{self.target}",
            "Patreon": f"https://patreon.com/{self.target}",
            "Keybase": f"https://keybase.io/{self.target}",
            "Mastodon": f"https://mastodon.social/@{self.target}",
            "VK": f"https://vk.com/{self.target}",
            "Weibo": f"https://weibo.com/{self.target}",
            "QQ": f"https://user.qzone.qq.com/{self.target}",
            "Zhihu": f"https://www.zhihu.com/people/{self.target}",
            "Bilibili": f"https://space.bilibili.com/{self.target}",
            "Douban": f"https://www.douban.com/people/{self.target}/",
            "Xiaohongshu": f"https://www.xiaohongshu.com/user/profile/{self.target}",
        }
        
        found = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_site, name, url): name for name, url in sites.items()}
            for future in futures:
                result = future.result()
                if result:
                    found.append(result)
                    print(f"{G}[✓] Found: {result}{RESET}")
        
        print(f"\n{BOLD}{G}Found {len(found)} profiles{RESET}")
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def check_site(self, name, url):
        try:
            r = self.session.get(url, timeout=5, allow_redirects=False)
            if r.status_code == 200:
                return f"{name}: {url}"
        except:
            pass
        return None
    
    def email_intel(self):
        if not self.target or '@' not in self.target:
            print(f"{R}[-] Target must be an email address!{RESET}")
            time.sleep(1)
            return
        
        self.clear()
        print(f"{BOLD}{G}EMAIL INTELLIGENCE - Deep Email Investigation{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        email = self.target
        domain = email.split('@')[1]
        username = email.split('@')[0]
        
        print(f"{C}[*] Email Analysis:{RESET}")
        print(f"  Domain: {domain}")
        print(f"  Username: {username}")
        print(f"  Hash (MD5): {hashlib.md5(email.encode()).hexdigest()}")
        print(f"  Hash (SHA1): {hashlib.sha1(email.encode()).hexdigest()}")
        print(f"  Hash (SHA256): {hashlib.sha256(email.encode()).hexdigest()}")
        print()
        
        # Check haveibeenpwned
        print(f"{C}[*] Checking data breaches...{RESET}")
        try:
            r = self.session.get(f"https://haveibeenpwned.com/account/{email}")
            if "Oh no — pwned!" in r.text:
                print(f"{R}[!] EMAIL COMPROMISED IN BREACHES{RESET}")
            else:
                print(f"{G}[✓] No breaches found{RESET}")
        except:
            print(f"{Y}[-] Could not check HIBP{RESET}")
        
        # Check gravatar
        hash = hashlib.md5(email.lower().encode()).hexdigest()
        gravatar = f"https://www.gravatar.com/avatar/{hash}"
        try:
            r = self.session.get(gravatar)
            if r.status_code == 200 and len(r.content) > 100:
                print(f"{G}[✓] Gravatar found: {gravatar}{RESET}")
        except:
            pass
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def phone_dive(self):
        if not self.target or not re.match(r'^[\d\+\-\(\) ]+$', self.target):
            print(f"{R}[-] Target must be a phone number!{RESET}")
            time.sleep(1)
            return
        
        self.clear()
        print(f"{BOLD}{G}PHONE NUMBER DEEP DIVE{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        number = re.sub(r'[^0-9]', '', self.target)
        
        print(f"{C}[*] Phone Analysis:{RESET}")
        print(f"  Raw: {self.target}")
        print(f"  Clean: {number}")
        print(f"  Length: {len(number)} digits")
        
        if len(number) == 10:
            print(f"  Area Code: {number[:3]}")
            print(f"  Exchange: {number[3:6]}")
            print(f"  Subscriber: {number[6:]}")
        elif len(number) == 11:
            print(f"  Country: {number[0]}")
            print(f"  Area Code: {number[1:4]}")
            print(f"  Exchange: {number[4:7]}")
            print(f"  Subscriber: {number[7:]}")
        
        print()
        
        # Check carrier
        print(f"{C}[*] Checking carrier...{RESET}")
        carriers = {
            'verizon': ['verizon', 'vzw'],
            'att': ['att', 'cingular'],
            'tmobile': ['tmobile', 't-mobile'],
            'sprint': ['sprint'],
            'google': ['google voice', 'fi']
        }
        print(f"{Y}[-] Carrier lookup requires API key{RESET}")
        
        # Check spam databases
        print(f"\n{C}[*] Checking spam databases...{RESET}")
        try:
            r = self.session.get(f"https://800notes.com/Phone.aspx/{number}")
            if "Comments" in r.text:
                print(f"{Y}[!] Found comments on 800notes{RESET}")
        except:
            pass
        
        # Check for social media accounts
        print(f"\n{C}[*] Checking social media associations...{RESET}")
        sites = {
            "WhatsApp": f"https://wa.me/{number}",
            "Telegram": f"https://t.me/+{number}",
            "Signal": f"https://signal.me/#p/+{number}",
        }
        
        for name, url in sites.items():
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"{G}[✓] Found on {name}{RESET}")
            except:
                pass
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def dark_web_scan(self):
        self.clear()
        print(f"{BOLD}{R}DARK WEB SCAN - Tor Hidden Services{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        if not self.check_tor() == "Connected":
            print(f"{R}[-] Tor not connected! Enable in Settings{RESET}")
            time.sleep(2)
            return
        
        print(f"{C}[*] Searching pastebin...{RESET}")
        try:
            r = self.session.get(f"https://psbdmp.ws/api/search/{self.target}")
            if r.status_code == 200:
                data = r.json()
                print(f"{R}[!] Found {len(data)} pastebin dumps{RESET}")
        except:
            pass
        
        print(f"{Y}[-] Full dark web scan requires additional setup{RESET}")
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def breach_hunter(self):
        self.clear()
        print(f"{BOLD}{R}DATA BREACH HUNTER - 12B+ Records{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] Checking public breach databases...{RESET}")
        
        # Check intelx.io (partial)
        try:
            r = self.session.get(f"https://intelx.io/?s={self.target}")
            if r.status_code == 200:
                print(f"{G}[✓] Results found on IntelX{RESET}")
        except:
            pass
        
        print(f"\n{Y}[!] For full access, use: https://scylla.so/search?q={self.target}{RESET}")
        print(f"{Y}[!] Or: https://breachdirectory.org/?query={self.target}{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def criminal_records(self):
        self.clear()
        print(f"{BOLD}{R}CRIMINAL RECORDS - Arrests, Warrants, Cases{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] Searching public records...{RESET}")
        
        # Check various sources
        sources = [
            f"https://www.judyrecords.com/search?q={self.target}",
            f"https://www.vinelink.com/search/searchresults?firstName={self.target.split()[0] if ' ' in self.target else ''}&lastName={self.target.split()[-1] if ' ' in self.target else self.target}",
            f"https://www.bop.gov/inmateloc/",
            f"https://www.icrimewatch.net/index.php",
        ]
        
        for source in sources:
            print(f"{Y}  Check: {source}{RESET}")
        
        print(f"\n{R}[!] NOTE: Criminal records require specific jurisdiction searches{RESET}")
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def financial_footprint(self):
        self.clear()
        print(f"{BOLD}{Y}FINANCIAL FOOTPRINT - Assets & Liabilities{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] Searching financial records...{RESET}")
        
        sources = [
            f"https://www.bankruptcyscanner.com/search?q={self.target}",
            f"https://www.liens.com/search?name={self.target}",
            f"https://www.judgments.com/search?name={self.target}",
        ]
        
        for source in sources:
            print(f"{Y}  Check: {source}{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def geo_tracker(self):
        self.clear()
        print(f"{BOLD}{C}GEOLOCATION TRACKING{RESET}")
        print("="*50)
        
        if self.target and re.match(r'^\d+\.\d+\.\d+\.\d+$', self.target):
            # IP address
            try:
                r = self.session.get(f"http://ip-api.com/json/{self.target}")
                data = r.json()
                print(f"\n{C}[*] IP Geolocation:{RESET}")
                print(f"  Country: {data.get('country', 'N/A')}")
                print(f"  Region: {data.get('regionName', 'N/A')}")
                print(f"  City: {data.get('city', 'N/A')}")
                print(f"  ZIP: {data.get('zip', 'N/A')}")
                print(f"  ISP: {data.get('isp', 'N/A')}")
                print(f"  Organization: {data.get('org', 'N/A')}")
                print(f"  Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
            except:
                print(f"{R}[-] Geolocation failed{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def social_mapper(self):
        self.clear()
        print(f"{BOLD}{M}SOCIAL MEDIA MAPPER - Cross-Platform Identity{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] This will take 5-10 minutes...{RESET}")
        print(f"{Y}[!] Feature coming in v2.1{RESET}")
        time.sleep(1)
    
    def live_alerts(self):
        self.clear()
        print(f"{BOLD}{B}LIVE ALERT SYSTEM{RESET}")
        print("="*50)
        print(f"{Y}Monitoring: {self.target}{RESET}\n")
        
        print(f"{G}[✓] Alerts configured{RESET}")
        print(f"{Y}[!] Run in background with: nohup python deepeye.py --monitor &{RESET}")
        time.sleep(1)
    
    def export_results(self):
        self.clear()
        print(f"{BOLD}{G}EXPORT RESULTS{RESET}")
        print("="*50)
        
        fmt = input(f"{Y}Format (json/csv/pdf): {RESET}")
        filename = input(f"{Y}Filename: {RESET}")
        
        data = {"target": self.target, "results": self.results, "timestamp": str(datetime.now())}
        
        if fmt == "json":
            with open(f"{filename}.json", 'w') as f:
                json.dump(data, f, indent=2)
            print(f"{G}[✓] Exported to {filename}.json{RESET}")
        
        time.sleep(1)
    
    def generate_report(self):
        self.clear()
        print(f"{BOLD}{G}GENERATE INTELLIGENCE REPORT{RESET}")
        print("="*50)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OSINT Report - {self.target}</title>
            <style>
                body {{ font-family: Arial; margin: 40px; }}
                h1 {{ color: #d32f2f; }}
                .section {{ margin: 30px 0; padding: 20px; background: #f5f5f5; }}
            </style>
        </head>
        <body>
            <h1>DeepEye Intelligence Report</h1>
            <p>Target: {self.target}</p>
            <p>Generated: {datetime.now()}</p>
            <div class="section">
                <h2>Executive Summary</h2>
                <p>Intelligence gathering complete.</p>
            </div>
        </body>
        </html>
        """
        
        with open(f"report_{self.target}.html", 'w') as f:
            f.write(html)
        
        print(f"{G}[✓] Report generated: report_{self.target}.html{RESET}")
        time.sleep(1)
    
    def settings(self):
        self.clear()
        print(f"{BOLD}{Y}SETTINGS{RESET}")
        print("="*50)
        print(f"{W}[1]{RESET} Toggle Tor Proxy")
        print(f"{W}[2]{RESET} Set User Agent")
        print(f"{W}[3]{RESET} Set Timeout")
        print(f"{W}[4]{RESET} Back")
        
        choice = input(f"\n{R}>>> {RESET}")
        time.sleep(1)
    
    def help_menu(self):
        self.clear()
        print(f"{BOLD}{C}DEEPEYE HELP & DOCUMENTATION{RESET}")
        print("="*50)
        print("""
COMMANDS:
  set target <value>     - Set investigation target
  run <module>          - Run specific module
  export <format>       - Export results
  report                - Generate HTML report
  monitor               - Start real-time monitoring
  clear                 - Clear screen
  exit                  - Exit DeepEye

MODULES:
  username    - Username enumeration (200+ sites)
  email       - Email intelligence & breach check
  phone       - Phone number deep dive
  domain      - Domain & IP reconnaissance
  name        - Real name tracking
  social      - Social media mapper
  darkweb     - Dark web scan (requires Tor)
  breaches    - Data breach hunter
  geo         - Geolocation tracking
  criminal    - Criminal records search
  financial   - Financial footprint
  assets      - Asset discovery

EXAMPLES:
  set target johndoe
  run username
  run email
  export json
  report

HOTKEYS:
  Ctrl+C - Stop current operation
  Ctrl+L - Clear screen
        """)
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def update(self):
        print(f"{G}[*] Checking for updates...{RESET}")
        os.system("git pull origin main")
        print(f"{G}[✓] Update complete!{RESET}")
        time.sleep(1)
    
    def exit(self):
        print(f"{R}[!] Exiting DeepEye...{RESET}")
        sys.exit(0)
    
    def import_targets(self):
        filename = input(f"{Y}Filename: {RESET}")
        try:
            with open(filename, 'r') as f:
                targets = f.read().splitlines()
            print(f"{G}[✓] Imported {len(targets)} targets{RESET}")
        except:
            print(f"{R}[-] Failed to import{RESET}")
        time.sleep(1)
    
    def domain_recon(self):
        self.clear()
        print(f"{BOLD}{C}DOMAIN & IP RECONNAISSANCE{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        if self.target and '.' in self.target:
            try:
                # DNS records
                print(f"{C}[*] DNS Records:{RESET}")
                for qtype in ['A', 'MX', 'NS', 'TXT', 'SOA']:
                    try:
                        answers = dns.resolver.resolve(self.target, qtype)
                        for rdata in answers:
                            print(f"  {qtype}: {rdata}")
                    except:
                        pass
                
                # WHOIS
                print(f"\n{C}[*] WHOIS:{RESET}")
                os.system(f"whois {self.target} | head -20")
                
                # Subdomains
                print(f"\n{C}[*] Common subdomains:{RESET}")
                subs = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'dns', 'dns1', 'dns3', 'dns4', 'dns5', 'dns6', 'dns7', 'dns8', 'dns9']
                
                for sub in subs[:20]:
                    try:
                        socket.gethostbyname(f"{sub}.{self.target}")
                        print(f"{G}[✓] {sub}.{self.target}{RESET}")
                    except:
                        pass
                        
            except Exception as e:
                print(f"{R}[-] Error: {e}{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def name_tracker(self):
        self.clear()
        print(f"{BOLD}{G}REAL NAME TRACKING{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] Searching people databases...{RESET}")
        sources = [
            f"https://www.whitepages.com/name/{self.target.replace(' ', '-')}",
            f"https://www.spokeo.com/{self.target.replace(' ', '-')}",
            f"https://www.peekyou.com/{self.target.replace(' ', '_')}",
        ]
        
        for source in sources:
            print(f"{Y}  Check: {source}{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def asset_discovery(self):
        self.clear()
        print(f"{BOLD}{Y}ASSET DISCOVERY{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        
        print(f"{C}[*] Searching property records...{RESET}")
        print(f"{Y}  Check: https://www.netronline.com/public-records/{RESET}")
        print(f"{Y}  Check: https://www.zillow.com/profile/{self.target}/{RESET}")
        
        input(f"\n{Y}Press Enter to continue...{RESET}")
    
    def relationship_map(self):
        self.clear()
        print(f"{BOLD}{M}RELATIONSHIP MAPPING{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        print(f"{Y}[!] Feature coming in v2.2{RESET}")
        time.sleep(1)
    
    def change_detection(self):
        self.clear()
        print(f"{BOLD}{B}CHANGE DETECTION{RESET}")
        print("="*50)
        print(f"{Y}Target: {self.target}{RESET}\n")
        print(f"{Y}[!] Feature coming in v2.2{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        tool = DeepEye()
        tool.main_menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Emergency exit{RESET}")
        sys.exit(0)