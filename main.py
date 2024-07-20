import os
from os.path import exists
import random
import time
from colorama import init
from colorama import Fore, Back, Style
import importlib.util
from pathlib import Path
import re

import colorama

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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
    ## MOTD ###
    if not exists("shutmotd"):
        motd = [
            "SIP is the package manager, type 'sip help' for more info",
            f"If you don't want this Message Of The Day to appear, create a file name {Fore.GREEN}shutmotd{Fore.RESET} in the root.",
            "The repository's wiki has some great info, check it out later.",
            "MOTDs will be added from time to time without notice, check back later."
        ]
        print(Style.BRIGHT + "Welcome to PyKern" + Style.RESET_ALL)
        print(motd[random.randint(0, 3)])
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
    time.sleep(1.2)
    cls()
    pykern()
boot()