#!/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/bin/python

# usage dans histfactory_hh : python launchHistFactory.py outputName [submit]

import sys, os, json
sys.path.append("../../CommonTools/Factories/")
import copy
import datetime

import argparse

from cp3_llbb.CommonTools.condorTools import condorSubmitter

# Add default ingrid storm package
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/storm-0.20-py2.7-linux-x86_64.egg')
sys.path.append('/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/lib/python2.7/site-packages/MySQL_python-1.2.3-py2.7-linux-x86_64.egg')

CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']
sys.path.append(os.path.join(CMSSW_BASE, 'bin', SCRAM_ARCH))
from SAMADhi import Dataset, Sample, DbStore

def build_sample_name(name, tag):
    return "{}*{}".format(name, tag)

# Connect to the database
dbstore = DbStore()

def get_sample_id_from_name(name):
    results = dbstore.find(Sample, Sample.name.like(unicode(name.replace('*', '%'))))

    if results.count() == 0:
        return None

    if results.count() > 1:
        raise Exception("More than one sample found in the database matching %r. This is not supported." % name)

    sample = results.one()
    return sample.sample_id

def get_sample(iSample):
    resultset = dbstore.find(Sample, Sample.sample_id == iSample)
    return resultset.one()

import samplesToRunOn
analysis_tags = samplesToRunOn.analysis_tags
analysis_tags_for_evt_perJob = samplesToRunOn.analysis_tags_for_evt_perJob
Samples = samplesToRunOn.Samples
SamplesToSplitMore = samplesToRunOn.SamplesToSplitMore
SamplesToSplitAbitMore = samplesToRunOn.SamplesToSplitAbitMore

json_evt_per_job = open("/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/HHTools/histFactory_hh/event_per_job.json")
evt_per_job = json.load(json_evt_per_job)


parser = argparse.ArgumentParser(description='Facility to submit histFactory jobs on condor.')
parser.add_argument('-o', '--output', dest='output', default=str(datetime.date.today()), help='Name of the output directory.')
parser.add_argument('-s', '--submit', help='Choice to actually submit the jobs or not.', action="store_true")
parser.add_argument('-f', '--filter', dest='filter', default=True, help='Apply filter on DY ht.')
parser.add_argument('-t', '--test', help='Run on the output of HHAnalyzer not yet in the DB.', action="store_true")
parser.add_argument('-p', '--plotter', dest='plotter', default="generatePlots.py", help='Code generating the plots.')
parser.add_argument('-r', '--remove', help='Overwrite output directory if it already exists.', action="store_true")
parser.add_argument('--skip', help='Skip the building part.', action="store_true")
parser.add_argument('--tree', dest='treeFactory', action='store_true', default=False, help='Use treeFactory instead of histFactory')
parser.add_argument('--reweight', dest='reweight', default=True, help='Applying reweighting to the DY and TT TH1s')

args = parser.parse_args()

# Convert samples into ids
def convert_to_ids(samples):
    ids = []
    for sample in samples:
        found = False
        for tag in analysis_tags:
            id = get_sample_id_from_name(build_sample_name(sample, tag))
            if id:
                found = True
                ids.append(id)
                break

        if not found:
            raise Exception("No sample found in the database for %r" % sample)

    return ids

IDs = convert_to_ids(Samples)
IDsToSplitMore = convert_to_ids(SamplesToSplitMore)
IDsToSplitAbitMore = convert_to_ids(SamplesToSplitAbitMore)

weightFromFile = True

# Find first MC sample and use one file as skeleton
for id in IDs:
    sample = get_sample(id)
    if sample.source_dataset.datatype != "mc":
        continue
    if sample.sampletype == u'SKIM':
        skeleton_file = sample.files.any().lfn
        weightFromFile = False
    else :
        skeleton_file = "/storage/data/cms/" + sample.files.any().lfn
    break

if args.test: 
    jsonName = "jsonTest.json"
    jsonFile = open(jsonName)
    datasetDict = json.load(jsonFile)
    for datasetName in datasetDict.keys():
        rootFileName = datasetDict[datasetName]["files"][0]
        break

samples = []
for ID in IDs :
    #eventsPerJob = evt_per_job[str(ID)]
    eventsPerJob = 10000
    samples.append(
        {
            "ID": ID,
            "events_per_job": eventsPerJob,
            #"sample_fraction": sample_fraction,
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

toolDir = "Factories"
toolScript = "createPlotter.sh"
executable = "plotter.exe"

if args.treeFactory: 
    executable = "skimmer.exe"
    toolScript = "createSkimmer.sh"

if not args.skip :
    if args.test : 
        os.system(os.path.join("../../", "CommonTools", toolDir, "build", toolScript) + " %s %s %s"%(rootFileName, args.plotter, args.output))
    else : 
        os.system(os.path.join("../../", "CommonTools", toolDir, "build", toolScript) + " %s %s %s"%(skeleton_file, args.plotter, args.output))


## Create Condor submitter to handle job creating
mySub = condorSubmitter(samples, "%s/build/" % args.output + executable, "DUMMY", args.output+"/", rescale = True, weightFromFile = weightFromFile)
#mySub = condorSubmitter(samples, "%s/build/" % args.output + executable, "DUMMY", args.output+"/", rescale = True)

## Create test_condor directory and subdirs
mySub.setupCondorDirs()


splitTT = False
splitDY = True
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

        if splitDY and 'DYJetsToLL_' in sample["db_name"]:
            print "Splitting DY flavour content."
            print '\033[93m'+"Careful!!!! We use hh_llmetjj_HWWleptons_btagM_csv[0].gen_**"+'\033[0m'
            # DY bb
            dy_bb_sample = copy.deepcopy(sample)
            dy_bb_sample["db_name"] = dy_bb_sample["db_name"].replace("DYJets", "DYbb")
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            newJson["sample_cut"] = "(hh_llmetjj_HWWleptons_btagM_csv[0].gen_bb)"
            dy_bb_sample["json_skeleton"][dy_bb_sample["db_name"]] = newJson
            dy_bb_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(dy_bb_sample)

            # DY bx
            dy_bx_sample = copy.deepcopy(sample)
            dy_bx_sample["db_name"] = dy_bx_sample["db_name"].replace("DYJets", "DYbx")
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            newJson["sample_cut"] = "(hh_llmetjj_HWWleptons_btagM_csv[0].gen_bl || hh_llmetjj_HWWleptons_btagM_csv[0].gen_bc)"
            dy_bx_sample["json_skeleton"][dy_bx_sample["db_name"]] = newJson
            dy_bx_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(dy_bx_sample)

            # DY xx
            dy_xx_sample = copy.deepcopy(sample)
            dy_xx_sample["db_name"] = dy_xx_sample["db_name"].replace("DYJets", "DYxx")
            newJson = copy.deepcopy(sample["json_skeleton"][sample["db_name"]])
            newJson["sample_cut"] = "(hh_llmetjj_HWWleptons_btagM_csv[0].gen_cc || hh_llmetjj_HWWleptons_btagM_csv[0].gen_cl || hh_llmetjj_HWWleptons_btagM_csv[0].gen_ll)"
            dy_xx_sample["json_skeleton"][dy_xx_sample["db_name"]] = newJson
            dy_xx_sample["json_skeleton"].pop(sample["db_name"])
            mySub.sampleCfg.append(dy_xx_sample)

            # IF you do not want to run on the nominal sample:
            #mySub.sampleCfg.remove(sample)


        # Merging with HT binned sample: add cut on inclusive one
        if 'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' in sample["db_name"] or 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' in sample["db_name"]: 
            sample["json_skeleton"][sample["db_name"]]["sample_cut"] = "event_ht < 100"


        #if 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' in sample["db_name"]:
        #    sample["json_skeleton"][sample["db_name"]]["sample_cut"] = "event_ht < 100"

if args.reweight :
    for sample in mySub.sampleCfg[:]:
        if 'TTTo2L2Nu_13TeV-powheg_Fall15MiniAODv2' in sample["db_name"]:
            sample["json_skeleton"][sample["db_name"]]["sample-weight"] = "tt"
            #sample["json_skeleton"][sample["db_name"]]["cross-section"] = sample["json_skeleton"][sample["db_name"]]["cross-section"]*0.9543
        if 'ToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext4' in sample["db_name"]:
            sample["json_skeleton"][sample["db_name"]]["sample-weight"] = "dy"
            #sample["json_skeleton"][sample["db_name"]]["cross-section"] = sample["json_skeleton"][sample["db_name"]]["cross-section"]*0.78114

## Write command and data files in the condor directory
mySub.createCondorFiles()

# Actually submit the jobs
# It is recommended to do a dry-run first without submitting to condor
if args.submit: 
   mySub.submitOnCondor()

