#!/usr/bin/python3

import os
import sys
import getopt
import urllib.request
from github import Github

system = ''
tag = ''
outputdir = ''
winplatform = ''
repository = ''


def do_bsdiff(url, newfile):
    # gets filename from url
    idx = asset.browser_download_url.rfind('/')
    oldfile = outputdir + asset.browser_download_url[idx:end]

    urllib.request.urlretrieve(asset.browser_download_url, oldfile)
    update = "update-" + newfile
    downgrade = "downgrade-" + newfile

    os.system("bsdiff " + oldfile + " " + newfile + " " + update)
    os.system("bsdiff " + newfile + " " + oldfile + " " + downgrade)

    os.remove(oldfile)
    pass


try:
    opts, args = getopt.getopt(sys.argv[1:], "s:t:o:r:", [
                               "system=", "tag=", "outputdir=", "repository="])
except getopt.GetoptError:
    print("launcherBindiffs.py -s <system> -t <tag> -o <outputdir> -r <repository>")
    sys.exit(2)

for opt, arg in opts:
    print(opt, " - ", arg)
    if opt in ("-s", "--system"):
        system = arg
    elif opt in ("-t", "--tag"):
        tag = arg
    elif opt in ("-o", "--outputdir"):
        outputdir = arg
    elif opt in ("-r", "--repository"):
        repository = arg

print("Getting latest release")
g = Github()
repo = g.get_repo(repository)
assets = repo.get_latest_release().get_assets()

linuxnewfile = os.environ[OUTPUTDIR] + "/" + \
    os.environ[PACKAGING_INSTALLER_NAME] + "-" + tag + "-x86_64.AppImage"
macoscompatnewfile = os.environ[OUTPUTDIR] + "/" + \
    os.environ[PACKAGING_INSTALLER_NAME] + "-" + tag + "-compat.dmg"
macosnewfile = os.environ[OUTPUTDIR] + "/" + \
    os.environ[PACKAGING_INSTALLER_NAME] + "-" + tag + ".dmg"
winx64newfile = os.environ[OUTPUTDIR] + "/" + \
    os.environ[PACKAGING_INSTALLER_NAME] + \
    "-" + tag + "-" + "x64-winportable.zip"
winx86newfile = os.environ[OUTPUTDIR] + "/" + \
    os.environ[PACKAGING_INSTALLER_NAME] + \
    "-" + tag + "-" + "x86-winportable.zip"

for asset in assets:
    if "update" in asset.browser_download_url or "downgrade" in asset.browser_download_url:
        continue

    if system == "linux":
        if "AppImage" in asset.browser_download_url and os.path.isfile(linuxnewfile):
            do_bsdiff(asset.browser_download_url, linuxnewfile)
    elif system == "macos":
        if "compat" in asset.browser_download_url and os.path.isfile(macoscompatnewfile):
            do_bsdiff(asset.browser_download_url, macoscompatnewfile)
        elif "compat" not in asset.browser_download_url and "dmg" in asset.browser_download_url and os.path.isfile(macosnewfile):
            do_bsdiff(asset.browser_download_url, macosnewfile)
    else:
        if "x64-winportable" in asset.browser_download_url and os.path.isfile(winx64newfile):
            do_bsdiff(asset.browser_download_url, winx64newfile)
        if "x86-winportable" in asset.browser_download_url and os.path.isfile(winx86newfile):
            do_bsdiff(asset.browser_download_url, winx86newfile)
