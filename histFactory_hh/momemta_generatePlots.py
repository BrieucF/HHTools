import ROOT as R
import copy, sys, os, inspect 

# Usage from histFactory/plots/HHAnalysis/ : ./../../build/createHistoWithMultiDraw.exe -d ../../samples.json generatePlots.py 
scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
from basePlotter import *
from HHAnalysis import HH

# Plot configuration
plots = []
# llbb 
basePlotter = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = "nominal")
weights_llbb = ['trigeff', 'llidiso', 'pu', 'jjbtag']
flavour = "ElEl" # Careful! only one is allow otherwise the check "if (%s) {\n"%basePlotter.totalCut" is not fullfilled in the in_loop_code
categories_llbb = [flavour]
stage_llbb = "no_cut"
#plots_llbb = ["momemta_weights", "basic", "flavour", "mll", "mjj"]  #["mll", "mjj", "basic", "bdtinput", "ht", "other", "llidisoWeight", 'jjbtagWeight', 'trigeffWeight', 'puWeight', 'forSkimmer', 'csv', 'flavour', 'mis', 'evt']
plots_llbb = ["momemta_weights"]  #["mll", "mjj", "basic", "bdtinput", "ht", "other", "llidisoWeight", 'jjbtagWeight', 'trigeffWeight', 'puWeight', 'forSkimmer', 'csv', 'flavour', 'mis', 'evt']
plots.extend(basePlotter.generatePlots(categories_llbb, stage_llbb, systematic = "nominal", weights = weights_llbb, requested_plots = plots_llbb))

# Needed for momemta weights computation
includes = []
includes.append("<momemta/ConfigurationReader.h>")
includes.append("<momemta/MoMEMta.h>")
includes.append("<chrono>")
libraries = ["/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta/build/install/lib/libmomemta.so"]
code_before_loop = """
    using namespace std::chrono;\n
    ParameterSet dy_lua_parameters;\n
"""
#dy_lua_parameters.set("matrix_element_prefix", "pp_to_Z_to_llbb"); //  pp_to_llbb, gg_to_z_to_llbb, pp_to_Z_to_llbb

#matrix_element_prefix = "pp_to_Z_to_llbb"

TfFile = "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/HHTools/histFactory_hh/tf_genCut0_noRecoCut_lljjorbb_Oct18/condor/output/allTT_smoothed_notPutToZero.root"
MatrixElementDir = "/home/fynu/bfrancois/scratch/MoMEMta/plugin_mode/"
baseGlobalParameters = {
        "lep1TFFile":TfFile,
        "lep2TFFile":TfFile,
        "jet1TFFile":TfFile,
        "jet2TFFile":TfFile,

        #"lep1TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
        #"lep2TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
        #"jet1TFName":"ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
        #"jet2TFName":"ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",

        "matrix_element":"pp_to_Z_to_llbb_sm_P1_Sigma_sm_gg_epembbx",
        "matrix_element_parameters":MatrixElementDir+"/pp_to_Z_to_llbb/Cards/param_card.dat",
        "matrix_element_prefix": "pp_to_Z_to_llbb" #carefull this is a lua parameter, not global!!!!
        }
code_in_loop = ""

#print code_before_loop
tf_categories = {
        "elel":{
            "lep1TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv", 
            "lep2TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
            },
        "muel":{
            "lep1TFName":"ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv", 
            "lep2TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
            },
        "mumu":{
            "lep1TFName":"ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv", 
            "lep2TFName":"ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
            },
        "elmu":{
            "lep1TFName":"ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv", 
            "lep2TFName":"ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv",
            },
        }

code_in_loop_per_category = {
            "elel": [],
            "muel": [],
            "mumu": [],
            "elmu": [],
}

def newConfig(name, luaConfig, globalParameters, computeWeight_input = "{neg_lepton, pos_lepton, bjet1, bjet2, isr}, met", tf_categories=tf_categories, prefixLuaParameters="dy"):
    global code_before_loop
    global code_in_loop_per_category
    global basePlotter

    code_before_loop += "\n"
    name = name
    weightsName = name + "_weights"
    code_before_loop += "    std::vector<std::pair<double, double>> %s;\n"%(weightsName)
    weightsIntegStatusName = name + "_integStatus"
    code_before_loop += "    bool %s;\n"%(weightsIntegStatusName)
    weightsTimeName = name + "_time"
    weightsStartTimeName = name + "_startTime"
    weightsEndTimeName = name + "_endTime"
    code_before_loop += "    auto %s = system_clock::now();\n"%(weightsStartTimeName)
    code_before_loop += "    auto %s = system_clock::now();\n"%(weightsEndTimeName)
    code_before_loop += "    double %s;\n"%(weightsTimeName)
    lua_parameterSetName = "%s_lua_parameters"%prefixLuaParameters
    code_before_loop += "    " + lua_parameterSetName + """.set("matrix_element_prefix", "%s");\n"""%(globalParameters["matrix_element_prefix"])
    configReaderName =  "%s_configuration" % name
    code_before_loop += """    ConfigurationReader %s("%s", %s_lua_parameters);\n""" % (configReaderName, luaConfig, prefixLuaParameters)
    for parameter in globalParameters.keys():
        code_before_loop += """    %s.getGlobalParameters().set("%s", "%s");\n""" % (configReaderName, parameter, globalParameters[parameter])
    for category in tf_categories:
        # Set the proper tf for elel, mumu etc. One config for all tf category, just modify relevant params.
        nameWithFlavour = name + "_" + category
        code_before_loop += "\n"
        for tfentry in tf_categories[category]:
            code_before_loop += """    %s.getGlobalParameters().set("%s", "%s");\n""" % (configReaderName, tfentry, tf_categories[category][tfentry])
        weightComputerName = "%s_weightComputer"%nameWithFlavour
        code_before_loop += """\n    MoMEMta %s(%s.freeze());\n\n""" % (weightComputerName, configReaderName)
#        code_in_loop_per_category[category].append("""          std::cout << "Start computing weight %s" << std::endl;\n"""% (nameWithFlavour))
        code_in_loop_per_category[category].append("""          %s = system_clock::now();\n"""%weightsStartTimeName)
        code_in_loop_per_category[category].append("            %s = %s.computeWeights(%s);\n"% (weightsName, weightComputerName, computeWeight_input))
        code_in_loop_per_category[category].append("""          %s = system_clock::now();\n"""%weightsEndTimeName)
        code_in_loop_per_category[category].append("""          %s = (std::chrono::duration_cast<seconds>(%s - %s).count())/60.0;\n"""%(weightsTimeName, weightsEndTimeName, weightsStartTimeName))
        code_in_loop_per_category[category].append("            %s = (%s.getIntegrationStatus() == MoMEMta::IntegrationStatus::SUCCESS);\n"%(weightsIntegStatusName, weightComputerName))
        code_in_loop_per_category[category].append("            if (%s.at(0).first == 0) %s = { std::make_pair(std::numeric_limits<double>::min(), 0) };\n"% (weightsName, weightsName))
        code_in_loop_per_category[category].append("""          std::cout << "Computed weight %s : " << %s.at(0).first << " +- " << %s.at(0).second << " in " << %s << " min." << std::endl;\n"""% (nameWithFlavour, weightsName, weightsName, weightsTimeName))
        code_in_loop_per_category[category].append("\n")

#newConfig("dy_tradeElep2ForZMass_Jet_ba_ec_Ele_ba_Mu_ba", {} , "dy")
#weight_dict = {
#        weightName: "pp_Z_llbb_elel_tfJetAllEta"
#        globalParameters_tomodify: ""
#        }

#newConfig("pp_Z_llbb_elel_tfJetAllEta_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", baseGlobalParameters)


# DY weight
#newConfig("pp_Z_llbb_TFCATEG_tfJetAllEta_simple", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_simple.lua", baseGlobalParameters)

## TT weight
#parameters_pp_tt_llbb = copy.deepcopy(baseGlobalParameters)
#parameters_pp_tt_llbb["matrix_element_parameters"] = MatrixElementDir+"/pp_to_tt_to_lvlvbb/Cards/param_card.dat"
#parameters_pp_tt_llbb["matrix_element_prefix"] = "pp_to_tt_to_lvlvbb"
#parameters_pp_tt_llbb["matrix_element"] = "pp_to_tt_to_lvlvbb_sm_P1_Sigma_sm_gg_emvexepvebbx"
#newConfig("pp_tt_llbb_tfJetAllEta", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/tt_fullyleptonic_custom.lua", parameters_pp_tt_llbb, computeWeight_input = "{neg_lepton, pos_lepton, bjet1, bjet2}, met")

# tW- weight
parameters_twminus = copy.deepcopy(baseGlobalParameters)
parameters_twminus["matrix_element_parameters"] = MatrixElementDir+"/pp_twMinusbbar_tAndWOnshell/Cards/param_card.dat"
parameters_twminus["matrix_element_prefix"] = "pp_twMinusbbar_tAndWOnshell"
parameters_twminus["matrix_element"] = "pp_twMinusbbar_tAndWOnshell_sm_P1_Sigma_sm_gg_mupvmbmumvmxbx"
newConfig("twminus_tfJetAllEta", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/twMinusbbar.lua", parameters_twminus, computeWeight_input = "{neg_lepton, pos_lepton, bjet1, bjet2, dummy_neutrino}, met")
## ZZ weights
#parameters_pp_zz_llbb_simple = copy.deepcopy(baseGlobalParameters)
#parameters_pp_zz_llbb_simple["matrix_element_parameters"] = MatrixElementDir+"/pp_to_zz_to_llbb/Cards/param_card.dat"
#parameters_pp_zz_llbb_simple["matrix_element_prefix"] = "pp_to_zz_to_llbb"
#parameters_pp_zz_llbb_simple["matrix_element"] = "pp_to_zz_to_llbb_sm_P1_Sigma_sm_uux_mupmumbbx"
#parameters_pp_zz_llbb_simple["lep1_me_index"] = 1
#parameters_pp_zz_llbb_simple["lep2_me_index"] = 2
#newConfig("pp_zz_llbb_simple_TFCATEG_tfJetAllEta", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/zz_to_llbb_simple.lua", parameters_pp_zz_llbb_simple)
#newConfig("pp_zz_llbb_blockG_TFCATEG_tfJetAllEta", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/zz_to_llbb_blockG.lua", parameters_pp_zz_llbb_simple)
#newConfig("pp_zz_llbb_SBCDblockA_TFCATEG_tfJetAllEta", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/zz_to_llbb_SBCD_blockA.lua", parameters_pp_zz_llbb_simple)

#parameters_pp_Z_llbb_elel_tfJet_ba_ba = copy.deepcopy(baseGlobalParameters)
#parameters_pp_Z_llbb_elel_tfJet_ba_ba["jet1TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#parameters_pp_Z_llbb_elel_tfJet_ba_ba["jet2TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#newConfig("pp_Z_llbb_elel_tfJet_ba_ba_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", baseGlobalParameters)
#
#parameters_pp_Z_llbb_elel_tfJet_ec_ba = copy.deepcopy(baseGlobalParameters)
#parameters_pp_Z_llbb_elel_tfJet_ec_ba["jet1TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#parameters_pp_Z_llbb_elel_tfJet_ec_ba["jet2TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#newConfig("pp_Z_llbb_elel_tfJet_ec_ba_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", baseGlobalParameters)
#
#parameters_pp_Z_llbb_elel_tfJet_ba_ec = copy.deepcopy(baseGlobalParameters)
#parameters_pp_Z_llbb_elel_tfJet_ba_ec["jet1TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#parameters_pp_Z_llbb_elel_tfJet_ba_ec["jet2TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#newConfig("pp_Z_llbb_elel_tfJet_ba_ec_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", baseGlobalParameters)
#
#parameters_pp_Z_llbb_elel_tfJet_ec_ec = copy.deepcopy(baseGlobalParameters)
#parameters_pp_Z_llbb_elel_tfJet_ec_ec["jet1TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#parameters_pp_Z_llbb_elel_tfJet_ec_ec["jet2TFName"] = "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
#newConfig("pp_Z_llbb_elel_tfJet_ec_ec_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", baseGlobalParameters)
#
#parameters_pp_llbb = copy.deepcopy(baseGlobalParameters)
#parameters_pp_llbb["matrix_element_parameters"] = MatrixElementDir+"/pp_to_llbb/Cards/param_card.dat"
#parameters_pp_llbb["matrix_element_prefix"] = "pp_to_llbb"
#parameters_pp_llbb["matrix_element"] = "pp_to_llbb_sm_P1_Sigma_sm_gg_epembbx"
#newConfig("pp_llbb_elel_tfJetAllEta_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", parameters_pp_llbb)
#
#parameters_gg_Z_llbb = copy.deepcopy(baseGlobalParameters)
#parameters_gg_Z_llbb["matrix_element_parameters"] = MatrixElementDir+"/gg_to_z_to_llbb/Cards/param_card.dat"
#parameters_gg_Z_llbb["matrix_element_prefix"] = "gg_to_z_to_llbb"
#parameters_gg_Z_llbb["matrix_element"] = "gg_to_z_to_llbb_sm_P1_Sigma_sm_gg_epembbx"
#newConfig("gg_Z_llbb_elel_tfJetAllEta_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_tradeElep2ForZMass.lua", parameters_gg_Z_llbb)
#
#parameters_mumu = copy.deepcopy(baseGlobalParameters)
#parameters_mumu["lep1TFName"] = "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv" 
#parameters_mumu["lep2TFName"] = "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv" 
#newConfig("pp_llbb_mumu_tfJetAllEta_tradeElep2ForZMass", "/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/MoMEMta_cfg/dy_to_ll_simple.lua", baseGlobalParameters)
#

#code_before_loop += """ 
#    std::vector<std::pair<double, double>> pp_Z_llbb_weights_simple;\n
#    std::vector<std::pair<double, double>> pp_Z_llbb_weights_tradeElep2ForZMass;\n
#    std::vector<std::pair<double, double>> gg_Z_llbb_weights_tradeElep2ForZMass;\n
#    std::vector<std::pair<double, double>> pp_llbb_weights_tradeElep2ForZMass;\n
#    std::vector<std::pair<double, double>> pp_Z_llbb_tradeElep2ForZMass_2jetEtaBins;\n
#    std::vector<std::pair<double, double>> pp_tt_llbb_tfJetAllEta_weights;\n
#"""

code_in_loop += "   if (%s) {\n"%basePlotter.totalCut
code_in_loop += "       LorentzVector neg_lepton_p4;\n"
code_in_loop += "       LorentzVector pos_lepton_p4;\n"
code_in_loop += "       if (%s.charge == -1) {\n"%basePlotter.lep1_str
code_in_loop += "           neg_lepton_p4 = %s.p4;\n"%basePlotter.lep1_str
code_in_loop += "           pos_lepton_p4 = %s.p4;\n"%basePlotter.lep2_str
code_in_loop += "       }\n\n"
code_in_loop += "       else {\n"
code_in_loop += "           neg_lepton_p4 = %s.p4;\n"%basePlotter.lep2_str
code_in_loop += "           pos_lepton_p4 = %s.p4;\n"%basePlotter.lep1_str
code_in_loop += "       }\n\n"

code_in_loop += "       const double lepMass = 0.0001;\n"
code_in_loop += "       const double modifFactor_neg_lepton_p4 = std::sqrt((neg_lepton_p4.E() - lepMass) * (neg_lepton_p4.E() + lepMass)) / neg_lepton_p4.P();\n"
code_in_loop += "       neg_lepton_p4.SetPxPyPzE(modifFactor_neg_lepton_p4 * neg_lepton_p4.Px(), modifFactor_neg_lepton_p4 * neg_lepton_p4.Py(), modifFactor_neg_lepton_p4 * neg_lepton_p4.Pz(), neg_lepton_p4.E());\n"
code_in_loop += "       const double modifFactor_pos_lepton_p4 = std::sqrt((pos_lepton_p4.E() - lepMass) * (pos_lepton_p4.E() + lepMass)) / pos_lepton_p4.P();\n"
code_in_loop += "       pos_lepton_p4.SetPxPyPzE(modifFactor_pos_lepton_p4 * pos_lepton_p4.Px(), modifFactor_pos_lepton_p4 * pos_lepton_p4.Py(), modifFactor_pos_lepton_p4 * pos_lepton_p4.Pz(), pos_lepton_p4.E());\n"

code_in_loop += "       const double bjetMass = 4.2;\n"
code_in_loop += "       LorentzVector bjet1_p4(%s.p4);\n"%basePlotter.jet1_str
code_in_loop += "       const double modifFactor_bjet1_p4 = std::sqrt((bjet1_p4.E() - lepMass) * (bjet1_p4.E() + lepMass)) / bjet1_p4.P();\n"
code_in_loop += "       bjet1_p4.SetPxPyPzE(modifFactor_bjet1_p4 * bjet1_p4.Px(), modifFactor_bjet1_p4 * bjet1_p4.Py(), modifFactor_bjet1_p4 * bjet1_p4.Pz(), bjet1_p4.E());\n"
code_in_loop += "       LorentzVector bjet2_p4(%s.p4);\n"%basePlotter.jet2_str
code_in_loop += "       const double modifFactor_bjet2_p4 = std::sqrt((bjet2_p4.E() - lepMass) * (bjet2_p4.E() + lepMass)) / bjet2_p4.P();\n"
code_in_loop += "       bjet2_p4.SetPxPyPzE(modifFactor_bjet2_p4 * bjet2_p4.Px(), modifFactor_bjet2_p4 * bjet2_p4.Py(), modifFactor_bjet2_p4 * bjet2_p4.Pz(), bjet2_p4.E());\n"
code_in_loop += "       LorentzVector minus_isr_p4 = neg_lepton_p4+pos_lepton_p4+bjet1_p4+bjet2_p4;\n"
code_in_loop += "       LorentzVector isr_p4;\n"
code_in_loop += "       isr_p4.SetPxPyPzE(-minus_isr_p4.Px(), -minus_isr_p4.Py(), -minus_isr_p4.Pz(), minus_isr_p4.E());\n"

code_in_loop += """       LorentzVector met(%s);\n"""%basePlotter.met_str
code_in_loop += """       Particle pos_lepton { "pos_lepton", pos_lepton_p4, -11 };"""
code_in_loop += """       Particle neg_lepton { "neg_lepton", neg_lepton_p4, 11 };"""
code_in_loop += """       Particle bjet1 { "bjet1", bjet1_p4, 5 };"""
code_in_loop += """       Particle bjet2 { "bjet2", bjet2_p4, -5 };"""
code_in_loop += """       Particle isr { "isr", isr_p4, 0 };"""
code_in_loop += """       Particle dummy_neutrino { "dummy_neutrino", LorentzVector(1,0,0,1), 0 };\n"""

code_in_loop += "       if (%s.isEl && %s.isEl){\n\n"%(basePlotter.lep1_str, basePlotter.lep2_str)
for line in code_in_loop_per_category["elel"] :
    code_in_loop += line
code_in_loop += "       }\n"
# MuEl
code_in_loop += "       if (%s.isMu && %s.isEl){\n\n"%(basePlotter.lep1_str, basePlotter.lep2_str)
for line in code_in_loop_per_category["muel"] :
    code_in_loop += line
code_in_loop += "       }\n\n"
# MuMu
code_in_loop += "       if (%s.isMu && %s.isMu){\n\n"%(basePlotter.lep1_str, basePlotter.lep2_str)
for line in code_in_loop_per_category["mumu"] :
    code_in_loop += line
code_in_loop += "       }\n\n"
# ElMu
code_in_loop += "        if (%s.isEl && %s.isMu){\n\n"%(basePlotter.lep1_str, basePlotter.lep2_str)
for line in code_in_loop_per_category["elmu"] :
    code_in_loop += line
code_in_loop += "       }\n"
code_in_loop += "   }\n\n"#sanity check ends here


#code_in_loop += "       std::cout << p1 << std::endl;\n"
#code_in_loop += "       std::cout << p2 << std::endl;\n"
#code_in_loop += "       std::cout << p3 << std::endl;\n"
#code_in_loop += "       std::cout << p4 << std::endl;\n"
#code_in_loop += "       std::cout << -(p1+p2+p3+p4) << std::endl;\n"
# ElEl
#code_in_loop += "       }\n"

#code_in_loop += """
#                    if (%s.isEl && %s.isEl) {\n
#
#                        //pp_Z_llbb_weights_tradeElep2ForZMass = pp_Z_llbb_elel_tfJetAllEta_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#
#                        //gg_Z_llbb_weights_tradeElep2ForZMass = gg_Z_llbb_elel_tfJetAllEta_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#
#                        //pp_llbb_weights_tradeElep2ForZMass = pp_llbb_elel_tfJetAllEta_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#
#                        pp_Z_llbb_weights_simple = pp_Z_llbb_elel_tfJetAllEta_simple_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4) });\n
#                        if (pp_Z_llbb_weights_simple.at(0).first == 0) pp_Z_llbb_weights_simple = { std::make_pair(std::numeric_limits<double>::min(), 0) };\n
#
#                        pp_tt_llbb_tfJetAllEta_weights = pp_tt_llbb_elel_tfJetAllEta_weightComputer.computeWeights({p1, p2, p3, p4}, met);\n
#                        if (pp_tt_llbb_tfJetAllEta_weights.at(0).first == 0) pp_tt_llbb_tfJetAllEta_weights = { std::make_pair(std::numeric_limits<double>::min(), 0) };\n
#
#                        //if (p3.Eta() < 1.3 && p4.Eta() < 1.3){\n
#                        //    pp_Z_llbb_weights_tradeElep2ForZMass_2jetEtaBins = pp_Z_llbb_elel_tfJet_ba_ba_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#                        //}
#                        //else if (p3.Eta() > 1.3 && p4.Eta() < 1.3){\n
#                        //    pp_Z_llbb_weights_tradeElep2ForZMass_2jetEtaBins = pp_Z_llbb_elel_tfJet_ec_ba_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#                        //}
#                        //else if (p3.Eta() < 1.3 && p4.Eta() > 1.3){\n
#                        //    pp_Z_llbb_weights_tradeElep2ForZMass_2jetEtaBins = pp_Z_llbb_elel_tfJet_ba_ec_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#                        //}
#                        //else if (p3.Eta() > 1.3 && p4.Eta() > 1.3){\n
#                        //    pp_Z_llbb_weights_tradeElep2ForZMass_2jetEtaBins = pp_Z_llbb_elel_tfJet_ec_ec_tradeElep2ForZMass_weightComputer.computeWeights({p1, p2, p3, p4, -(p1+p2+p3+p4)});\n
#                        //}
#                        //else{\n
#                        //    pp_Z_llbb_weights_tradeElep2ForZMass_2jetEtaBins = { std::make_pair(std::numeric_limits<double>::min(), 0) };\n
#                        //}
#                    }
#                        
#"""%(basePlotter.lep1_str, basePlotter.lep2_str)
#code_in_loop += "}\n"


#tree = {}
#tree["name"] = "t"
#tree["cut"] = basePlotter.joinCuts(basePlotter.sanityCheck, basePlotter.dict_cat_cut["All"])
#tree["branches"] = []
#
#for plot in plots :
#    print plots
#    branch = {}
#    branch["name"] = plot["name"].split("_"+flavour)[0]
#    branch["variable"] = plot["variable"]
#    tree["branches"].append(branch)
#    
#for banch in tree["branches"] :
#    print banch
