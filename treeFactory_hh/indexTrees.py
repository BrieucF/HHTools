import ROOT
import os, argparse

parser = argparse.ArgumentParser(description='Facility to index ttrees with event numbers.')
parser.add_argument('-d', '--directory', dest='directory', help='Name of the directory where are rootFile to be indexed.')
args = parser.parse_args()

rootFileDirectory = args.directory
fileToIndex = [file for file in os.listdir(rootFileDirectory) if "histos_" in file]
for file in fileToIndex :
    print "Start indexing %s"%file
    rootFile = ROOT.TFile(rootFileDirectory + file, "update")
    ttree = rootFile.Get("t")
    ttree.BuildIndex("event_run", "event_event")
    ttree.Write()
    rootFile.Close()
    print "Done."
