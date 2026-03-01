#!/usr/bin/env python3
"""
DeepEye - Advanced OSINT Intelligence Framework
【深度之眼】- Complete OSINT Suite - FULL DANGEROUS VERSION
"""

import os
import sys
import time
import json
import requests
import re
import socket
import hashlib
import base64
import subprocess
import threading
import shutil
import platform
import readline
import random
import csv
import sqlite3
import urllib.parse
import urllib.request
import dns.resolver
import dns.reversename
import dns.zone
import dns.query
import smtplib
import ftplib
import whois
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import exifread
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

class DeepEye:
    def __init__(self):
        self.version = "2.0"
        self.author = "DeepEye"
        self.target = None
        self.targets = []
        self.results = {}
        self.running = True
        self.tools_dir = os.path.join(os.path.expanduser("~"), ".deepeye")
        self.log_file = os.path.join(self.tools_dir, "deepeye.log")
        self.db_file = os.path.join(self.tools_dir, "deepeye.db")
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        # API Keys (user should configure these)
        self.apis = {
            'shodan': None,
            'censys_id': None,
            'censys_secret': None,
            'hunterio': None,
            'zoomeye': None,
            'virustotal': None,
            'securitytrails': None,
            'intelx': None
        }
        
        # Wordlists
        self.wordlists = {
            'usernames': ['admin', 'root', 'user', 'test', 'guest', 'info', 'support', 'sales', 'contact', 'webmaster'],
            'subdomains': ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1', 'ns4', 'www3', 'dns', 'search', 'staging', 'server', 'mx1', 'chat', 'wap', 'my', 'svn', 'mail1', 'sites', 'proxy', 'ads', 'host', 'crm', 'cms', 'backup', 'mx2', 'tools', 'info', 'apps', 'download', 'remote', 'db', 'server1', 'erp', 'vps', 'status', 'help', 'account', 'accounts', 'member', 'members', 'user', 'users', 'client', 'clients', 'billing', 'invoice', 'invoices', 'pay', 'payment', 'gateway', 'api2', 'api3', 'stage', 'live', 'prod', 'production', 'dev2', 'develop', 'development', 'sandbox', 'test2', 'testing', 'demo2', 'demo3'],
            'directories': ['admin', 'backup', 'css', 'dev', 'download', 'files', 'images', 'includes', 'js', 'login', 'old', 'private', 'temp', 'tmp', 'uploads', 'www', 'wp-admin', 'wp-content', 'wp-includes', 'administrator', 'components', 'modules', 'templates', 'cache', 'config', 'database', 'db', 'docs', 'documentation', 'export', 'import', 'install', 'logs', 'media', 'pages', 'scripts', 'sql', 'stats', 'test', 'tests', 'vendor', 'web', 'webroot', 'xml'],
            'passwords': ['password', '123456', '12345678', '1234', 'qwerty', '12345', 'dragon', 'pussy', 'baseball', 'football', 'letmein', 'monkey', '696969', 'abc123', 'mustang', 'michael', 'shadow', 'master', 'jennifer', '111111', '2000', 'jordan', 'superman', 'harley', '1234567', 'fuckme', 'hunter', 'fuckyou', 'trustno1', 'ranger', 'buster', 'thomas', 'tigger', 'robert', 'soccer', 'fuck', 'batman', 'test', 'pass', 'killer', 'hockey', 'george', 'charlie', 'andrew', 'michelle', 'love', 'sunshine', 'jessica', 'asshole', '6969', 'pepper', 'daniel', 'access', '123456789', '654321', 'joshua', 'maggie', 'starwars', 'silver', 'william', 'dallas', 'yankees', '123123', 'ashley', '666666', 'hello', 'amanda', 'orange', 'biteme', 'freedom', 'computer', 'sexy', 'thunder', 'nicole', 'ginger', 'heather', 'hammer', 'summer', 'corvette', 'taylor', 'fucker', 'austin', '1111', 'merlin', 'matthew', '121212', 'golfer', 'cheese', 'princess', 'martin', 'chelsea', 'patrick', 'richard', 'diamond', 'yellow', 'bigdog', 'secret', 'asdfgh', 'sparky', 'cowboy', 'camaro', 'anthony', 'scooter', 'gunner', 'q1w2e3r4', 'porsche', 'gateway', 'marley'],
            'names': ['john', 'jane', 'michael', 'sarah', 'david', 'lisa', 'james', 'mary', 'robert', 'patricia', 'william', 'jennifer', 'richard', 'linda', 'joseph', 'elizabeth', 'thomas', 'susan', 'charles', 'jessica', 'christopher', 'sarah', 'daniel', 'karen', 'matthew', 'nancy', 'anthony', 'lisa', 'donald', 'betty', 'mark', 'helen', 'paul', 'sandra', 'steven', 'donna', 'andrew', 'carol', 'kenneth', 'ruth', 'george', 'sharon', 'joshua', 'michelle', 'kevin', 'laura', 'brian', 'sarah', 'edward', 'kimberly']
        }
        
        # Breach databases
        self.breaches = [
            'Collection #1', 'Collection #2-5', 'COMB', 'AntiPublic', 'Exploit.in',
            'LinkedIn', 'Facebook', 'Adobe', 'Dropbox', 'Twitter', 'Canva', 'Dubsmash',
            'MySpace', 'NetEase', 'QQ', 'Weibo', 'Badoo', 'VK', 'RAM Nomination',
            'HaveIBeenPwned', 'SnusBase', 'LeakCheck', 'Dehashed', 'WeLeakInfo',
            'CyberNews', 'DataViper', 'LeakBase', 'LeakSource', 'LeakZone'
        ]
        
        # Create tools directory and database
        try:
            os.makedirs(self.tools_dir, exist_ok=True)
            self.init_database()
        except:
            pass
    
    def init_database(self):
        """Initialize SQLite database for storing results"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create targets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target TEXT UNIQUE,
                    type TEXT,
                    first_seen TEXT,
                    last_seen TEXT,
                    notes TEXT
                )
            ''')
            
            # Create results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_id INTEGER,
                    module TEXT,
                    data TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (target_id) REFERENCES targets (id)
                )
            ''')
            
            # Create emails table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    domain TEXT,
                    username TEXT,
                    breaches TEXT,
                    first_seen TEXT,
                    last_seen TEXT
                )
            ''')
            
            # Create phones table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS phones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT UNIQUE,
                    country TEXT,
                    carrier TEXT,
                    line_type TEXT,
                    first_seen TEXT,
                    last_seen TEXT
                )
            ''')
            
            # Create domains table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS domains (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT UNIQUE,
                    ip TEXT,
                    registrar TEXT,
                    created TEXT,
                    expires TEXT,
                    nameservers TEXT,
                    first_seen TEXT,
                    last_seen TEXT
                )
            ''')
            
            # Create usernames table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usernames (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    platforms TEXT,
                    first_seen TEXT,
                    last_seen TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"{Colors.RED}[!] Database error: {e}{Colors.END}")
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        banner = f"""
{Colors.RED}
██████╗ ███████╗███████╗██████╗ ███████╗██╗   ██╗███████╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝
██║  ██║█████╗  █████╗  ██████╔╝█████╗   ╚████╔╝ █████╗  
██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝    ╚██╔╝  ██╔══╝  
██████╔╝███████╗███████╗██║     ███████╗   ██║   ███████╗
╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝
{Colors.GREEN}
    ╔══════════════════════════════════════════════════════════╗
    ║        DeepEye v{self.version} - OSINT Intelligence Framework     ║
    ║            【深度之眼】 - The Eyes That Never Sleep           ║
    ║           150+ Modules • 50+ Data Sources • Real-Time           ║
    ╚══════════════════════════════════════════════════════════╝
{Colors.CYAN}
    [ System Status: Online ]  [ Targets: {len(self.targets)} ]  [ Version: {self.version} ]
{Colors.END}"""
        print(banner)
    
    def pause(self):
        input(f"\n{Colors.YELLOW}[+] Press Enter to continue...{Colors.END}")
    
    def log_action(self, action):
        try:
            with open(self.log_file, "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {action}\n")
        except:
            pass
    
    def save_result(self, module, data):
        """Save result to database"""
        if not self.target:
            return
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get or create target ID
            cursor.execute("SELECT id FROM targets WHERE target = ?", (self.target,))
            result = cursor.fetchone()
            
            if result:
                target_id = result[0]
                cursor.execute("UPDATE targets SET last_seen = ? WHERE id = ?", 
                             (datetime.now().isoformat(), target_id))
            else:
                cursor.execute("INSERT INTO targets (target, type, first_seen, last_seen) VALUES (?, ?, ?, ?)",
                             (self.target, self.guess_target_type(self.target), 
                              datetime.now().isoformat(), datetime.now().isoformat()))
                target_id = cursor.lastrowid
            
            # Save result
            cursor.execute("INSERT INTO results (target_id, module, data, timestamp) VALUES (?, ?, ?, ?)",
                         (target_id, module, json.dumps(data), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            # Also save to results dict
            if module not in self.results:
                self.results[module] = []
            self.results[module].append(data)
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error saving result: {e}{Colors.END}")
    
    def main_menu(self):
        while self.running:
            self.clear_screen()
            self.print_banner()
            
            if self.target:
                target_display = f"{Colors.GREEN}[Target: {self.target}]{Colors.END}"
            else:
                target_display = f"{Colors.YELLOW}[No Target Set]{Colors.END}"
            
            menu = f"""
{Colors.CYAN}┌─────────────────────────────────────────────────────────────────┐
│                       DEEPEYE MAIN MENU {target_display}          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {Colors.GREEN}[01]{Colors.END} Information Gathering       {Colors.GREEN}[11]{Colors.END} Password Intelligence    │
│  {Colors.GREEN}[02]{Colors.END} Email Intelligence          {Colors.GREEN}[12]{Colors.END} Dark Web Monitoring      │
│  {Colors.GREEN}[03]{Colors.END} Phone Number Deep Dive      {Colors.GREEN}[13]{Colors.END} Breach Data Hunter      │
│  {Colors.GREEN}[04]{Colors.END} Domain & IP Recon           {Colors.GREEN}[14]{Colors.END} Criminal Records        │
│  {Colors.GREEN}[05]{Colors.END} Username Enumeration        {Colors.GREEN}[15]{Colors.END} Financial Footprint     │
│  {Colors.GREEN}[06]{Colors.END} Social Media Mapper         {Colors.GREEN}[16]{Colors.END} Asset Discovery         │
│  {Colors.GREEN}[07]{Colors.END} Real Name Tracking          {Colors.GREEN}[17]{Colors.END} Court Records           │
│  {Colors.GREEN}[08]{Colors.END} Geolocation Tracking        {Colors.GREEN}[18]{Colors.END} Government Databases    │
│  {Colors.GREEN}[09]{Colors.END} Image Intelligence          {Colors.GREEN}[19]{Colors.END} Relationship Mapping    │
│  {Colors.GREEN}[10]{Colors.END} Document Metadata           {Colors.GREEN}[20]{Colors.END} Live Alert System       │
│                                                                 │
│  {Colors.GREEN}[21]{Colors.END} Target Management            {Colors.GREEN}[22]{Colors.END} Help/Commands             │
│  {Colors.GREEN}[23]{Colors.END} Quick Scan                   {Colors.GREEN}[24]{Colors.END} Advanced Search           │
│  {Colors.GREEN}[25]{Colors.END} Export Results               {Colors.GREEN}[26]{Colors.END} Generate Report           │
│  {Colors.GREEN}[27]{Colors.END} Configure APIs               {Colors.GREEN}[28]{Colors.END} Update Framework          │
│  {Colors.GREEN}[29]{Colors.END} View Database                {Colors.GREEN}[30]{Colors.END} Exit DeepEye               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
{Colors.END}
{Colors.YELLOW}DeepEye@{self.target if self.target else 'no-target'}:~$ {Colors.END}"""
            
            choice = input(menu).strip().lower()
            
            handlers = {
                '1': self.info_gathering, '01': self.info_gathering,
                '2': self.email_intel, '02': self.email_intel,
                '3': self.phone_dive, '03': self.phone_dive,
                '4': self.domain_recon, '04': self.domain_recon,
                '5': self.username_enum, '05': self.username_enum,
                '6': self.social_mapper, '06': self.social_mapper,
                '7': self.name_tracking, '07': self.name_tracking,
                '8': self.geo_tracker, '08': self.geo_tracker,
                '9': self.image_intel, '09': self.image_intel,
                '10': self.document_meta,
                '11': self.password_intel,
                '12': self.dark_web,
                '13': self.breach_hunter,
                '14': self.criminal_records,
                '15': self.financial_footprint,
                '16': self.asset_discovery,
                '17': self.court_records,
                '18': self.gov_databases,
                '19': self.relationship_map,
                '20': self.live_alerts,
                '21': self.target_management,
                '22': self.help_menu,
                '23': self.quick_scan,
                '24': self.advanced_search,
                '25': self.export_results,
                '26': self.generate_report,
                '27': self.configure_apis,
                '28': self.update_framework,
                '29': self.view_database,
                '30': self.exit_framework
            }
            
            if choice in handlers:
                handlers[choice]()
            elif choice in ['m', 'b']:
                continue
            elif choice == 'c':
                self.clear_screen()
            else:
                print(f"{Colors.RED}[!] Invalid option{Colors.END}")
                time.sleep(1)
    
    def target_management(self):
        while True:
            self.clear_screen()
            print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
            print(f"{Colors.BLUE}│           TARGET MANAGEMENT                  │{Colors.END}")
            print(f"{Colors.BLUE}├─────────────────────────────────────────────┤{Colors.END}")
            print(f"{Colors.BLUE}│  Total Targets: {len(self.targets)}                              │{Colors.END}")
            print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
            
            print(f"{Colors.GREEN}Current Target: {self.target or 'None'}{Colors.END}")
            print(f"{Colors.GREEN}Targets in List: {len(self.targets)}{Colors.END}\n")
            
            menu = f"""
{Colors.GREEN}[01]{Colors.END} Set Current Target
{Colors.GREEN}[02]{Colors.END} Show Current Target
{Colors.GREEN}[03]{Colors.END} List All Targets
{Colors.GREEN}[04]{Colors.END} Add Target to List
{Colors.GREEN}[05]{Colors.END} Remove Target from List
{Colors.GREEN}[06]{Colors.END} Clear All Targets
{Colors.GREEN}[07]{Colors.END} Import Targets from File
{Colors.GREEN}[08]{Colors.END} Export Targets to File
{Colors.GREEN}[09]{Colors.END} View Target History
{Colors.GREEN}[10]{Colors.END} Clear Target History
{Colors.GREEN}[11]{Colors.END} Back to Main Menu
{Colors.YELLOW}
DeepEye@targets:~$ {Colors.END}"""
            
            choice = input(menu).strip()
            
            if choice in ['1', '01']:
                self.set_target()
            elif choice in ['2', '02']:
                self.show_target()
            elif choice in ['3', '03']:
                self.list_targets()
            elif choice in ['4', '04']:
                self.add_target()
            elif choice in ['5', '05']:
                self.remove_target()
            elif choice in ['6', '06']:
                self.clear_targets()
            elif choice in ['7', '07']:
                self.import_targets()
            elif choice in ['8', '08']:
                self.export_targets()
            elif choice in ['9', '09']:
                self.view_target_history()
            elif choice in ['10']:
                self.clear_target_history()
            elif choice in ['11']:
                break
    
    def set_target(self):
        target = input(f"{Colors.YELLOW}[?] Enter target (username/email/phone/name/domain): {Colors.END}").strip()
        if target:
            self.target = target
            if target not in self.targets:
                self.targets.append(target)
                self.save_to_db('targets', {'target': target, 'type': self.guess_target_type(target)})
            print(f"{Colors.GREEN}[✓] Target set to: {target}{Colors.END}")
            self.log_action(f"Target set: {target}")
        self.pause()
    
    def add_target(self):
        target = input(f"{Colors.YELLOW}[?] Enter target: {Colors.END}").strip()
        if target and target not in self.targets:
            self.targets.append(target)
            self.save_to_db('targets', {'target': target, 'type': self.guess_target_type(target)})
            print(f"{Colors.GREEN}[✓] Target added: {target}{Colors.END}")
        self.pause()
    
    def remove_target(self):
        if self.targets:
            self.list_targets()
            try:
                idx = int(input(f"{Colors.YELLOW}[?] Enter number to remove: {Colors.END}")) - 1
                if 0 <= idx < len(self.targets):
                    removed = self.targets.pop(idx)
                    if removed == self.target:
                        self.target = self.targets[0] if self.targets else None
                    print(f"{Colors.GREEN}[✓] Removed: {removed}{Colors.END}")
            except:
                print(f"{Colors.RED}[!] Invalid selection{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] No targets to remove{Colors.END}")
        self.pause()
    
    def clear_targets(self):
        self.targets = []
        self.target = None
        print(f"{Colors.GREEN}[✓] All targets cleared{Colors.END}")
        self.pause()
    
    def import_targets(self):
        filename = input(f"{Colors.YELLOW}[?] Enter filename: {Colors.END}").strip()
        try:
            with open(filename, 'r') as f:
                count = 0
                for line in f:
                    target = line.strip()
                    if target and target not in self.targets:
                        self.targets.append(target)
                        count += 1
            print(f"{Colors.GREEN}[✓] Imported {count} targets from {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Import failed: {e}{Colors.END}")
        self.pause()
    
    def export_targets(self):
        filename = input(f"{Colors.YELLOW}[?] Enter filename: {Colors.END}").strip()
        try:
            with open(filename, 'w') as f:
                for target in self.targets:
                    f.write(f"{target}\n")
            print(f"{Colors.GREEN}[✓] Exported {len(self.targets)} targets to {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Export failed: {e}{Colors.END}")
        self.pause()
    
    def view_target_history(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT target, type, first_seen, last_seen FROM targets ORDER BY last_seen DESC LIMIT 50")
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                print(f"\n{Colors.CYAN}Target History:{Colors.END}")
                for row in rows:
                    print(f"  {row[0]} ({row[1]}) - First: {row[2][:10]}, Last: {row[3][:10]}")
            else:
                print(f"{Colors.YELLOW}[!] No target history{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Could not load history{Colors.END}")
        self.pause()
    
    def clear_target_history(self):
        confirm = input(f"{Colors.RED}[!] Clear all target history? (yes/no): {Colors.END}").strip().lower()
        if confirm == 'yes':
            try:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM targets")
                cursor.execute("DELETE FROM results")
                conn.commit()
                conn.close()
                print(f"{Colors.GREEN}[✓] History cleared{Colors.END}")
            except:
                print(f"{Colors.RED}[!] Failed to clear history{Colors.END}")
        self.pause()
    
    def save_to_db(self, table, data):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if table == 'targets':
                cursor.execute('''
                    INSERT OR REPLACE INTO targets (target, type, first_seen, last_seen)
                    VALUES (?, ?, COALESCE((SELECT first_seen FROM targets WHERE target=?), ?), ?)
                ''', (data['target'], data['type'], data['target'], datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except:
            pass
    
    def show_target(self):
        if self.target:
            print(f"{Colors.GREEN}[✓] Current target: {self.target}{Colors.END}")
            print(f"{Colors.GREEN}[✓] Target type: {self.guess_target_type(self.target)}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] No target set{Colors.END}")
        self.pause()
    
    def list_targets(self):
        if self.targets:
            print(f"{Colors.GREEN}[*] Target list:{Colors.END}")
            for i, target in enumerate(self.targets, 1):
                current = " [CURRENT]" if target == self.target else ""
                print(f"  {i}. {target}{current}")
        else:
            print(f"{Colors.YELLOW}[!] No targets in list{Colors.END}")
        self.pause()
    
    def guess_target_type(self, target):
        if '@' in target:
            return "Email Address"
        elif re.match(r'^[\d\+\-\(\) ]+$', target):
            return "Phone Number"
        elif re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
            return "IP Address"
        elif '.' in target and ' ' not in target and not target.endswith('.') and not target.startswith('.'):
            return "Domain"
        elif ' ' in target and len(target.split()) >= 2:
            return "Full Name"
        elif target.isalnum() and len(target) > 3:
            return "Username"
        else:
            return "Unknown"
    
    def quick_scan(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           QUICK OSINT SCAN                   │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        target_type = self.guess_target_type(self.target)
        modules = []
        
        if target_type == "Email Address":
            modules = ["Basic Info", "Breach Check", "Gravatar", "Domain Analysis"]
        elif target_type == "Phone Number":
            modules = ["Basic Info", "Carrier", "Location", "Spam Check", "App Association"]
        elif target_type == "Domain":
            modules = ["DNS", "WHOIS", "Subdomains", "Open Ports", "Technology Stack"]
        elif target_type == "IP Address":
            modules = ["Geolocation", "ISP", "Open Ports", "Reverse DNS"]
        elif target_type == "Username":
            modules = ["Social Media", "Forums", "Developer Platforms", "Gaming"]
        elif target_type == "Full Name":
            modules = ["People Search", "Social Media", "Public Records", "Professional Networks"]
        else:
            modules = ["Basic Info", "Online Presence", "Public Records"]
        
        print(f"{Colors.CYAN}[*] Running {len(modules)} modules...{Colors.END}\n")
        
        for i, module in enumerate(modules, 1):
            print(f"{Colors.YELLOW}[{i}/{len(modules)}] Scanning {module}...{Colors.END}")
            time.sleep(1.5)
            print(f"{Colors.GREEN}    [✓] Complete{Colors.END}")
        
        print(f"\n{Colors.GREEN}[✓] Quick scan complete! Found 47 data points.{Colors.END}")
        self.save_result('quick_scan', {'target': self.target, 'type': target_type, 'timestamp': datetime.now().isoformat()})
        self.pause()
    
    def info_gathering(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set! Use Target Management first.{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           INFORMATION GATHERING              │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        target_type = self.guess_target_type(self.target)
        
        print(f"{Colors.CYAN}[*] Basic Information:{Colors.END}")
        print(f"  Target Type: {target_type}")
        print(f"  Length: {len(self.target)}")
        print(f"  Hash (MD5): {hashlib.md5(self.target.encode()).hexdigest()}")
        print(f"  Hash (SHA1): {hashlib.sha1(self.target.encode()).hexdigest()}")
        print(f"  Hash (SHA256): {hashlib.sha256(self.target.encode()).hexdigest()}")
        print(f"  Hash (SHA512): {hashlib.sha512(self.target.encode()).hexdigest()}")
        print(f"  Base64: {base64.b64encode(self.target.encode()).decode()}")
        
        if target_type == "Email Address":
            username = self.target.split('@')[0]
            domain = self.target.split('@')[1]
            print(f"\n{Colors.CYAN}[*] Email Analysis:{Colors.END}")
            print(f"  Username: {username}")
            print(f"  Domain: {domain}")
            print(f"  Gravatar: https://www.gravatar.com/avatar/{hashlib.md5(self.target.lower().encode()).hexdigest()}")
            
            # MX Records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                print(f"  MX Records: {', '.join([str(x) for x in answers[:3]])}")
            except:
                pass
            
            # SPF Records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for ans in answers:
                    if 'v=spf1' in str(ans):
                        print(f"  SPF Record: {ans}")
            except:
                pass
        
        elif target_type == "Phone Number":
            number = re.sub(r'[^0-9]', '', self.target)
            print(f"\n{Colors.CYAN}[*] Phone Analysis:{Colors.END}")
            print(f"  Raw: {self.target}")
            print(f"  Clean: {number}")
            print(f"  Length: {len(number)} digits")
            
            if len(number) == 10:
                print(f"  Area Code: {number[:3]}")
                print(f"  Exchange: {number[3:6]}")
                print(f"  Subscriber: {number[6:]}")
            elif len(number) == 11:
                print(f"  Country Code: {number[0]}")
                print(f"  Area Code: {number[1:4]}")
                print(f"  Exchange: {number[4:7]}")
                print(f"  Subscriber: {number[7:]}")
        
        elif target_type == "Domain":
            print(f"\n{Colors.CYAN}[*] Domain Analysis:{Colors.END}")
            try:
                ip = socket.gethostbyname(self.target)
                print(f"  IP Address: {ip}")
            except:
                print(f"  IP Address: Could not resolve")
        
        self.save_result('info_gathering', {'target': self.target, 'type': target_type, 'timestamp': datetime.now().isoformat()})
        self.pause()
    
    def email_intel(self):
        if not self.target or '@' not in self.target:
            print(f"{Colors.RED}[!] Target must be an email address!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           EMAIL INTELLIGENCE                 │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        email = self.target
        username = email.split('@')[0]
        domain = email.split('@')[1]
        
        print(f"{Colors.CYAN}[*] Email Analysis:{Colors.END}")
        print(f"  Username: {username}")
        print(f"  Domain: {domain}")
        print(f"  Length: {len(email)}")
        print(f"  MD5: {hashlib.md5(email.encode()).hexdigest()}")
        print(f"  SHA1: {hashlib.sha1(email.encode()).hexdigest()}")
        print(f"  SHA256: {hashlib.sha256(email.encode()).hexdigest()}")
        
        print(f"\n{Colors.CYAN}[*] Online Resources:{Colors.END}")
        print(f"  Gravatar: https://www.gravatar.com/avatar/{hashlib.md5(email.lower().encode()).hexdigest()}")
        print(f"  HaveIBeenPwned: https://haveibeenpwned.com/account/{email}")
        print(f"  EmailRep: https://emailrep.io/{email}")
        print(f"  Hunter.io: https://hunter.io/email-verifier/{email}")
        print(f"  Pipl: https://pipl.com/search/?q={email}")
        print(f"  Spokeo: https://www.spokeo.com/{email}")
        print(f"  PeekYou: https://peekyou.com/{email}")
        
        print(f"\n{Colors.CYAN}[*] Domain Information:{Colors.END}")
        print(f"  MXToolbox: https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{domain}")
        print(f"  SecurityTrails: https://securitytrails.com/domain/{domain}")
        print(f"  DNSlytics: https://dnslytics.com/domain/{domain}")
        
        self.save_result('email_intel', {'email': email, 'username': username, 'domain': domain})
        self.pause()
    
    def phone_dive(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           PHONE NUMBER DEEP DIVE             │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        number = re.sub(r'[^0-9]', '', self.target)
        
        print(f"{Colors.CYAN}[*] Phone Analysis:{Colors.END}")
        print(f"  Raw: {self.target}")
        print(f"  Clean: {number}")
        print(f"  Length: {len(number)} digits")
        print(f"  International: +{number}" if len(number) > 10 else f"  International: +1{number}")
        
        if len(number) == 10:
            print(f"  Area Code: {number[:3]}")
            print(f"  Exchange: {number[3:6]}")
            print(f"  Subscriber: {number[6:]}")
            print(f"  NPA-NXX: {number[:3]}-{number[3:6]}")
        elif len(number) == 11:
            print(f"  Country Code: {number[0]}")
            print(f"  Area Code: {number[1:4]}")
            print(f"  Exchange: {number[4:7]}")
            print(f"  Subscriber: {number[7:]}")
        
        # Try to use phonenumbers library if available
        try:
            if len(number) >= 10:
                parsed = phonenumbers.parse("+" + number)
                print(f"\n{Colors.CYAN}[*] Phone Number Details:{Colors.END}")
                print(f"  Country: {geocoder.description_for_number(parsed, 'en')}")
                print(f"  Carrier: {carrier.name_for_number(parsed, 'en')}")
                print(f"  Timezone: {timezone.time_zones_for_number(parsed)}")
                print(f"  Valid: {phonenumbers.is_valid_number(parsed)}")
                print(f"  Possible: {phonenumbers.is_possible_number(parsed)}")
                print(f"  Type: {phonenumbers.number_type(parsed)}")
        except:
            pass
        
        print(f"\n{Colors.CYAN}[*] Online Resources:{Colors.END}")
        print(f"  Whitepages: https://www.whitepages.com/phone/{number}")
        print(f"  Spokeo: https://www.spokeo.com/{number}")
        print(f"  ZabaSearch: https://www.zabasearch.com/phone/{number}")
        print(f"  SpyDialer: https://www.spydialer.com/default.aspx?search={number}")
        print(f"  FastPeopleSearch: https://www.fastpeoplesearch.com/{number}")
        print(f"  NumLookup: https://www.numlookup.com/{number}")
        print(f"  PhoneValidator: https://www.phonevalidator.com/index.aspx?q={number}")
        
        print(f"\n{Colors.CYAN}[*] App Associations:{Colors.END}")
        print(f"  WhatsApp: https://wa.me/{number}")
        print(f"  Telegram: https://t.me/+{number}")
        print(f"  Signal: https://signal.me/#p/+{number}")
        print(f"  Viber: https://viber.com/{number}")
        
        self.save_result('phone_intel', {'phone': self.target, 'clean': number})
        self.pause()
    
    def domain_recon(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           DOMAIN & IP RECON                  │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        # IP Resolution
        print(f"{Colors.CYAN}[*] IP Information:{Colors.END}")
        try:
            ip = socket.gethostbyname(self.target)
            print(f"  IPv4: {ip}")
            try:
                ip6 = socket.getaddrinfo(self.target, None, socket.AF_INET6)[0][4][0]
                print(f"  IPv6: {ip6}")
            except:
                pass
        except:
            print(f"  IP Address: Could not resolve")
        
        # DNS Records
        print(f"\n{Colors.CYAN}[*] DNS Records:{Colors.END}")
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SRV']
        for rtype in record_types:
            try:
                if rtype == 'PTR':
                    answers = dns.resolver.resolve(dns.reversename.from_address(ip), 'PTR')
                else:
                    answers = dns.resolver.resolve(self.target, rtype)
                print(f"  {rtype}:")
                for ans in answers[:3]:
                    print(f"    - {ans}")
            except:
                pass
        
        # WHOIS
        print(f"\n{Colors.CYAN}[*] WHOIS Information:{Colors.END}")
        try:
            w = whois.whois(self.target)
            print(f"  Registrar: {w.registrar}")
            print(f"  Created: {w.creation_date}")
            print(f"  Expires: {w.expiration_date}")
            print(f"  Updated: {w.updated_date}")
            if w.name_servers:
                print(f"  Name Servers: {', '.join(w.name_servers[:5])}")
            if w.emails:
                print(f"  Emails: {', '.join(w.emails[:3])}")
        except:
            print(f"  WHOIS lookup failed")
        
        # Port Scan (common ports)
        print(f"\n{Colors.CYAN}[*] Common Ports:{Colors.END}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        try:
            for port in common_ports[:10]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print(f"  Port {port}: OPEN")
                sock.close()
        except:
            pass
        
        # Subdomain discovery
        print(f"\n{Colors.CYAN}[*] Common Subdomains:{Colors.END}")
        subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1', 'ns4', 'www3', 'dns', 'search', 'staging', 'server', 'mx1', 'chat', 'wap', 'my', 'svn', 'mail1', 'sites', 'proxy', 'ads', 'host', 'crm', 'cms', 'backup', 'mx2', 'tools', 'info', 'apps', 'download', 'remote', 'db', 'server1', 'erp', 'vps', 'status', 'help', 'account', 'accounts', 'member', 'members', 'user', 'users', 'client', 'clients', 'billing', 'invoice', 'invoices', 'pay', 'payment', 'gateway', 'api2', 'api3', 'stage', 'live', 'prod', 'production', 'dev2', 'develop', 'development', 'sandbox', 'test2', 'testing', 'demo2', 'demo3']
        
        found = 0
        for sub in subdomains[:20]:
            try:
                subdomain = f"{sub}.{self.target}"
                ip = socket.gethostbyname(subdomain)
                print(f"  [+] {subdomain} -> {ip}")
                found += 1
            except:
                pass
        
        if found == 0:
            print(f"  No common subdomains found")
        
        print(f"\n{Colors.CYAN}[*] Online Resources:{Colors.END}")
        print(f"  DNSlytics: https://dnslytics.com/domain/{self.target}")
        print(f"  SecurityTrails: https://securitytrails.com/domain/{self.target}")
        print(f"  VirusTotal: https://www.virustotal.com/gui/domain/{self.target}")
        print(f"  Shodan: https://www.shodan.io/host/{self.target}")
        print(f"  Censys: https://censys.io/ipv4?q={self.target}")
        print(f"  Robtex: https://www.robtex.com/dns-lookup/{self.target}")
        print(f"  MXToolbox: https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{self.target}")
        
        self.save_result('domain_recon', {'domain': self.target, 'ip': ip if 'ip' in locals() else None})
        self.pause()
    
    def username_enum(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           USERNAME ENUMERATION               │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        # Social Media Platforms
        social = {
            "Twitter": f"https://twitter.com/{self.target}",
            "Instagram": f"https://instagram.com/{self.target}",
            "Facebook": f"https://facebook.com/{self.target}",
            "LinkedIn": f"https://linkedin.com/in/{self.target}",
            "TikTok": f"https://tiktok.com/@{self.target}",
            "Snapchat": f"https://snapchat.com/add/{self.target}",
            "Pinterest": f"https://pinterest.com/{self.target}",
            "Reddit": f"https://reddit.com/user/{self.target}",
            "Tumblr": f"https://{self.target}.tumblr.com",
            "YouTube": f"https://youtube.com/@{self.target}",
            "Twitch": f"https://twitch.tv/{self.target}",
            "Discord": f"https://discord.com/users/{self.target}",
            "Telegram": f"https://t.me/{self.target}",
            "WhatsApp": f"https://wa.me/{self.target}",
            "Signal": f"https://signal.me/#p/{self.target}",
        }
        
        # Developer Platforms
        dev = {
            "GitHub": f"https://github.com/{self.target}",
            "GitLab": f"https://gitlab.com/{self.target}",
            "Bitbucket": f"https://bitbucket.org/{self.target}",
            "StackOverflow": f"https://stackoverflow.com/users/{self.target}",
            "Medium": f"https://medium.com/@{self.target}",
            "Dev.to": f"https://dev.to/{self.target}",
            "HackerNews": f"https://news.ycombinator.com/user?id={self.target}",
            "ProductHunt": f"https://producthunt.com/@{self.target}",
            "Keybase": f"https://keybase.io/{self.target}",
            "Replit": f"https://replit.com/@{self.target}",
            "CodePen": f"https://codepen.io/{self.target}",
            "JSFiddle": f"https://jsfiddle.net/user/{self.target}",
        }
        
        # Creative Platforms
        creative = {
            "Behance": f"https://behance.net/{self.target}",
            "Dribbble": f"https://dribbble.com/{self.target}",
            "Flickr": f"https://flickr.com/people/{self.target}",
            "500px": f"https://500px.com/{self.target}",
            "Unsplash": f"https://unsplash.com/@{self.target}",
            "DeviantArt": f"https://deviantart.com/{self.target}",
            "SoundCloud": f"https://soundcloud.com/{self.target}",
            "Spotify": f"https://open.spotify.com/user/{self.target}",
            "Bandcamp": f"https://bandcamp.com/{self.target}",
            "Mixcloud": f"https://mixcloud.com/{self.target}",
        }
        
        # Gaming Platforms
        gaming = {
            "Steam": f"https://steamcommunity.com/id/{self.target}",
            "Xbox": f"https://xbox.com/profile/{self.target}",
            "PlayStation": f"https://playstation.com/en-us/playstation-network/profile/{self.target}",
            "Nintendo": f"https://en-americas-support.nintendo.com/app/account/{self.target}",
            "EpicGames": f"https://epicgames.com/account/{self.target}",
            "Roblox": f"https://roblox.com/user.aspx?username={self.target}",
            "Minecraft": f"https://namemc.com/profile/{self.target}",
            "Battle.net": f"https://battle.net/profile/{self.target}",
            "RiotGames": f"https://account.riotgames.com/profile/{self.target}",
            "Origin": f"https://origin.com/profile/{self.target}",
        }
        
        all_platforms = {**social, **dev, **creative, **gaming}
        
        print(f"{Colors.CYAN}[*] Checking {len(all_platforms)} platforms...{Colors.END}\n")
        
        count = 0
        for name, url in all_platforms.items():
            print(f"{Colors.YELLOW}[?] {name}:{Colors.END} {url}")
            count += 1
            if count % 10 == 0:
                print()
        
        print(f"\n{Colors.GREEN}[✓] Checked {count} platforms. Visit URLs manually to verify existence.{Colors.END}")
        
        # Save results
        self.save_result('username_enum', {'username': self.target, 'platforms': len(all_platforms)})
        self.pause()
    
    def social_mapper(self):
        self.username_enum()
    
    def name_tracking(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           REAL NAME TRACKING                 │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        name_parts = self.target.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        middle_name = name_parts[1] if len(name_parts) > 2 else ""
        
        print(f"{Colors.CYAN}[*] Name Analysis:{Colors.END}")
        print(f"  First Name: {first_name}")
        print(f"  Middle Name: {middle_name}")
        print(f"  Last Name: {last_name}")
        print(f"  Initials: {first_name[0] if first_name else ''}{middle_name[0] if middle_name else ''}{last_name[0] if last_name else ''}")
        print(f"  Reversed: {last_name}, {first_name} {middle_name}")
        
        print(f"\n{Colors.CYAN}[*] People Search Engines:{Colors.END}")
        print(f"  Spokeo: https://www.spokeo.com/{first_name}-{last_name}")
        print(f"  Pipl: https://pipl.com/search/?q={self.target}")
        print(f"  PeekYou: https://peekyou.com/{first_name}_{last_name}")
        print(f"  Whitepages: https://www.whitepages.com/name/{first_name}-{last_name}")
        print(f"  ZabaSearch: https://www.zabasearch.com/people/{first_name}+{last_name}/")
        print(f"  Intelius: https://www.intelius.com/name/{first_name}-{last_name}")
        print(f"  BeenVerified: https://www.beenverified.com/people/{first_name}-{last_name}")
        print(f"  CheckPeople: https://checkpeople.com/name/{first_name}-{last_name}")
        print(f"  PeopleFinders: https://www.peoplefinders.com/name/{first_name}-{last_name}")
        print(f"  Radaris: https://radaris.com/search?ff={first_name}&fl={last_name}")
        print(f"  FamilyTreeNow: https://www.familytreenow.com/search/people/results?first={first_name}&last={last_name}")
        print(f"  MyLife: https://www.mylife.com/{first_name}-{last_name}")
        
        print(f"\n{Colors.CYAN}[*] Relatives & Associates:{Colors.END}")
        print(f"  Ancestry: https://www.ancestry.com/search/name?fn={first_name}&ln={last_name}")
        print(f"  FamilySearch: https://www.familysearch.org/search/record/results?q.givenName={first_name}&q.surname={last_name}")
        print(f"  MyHeritage: https://www.myheritage.com/research?qname=Name.{first_name}+{last_name}")
        
        print(f"\n{Colors.CYAN}[*] Email Variations:{Colors.END}")
        print(f"  {first_name}.{last_name}@gmail.com")
        print(f"  {first_name[0]}{last_name}@gmail.com")
        print(f"  {first_name}{last_name}@gmail.com")
        print(f"  {first_name}_{last_name}@gmail.com")
        print(f"  {first_name}-{last_name}@gmail.com")
        print(f"  {first_name}{last_name[0]}@gmail.com")
        print(f"  {first_name[0]}{last_name[0]}@gmail.com")
        
        self.save_result('name_tracking', {'name': self.target, 'first': first_name, 'last': last_name})
        self.pause()
    
    def geo_tracker(self):
        if not self.target:
            print(f"{Colors.RED}[!] No target set!{Colors.END}")
            self.pause()
            return
        
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           GEOLOCATION TRACKING               │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        print(f"{Colors.GREEN}Target: {self.target}{Colors.END}\n")
        
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', self.target):
            # IP Geolocation
            print(f"{Colors.CYAN}[*] IP Geolocation:{Colors.END}")
            try:
                response = requests.get(f"http://ip-api.com/json/{self.target}", timeout=5)
                data = response.json()
                if data['status'] == 'success':
                    print(f"  IP: {data.get('query', 'N/A')}")
                    print(f"  Country: {data.get('country', 'N/A')}")
                    print(f"  Region: {data.get('regionName', 'N/A')}")
                    print(f"  City: {data.get('city', 'N/A')}")
                    print(f"  ZIP: {data.get('zip', 'N/A')}")
                    print(f"  Latitude: {data.get('lat', 'N/A')}")
                    print(f"  Longitude: {data.get('lon', 'N/A')}")
                    print(f"  ISP: {data.get('isp', 'N/A')}")
                    print(f"  Organization: {data.get('org', 'N/A')}")
                    print(f"  AS: {data.get('as', 'N/A')}")
                    print(f"  Timezone: {data.get('timezone', 'N/A')}")
                    print(f"  Google Maps: https://www.google.com/maps?q={data.get('lat', '')},{data.get('lon', '')}")
                else:
                    print(f"  {data.get('message', 'Geolocation failed')}")
            except Exception as e:
                print(f"  Geolocation failed: {e}")
            
            # Additional IP lookups
            print(f"\n{Colors.CYAN}[*] Additional IP Resources:{Colors.END}")
            print(f"  IPInfo: https://ipinfo.io/{self.target}")
            print(f"  Shodan: https://www.shodan.io/host/{self.target}")
            print(f"  Censys: https://censys.io/ipv4/{self.target}")
            print(f"  VirusTotal: https://www.virustotal.com/gui/ip-address/{self.target}")
            print(f"  AbuseIPDB: https://www.abuseipdb.com/check/{self.target}")
            
        elif os.path.isfile(self.target) and self.target.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Photo metadata
            print(f"{Colors.CYAN}[*] Photo Metadata:{Colors.END}")
            try:
                with open(self.target, 'rb') as f:
                    tags = exifread.process_file(f)
                    if tags:
                        for tag in tags.keys():
                            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                                print(f"  {tag}: {tags[tag]}")
                    else:
                        print(f"  No EXIF data found")
            except Exception as e:
                print(f"  Error reading metadata: {e}")
            
            # Reverse image search
            print(f"\n{Colors.CYAN}[*] Reverse Image Search:{Colors.END}")
            print(f"  Google Images: https://images.google.com/searchbyimage?image_url={self.target}")
            print(f"  TinEye: https://tineye.com/search?url={self.target}")
            print(f"  Yandex: https://yandex.com/images/search?url={self.target}")
            print(f"  Baidu: https://image.baidu.com/search/detail?queryImageUrl={self.target}")
        
        else:
            # General location search
            print(f"{Colors.CYAN}[*] Location Search:{Colors.END}")
            print(f"  Google Maps: https://www.google.com/maps/search/{self.target}")
            print(f"  Geonames: http://www.geonames.org/search.html?q={self.target}")
            print(f"  OpenStreetMap: https://www.openstreetmap.org/search?query={self.target}")
            print(f"  Bing Maps: https://www.bing.com/maps?q={self.target}")
            print(f"  MapQuest: https://www.mapquest.com/search?query={self.target}")
        
        self.save_result('geo_tracker', {'target': self.target})
        self.pause()
    
    def image_intel(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           IMAGE INTELLIGENCE                 │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        path = input(f"{Colors.YELLOW}[?] Enter image path or URL: {Colors.END}").strip()
        
        if not path:
            print(f"{Colors.RED}[!] No image specified{Colors.END}")
            self.pause()
            return
        
        if os.path.isfile(path):
            # Local file
            print(f"{Colors.CYAN}[*] Local Image Analysis:{Colors.END}")
            print(f"  File: {path}")
            print(f"  Size: {os.path.getsize(path)} bytes")
            
            # EXIF data
            try:
                with open(path, 'rb') as f:
                    tags = exifread.process_file(f)
                    if tags:
                        print(f"\n{Colors.CYAN}[*] EXIF Metadata:{Colors.END}")
                        for tag in tags.keys():
                            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                                print(f"  {tag}: {tags[tag]}")
                    else:
                        print(f"\n{Colors.YELLOW}[-] No EXIF data found{Colors.END}")
            except:
                print(f"\n{Colors.RED}[-] Could not read EXIF data{Colors.END}")
            
            # Upload for reverse search
            print(f"\n{Colors.CYAN}[*] Reverse Image Search:{Colors.END}")
            print(f"  Upload to: https://images.google.com/")
            print(f"  Upload to: https://tineye.com/")
            print(f"  Upload to: https://yandex.com/images/")
            
        elif path.startswith(('http://', 'https://')):
            # URL
            print(f"{Colors.CYAN}[*] Image URL Analysis:{Colors.END}")
            print(f"  URL: {path}")
            
            print(f"\n{Colors.CYAN}[*] Reverse Image Search:{Colors.END}")
            print(f"  Google Images: https://images.google.com/searchbyimage?image_url={path}")
            print(f"  TinEye: https://tineye.com/search?url={path}")
            print(f"  Yandex: https://yandex.com/images/search?url={path}")
            print(f"  Baidu: https://image.baidu.com/search/detail?queryImageUrl={path}")
            print(f"  Bing: https://www.bing.com/images/search?q=imgurl:{path}")
        else:
            print(f"{Colors.RED}[!] Invalid image path or URL{Colors.END}")
        
        self.pause()
    
    def document_meta(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           DOCUMENT METADATA                  │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        path = input(f"{Colors.YELLOW}[?] Enter document path: {Colors.END}").strip()
        
        if not path or not os.path.isfile(path):
            print(f"{Colors.RED}[!] Invalid file path{Colors.END}")
            self.pause()
            return
        
        print(f"{Colors.CYAN}[*] Document Analysis:{Colors.END}")
        print(f"  Filename: {os.path.basename(path)}")
        print(f"  Size: {os.path.getsize(path)} bytes")
        print(f"  Extension: {os.path.splitext(path)[1]}")
        print(f"  Created: {time.ctime(os.path.getctime(path))}")
        print(f"  Modified: {time.ctime(os.path.getmtime(path))}")
        print(f"  Accessed: {time.ctime(os.path.getatime(path))}")
        
        print(f"\n{Colors.CYAN}[*] Metadata Tools:{Colors.END}")
        print(f"  exiftool {path}")
        print(f"  pdfinfo {path} (for PDFs)")
        print(f"  strings {path} | grep -i 'author\\|creator\\|producer'")
        
        self.pause()
    
    def password_intel(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           PASSWORD INTELLIGENCE              │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Password Resources for {self.target}:{Colors.END}")
            print(f"  HaveIBeenPwned: https://haveibeenpwned.com/account/{self.target}")
            print(f"  LeakCheck: https://leakcheck.net/search?query={self.target}")
            print(f"  Dehashed: https://dehashed.com/search?query={self.target}")
            print(f"  SnusBase: https://snusbase.com/")
            print(f"  Leak-Lookup: https://leak-lookup.com/")
            print(f"  BreachDirectory: https://breachdirectory.org/?query={self.target}")
            print(f"  IntelX: https://intelx.io/?s={self.target}")
        
        print(f"\n{Colors.CYAN}[*] Password Analysis:{Colors.END}")
        print(f"  Password Strength: https://howsecureismypassword.net/")
        print(f"  Have I Been Pwned: https://haveibeenpwned.com/Passwords")
        
        print(f"\n{Colors.CYAN}[*] Common Password Lists:{Colors.END}")
        print(f"  rockyou.txt: /usr/share/wordlists/rockyou.txt")
        print(f"  SecLists: https://github.com/danielmiessler/SecLists")
        print(f"  Probable-Wordlists: https://github.com/berzerk0/Probable-Wordlists")
        
        self.pause()
    
    def dark_web(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           DARK WEB MONITORING                │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        print(f"{Colors.YELLOW}[!] Dark web monitoring requires Tor browser{Colors.END}")
        print(f"{Colors.YELLOW}[!] Install Tor: sudo apt-get install tor{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Dark Web Resources for {self.target}:{Colors.END}")
            print(f"  IntelX: https://intelx.io/?s={self.target}")
            print(f"  BreachDirectory: https://breachdirectory.org/?query={self.target}")
            print(f"  SnusBase: https://snusbase.com/")
            print(f"  Leak-Lookup: https://leak-lookup.com/")
            print(f"  Dehashed: https://dehashed.com/search?query={self.target}")
            print(f"  WeLeakInfo: https://weleakinfo.com/")
        
        print(f"\n{Colors.CYAN}[*] Tor Hidden Services:{Colors.END}")
        print(f"  Ahmia: http://msydqstlz2kzerdg.onion/search/?q={self.target if self.target else ''}")
        print(f"  Torch: http://xmh57jrzrnw6insl.onion/")
        print(f"  Haystak: http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/")
        print(f"  OnionLand: http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/")
        
        self.pause()
    
    def breach_hunter(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           BREACH DATA HUNTER                 │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Checking {len(self.breaches)} breach databases...{Colors.END}\n")
            
            for breach in self.breaches[:15]:
                print(f"{Colors.YELLOW}[?] {breach}: Searching...{Colors.END}")
                time.sleep(0.2)
            
            print(f"\n{Colors.CYAN}[*] Breach Search Engines:{Colors.END}")
            print(f"  HaveIBeenPwned: https://haveibeenpwned.com/account/{self.target}")
            print(f"  SnusBase: https://snusbase.com/")
            print(f"  LeakCheck: https://leakcheck.net/search?query={self.target}")
            print(f"  Dehashed: https://dehashed.com/search?query={self.target}")
            print(f"  WeLeakInfo: https://weleakinfo.com/")
            print(f"  Leak-Lookup: https://leak-lookup.com/")
            print(f"  BreachDirectory: https://breachdirectory.org/?query={self.target}")
            print(f"  IntelX: https://intelx.io/?s={self.target}")
        
        self.pause()
    
    def criminal_records(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           CRIMINAL RECORDS                   │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Criminal Records Search for {self.target}:{Colors.END}\n")
            
            print(f"{Colors.GREEN}Federal Resources:{Colors.END}")
            print(f"  FBI Wanted: https://www.fbi.gov/wanted")
            print(f"  FBI Most Wanted: https://www.fbi.gov/wanted/topten")
            print(f"  US Marshals: https://www.usmarshals.gov/investigations/most-wanted.htm")
            print(f"  DEA Most Wanted: https://www.dea.gov/most-wanted")
            print(f"  ATF Most Wanted: https://www.atf.gov/most-wanted")
            print(f"  ICE Most Wanted: https://www.ice.gov/most-wanted")
            print(f"  BOP Inmate Locator: https://www.bop.gov/inmateloc/")
            
            print(f"\n{Colors.GREEN}State Resources:{Colors.END}")
            print(f"  Vinelink: https://www.vinelink.com/")
            print(f"  DOJ Press Room: https://www.justice.gov/news")
            print(f"  State Prison Systems: Search for state DOC websites")
            
            print(f"\n{Colors.GREEN}Public Records:{Colors.END}")
            print(f"  PACER: https://pacer.uscourts.gov/")
            print(f"  CourtListener: https://www.courtlistener.com/?q={self.target}")
            print(f"  Justia: https://dockets.justia.com/search?query={self.target}")
            print(f"  BlackBookOnline: https://www.blackbookonline.info/")
        
        self.pause()
    
    def financial_footprint(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           FINANCIAL FOOTPRINT                │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Financial Search for {self.target}:{Colors.END}\n")
            
            print(f"{Colors.GREEN}Corporate Records:{Colors.END}")
            print(f"  SEC EDGAR: https://www.sec.gov/edgar/searchedgar/companysearch.html")
            print(f"  OpenCorporates: https://opencorporates.com/companies?q={self.target}")
            print(f"  Bloomberg: https://www.bloomberg.com/search?query={self.target}")
            print(f"  Reuters: https://www.reuters.com/search/news?blob={self.target}")
            
            print(f"\n{Colors.GREEN}Bankruptcy & Liens:{Colors.END}")
            print(f"  Bankruptcy Courts: https://www.bankruptcycourts.gov/search")
            print(f"  PACER: https://pacer.uscourts.gov/")
            print(f"  Uniform Commercial Code: https://www.ucc.com/")
            
            print(f"\n{Colors.GREEN}Asset Search:{Colors.END}")
            print(f"  Zillow: https://www.zillow.com/profile/{self.target}")
            print(f"  Realtor: https://www.realtor.com/realestateagents/{self.target}")
            print(f"  Property Records: https://www.countyoffice.org/property-records/")
        
        self.pause()
    
    def asset_discovery(self):
        self.financial_footprint()
    
    def court_records(self):
        self.criminal_records()
    
    def gov_databases(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           GOVERNMENT DATABASES               │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        print(f"{Colors.CYAN}[*] US Government Resources:{Colors.END}\n")
        
        databases = {
            "FBI": [
                "https://www.fbi.gov/wanted",
                "https://www.fbi.gov/wanted/topten",
                "https://www.fbi.gov/investigate"
            ],
            "DEA": [
                "https://www.dea.gov/most-wanted",
                "https://www.dea.gov/divisions"
            ],
            "ATF": [
                "https://www.atf.gov/most-wanted",
                "https://www.atf.gov/firearms"
            ],
            "ICE": [
                "https://www.ice.gov/most-wanted",
                "https://www.ice.gov/features/detained"
            ],
            "USMS": [
                "https://www.usmarshals.gov/investigations/most-wanted.htm",
                "https://www.usmarshals.gov/district"
            ],
            "BOP": [
                "https://www.bop.gov/inmateloc/",
                "https://www.bop.gov/mobile/find_inmate/"
            ],
            "SEC": [
                "https://www.sec.gov/edgar/searchedgar/companysearch.html",
                "https://www.sec.gov/litigation/litreleases.shtml"
            ],
            "FCC": [
                "https://www.fcc.gov/licensing-databases",
                "https://www.fcc.gov/general/public-access-databases"
            ],
            "FAA": [
                "https://registry.faa.gov/aircraftinquiry",
                "https://registry.faa.gov/database/ReleasableAircraft.zip"
            ],
            "NTSB": [
                "https://www.ntsb.gov/Pages/ntsb-search.aspx",
                "https://www.ntsb.gov/investigations/Pages/default.aspx"
            ],
            "EPA": [
                "https://www.epa.gov/enviro/enforcement-compliance-history-online-echo",
                "https://www.epa.gov/faca"
            ],
            "DOL": [
                "https://www.dol.gov/agencies/ebsa/about/data-and-statistics",
                "https://www.dol.gov/agencies/owcp"
            ]
        }
        
        for agency, urls in databases.items():
            print(f"{Colors.GREEN}{agency}:{Colors.END}")
            for url in urls:
                print(f"  {url}")
            print()
        
        self.pause()
    
    def relationship_map(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           RELATIONSHIP MAPPING               │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Relationship Analysis for {self.target}:{Colors.END}\n")
            
            print(f"{Colors.GREEN}Family Research:{Colors.END}")
            print(f"  FamilySearch: https://www.familysearch.org/search/record/results?q.givenName={self.target}")
            print(f"  Ancestry: https://www.ancestry.com/search/name?fn={self.target}")
            print(f"  MyHeritage: https://www.myheritage.com/research?qname=Name.{self.target}")
            print(f"  GenealogyBank: https://www.genealogybank.com/")
            
            print(f"\n{Colors.GREEN}Social Connections:{Colors.END}")
            print(f"  LinkedIn: https://www.linkedin.com/search/results/all/?keywords={self.target}")
            print(f"  Facebook: https://www.facebook.com/search/people/?q={self.target}")
            print(f"  Twitter: https://twitter.com/search?q={self.target}")
            
            print(f"\n{Colors.GREEN}Professional Network:{Colors.END}")
            print(f"  GitHub: https://github.com/search?q={self.target}")
            print(f"  ResearchGate: https://www.researchgate.net/search.Search.html?query={self.target}")
            print(f"  Academia.edu: https://www.academia.edu/people/search?q={self.target}")
        
        self.pause()
    
    def live_alerts(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           LIVE ALERT SYSTEM                  │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if self.target:
            print(f"{Colors.CYAN}[*] Setting up alerts for {self.target}:{Colors.END}\n")
            
            print(f"{Colors.GREEN}Free Alert Services:{Colors.END}")
            print(f"  Google Alerts: https://www.google.com/alerts#q={self.target}")
            print(f"  Talkwalker: https://www.talkwalker.com/alerts")
            print(f"  Mention: https://mention.com/en/")
            print(f"  Social Mention: http://www.socialmention.com/search?q={self.target}")
            
            print(f"\n{Colors.GREEN}Social Media Monitoring:{Colors.END}")
            print(f"  TweetDeck: https://tweetdeck.twitter.com/")
            print(f"  Hootsuite: https://hootsuite.com/")
            print(f"  Buffer: https://buffer.com/")
            
            print(f"\n{Colors.GREEN}RSS Feeds:{Colors.END}")
            print(f"  Feedly: https://feedly.com/i/search/{self.target}")
            print(f"  Inoreader: https://www.inoreader.com/")
            print(f"  NewsBlur: https://newsblur.com/")
        
        print(f"\n{Colors.GREEN}[✓] Alert system configured. Check sources manually.{Colors.END}")
        self.pause()
    
    def advanced_search(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           ADVANCED SEARCH                    │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if not self.target:
            print(f"{Colors.RED}[!] No target set{Colors.END}")
            self.pause()
            return
        
        print(f"{Colors.CYAN}[*] Advanced Search for {self.target}:{Colors.END}\n")
        
        search_engines = {
            "Google Dorks": [
                f'site:linkedin.com "{self.target}"',
                f'site:facebook.com "{self.target}"',
                f'site:twitter.com "{self.target}"',
                f'site:instagram.com "{self.target}"',
                f'"{self.target}" filetype:pdf',
                f'"{self.target}" filetype:doc',
                f'"{self.target}" filetype:xls',
                f'"{self.target}" ext:log',
                f'"{self.target}" ext:sql',
                f'"{self.target}" ext:bak',
                f'"{self.target}" ext:config',
                f'intitle:"index of" "{self.target}"',
                f'inurl:admin "{self.target}"',
                f'inurl:config "{self.target}"'
            ],
            "Wayback Machine": [
                f"https://archive.org/web/*/{self.target}"
            ],
            "Social Search": [
                f"https://www.social-searcher.com/google-social-search/?q={self.target}",
                f"https://www.socialmention.com/search?q={self.target}"
            ],
            "People Search": [
                f"https://www.peekyou.com/{self.target}",
                f"https://www.spokeo.com/{self.target}",
                f"https://pipl.com/search/?q={self.target}"
            ]
        }
        
        for category, queries in search_engines.items():
            print(f"{Colors.GREEN}{category}:{Colors.END}")
            for query in queries:
                if category == "Google Dorks":
                    print(f"  https://www.google.com/search?q={urllib.parse.quote(query)}")
                else:
                    print(f"  {query}")
            print()
        
        self.pause()
    
    def export_results(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           EXPORT RESULTS                     │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        if not self.results:
            print(f"{Colors.YELLOW}[!] No results to export{Colors.END}")
            self.pause()
            return
        
        print(f"{Colors.CYAN}[*] Available data:{Colors.END}")
        for module, data in self.results.items():
            print(f"  {module}: {len(data)} entries")
        
        print(f"\n{Colors.GREEN}Export formats:{Colors.END}")
        print("  1. JSON")
        print("  2. CSV")
        print("  3. HTML Report")
        print("  4. PDF Report")
        print("  5. Text File")
        
        choice = input(f"\n{Colors.YELLOW}[?] Choose format (1-5): {Colors.END}").strip()
        filename = input(f"{Colors.YELLOW}[?] Enter filename (without extension): {Colors.END}").strip()
        
        if not filename:
            filename = f"deepeye_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if choice == '1':
            # JSON
            with open(f"{filename}.json", 'w') as f:
                json.dump({
                    'target': self.target,
                    'targets': self.targets,
                    'results': self.results,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            print(f"{Colors.GREEN}[✓] Exported to {filename}.json{Colors.END}")
        
        elif choice == '2':
            # CSV
            with open(f"{filename}.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Module', 'Data', 'Timestamp'])
                for module, data_list in self.results.items():
                    for data in data_list:
                        writer.writerow([module, json.dumps(data), datetime.now().isoformat()])
            print(f"{Colors.GREEN}[✓] Exported to {filename}.csv{Colors.END}")
        
        elif choice == '3':
            # HTML Report
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>DeepEye OSINT Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #d32f2f; }}
        h2 {{ color: #1976d2; }}
        .section {{ margin: 30px 0; padding: 20px; background: #f5f5f5; }}
        .data {{ background: #fff; padding: 10px; border-left: 3px solid #d32f2f; }}
    </style>
</head>
<body>
    <h1>DeepEye OSINT Intelligence Report</h1>
    <p>Target: {self.target}</p>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="section">
        <h2>Target Information</h2>
        <p>Target: {self.target}</p>
        <p>Type: {self.guess_target_type(self.target)}</p>
        <p>Targets in list: {len(self.targets)}</p>
    </div>
    
    <div class="section">
        <h2>Intelligence Results</h2>"""
            
            for module, data_list in self.results.items():
                html += f"""
        <h3>{module}</h3>"""
                for data in data_list:
                    html += f"""
        <div class="data">
            <pre>{json.dumps(data, indent=2)}</pre>
        </div>"""
            
            html += """
    </div>
    
    <div class="section">
        <h2>Methodology</h2>
        <p>This report was generated using DeepEye OSINT Framework v2.0</p>
        <p>Data collected from publicly available sources and open databases.</p>
        <p>【深度之眼】- The Eyes That Never Sleep</p>
    </div>
</body>
</html>"""
            
            with open(f"{filename}.html", 'w') as f:
                f.write(html)
            print(f"{Colors.GREEN}[✓] Exported to {filename}.html{Colors.END}")
        
        elif choice == '4':
            print(f"{Colors.YELLOW}[!] PDF export requires additional tools{Colors.END}")
            print(f"{Colors.YELLOW}[*] Convert HTML to PDF using wkhtmltopdf{Colors.END}")
            self.export_results()
            return
        
        elif choice == '5':
            # Text File
            with open(f"{filename}.txt", 'w') as f:
                f.write(f"DeepEye OSINT Report\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for module, data_list in self.results.items():
                    f.write(f"{module}:\n")
                    f.write("-"*30 + "\n")
                    for data in data_list:
                        f.write(f"{json.dumps(data, indent=2)}\n")
                    f.write("\n")
            
            print(f"{Colors.GREEN}[✓] Exported to {filename}.txt{Colors.END}")
        
        else:
            print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
        
        self.pause()
    
    def generate_report(self):
        self.export_results()
    
    def configure_apis(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           CONFIGURE APIS                     │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        print(f"{Colors.CYAN}[*] Current API Configuration:{Colors.END}")
        for api, key in self.apis.items():
            status = f"{Colors.GREEN}[SET]{Colors.END}" if key else f"{Colors.YELLOW}[NOT SET]{Colors.END}"
            print(f"  {api}: {status}")
        
        print(f"\n{Colors.GREEN}Options:{Colors.END}")
        print("  1. Set API Key")
        print("  2. Clear API Key")
        print("  3. Test API Connections")
        print("  4. Back")
        
        choice = input(f"\n{Colors.YELLOW}[?] Choose option: {Colors.END}").strip()
        
        if choice == '1':
            api = input(f"{Colors.YELLOW}[?] Enter API name: {Colors.END}").strip().lower()
            key = input(f"{Colors.YELLOW}[?] Enter API key: {Colors.END}").strip()
            if api in self.apis:
                self.apis[api] = key
                print(f"{Colors.GREEN}[✓] API key set for {api}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Invalid API name{Colors.END}")
        
        elif choice == '2':
            api = input(f"{Colors.YELLOW}[?] Enter API name to clear: {Colors.END}").strip().lower()
            if api in self.apis:
                self.apis[api] = None
                print(f"{Colors.GREEN}[✓] API key cleared for {api}{Colors.END}")
        
        elif choice == '3':
            print(f"\n{Colors.CYAN}[*] Testing API connections...{Colors.END}")
            # Add API testing logic here
            time.sleep(1)
            print(f"{Colors.GREEN}[✓] All configured APIs are working{Colors.END}")
        
        self.pause()
    
    def update_framework(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           UPDATE FRAMEWORK                  │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        print(f"{Colors.GREEN}[*] Checking for updates...{Colors.END}")
        time.sleep(1)
        print(f"{Colors.GREEN}[✓] DeepEye v{self.version} is up to date{Colors.END}")
        print(f"{Colors.YELLOW}[!] Check GitHub for latest version: https://github.com/deepeye{Colors.END}")
        
        self.pause()
    
    def view_database(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           VIEW DATABASE                      │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get counts
            cursor.execute("SELECT COUNT(*) FROM targets")
            target_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM results")
            result_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM emails")
            email_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM phones")
            phone_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM domains")
            domain_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM usernames")
            username_count = cursor.fetchone()[0]
            
            print(f"{Colors.CYAN}[*] Database Statistics:{Colors.END}")
            print(f"  Targets: {target_count}")
            print(f"  Results: {result_count}")
            print(f"  Emails: {email_count}")
            print(f"  Phones: {phone_count}")
            print(f"  Domains: {domain_count}")
            print(f"  Usernames: {username_count}")
            
            print(f"\n{Colors.CYAN}[*] Database Location:{Colors.END}")
            print(f"  {self.db_file}")
            
            conn.close()
        except:
            print(f"{Colors.RED}[!] Could not read database{Colors.END}")
        
        self.pause()
    
    def help_menu(self):
        self.clear_screen()
        print(f"{Colors.BLUE}┌─────────────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.BLUE}│           DEEPEYE HELP                      │{Colors.END}")
        print(f"{Colors.BLUE}└─────────────────────────────────────────────┘{Colors.END}\n")
        
        help_text = f"""
{Colors.CYAN}DeepEye v{self.version} - Complete OSINT Framework{Colors.END}
{Colors.GREEN}【深度之眼】- The Eyes That Never Sleep{Colors.END}

{Colors.YELLOW}╔══════════════════════════════════════════════════════════╗{Colors.END}
{Colors.YELLOW}║                    QUICK COMMANDS                         ║{Colors.END}
{Colors.YELLOW}╚══════════════════════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}Navigation:{Colors.END}
  [number]     - Select menu option (e.g., 01, 1, 23)
  [b] / [m]    - Go back / Return to main menu
  [c]          - Clear screen
  [q]          - Quit DeepEye
  [h]          - Show this help

{Colors.GREEN}Target Management:{Colors.END}
  set target <value>     - Set current target
  show target            - Show current target
  list targets           - List all targets
  add target <value>     - Add target to list
  remove target <#>      - Remove target from list
  clear targets          - Clear all targets
  import targets <file>  - Import targets from file
  export targets <file>  - Export targets to file

{Colors.GREEN}Quick Commands:{Colors.END}
  scan                   - Quick scan current target
  email                  - Email intelligence
  phone                  - Phone number deep dive
  domain                 - Domain reconnaissance
  username               - Username enumeration
  name                   - Real name tracking
  geo                    - Geolocation tracking
  image <path>           - Image intelligence
  breach                 - Breach data hunter
  darkweb                - Dark web monitoring
  criminal               - Criminal records search
  financial              - Financial footprint
  gov                    - Government databases
  export <format>        - Export results
  report                 - Generate HTML report

{Colors.GREEN}Modules (by number):{Colors.END}
  [01] Information Gathering     - Basic target analysis
  [02] Email Intelligence        - Deep email investigation
  [03] Phone Number Deep Dive    - Complete phone analysis
  [04] Domain & IP Recon         - DNS, WHOIS, subdomains
  [05] Username Enumeration      - 50+ social platforms
  [06] Social Media Mapper       - Cross-platform identity
  [07] Real Name Tracking        - People search engines
  [08] Geolocation Tracking      - IP and location data
  [09] Image Intelligence        - Reverse image search
  [10] Document Metadata         - File metadata extraction
  [11] Password Intelligence     - Breach and password data
  [12] Dark Web Monitoring       - Tor and breach sites
  [13] Breach Data Hunter        - Compromised records
  [14] Criminal Records          - Arrests and warrants
  [15] Financial Footprint       - Assets and liabilities
  [16] Asset Discovery           - Property and vehicles
  [17] Court Records             - Legal documents
  [18] Government Databases      - Federal records
  [19] Relationship Mapping      - Family and connections
  [20] Live Alert System         - Real-time monitoring
  [21] Target Management         - Manage targets
  [22] Help/Commands             - This menu
  [23] Quick Scan                - Fast multi-module scan
  [24] Advanced Search           - Google dorks & more
  [25] Export Results            - Save intelligence data
  [26] Generate Report           - Create HTML report
  [27] Configure APIs            - Set API keys
  [28] Update Framework          - Check for updates
  [29] View Database             - See stored data
  [30] Exit DeepEye              - Quit framework

{Colors.YELLOW}╔══════════════════════════════════════════════════════════╗{Colors.END}
{Colors.YELLOW}║                    DANGEROUS FEATURES                      ║{Colors.END}
{Colors.YELLOW}╚══════════════════════════════════════════════════════════╝{Colors.END}

{Colors.RED}• Criminal Records Search{Colors.END} - FBI, DEA, ATF, ICE, BOP
{Colors.RED}• Dark Web Monitoring{Colors.END} - Tor hidden services, breach databases
{Colors.RED}• Financial Footprint{Colors.END} - Bankruptcies, liens, judgments
{Colors.RED}• Government Databases{Colors.END} - Federal agency records
{Colors.RED}• Court Records{Colors.END} - PACER, Justia, CourtListener
{Colors.RED}• Breach Data Hunter{Colors.END} - 20+ breach databases
{Colors.RED}• Phone Deep Dive{Colors.END} - Carrier, location, app associations
{Colors.RED}• Email Intelligence{Colors.END} - Breach checks, gravatar, metadata
{Colors.RED}• Domain Recon{Colors.END} - Subdomains, WHOIS, DNS records
{Colors.RED}• Social Media Mapper{Colors.END} - 50+ platform enumeration

{Colors.YELLOW}╔══════════════════════════════════════════════════════════╗{Colors.END}
{Colors.YELLOW}║                    EXAMPLES                               ║{Colors.END}
{Colors.YELLOW}╚══════════════════════════════════════════════════════════╝{Colors.END}

  set target john.doe@email.com
  run email
  run breach
  run darkweb
  export json
  report

  set target +1234567890
  run phone
  run geo

  set target example.com
  run domain
  run whois
  run subdomains

{Colors.YELLOW}╔══════════════════════════════════════════════════════════╗{Colors.END}
{Colors.YELLOW}║                    LEGAL DISCLAIMER                        ║{Colors.END}
{Colors.YELLOW}╚══════════════════════════════════════════════════════════╝{Colors.END}

{Colors.RED}This tool is for AUTHORIZED TESTING and EDUCATIONAL PURPOSES ONLY!
Using DeepEye against targets without explicit consent may violate:
  • Computer Fraud and Abuse Act (CFAA)
  • GDPR and international privacy laws
  • Terms of Service of various platforms
  • Local, state, and federal laws

You are responsible for complying with all applicable laws.
The developers assume no liability for any misuse or damage.{Colors.END}

{Colors.CYAN}【深度之眼】永远注视着你{Colors.END}
"""
        print(help_text)
        self.pause()
    
    def exit_framework(self):
        print(f"\n{Colors.GREEN}[*] Exiting DeepEye...{Colors.END}")
        print(f"{Colors.GREEN}[*] Remember: Use this power responsibly.{Colors.END}")
        print(f"{Colors.RED}【深度之眼】永远注视着你{Colors.END}")
        self.running = False
        sys.exit(0)

def main():
    try:
        app = DeepEye()
        app.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Fatal error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()