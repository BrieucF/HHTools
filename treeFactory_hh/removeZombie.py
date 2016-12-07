import ROOT
import os, argparse

parser = argparse.ArgumentParser(description='Facility to index ttrees with event numbers.')
parser.add_argument('-d', '--directory', dest='directory', help='Name of the directory where are rootFile to be indexed.')
args = parser.parse_args()

rootFileDirectory = args.directory
#fileToIndex = [file for file in os.listdir(rootFileDirectory) if "histos_" in file]
fileToIndex = [file for file in os.listdir(rootFileDirectory) if "_histos_" in file]
for file in fileToIndex :
    rootFile = ROOT.TFile(rootFileDirectory + file, "read")
    if rootFile.IsZombie():
        print rootFileDirectory + file, " is zombie."
        os.remove(rootFileDirectory + file)
    print file
    t = rootFile.Get("t")
    if t == None :
        os.remove(rootFileDirectory + file)
        print rootFileDirectory + file, " had not tree, deleting it."
    rootFile.Close()
