#!/nfs/soft/python/python-2.7.5-sl6_amd64_gcc44/bin/python

# usage python selection_efficiency.py -d ../treeFactory_hh/MIS_RUNII_firstRound_skim_llbb/condor/output/ --tree

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

import ROOT

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
def get_dataset(iDataset):
    resultset = dbstore.find(Dataset, Dataset.dataset_id == iDataset)
    return resultset.one()

import samplesToRunOn
analysis_tags = samplesToRunOn.analysis_tags
analysis_tags_for_evt_perJob = samplesToRunOn.analysis_tags_for_evt_perJob
Samples = samplesToRunOn.Samples
SamplesToSplitMore = samplesToRunOn.SamplesToSplitMore
SamplesToSplitAbitMore = samplesToRunOn.SamplesToSplitAbitMore

parser = argparse.ArgumentParser(description='Facility to submit histFactory jobs on condor.')
parser.add_argument('-d', '--directory', dest='directory', default = 'MIS_RUNII_firstRound/condor/output/', help='Directory of the rootFile with selection applied are.')
parser.add_argument('-v', '--variable', dest='variable', default = 'isElEl_All_hh_llmetjj_HWWleptons_btagM_csv_no_cut', help='Name of the variable to use for the integral.')
parser.add_argument('-t', '--tree', help='Set to true if you use tree instead of TH1.', action="store_true")

args = parser.parse_args()

# Convert samples into ids
def convert_to_ids(samples, analysis_tags):
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

IDs = convert_to_ids(Samples, analysis_tags)
IDsToSplitMore = convert_to_ids(SamplesToSplitMore, analysis_tags)
IDsToSplitAbitMore = convert_to_ids(SamplesToSplitAbitMore, analysis_tags)

IDs_for_evt_per_job = convert_to_ids(Samples, analysis_tags_for_evt_perJob)
print IDs_for_evt_per_job

efficiencies = {}
#target_n_evt_to_compute_weight = 1000 # ~30 hour of running time with weight computation
target_n_evt_to_compute_weight = 1000
n_evt_per_job = {}

i = 0
samples = []
for ID in IDs :
    db_sample = get_sample(ID)
    db_dataset = get_dataset(db_sample.source_dataset_id)
    db_name = db_sample.name

    n_entries_after_framework = float(db_sample.nevents)
    cross_section = db_dataset.xsection

    rootFileName = args.directory + db_name + "_histos.root"
    fileExists = os.path.isfile(rootFileName)
    if fileExists :
        rootFile = ROOT.TFile(rootFileName)
        if args.tree :
            tree = rootFile.Get("t")
            n_event_after_selection = tree.GetEntries()
            n_entries_after_selection = tree.GetEntries()
        else :
            th1 = rootFile.Get(args.variable)
            n_event_after_selection = th1.Integral(0, th1.GetNbinsX()+1)
            n_entries_after_selection = th1.GetEntries()

        efficiency_ntuple_to_sel = n_entries_after_selection/n_entries_after_framework
        real_efficiency = n_event_after_selection/cross_section
        #efficiencies[db_name] = efficiency_ntuple_to_sel
        if efficiency_ntuple_to_sel == 0:
            efficiency_ntuple_to_sel = 0.001
        n_evt_per_job[IDs_for_evt_per_job[i]] = int(target_n_evt_to_compute_weight/efficiency_ntuple_to_sel)
        print db_name, " ", n_evt_per_job[IDs_for_evt_per_job[i]], " event per job"
        #print db_name
        #print "     Efficiency ntuple to selection : %0.2f "%(bare_efficiency*100)
        #print "     Real efficiency : %0.2f "%(real_efficiency*100)
    else :
        if ID in IDsToSplitAbitMore :
            n_evt_per_job[IDs_for_evt_per_job[i]] = 8000 
        else :
            n_evt_per_job[IDs_for_evt_per_job[i]] = 4000
        print db_name, " ", n_evt_per_job[IDs_for_evt_per_job[i]], " event per job (file not found)"
    i += 1

with open("event_per_job.json", "w") as outJson:
    json.dump(n_evt_per_job, outJson)

