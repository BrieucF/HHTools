import ROOT as R
import copy, sys, os, inspect 

# Usage from histFactory/plots/HHAnalysis/ : ./../../build/createHistoWithMultiDraw.exe -d ../../samples.json generatePlots.py 
scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
from basePlotter import *
from HHAnalysis import HH


def getBinningStrWithMax(nBins, start, end, max):
    """Return string defining a binning in histFactory, with 'nBins' bins between
    'start' and 'end', but with the upper edge replaced by 'max'."""
    
    bins = [start]
    pos = start
    for i in range(nBins):
        pos += (end-start)/nBins
        bins.append(pos)
    if bins[-1] < max:
        bins[-1] = max

    m_string = str(len(bins)-1) + ", { "
    for b in bins[0:len(bins)-1]:
        m_string += str(b) + ", "
    m_string += str(bins[-1]) + "}"

    return m_string


includes = []
plots = []

# Needed to evaluate MVA outputs
#includes.append( os.path.join(scriptDir, "..", "common", "readMVA.h") )

# Plot configuration

# lljj 
weights_lljj = ['trigeff', 'llidiso', 'pu']
categories_lljj = ["All"] 
stage_lljj = "no_cut"
plots_lljj = ["mll", "mjj", "basic", "csv", "bdtinput", "gen"]

#llbb
weights_llbb = ['trigeff', 'llidiso', 'pu', 'jjbtag']
categories_llbb = ["All"]
stage_llbb = "no_cut"
plots_llbb = plots_lljj
#plots_llbb = ["bdtinput", "mjj"]

systematics = {"modifObjects" : ["nominal"]}
#systematics = {"modifObjects" : ["nominal", "jecup", "jecdown", "jerup", "jerdown"], "SF" : ["elidisoup", "elidisodown", "muidup", "muiddown", "muisoup", "muisodown", "jjbtagup", "jjbtagdown", "puup", "pudown", "trigeffup", "trigeffdown", "pdfup", "pdfdown", "scale", "scaleUncorr"]}
#systematics = {"modifObjects" : ["nominal"], "SF" : ["scale"]}

for systematicType in systematics.keys():
    
    for systematic in systematics[systematicType]:
        if systematicType == "modifObjects":
            objects = systematic
        else:
            objects = "nominal" #ensure that we use normal hh_objects for systematics not modifying obect such as scale factors 

        ## llbb 
        basePlotter_llbb = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = objects)      
        ## No mll cut
        #plots.extend(basePlotter_llbb.generatePlots(categories_llbb, stage_llbb, systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))
        plots.extend(basePlotter_llbb.generatePlots(["All"], stage_llbb, systematic = systematic, weights = weights_llbb, requested_plots = ["isElEl", "momemta_combine", "momemta_weights_fromtree"], extraString=""))
        #basePlotter_llbb = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_pt", btagWP_str = 'medium', objects = objects)
        #plots.extend(basePlotter_llbb.generatePlots(["All", "MuMu", "ElEl", "MuEl", "SF"], stage_llbb, systematic = systematic, weights = weights_llbb, requested_plots = ["mll", "basic", "mjj", "csv", "bdtinput", "isElEl"], extraString=""))
        #basePlotter_llbb = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = objects)
        #plots.extend(basePlotter_llbb.generatePlots(["All", "MuMu", "ElEl", "MuEl", "SF"], stage_llbb, systematic = systematic, weights = weights_llbb, requested_plots = ["mll", "basic", "mjj", "csv", "bdtinput", "isElEl"], extraString=""))
       
