#import ROOT as R
import sys, os, inspect 

# Usage from histFactory/plots/HHAnalysis/ : ./../../build/createHistoWithMultiDraw.exe -d ../../samples.json generatePlots.py 
scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir, "../histFactory_hh"))
from basePlotter import *
from HHAnalysis import HH

# Plot configuration
plots = []
# llbb 
basePlotter = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = "nominal")
weights_llbb = []
flavour = "All" # Careful! only one is allow otherwise the check "if (%s) {\n"%basePlotter.totalCut" is not fullfilled in the in_loop_code
categories_llbb = [flavour]
stage_llbb = "no_cut"
#plots_llbb = ["momemta_weights", "basic", "flavour", "mll", "mjj"]  #["mll", "mjj", "basic", "bdtinput", "ht", "other", "llidisoWeight", 'jjbtagWeight', 'trigeffWeight', 'puWeight', 'forSkimmer', 'csv', 'flavour', 'mis', 'evt']
plots_llbb = ["momemta_weights", "momemta_weights_skimmer"]  #["mll", "mjj", "basic", "bdtinput", "ht", "other", "llidisoWeight", 'jjbtagWeight', 'trigeffWeight', 'puWeight', 'forSkimmer', 'csv', 'flavour', 'mis', 'evt']
plots.extend(basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = "nominal", weights = weights_llbb, requested_plots = plots_llbb))

tree = {}
tree["name"] = "t"
tree["cut"] = basePlotter.totalCut
tree["branches"] = []
tree["clone"] = True

for plot in plots :
    branch = {}
    branch["name"] = plot["name"].split("_"+flavour)[0]
    branch["variable"] = plot["variable"]
    tree["branches"].append(branch)
    
for banch in tree["branches"] :
    print banch

# initialize globals code_before_loop, headers, etc...
import globals
globals.init()

# Fill code_before_loop, headers, etc... with what is needed for momemta
from skeleton_momemta import generate_weight_code
generate_weight_code(basePlotter)

include_directories = globals.include_directories
headers = globals.headers
libraries = globals.libraries
library_directories = globals.library_directories
code_before_loop = globals.code_before_loop
code_in_loop = globals.code_in_loop
extra_branches = globals.extra_branches
code_after_loop = globals.code_after_loop

include_directories.append(os.path.join(scriptDir, "..", "common"))
