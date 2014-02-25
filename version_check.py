#!/usr/bin/python3

import os, subprocess
import urllib.request
from bs4 import BeautifulSoup
from IPython import embed

arch_to_gnome = {
  "gconf": "GConf"
}

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
            version = link_url.split("-")[-1].replace(".tar.xz", "").replace(".tar.gz", "")
            
    return version

def get_upstream_version(package):

    if package in arch_to_gnome:
        package = arch_to_gnome[package]

    url = "http://ftp.gnome.org/pub/GNOME/sources/" + package
    major_version = get_largest_major_version(url)
    
    if major_version == "N/A":
        return "N/A"

    url += "/" + major_version
    minor_version = get_largest_minor_version(url, package)
    return minor_version

def get_pacman_version(package):
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
        print(
          fill(package, longest),
          fill(get_local_version(package), 10),
          fill(get_pacman_version(package), 10),
          get_upstream_version(package))
    

list_packages()
#print(get_pacman_version("gtk-xfce-engine"))
#print(get_upstream_version("nautilus"))
#embed()
