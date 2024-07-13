import os
from os.path import exists
import time
import urllib.request
# debug printing added

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def datafolder():
    return os.path.expanduser("~")

def installPackage(pkname, dir, username):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Special-Rocket-Agents/sip/main/" + pkname + ".py", dir + "/user/" + username + "/pkg/" + pkname + ".py")

def mkdir(newpath):
    if not os.path.exists(newpath):
        print("A new path doesn't exist, creating a new one")
        os.makedirs(newpath)
        

def setupInit():
    import main
    cls()
    print("PyKern Setup")
    print("The Terminal OS made on python for fun!")
    print("Choosing a name for your install directory has been deprecated. It is set to pykern")
    print("Press ENTER to continue")
    input()
    installdir = "pykern"
    print("[-] Creating config file...")
    configfile = open("config.pykern", "w")
    configfile.write(installdir)
    configfile.close()
    print("[-] Creating the directory for installation...")

    mkdir(installdir)

    cls()
    print("Choose a username you want to use: ")
    username = input()
    print("[-] Creating the directory for user...")

    mkdir(installdir + "/user/" + username)

    print(installdir + "/user/" + username + "/pkg")

    mkdir(installdir + "/user/" + username + "/pkg")

    usrfile = open(installdir + "/user/.curuser", "w")
    usrfile.write(username)
    usrfile.close()

    print("[=] Downloading SIP package manager, please hold on...")
    try:
        installPackage("sip", installdir, username)
        installPackage("sip-uninstall", installdir, username)
        installPackage("fetch", installdir, username)
    except Exception as e:
        print(f"FAILED TO INSTALL SIP! PLEASE REDOWNLOAD OR CONTACT - {e}")
        time.sleep(1.8)
        print("Alright, here's what to do step-by-step: ")
        print(f"""1. Check your internet connection
2. Remove the created directory ({installdir}) and its entire contents
3. Restart the installation""")
        input("Press ENTER to remove config.pykern and exit. Do NOT press Ctrl + C/Z")
        os.remove("config.pykern")
        exit()
    print("[-] Setup has ended successfully!")
    print("Attempting to boot...")
    #installPackage("sip-update", installdir, username)
    main.boot()
