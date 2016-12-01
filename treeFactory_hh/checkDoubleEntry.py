import ROOT

file = ROOT.TFile("MIS_RUNII_firstRound_skim_llbb/condor/output/MuonEG_Run2015D-16Dec2015-v1_2016-03-03_v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3_histos.root")
tree = file.Get("t")
dict = {}
for entry in tree :
    if str(entry.event_run) in dict.keys():
        if entry.event_number in dict[str(entry.event_run)]:
            print "BADDD"
        dict[str(entry.event_run)].append(entry.event_number)
    else:
        dict[str(entry.event_run)] = [entry.event_number]
