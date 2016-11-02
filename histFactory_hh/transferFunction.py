import ROOT as R
import copy, sys, os, inspect 


# Usage from histFactory/plots/HHAnalysis/ : ./../../build/createHistoWithMultiDraw.exe -d ../../samples.json generatePlots.py 
scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)

from basePlotter import *
from HHAnalysis import HH

includes = []
plots = []

basePlotter_lljj = BasePlotter(baseObjectName = 'hh_llmetjj_HWWleptons_nobtag_csv', btagWP_str = 'nobtag', objects = "nominal")
plots.extend(basePlotter_lljj.generatePlots(["All"], 'no_cut', systematic = 'nominal', weights = [], requested_plots = ["jet_tf", "mu_tf", "el_tf"])) 
basePlotter_lljj = BasePlotter(baseObjectName = 'hh_llmetjj_HWWleptons_btagM_csv', btagWP_str = 'btagM', objects = "nominal")
plots.extend(basePlotter_lljj.generatePlots(["All"], 'no_cut', systematic = 'nominal', weights = [], requested_plots = ["jet_tf", "mu_tf", "el_tf"])) 

