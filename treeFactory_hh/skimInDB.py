import os, sys, argparse, subprocess
import ROOT

#from generateTrees import cut
#usage :python HHAnalysis/skimInDB.py rootFileDir(relativePath) [SkimDescription]

# Add default ingrid storm package
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/storm-0.20-py2.7-linux-x86_64.egg')
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-linux-x86_64.egg')

CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']
sys.path.append(os.path.join(CMSSW_BASE,'bin', SCRAM_ARCH))

from SAMADhi import Sample, DbStore, File
dbstore = DbStore()
#import add_sample

parser = argparse.ArgumentParser(description='Facility to add skimmed production to the DB.')
parser.add_argument('-d', '--directory', dest='directory', help='Name of the directory where are rootFile to be added to the db.')
parser.add_argument('-s', '--suffix', dest='suffix', default = '_skimmed', help='Suffix to append to the Sample name in the DB.')
args = parser.parse_args()

def get_sample(name):
    resultset = dbstore.find(Sample, Sample.name == name)
    return resultset.one()

code_version = unicode("HHTools_MIS_RUN_II_" + subprocess.check_output(["git", "rev-parse", "HEAD"]).replace("\n",""))

currentDir = os.getcwd()+"/"
fileList = [file for file in os.listdir(args.directory) if "histos_" in file]
samplesDict = {}
for file in fileList:
    sampleName = file.split("_histos_")[0]
    if not sampleName in samplesDict.keys():
        samplesDict[sampleName] = []
    samplesDict[sampleName].append(os.path.join(currentDir, args.directory, file))

for sampleName in samplesDict.keys():
    father_db_sample = get_sample(unicode(sampleName)) # Construct the new sample from his father
    nevents = 0
    db_fileList = []
    for fileName in samplesDict[sampleName] :
        print fileName
        rootFile = ROOT.TFile(fileName)
        rootTree = rootFile.Get("t")
        temp_nevent = rootTree.GetEntries()
        nevents += temp_nevent
        db_fileList.append(File(unicode(fileName), u"", 0, u"{}", temp_nevent))
    db_sample = Sample(unicode(sampleName + args.suffix), unicode(os.path.join(currentDir, args.directory)), u'SKIM', nevents)
    for db_file in db_fileList :
        db_sample.files.add(db_file)
    db_sample.source_sample_id = father_db_sample.sample_id
    db_sample.nevents = nevents
    db_sample.code_version = code_version
    # Get what was defined for father sample and does not have to change
    db_sample.nevents_processed = father_db_sample.nevents
    db_sample.normalization = father_db_sample.normalization
    db_sample.event_weight_sum = father_db_sample.event_weight_sum
    db_sample.extras_event_weight_sum = father_db_sample.extras_event_weight_sum
    db_sample.luminosity = father_db_sample.luminosity
    db_sample.processed_lumi = father_db_sample.processed_lumi
    db_sample.user_comment = father_db_sample.user_comment 
    db_sample.source_dataset_id = father_db_sample.source_dataset_id
    #dbstore.add(db_sample)
    print "Will add the following sample to the database :"
    #print db_sample
    print "\n"
#dbstore.commit()


