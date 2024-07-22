import os
from os.path import exists
import random
import time
from colorama import init
from colorama import Fore, Back, Style
import importlib.util
from pathlib import Path
import re
## Sys is used for arguments. Nothing else
import sys

import colorama

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
try:
    args = str(sys.argv[1])
except:
    args = None
    pass
osdir = ""
username = ""
packagecount = 0

curdir = ""

su = False

datafolder = Path.cwd()

############ COLOR ALIASING ############
# To make coloring easier #
yellow = Fore.YELLOW
red = Fore.RED
blue = Fore.BLUE
cyan = Fore.CYAN
bold = Style.BRIGHT
normal = Style.NORMAL
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
white = Fore.WHITE
reset = Fore.RESET

########################################
output = ""
Fore.LIGHTBLUE_EX
THISISLIGHTYELLOW = Fore.LIGHTYELLOW_EX # to make the icon readable
osicon = (
    Fore.LIGHTBLUE_EX + " ================== " + Style.RESET_ALL,
    Fore.LIGHTBLUE_EX + "|                  |" + Style.RESET_ALL,
    THISISLIGHTYELLOW + "|  ######          |" + Style.RESET_ALL,
    THISISLIGHTYELLOW + "|  #    #          |" + Style.RESET_ALL,
    Fore.LIGHTBLUE_EX + "|  ######          |" + Style.RESET_ALL,
    Fore.LIGHTBLUE_EX + "|  #        #   #  |" + Style.RESET_ALL,
    THISISLIGHTYELLOW + "|  #         # #   |" + Style.RESET_ALL,
    THISISLIGHTYELLOW + "|  #          #    |" + Style.RESET_ALL,
    Fore.LIGHTBLUE_EX + "|  #         #     |" + Style.RESET_ALL,
    Fore.LIGHTBLUE_EX + "|                  |" + Style.RESET_ALL,
    THISISLIGHTYELLOW + " ================== " + Style.RESET_ALL
)

def setPath(new):
    global curdir
    curdir = new

displayusername = username

def pykern():
    booten = True
    global osdir
    global username
    global packagecount
    global curdir
    global output
    global osicon
    global su
    global displayusername
    global args
    curdir = osdir
    displayusername = username
    print(Style.BRIGHT + "Welcome to PyKern" + Style.RESET_ALL)
    ## MOTD ###
    if not exists("shutmotd") or args != "debug":
        motd = [
            "SIP is the package manager, type 'sip help' for more info",
            f"If you don't want this Message Of The Day to appear, create a file named {Fore.GREEN}shutmotd{Fore.RESET} in the root.",
            "The repository's wiki has some great info, check it out later at https://github.com/Special-Rocket-Agents/pykern/wiki\nYour (reasonable) contribution is also welcome.",
            "SIP is also hosted on GitHub. Maybe the next big package is yours to create?",
            "The original code was by NitrogenDioxide, more explained in the README",
            "Heads-up! You can't use the arrow keys (↑/↓) to navigate recent commands!",
            "Check out our other products, such as KawaiiXOR to encrypt day to day texts",
            f"Installing the {green}kernset{reset} package will be beneficial to you in the long run.",
            "MOTDs will be added from time to time without notice, check back later."
        ]
        print(motd[random.randint(0, 8)])
    elif args == "debug":
        print(f"{bold}You have finished startup with {red}Debug Mode{reset} activated. Risk of system-wrecking even")
    while (True):
        if su == True:
            displayusername = "root"
        if curdir.find(osdir) == -1:
            curdir = osdir
        cmd = input(Fore.GREEN + curdir + Style.RESET_ALL + ": " + Fore.RED + displayusername + Style.RESET_ALL + " >> ")
        try:
            ## first setup
            args = []
            if cmd.find(" ") != -1:
                args = re.split(" (?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))", cmd)
                for x in range(len(args)):
                    args[x] = args[x].replace("\"", "")
                cmd = args[0]
            
            ## filecheck
            cf = open(osdir + "/user/" + username + "/pkg/" + cmd + ".py", "r")
            cf.close()
            ## actual command

            importantFunctions = [setPath]
            importantVars = [osdir, username, curdir, args, osicon] # do not change this order, you can add things to it
            if cmd == "":
                pass
            spec = importlib.util.spec_from_file_location(cmd,osdir + "/user/" + username + "/pkg/" + cmd + ".py")
            cmdmod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cmdmod)
            try:
                cmdmod.run(importantFunctions, importantVars)
            except Exception as error:
                print(f"{Style.BRIGHT}{Fore.RED}ERROR:{Style.RESET_ALL}{Fore.RESET} {error}")
        except Exception as error:
            if cmd == str("exit"):
                exit()
            elif cmd == "":
                pass

            else:
                print(Fore.LIGHTRED_EX + "Failed to find command \"" + cmd + "\"" + Style.RESET_ALL + ":")
                print(error)
def crit_error(reason):
    """
    The reason that this damn function exists is to avoid repetitive try/except statements.
    
    I'm essentially lying, this is for customized text and repetitive printing.
    """
    print(f"{bold}{red}[ERROR]{normal}{reset} {reason}")
    exit()
def boot():
    colorama.init(autoreset=True)

    global osdir
    global username
    global packagecount
    from setup import setupInit
    cls()
    print(bold + "Pykern Bootloader" + normal)        
    if not exists("config.pykern"):
        setupInit()
    print("[-] Connecting installdir to PyKern instance")
    f = open("config.pykern", "r")
    osdir = f.readlines()[0]
    f.close()
    if osdir != "pykern":
        crit_error(f"Configuration file does not match ({osdir}). Rename {bold}config.pykern{normal} to {yellow}pykern{reset}")
    print(f"{green}[x]{reset} Connected to:  " + osdir + ".")
    print(f"{blue}[-]{reset} Loading user")
    try:
        uf = open(osdir + "/user/.curuser", "r")
        username = uf.readline().lstrip().rstrip()
        uf.close()
    except:
        crit_error("Could not load current user, Delete the configuration file and the Pykern directory to reinstall.")
    print(f"{green}[x]{reset} Connected to the user: " + username)
    print(f"{blue}[-]{reset} Loading the packages")
    pkgdir = osdir + "/user/" + username + "/pkg"
    for path in os.listdir(pkgdir):
        if os.path.isfile(os.path.join(pkgdir, path)):
            print(f"{cyan}[-]{reset} - Loaded " + bold + path.replace(".py", "") + normal)
            packagecount += 1
    print(f"{green}{bold}[x]{normal}{reset} {lgreen}Done,{reset} loaded: " + bold + str(packagecount) + normal + " package(s).")
    print(f"{bold}{red}If this is your second time seeing this screen, it's a trivial bug I can't fix{reset}{normal}")
    # Note to self: You commented this for dev purposes. Uncomment it
    cls()
    pykern()
def debugboot():
    """
    Happy Trigger Finger

    Deviates from the usual boot process to troubleshitshoot.

    Triggered by passing the 'debug' argument aka 'python3 main.py debug'
    """
    colorama.init(autoreset=True)

    global osdir
    global username
    global packagecount
    from setup import setupInit
    danswer = input("Is it in your importance to clear the screen? [y/N]")
    if danswer.lower().startswith("y"):
        cls()
    else:
        print("=====================================================================================")
    del danswer
    print(bold + "Pykern Bootloader" + normal)
    print(f"{bold}{red}[!] You have enabled the debug mode.{reset}{normal}")
    print(f"{bold}{white}[i] {red}You can control some of the boot process to troubleshoot Pykern{reset}{normal}")
    print(f"{bold}{white}[i] {red}If you can reach the terminal, it is suggested that you use Kernset to reinstall your system{reset}{normal}")
    danswer = input(f"{green}[important]{reset} If this is your second time seeing this screen and you can't handle the debug hassle, type yes NOW! [yes/don't type anything] ")
    if danswer.lower().startswith("y"):
        print("This is a bug I am yet able to fix. You've probably seen it on normal boots too.")
        input()
        input("Press ENTER now to continue")
        packagecount = 0
        del danswer
        boot()
    else:
        print("First time debug selected.")
        del danswer
        pass
    input("Press ENTER to continue")
    if exists("config.pykern"):
        danswer = input(f"Would you like to rerun the {bold}S{normal}etup OR {bold}C{normal}ontinue as usual? [s/C] ")
        if danswer.lower() == "s" or danswer == "S" or danswer.lower() == "setup":
            print("Setup selected")
            del danswer
            setupInit()
        else:
            print("Continuing as usual...")
            del danswer
            pass
    else:
        danswer = input(f"The configuration file does not exist. It is recommended to run the setup.\n{red}WARNING: you will literally, like be unable to proceed further if you discomply.{reset} Do so? [Y/n]")
        if danswer.lower() == "n" or danswer.lower() == "no" or danswer.lower().startswith("no") == True:
            del danswer
            pass
        else:
            del danswer
            setupInit()
    print("[-] Preparing to access config.pykern / installdir...")
    input(f"{green}This part has automatic troubleshooting and thus you can only proceed further by pressing ENTER.{reset}")
    ## State of the art troubleshooting xd
    try:
        print("[-] Connecting installdir to PyKern instance [Accessing file (1/3)]")
        f = open("config.pykern", "r")
        print("[-] Connecting installdir to PyKern instance [Accessing file (2/3)]")
        osdir = f.readlines()[0]
        print("[-] Connecting installdir to PyKern instance [Accessing file (3/3)]")
        f.close()
    except Exception as e:
        print(f"{bold}{red}[ERROR]{normal}{reset} Holy shit! Configuration file does not exist.")
        input("osdir will be set to pykern")
        osdir = "pykern"
    print(f"{green}[x]{reset} Connected to:  " + osdir + ".")
    print(f"{blue}[-]{reset} Loading user")
    input(f"{green}Press ENTER to proceed{reset}")
    try:
        print("[-] Loading current user [Accessing file (1/3)]")
        uf = open(osdir + "/user/.curuser", "r")
        print("[-] Loading current user [Accessing file (2/3)]")
        username = uf.readline().lstrip().rstrip()
        print("[-] Loading current user [Accessing file (3/3)]")
        uf.close()
    except:
        print(f"{bold}{red}[ERROR]{normal}{reset} dawg how did you manage to remove user/.curuser?")
        username = input("Imma need u to be honest... what is that username of yours? ")
        print("[-] Writing current user [Accessing file (1/3)]")
        usrfile = open("pykern/user/.curuser", "w")
        print("[-] Writing current user [Accessing file (2/3)]")
        usrfile.write(username)
        print("[-] Writing current user [Accessing file (3/3)]")
        usrfile.close()
    input(f"{Fore.LIGHTBLUE_EX}The system will now access the Package Directory (pykern/user/{username}/pkg). This is your chance to fix things, then press {bold}ENTER{normal}{reset}")
    print(f"{blue}[-]{reset} Loading the packages")
    pkgdir = osdir + "/user/" + username + "/pkg"
    try:
        for path in os.listdir(pkgdir):
            if os.path.isfile(os.path.join(pkgdir, path)):
                print(f"{cyan}[-]{reset} - Loaded " + bold + path.replace(".py", "") + normal)
                packagecount += 1
    except Exception as e:
        crit_error(e)
    print("Press ENTER to proceed. Almost there.")
    danswer = input("Do you want to clear the screen? [Y/n] ")
    if danswer.lower().startswith("n"):
        pass
    else:
        cls()
    pykern()
# Great idea to split the interaction
if args == "debug":
    debugboot()
else:
    boot()