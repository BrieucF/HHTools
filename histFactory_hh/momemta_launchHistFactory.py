#!/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/bin/python

# usage dans histfactory_hh : python launchHistFactory.py outputName [submit]

import sys, os, json
sys.path.append("../../CommonTools/histFactory/")
import copy
import datetime

import argparse

from condorTools import condorSubmitter

# Add default ingrid storm package
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/storm-0.20-py2.7-linux-x86_64.egg')
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-linux-x86_64.egg')

CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']
sys.path.append(os.path.join(CMSSW_BASE, 'bin', SCRAM_ARCH))
from SAMADhi import Dataset, Sample, DbStore

def get_sample(iSample):
    dbstore = DbStore()
    resultset = dbstore.find(Sample, Sample.sample_id == iSample)
    return resultset.one()

IDs = [2152]# 2133, 2040] # DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext4,DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext4_Fall15MiniAODv2_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3 ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_Fall15MiniAODv2_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3 
IDsToSplitMore = [2032, 2050, 2068] ## TTFL, singletop
IDfullStat = [2050, 2068]

#IDsToSplitMore.append(2152) ## DY

# Data
#IDs.extend([
#    2008, # DoubleEG
#    2009, # MuonEG
#    2010, # DoubleMuon
#    ])
#
#IDs.extend(range(2011, 2068+1))
#IDs.extend([2072]) #WZTo2L2Q
#IDs.extend(range(2134, 2151+1)) # DYJetsToLL_M-50_HT-400to600, VBFHToWWTo2L2Nu,  etc
##Merged samples
#IDs.extend([2133]) #DY_10_50 merged
#IDs.remove(2059) # DY_10_50 not merged
#IDs.remove(2030) # DY_10_50 not merged
#IDs.remove(2017) # DY_10_50 not merged
#
## DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3
#IDs.extend([2155])
#IDs.remove(2138)
#IDs.remove(2151)
#
## DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3
#IDs.extend([2154])
#IDs.remove(2134)
#IDs.remove(2147)
#
## DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3
#IDs.extend([2153])
#IDs.remove(2137)
#IDs.remove(2145)

# DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext4_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3
#IDs.extend([2152])
#IDs.remove(2037)
#IDs.remove(2142)
#IDs.remove(2150)

# Stop 
#IDs.extend([2286, 2288]) # crab_SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2.py &&  crab_SMS-T2tt_mStop-850_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2.py

parser = argparse.ArgumentParser(description='Facility to submit histFactory jobs on condor.')
parser.add_argument('-o', '--output', dest='output', default=str(datetime.date.today()), help='Name of the output directory.')
parser.add_argument('-s', '--submit', help='Choice to actually submit the jobs or not.', action="store_true")
parser.add_argument('-f', '--filter', dest='filter', default=True, help='Apply filter on DY ht.')
parser.add_argument('-t', '--test', help='Run on the output of HHAnalyzer not yet in the DB.', action="store_true")
parser.add_argument('-p', '--plotter', dest='plotter', default="momemta_generatePlots.py", help='Code generating the plots.')
parser.add_argument('-r', '--remove', help='Overwrite output directory if it already exists.', action="store_true")
parser.add_argument('--skip', help='Skip the building part.', action="store_true")
parser.add_argument('--tree', dest='treeFactory', action='store_true', default=False, help='Use treeFactory instead of histFactory')

args = parser.parse_args()

# get one of the new samples with gen info to read Tree structure
sample = get_sample(IDs[-1])
files = ["/storage/data/cms/" + x.lfn for x  in sample.files]


if args.test: 
    jsonName = "jsonTest.json"
    jsonFile = open(jsonName)
    datasetDict = json.load(jsonFile)
    for datasetName in datasetDict.keys():
        rootFileName = datasetDict[datasetName]["files"][0]
        break
    print "Will build things based on %s"%rootFileName

samples = []
for ID in IDs + IDsToSplitMore:
    filesperJob = 4
    eventsPerJob = 5000
    sample_fraction = 0.2
    if ID in IDsToSplitMore:
        filesperJob = 1
        eventsPerJob = 500
        sample_fraction = 0.07
    if ID in IDfullStat :
        sample_fraction = 1.
    samples.append(
        {
            "ID": ID,
            "events_per_job": eventsPerJob,
            "sample_fraction": sample_fraction,
            #"files_per_job": filesperJob,
        }
    )

if args.remove :
    if os.path.isdir(args.output):
        print "Are you sure you want to execute the following command ?"
        print "rm -r " + args.output
        print "Type enter if yes, ctrl-c if not."
        raw_input()
        os.system("rm -r " + args.output)
        print "Deleted ", args.output, " folder."

## Use treeFactory or histFactory

toolDir = "histFactory"
toolScript = "createPlotter.sh"
executable = "plotter.exe"

if args.treeFactory: 
    toolDir = "treeFactory"
    executable = "skimmer.exe"
    toolScript = "createSkimmer.sh"

if not args.skip :
    if args.test : 
        os.system(os.path.join("../../", "CommonTools", toolDir, "build", toolScript) + " %s %s %s"%(rootFileName, args.plotter, args.output))
    else : 
        print "Will build things based on %s"%files[0]
        os.system(os.path.join("../../", "CommonTools", toolDir, "build", toolScript) + " %s %s %s"%(files[0], args.plotter, args.output))


## Create Condor submitter to handle job creating
mySub = condorSubmitter(samples, "%s/build/" % args.output + executable, "DUMMY", args.output+"/", rescale = True)

## Create test_condor directory and subdirs
mySub.setupCondorDirs()

splitTT = False

## Modify the input samples to add sample cuts and stuff
if args.filter: 
    for sample in mySub.sampleCfg[:]:
        # TTbar final state splitting
        if splitTT and 'TT_TuneCUETP8M1_13TeV-powheg-pythia8_Fall15MiniAODv2' in sample["db_name"]:

            # Fully leptonic
            tt_fl_sample = copy.deepcopy(sample)
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            
            tt_fl_sample["db_name"] = sample["db_name"].replace("TT_Tune", "TT_FL_Tune")
            newJson["sample_cut"] = "(hh_gen_ttbar_decay_type >= 4 && hh_gen_ttbar_decay_type <= 10 && hh_gen_ttbar_decay_type != 7)"
            
            tt_fl_sample["json_skeleton"][tt_fl_sample["db_name"]] = newJson
            tt_fl_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(tt_fl_sample)

            # Semi leptonic
            tt_sl_sample = copy.deepcopy(sample)
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            
            tt_sl_sample["db_name"] = sample["db_name"].replace("TT_Tune", "TT_SL_Tune")
            newJson["sample_cut"] = "(hh_gen_ttbar_decay_type == 2 || hh_gen_ttbar_decay_type == 3 || hh_gen_ttbar_decay_type == 7)"
            
            tt_sl_sample["json_skeleton"][tt_sl_sample["db_name"]] = newJson
            tt_sl_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(tt_sl_sample)

            # Fully hadronic
            tt_fh_sample = copy.deepcopy(sample)
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            
            tt_fh_sample["db_name"] = sample["db_name"].replace("TT_Tune", "TT_FH_Tune")
            newJson["sample_cut"] = "(hh_gen_ttbar_decay_type == 1)"
            
            tt_fh_sample["json_skeleton"][tt_fh_sample["db_name"]] = newJson
            tt_fh_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(tt_fh_sample)

            mySub.sampleCfg.remove(sample)

        # Merging with HT binned sample: add cut on inclusive one
        if 'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' in sample["db_name"] or 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' in sample["db_name"]: 
            sample["json_skeleton"][sample["db_name"]]["sample_cut"] = "event_ht < 100"

        if 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' in sample["db_name"]:
            sample["json_skeleton"][sample["db_name"]]["sample_cut"] = "event_ht < 100"

        # Handle the cluster v1tov3 reweighting
        if "all_nodes" in sample["db_name"]:
            ## For v1->v1 reweighting check:
            #for node in range(2, 14):
            #    node_str = "node_rwgt_" + str(node)
            for node in range(1, 13):

                newSample = copy.deepcopy(sample)
                newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
                
                node_str = "node_" + str(node)
                newSample["db_name"] = sample["db_name"].replace("all_nodes", node_str)
                newJson["sample-weight"] = "cluster_" + node_str
                
                newSample["json_skeleton"][newSample["db_name"]] = newJson
                newSample["json_skeleton"].pop(sample["db_name"])
                mySub.sampleCfg.append(newSample)

            mySub.sampleCfg.remove(sample)

## Write command and data files in the condor directory
mySub.createCondorFiles()

# Actually submit the jobs
# It is recommended to do a dry-run first without submitting to condor
if args.submit: 
   mySub.submitOnCondor()
