#!/usr/bin/python3

import os, subprocess
import urllib.request
from bs4 import BeautifulSoup
from IPython import embed

arch_to_gnome = {
  "gconf": "GConf",
  "gdk-pixbuf2": "gdk-pixbuf",
  "glib2": "glib",
  "gphoto2": "gphoto",
  "gtk3": "gtk",
  "gtkhtml4": "gtkhtml",
  "gtkmm3": "gtkmm",
  "gtksourceview3" : "gtksourceview",
  "pygtksourceview2" : "pygtksourceview",
  "vte3": "vte",
  "totem-plparser": "totem-pl-parser",
  "networkmanager" : "NetworkManager"
}

pkgname_to_arch = {
  "pygobject": "python-gobject",
  "pyatspi" : "python-atspi"
}

GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'


def annotate(current, upstream):
    if current < upstream:
        return RED + current + END
    elif current == upstream:
        return GREEN + current + END
    return current

def get_local_version(package):
    pkgbuild = open(package + "/PKGBUILD").readlines()
    
    for line in pkgbuild:
        if "pkgver=" in line:
            return line.strip().replace("pkgver=", "")
    

def get_largest_major_version(url):
    version = ""

    try:
        f = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return "N/A"

    html = f.read()
    soup = BeautifulSoup(html)
    links = soup.findAll("a")
    
    for link in links:
        link_url = link.attrs["href"].replace("/", "")
        if link_url[0].isdigit():
            version = link_url
            
    return version

def get_largest_minor_version(url, package):
    version = ""

    try:
        f = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return "N/A"

    html = f.read()
    soup = BeautifulSoup(html)
    links = soup.findAll("a")
    
    for link in links:
        link_url = link.attrs["href"].replace("/", "")
        if package in link_url:
            version = link_url.split("-")[-1].replace(".tar.xz", "").replace(".tar.gz", "").replace(".tar.bz2", "").replace(".sha256sum", "")
            
    return version

def get_upstream_version(package):

    package = package.strip()

    if package in arch_to_gnome:
        package = arch_to_gnome[package]

    url = "http://ftp.gnome.org/pub/GNOME/sources/" + package
    major_version = get_largest_major_version(url)
    
    if major_version == "N/A":
        return "N/A"

    url += "/" + major_version + "/?C=M;O=A"
    minor_version = get_largest_minor_version(url, package)
    return minor_version

def get_pacman_version(package):

    package = package.strip()

    if package in pkgname_to_arch:
        package = pkgname_to_arch[package]

    command = ['pacman', '-Si', package]
    
    out = get_bash_out(command).decode()
    
    if not out:
        return "N/A"
    
    for line in out.split("\n"):
        if "Version" in line:
            return line.split(":")[-1].strip().split("-")[0]
    

def get_bash_out(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out

def find_longest(packages):
    longest = 0
    for package in packages:
        if len(package) > longest:
            longest = len(package)
    return longest
    
def fill(string, spaces):
    for i in range(0, spaces - len(string)):
        string += " "
    return string

def fill_color(original, string, spaces):
    for i in range(0, spaces - len(original)):
        string += " "
    return string

def print_package(package, longest):
        local = get_local_version(package)
        arch = get_pacman_version(package)
        upstream = get_upstream_version(package)
        
        local_color = annotate(local, upstream)
        arch_color = annotate(arch, upstream)
        
        if upstream == "N/A":
            upstream_color = RED + "N/A" + END
        else:
            upstream_color = upstream
        
        print(
          fill(package, longest),
          fill_color(local, local_color, 10),
          fill_color(arch, arch_color, 10),
          upstream_color)

def list_packages():
    packages = os.listdir(os.getcwd())
    packages.sort()

    longest = find_longest(packages)

    print(
          fill("", longest),
          fill("Local", 10),
          fill("Arch", 10),
          "GNOME")

    for package in packages:
      if os.path.isdir(package) and package != ".git":
          print_package(package, longest)

    

list_packages()
#print(get_pacman_version("gtk-xfce-engine"))
#print(get_upstream_version("gdk-p"))
#print_package("gdk-pixbuf2", 30)
#embed()
