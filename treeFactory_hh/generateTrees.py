import ROOT as R
import copy, sys, os, inspect 

# Usage from histFactory/plots/HHAnalysis/ : ./../../build/createHistoWithMultiDraw.exe -d ../../samples.json generatePlots.py 
scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir, "../histFactory_hh"))
from basePlotter import *

plots = []

# Needed to evaluate MVA outputs
#includes.append( os.path.join(scriptDir, "..", "common", "readMVA.h") )

# Plot configuration

# llbb 
basePlotter = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = "nominal")
weights_llbb = []
flavour = "All"
categories_llbb = [flavour]
stage_llbb = "no_cut"
plots_llbb = ["mll", "mjj", "basic", "bdtinput", "ht", "other", "llidisoWeight", 'jjbtagWeight', 'trigeffWeight', 'puWeight', 'forSkimmer', 'csv', 'flavour', 'mis', 'evt', "momemta_combine", "momemta_weights_fromtree", "mis"]
plots.extend(basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = "nominal", weights = weights_llbb, requested_plots = plots_llbb))

tree = {}
tree["name"] = "t"
tree["cut"] = basePlotter.totalCut
tree["branches"] = []

# Store scale factors with systematics. Careful!! Wust be after the tree["cut"] definition
def SF_systematics(name, lepton_SF = False):
    if lepton_SF : 
        plot_up = basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = name+"up", weights = weights_llbb, requested_plots = ["llidisoWeight"])[0]
        plot_up["name"] = plot_up["name"].replace("llidiso", "llidiso_"+name+"up")
        plot_down = basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = name+"down", weights = weights_llbb, requested_plots = ["llidisoWeight"])[0]
        plot_down["name"] = plot_down["name"].replace("llidiso", "llidiso_"+name+"down")
    else:
        plot_up = basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = name+"up", weights = weights_llbb, requested_plots = [name+"Weight"])[0]
        plot_up["name"] = plot_up["name"].replace(name, name+"_up")
        plot_down = basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = name+"down", weights = weights_llbb, requested_plots = [name+"Weight"])[0]
        plot_down["name"] = plot_down["name"].replace(name, name+"_down")
    plots.append(plot_up)
    plots.append(plot_down)

SF_systematics("trigeff")
SF_systematics("jjbtag")
SF_systematics("pu")
SF_systematics("elidiso", True) # more tricky
SF_systematics("muid", True) # more tricky
SF_systematics("muiso", True) # more tricky

for plot in plots :
    branch = {}
    branch["name"] = plot["name"].split("_"+flavour)[0]
    print branch["name"]
    branch["variable"] = plot["variable"]
    tree["branches"].append(branch)
    
for banch in tree["branches"] :
    print banch

import globals
globals.init()

include_directories = globals.include_directories
headers = globals.headers
libraries = globals.libraries
library_directories = globals.library_directories
code_before_loop = globals.code_before_loop
code_in_loop = globals.code_in_loop
extra_branches = globals.extra_branches
code_after_loop = globals.code_after_loop
include_directories.append(os.path.join(scriptDir, "..", "common"))
