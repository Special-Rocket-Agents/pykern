import os
from os.path import exists
import time
from colorama import init
from colorama import Fore, Back, Style
import importlib.util
from pathlib import Path
import re
init()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

osdir = ""
username = ""
packagecount = 0

curdir = ""

booten = False

su = False

datafolder = Path.cwd()


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
                print(error)
        except Exception as error:
            if cmd == "":
                pass
                continue
            else:
                print(Fore.LIGHTRED_EX + "Failed to find command \"" + cmd + "\"" + Style.RESET_ALL + ":")
                print(error)

def boot():
    global osdir
    global username
    global packagecount
    from setup import setupInit
    cls()
    if not exists("config.pykern"):
        setupInit()
    print("[-] Connecting installdir to PyKern instance")
    f = open("config.pykern", "r")
    osdir = f.readlines()[0]
    f.close()
    print("[x] Connected to:  " + osdir + ".")
    print("[-] Loading user")
    uf = open(osdir + "/user/.curuser", "r")
    username = uf.readline().lstrip().rstrip()
    uf.close()
    print("[x] Connected to the user: " + username)
    print("[-] Loading the packages")
    pkgdir = osdir + "/user/" + username + "/pkg"
    for path in os.listdir(pkgdir):
        if os.path.isfile(os.path.join(pkgdir, path)):
            print("[-] - Loaded " + path.replace(".py", ""))
            packagecount += 1
    print("[x] Done, loaded: " + str(packagecount) + " package(s).")
    time.sleep(2)
    cls()
    pykern()
boot()
