# CHANNEL : @Esfelurm | Github.com/esfelurm

import os
import subprocess
import threading
import time
from datetime import datetime
try:import requests
except:os.system("pip install requests")
try:os.system("cls")
except:os.system("clear")
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[00;34m', '\033[01;35m'
cn = '\033[00;36m'

# Global variable for IP change control
ip_change_active = False
ip_change_thread = None

def change_ip_linux():
    """Change IP on Linux using various methods"""
    try:
        # Method 1: Using dhclient (most common)
        print(f"{lgn}[+] Attempting to renew IP using dhclient...{cn}")
        os.system("sudo dhclient -r")  # Release IP
        time.sleep(2)
        os.system("sudo dhclient")      # Renew IP
        return True
    except:
        try:
            # Method 2: Using nmcli (NetworkManager)
            print(f"{lgn}[+] Trying nmcli method...{cn}")
            os.system("sudo nmcli networking off")
            time.sleep(2)
            os.system("sudo nmcli networking on")
            return True
        except:
            return False

def change_ip_windows():
    """Change IP on Windows"""
    try:
        print(f"{lgn}[+] Renewing IP on Windows...{cn}")
        os.system("ipconfig /release")
        time.sleep(2)
        os.system("ipconfig /renew")
        return True
    except:
        return False

def change_ip_mac():
    """Change IP on MacOS"""
    try:
        print(f"{lgn}[+] Renewing IP on MacOS...{cn}")
        os.system("sudo networksetup -setdhcp")
        return True
    except:
        return False

def get_current_ip():
    """Get current public IP address"""
    try:
        # Try multiple services for reliability
        services = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://checkip.amazonaws.com"
        ]
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue
        return "Unable to fetch IP"
    except:
        return "Error"

def ip_changer_auto(interval=40):
    """Auto change IP every specified interval"""
    global ip_change_active
    
    print(f"\n{lrd}{'='*60}")
    print(f"{lgn}[✓] IP Changer Started!")
    print(f"{yw}[!] IP will change every {interval} seconds")
    print(f"{lrd}{'='*60}\n")
    
    # Detect OS
    import platform
    os_name = platform.system().lower()
    
    change_count = 0
    while ip_change_active:
        try:
            # Get current IP before change
            old_ip = get_current_ip()
            print(f"{cn}[{datetime.now().strftime('%H:%M:%S')}] {yw}Current IP: {gn}{old_ip}")
            
            # Change IP based on OS
            print(f"{lgn}[*] Changing IP address...{cn}")
            
            if os_name == "windows":
                success = change_ip_windows()
            elif os_name == "darwin":  # MacOS
                success = change_ip_mac()
            else:  # Linux
                success = change_ip_linux()
            
            if success:
                time.sleep(3)  # Wait for IP to stabilize
                new_ip = get_current_ip()
                change_count += 1
                
                if old_ip != new_ip:
                    print(f"{lgn}[✓] IP Changed Successfully! {rd}Old: {old_ip} {gn}→ New: {new_ip}")
                    print(f"{lgn}[+] Total changes: {change_count}")
                else:
                    print(f"{lrd}[✗] IP might not have changed. Check network connection.")
            else:
                print(f"{lrd}[✗] Failed to change IP. Try running as administrator/root!")
                print(f"{yw}[!] On Linux/Mac: sudo python script.py")
                print(f"{yw}[!] On Windows: Run as Administrator")
            
            # Wait for next change
            for remaining in range(interval, 0, -1):
                if not ip_change_active:
                    break
                print(f"\r{cn}[*] Next IP change in: {yw}{remaining} seconds{cn}", end="")
                time.sleep(1)
            print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{lrd}[✗] Error: {e}")
            time.sleep(5)
    
    print(f"\n{lgn}[✓] IP Changer Stopped. Total changes: {change_count}")

def start_ip_changer():
    """Start the IP changer in a separate thread"""
    global ip_change_active, ip_change_thread
    
    if ip_change_active:
        print(f"{lrd}[!] IP Changer is already running!")
        return
    
    try:
        interval = int(input(f"\n{lrd}[{lgn}?{lrd}] {yw}Enter interval in seconds (default 40): {cn}") or "40")
        if interval < 10:
            print(f"{lrd}[!] Minimum interval is 10 seconds. Setting to 10.")
            interval = 10
    except:
        interval = 40
    
    ip_change_active = True
    ip_change_thread = threading.Thread(target=ip_changer_auto, args=(interval,), daemon=True)
    ip_change_thread.start()

def stop_ip_changer():
    """Stop the IP changer"""
    global ip_change_active
    if ip_change_active:
        ip_change_active = False
        print(f"\n{lgn}[✓] Stopping IP Changer...")
        return True
    else:
        print(f"{lrd}[!] IP Changer is not running!")
        return False

def show_ip_info():
    """Display current IP information"""
    print(f"\n{lrd}{'='*50}")
    print(f"{lgn}[+] Fetching IP Information...{cn}")
    
    ip = get_current_ip()
    print(f"{yw}Current Public IP: {gn}{ip}")
    
    # Try to get geolocation
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"{yw}Country: {gn}{data.get('country', 'N/A')}")
                print(f"{yw}City: {gn}{data.get('city', 'N/A')}")
                print(f"{yw}ISP: {gn}{data.get('isp', 'N/A')}")
    except:
        pass
    
    print(f"{lrd}{'='*50}\n")

def APIS_PROXY(PROX, Name_File, Save):
    if PROX == "1":
        f = open(Name_File,'wb')
        SOCKS4 = [			
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4",
            "https://openproxylist.xyz/socks4.txt",
            "https://proxyspace.pro/socks4.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://www.proxy-list.download/api/v1/get?type=socks4",
            "https://www.proxyscan.io/download?type=socks4",
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
            "https://api.openproxylist.xyz/socks4.txt",
        ]
        for api in SOCKS4:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}SOCKS4 : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()
        try:
            r = requests.get("https://www.socks-proxy.net/",timeout=5)
            Tag_H = str(r.content)
            Tag_H = Tag_H.split("<tbody>")
            Tag_H = Tag_H[1].split("</tbody>")
            Tag_H = Tag_H[0].split("<tr><td>")
            proxies = ""
            for proxy in Tag_H:
                proxy = proxy.split("<tr><td>")
                try:
                    proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
                except:
                    pass
                fd = open(Name_File,"a")
                fd.write(proxies)
                fd.close()
        except:
            pass
    if PROX == "2":
        f = open(Name_File,'wb')
        SOCKS5 = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
            "https://www.proxy-list.download/api/v1/get?type=socks5",
            "https://www.proxyscan.io/download?type=socks5",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
            "https://api.openproxylist.xyz/socks5.txt",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5",
            "https://openproxylist.xyz/socks5.txt",
            "https://proxyspace.pro/socks5.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
            "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
        ]
        for api in SOCKS5:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}SOCKS5 : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()
    if PROX == "3":
        f = open(Name_File,'wb')
        HTTP = [
            "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxyscan.io/download?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://api.openproxylist.xyz/http.txt",
            "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
            "http://alexa.lr2b.com/proxylist.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
            "https://proxy-spider.com/api/proxies.example.txt",
            "https://multiproxy.org/txt_all/proxy.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
            "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
            "https://openproxylist.xyz/http.txt",
            "https://proxyspace.pro/http.txt",
            "https://proxyspace.pro/https.txt",
            "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
            "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
            "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
            "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt",
            "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt",
            "https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt",
            "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://rootjazz.com/proxies/proxies.txt",
            "https://sheesh.rip/http.txt",
            "https://www.proxy-list.download/api/v1/get?type=https",
        ]
        for api in HTTP:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}HTTP : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()
    
    if PROX == "4":
        f = open(Name_File,'wb')
        HTTPS = ["https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
]
        for api in HTTPS:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}HTTPS : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()

    if PROX == "5":
        f = open(Name_File,'wb')
        Config = [
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub1.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub2.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub3.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub4.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub5.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub6.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub7.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Sub8.txt",
    "https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Splitted-By-Protocol/vmess.txt"
]
        for api in Config:
            try:
                r = requests.get(api,timeout=5)                
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}Config : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()

    if PROX == "6":
        f = open(Name_File,'wb')
        ShadowSocks = ["https://raw.githubusercontent.com/Bardiafa/Free-V2ray-Config/main/Splitted-By-Protocol/vless.txt","https://raw.githubusercontent.com/freefq/free/master/v2","https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub","https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt"]
        for api in ShadowSocks:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}Vless : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()
    if PROX == "7":
        f = open(Name_File,'wb')
        Vless = ["https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all"]
        for api in Vless:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}Trojan/SS : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()

    if PROX == "8":
        f = open(Name_File,'wb')
        Vless = ["https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt"]
        for api in Vless:
            try:
                r = requests.get(api,timeout=5)
                if Save == "y" or Save == "Y":
                    for Line in r.text.split('\n'):
                        time.sleep(0.5)
                        print (f"{lrd}[{lgn}+{lrd}] {lgn}Random : {gn}{Line}\n\n")
                else:f.write(r.content)
            except:
                pass
        f.close()
                                                                            
    print("\n\nHave already downloaded proxies list as "+Name_File)

def show_menu():
    """Display enhanced menu with IP Changer option"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
          {yw}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
          {yw}║                                                                                                                           {yw}║
          {yw}║                                                                                                                           {yw}║            
          {yw}║{lrd}                                        ____       {lgn} ____                                                                   {yw}║
          {yw}║{lrd}                                       / __ \\      {lgn}/ __ \\_________  _  ____  __                                            {yw}║
          {yw}║{lrd}                                      / / / /{rd}_____{lgn}/ /_/ / ___/ __ \\| |/_/ / / /                                            {yw}║
          {yw}║{lrd}                                     / /_/ /{rd}_____{lgn}/ ____/ /  / /_/ />  </ /_/ /                                             {yw}║
          {yw}║{lrd}                                    /_____/{lgn}     /_/   /_/   \\____/_/|_|\\__, /                                              {yw}║
          {yw}║{lgn}                                                                      /____/                                               {yw}║
          {yw}║                                              ==== P R O X Y ====                                                          {yw}║
          {yw}║                                                                                                                           {yw}║
          {yw}╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
          {yw}║                                                                                                                           {yw}║
          {yw}║{lgn}             | Written by: {gn}Root & Blade{yw}                                                  {lgn}Version: {gn}1.0{yw}                      ║
          {yw}║{cn}             | Github.com/more-dark{yw}                                                                                        ║
          {yw}║                                                                                                                           {yw}║
          {yw}╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    print(f"""
          {rd}╔═══════════════════════════════════════════════════════════╗
          {rd}║{yw}              PROXY COLLECTOR MENU                         {rd}║
          {rd}╠═══════════════════════════════════════════════════════════╣
          {rd}║{gn}  1{yw}. SOCKS4 Proxies                                        {rd}║
          {rd}║{gn}  2{yw}. SOCKS5 Proxies                                        {rd}║
          {rd}║{gn}  3{yw}. HTTP Proxies                                          {rd}║
          {rd}║{gn}  4{yw}. HTTPS Proxies                                         {rd}║
          {rd}║{gn}  5{yw}. V2Ray Configs                                         {rd}║
          {rd}║{gn}  6{yw}. VLESS Configs                                         {rd}║
          {rd}║{gn}  7{yw}. Trojan/SS Configs                                     {rd}║
          {rd}║{gn}  8{yw}. Random/Merged Proxies                                 {rd}║
          {rd}╠═══════════════════════════════════════════════════════════╣
          {rd}║{pe}  9{yw}. 🌐 IP CHANGER (Auto IP Rotation)                      {rd}║
          {rd}║{pe} 10{yw}. ℹ️  Show Current IP Info                              {rd}║
          {rd}║{pe} 11{yw}. ⏹️  Stop IP Changer                                   {rd}║
          {rd}╠═══════════════════════════════════════════════════════════╣
          {rd}║{lrd}  0{yw}. Exit                                                  {rd}║
          {rd}╚═══════════════════════════════════════════════════════════╝
""")

# Main program
while True:
    show_menu()
    choice = input(f"\n{lrd}[{lgn}?{lrd}] {yw}Select option [0-11] : {cn}")
    
    if choice == "0":
        if ip_change_active:
            stop_ip_changer()
        print(f"\n{lgn}[✓] Thank you for using! {yw}Goodbye!{cn}\n")
        break
    
    elif choice == "9":
        # IP Changer Feature
        print(f"\n{lrd}{'='*60}")
        print(f"{lgn}🌐 IP ADDRESS CHANGER {yw}(Auto IP Rotation)")
        print(f"{lrd}{'='*60}")
        print(f"{yw}[!] This feature will automatically change your IP address")
        print(f"{yw}[!] Requires administrator/root privileges")
        print(f"{lrd}[!] Works on: Linux, Windows, MacOS")
        print(f"{yw}[!] Note: May disconnect your internet temporarily{cn}")
        print(f"{lrd}{'='*60}\n")
        
        confirm = input(f"{lrd}[{lgn}?{lrd}] {yw}Start IP Changer? [Y/N]: {cn}")
        if confirm.lower() == 'y':
            start_ip_changer()
            print(f"\n{yw}[!] Press Enter to return to menu (IP changer runs in background)")
            input()
        else:
            continue
    
    elif choice == "10":
        show_ip_info()
        input(f"\n{yw}[!] Press Enter to continue...")
    
    elif choice == "11":
        if stop_ip_changer():
            time.sleep(2)
        input(f"\n{yw}[!] Press Enter to continue...")
    
    elif choice in ["1","2","3","4","5","6","7","8"]:
        Name_File = input(f"\n{lrd}[{lgn}+{lrd}] {cn}Enter filename to save proxies (e.g., proxies.txt): ")
        Save = input(f"\n{lrd}[{lgn}+{lrd}] {cn}Display in terminal? [Y/N]: ")
        print(f"\n{lgn}[*] Collecting proxies... Please wait{cn}\n")
        APIS_PROXY(choice, Name_File, Save)
        print(f"\n{yw}Thank you for using! {lrd}| {gn}Channel: @Esfelurm{cn}")
        input(f"\n{yw}[!] Press Enter to continue...")
    
    else:
        print(f"\n{lrd}[✗] Invalid option! Please select 0-11{cn}")
        time.sleep(1)
