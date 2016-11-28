import copy, sys

bjet_binningX = range(0, 200, 5) + range(200, 400, 20) + [400, 450, 500, 550, 600, 700, 800, 2000]
bjet_binningY = [-500, -400] + range(-300, -200, 50) + range(-200, -50, 10) + range(-50, 0, 5) + range(0, 50, 5) + range(50, 200, 10) + range(200, 300, 50) + [300, 400, 500]

#bjet_BA_binningX = range(0, 200, 5) + range(200, 360, 20) + [360, 400, 1000] 
#bjet_BA_binningY = range(-500, -200, 100) + range(-200, -100, 20) + range(-100, 0, 10) + range(0, 100, 10) + range(100, 200, 20) + range(200, 500, 100) + [500]
#
#bjet_EC_binningX = range(0, 200, 10) + range(200, 500, 20) + [500, 550, 600, 800, 2000]
#bjet_EC_binningY = range(-500, -200, 100) + range(-200, -50, 20) + range(-50, 0, 10) + range(0, 50, 10) + range(50, 200, 20) + range(200, 500, 100) + [500]

bjet_BA_binningX = bjet_binningX
bjet_BA_binningY = bjet_binningY

bjet_EC_binningX = bjet_binningX
bjet_EC_binningY = bjet_binningY

bjet_nBinsX = str(len(bjet_binningX)-1)
bjet_binningX = "{" + str(bjet_binningX).strip("[").strip("]") + "}"
bjet_nBinsY = str(len(bjet_binningY)-1)
bjet_binningY = "{" + str(bjet_binningY).strip("[").strip("]") + "}"

bjet_BA_nBinsX = str(len(bjet_BA_binningX)-1)
bjet_BA_binningX = "{" + str(bjet_BA_binningX).strip("[").strip("]") + "}"
bjet_BA_nBinsY = str(len(bjet_BA_binningY)-1)
bjet_BA_binningY = "{" + str(bjet_BA_binningY).strip("[").strip("]") + "}"

bjet_EC_nBinsX = str(len(bjet_EC_binningX)-1)
bjet_EC_binningX = "{" + str(bjet_EC_binningX).strip("[").strip("]") + "}"
bjet_EC_nBinsY = str(len(bjet_EC_binningY)-1)
bjet_EC_binningY = "{" + str(bjet_EC_binningY).strip("[").strip("]") + "}"

# Egen starts at 0 (bad if we do not reweight partonic config with efficiency to be reconstructed)
#mu_binningX = [0, 10, 20] + range(25, 200, 5) + range(200, 400, 20) + [400, 450, 500, 550, 600, 700, 800, 2000]
#mu_binningY = [-200, -100] + range(-50, -20, 10) + range(-20, -10, 5) + range(-10, -3, 1) + [-3 + x * 0.2 for x in range(0, 30)] + range(3, 10, 1) + range(10, 20, 2) + range(20, 50, 3) + [50, 100, 200]
# Egen starts at 0 (bad if we do not reweight partonic config with efficiency to be reconstructed)
mu_binningX = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] + range(25, 200, 5) + range(200, 400, 20) + [400, 450, 500, 550, 600, 700, 800, 2000]
mu_binningY = [-200, -100] + range(-50, -20, 10) + range(-20, -10, 5) + range(-10, -3, 1) + [-3 + x * 0.2 for x in range(0, 30)] + range(3, 10, 1) + range(10, 20, 5) + range(20, 50, 10) + [50, 100, 200]
#Dont put the following line after having stripped the mu_binning ;-)
el_binningX = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] + range(25, 200, 5) + range(200, 400, 20) + [400, 450, 500, 550, 600, 700, 800, 2000]
el_binningY = mu_binningY

mu_nBinsX = str(len(mu_binningX)-1)
mu_binningX = "{" + str(mu_binningX).strip("[").strip("]") + "}"
mu_nBinsY = str(len(mu_binningY)-1)
mu_binningY = "{" + str(mu_binningY).strip("[").strip("]") + "}"

el_nBinsX = str(len(el_binningX)-1)
el_binningX = "{" + str(el_binningX).strip("[").strip("]") + "}"
el_nBinsY = str(len(el_binningY)-1)
el_binningY = "{" + str(el_binningY).strip("[").strip("]") + "}"

class BasePlotter:
    def __init__(self, baseObjectName = "hh_llmetjj_HWWleptons_btagM_csv", btagWP_str = 'medium', objects = "nominal"):
        # systematic should be jecup, jecdown, jerup or jerdown. The one for lepton, btag, etc, have to be treated with the "weight" parameter in generatePlots.py (so far)

        self.baseObject = baseObjectName+"[0]"
        self.suffix = baseObjectName
        self.btagWP_str = btagWP_str
        
        self.lep1_str = "hh_leptons[%s.ilep1]"%self.baseObject
        self.lep2_str = "hh_leptons[%s.ilep2]"%self.baseObject
        self.jet1_str = "hh_jets[%s.ijet1]"%self.baseObject
        self.jet2_str = "hh_jets[%s.ijet2]"%self.baseObject
        self.ll_str = "%s.ll_p4"%self.baseObject 
        self.jj_str = "%s.jj_p4"%self.baseObject
        self.met_str = "%s.met_p4"%self.baseObject
        self.extrajet_cut = "Length$(%s.iExtraJets)>0"%self.baseObject
        self.extrajet_str = "hh_jets[%s.iExtraJets[0]]"%self.baseObject

        if objects != "nominal":
            baseObjectName = baseObjectName.replace("hh_", "hh_"+objects+"_")
            self.lep1_str = self.lep1_str.replace("hh_", "hh_"+objects+"_")
            self.lep2_str = self.lep2_str.replace("hh_", "hh_"+objects+"_")
            self.jet1_str = self.jet1_str.replace("hh_", "hh_"+objects+"_")
            self.jet2_str = self.jet2_str.replace("hh_", "hh_"+objects+"_")
            self.ll_str = self.ll_str.replace("hh_", "hh_"+objects+"_")
            self.jj_str = self.jj_str.replace("hh_", "hh_"+objects+"_")
            self.met_str = self.met_str.replace("hh_", "hh_"+objects+"_")
            self.extrajet_str = self.extrajet_str.replace("hh_", "hh_"+objects+"_")
            self.extrajet_cut = self.extrajet_str.replace("hh_", "hh_"+objects+"_")
            self.baseObject = self.baseObject.replace("hh_", "hh_"+objects+"_")

        # needed to get scale factors (needs to be after the object modification due to systematics)
        self.lep1_fwkIdx = self.lep1_str+".idx"
        self.lep2_fwkIdx = self.lep2_str+".idx"
        self.jet1_fwkIdx = self.jet1_str+".idx"
        self.jet2_fwkIdx = self.jet2_str+".idx"

        # Ensure we have one candidate, works also for jecup etc
        self.sanityCheck = "Length$(%s)>0"%baseObjectName

    
    def generatePlots(self, categories = ["All"], stage = "cleaning_cut", requested_plots = [], weights = ['trigeff', 'jjbtag', 'llidiso', 'pu'], extraCut = "", systematic = "nominal", extraString = ""):

        # MVA evaluation : ugly but necessary part
        baseStringForMVA_part1 = 'evaluateMVA("/home/fynu/sbrochet/scratch/Framework/CMSSW_7_6_5/src/cp3_llbb/HHTools//mvaTraining_hh/weights/BDTNAME_kBDT.weights.xml", '
        baseStringForMVA_part2 = '{{"jj_pt", %s}, {"ll_pt", %s}, {"ll_M", %s}, {"ll_DR_l_l", %s}, {"jj_DR_j_j", %s}, {"llmetjj_DPhi_ll_jj", %s}, {"llmetjj_minDR_l_j", %s}, {"llmetjj_MTformula", %s}})' % ( self.jj_str + ".Pt()", self.ll_str + ".Pt()", self.ll_str + ".M()", self.baseObject + ".DR_l_l", self.baseObject + ".DR_j_j", self.baseObject + ".minDR_l_j", self.baseObject + ".DPhi_ll_jj", self.baseObject + ".MT_formula")
        stringForMVA = baseStringForMVA_part1 + baseStringForMVA_part2
        
        # The following will need to be modified each time the name of the BDT output changes
        bdtNameTemplate = "DATE_BDT_NODE_SUFFIX"
        
        # v1 benchmark BDTs (w/ LO DY)
        #date = "2016_05_27"
        #nodes = ["SM", "box", "5", "8", "13", "all"]
        
        date = "2016_07_05"
        
        suffixes = ["VS_TT_DYHTonly_tW_8var"]
        BDToutputs = {}
        bdtNames = []
        BDToutputsVariable = {}

        # Possible stages (selection)
        mll_cut = "((91 - {0}.M()) > 15)".format(self.ll_str)
        mjj_blind = "({0}.M() < 75 || {0}.M() > 140)".format(self.jj_str)
        dict_stage_cut = {
               "no_cut": "", 
               "mll_cut": mll_cut,
               "mjj_blind": self.joinCuts(mjj_blind, mll_cut),
               }
        # High-BDT stages
        for suffix in suffixes:
            bdtName = bdtNameTemplate.replace("DATE", date).replace("SUFFIX", suffix)
            BDToutput = baseStringForMVA_part1.replace("BDTNAME", bdtName) + baseStringForMVA_part2
            dict_stage_cut["highBDT_node_"] = self.joinCuts(BDToutput + ">0", mll_cut)

        # Categories (lepton flavours) and trigger requirement
        self.dict_cat_cut =  {
            "ElEl": "({0}.isElEl && ((hh_elel_fire_trigger_Ele17_Ele12_cut || runOnMC) && (runOnElEl || runOnMC) && {1}.M() > 12))".format(self.baseObject, self.ll_str),
            "MuMu": "({0}.isMuMu && (hh_mumu_fire_trigger_Mu17_Mu8_cut || hh_mumu_fire_trigger_Mu17_TkMu8_cut || runOnMC) && (runOnMuMu || runOnMC) && {1}.M() > 12)".format(self.baseObject, self.ll_str),
            "MuEl": "(({0}.isElMu || {0}.isMuEl) && (hh_elmu_fire_trigger_Mu8_Ele17_cut || hh_muel_fire_trigger_Mu17_Ele12_cut || runOnMC) && (runOnElMu || runOnMC) && {1}.M() > 12)".format(self.baseObject, self.ll_str)
                        }
        cut_for_All_channel = "(" + self.dict_cat_cut["ElEl"] + "||" + self.dict_cat_cut["MuMu"] + "||" +self.dict_cat_cut["MuEl"] + ")"
        cut_for_SF_channel = "(" + self.dict_cat_cut["ElEl"] + "||" + self.dict_cat_cut["MuMu"] + ")"
        self.dict_cat_cut["SF"] = cut_for_SF_channel
        self.dict_cat_cut["All"] = cut_for_All_channel

        ###########
        # Weights #
        ###########

        # Lepton ID and Iso Scale Factors
        llIdIso_sfIdx = "[0]"
        llIdIso_strCommon = "NOMINAL"
        llIdIso_sf = "(common::combineScaleFactors<2>({{{{{{({0}.isEl) ? electron_sf_hww_wp[{1}][0] : muon_sf_id_hww[{1}][0]*muon_sf_iso_tight_id_hww[{1}][0], ({0}.isEl) ? electron_sf_hww_wp[{1}]{2} : muon_sf_id_hww[{1}]{2}*muon_sf_iso_tight_id_hww[{1}]{2}}}, {{ ({3}.isEl) ? electron_sf_hww_wp[{4}][0] : muon_sf_id_hww[{4}][0]*muon_sf_iso_tight_id_hww[{4}][0], ({3}.isEl) ? electron_sf_hww_wp[{4}]{2} : muon_sf_id_hww[{4}]{2}*muon_sf_iso_tight_id_hww[{4}]{2} }}}}}}, common::Variation::{5}) )".format(self.lep1_str, self.lep1_fwkIdx, llIdIso_sfIdx, self.lep2_str, self.lep2_fwkIdx, llIdIso_strCommon)
        # electrons
        if systematic == "elidisoup":
            llIdIso_sfIdx = "[2]" 
            llIdIso_strCommon = "UP"
        if systematic == "elidisodown":
            llIdIso_sfIdx = "[1]"
            llIdIso_strCommon = "DOWN"
        if systematic == "elidisoup" or systematic == "elidisodown":
            llIdIso_sf = "(common::combineScaleFactors<2>({{{{{{({0}.isEl) ? electron_sf_hww_wp[{1}][0] :muon_sf_id_hww[{1}][0]*muon_sf_iso_tight_id_hww[{1}][0], ({0}.isEl) ? electron_sf_hww_wp[{1}]{2} : 0 }}, {{ ({3}.isEl) ? electron_sf_hww_wp[{4}][0] :muon_sf_id_hww[{4}][0]*muon_sf_iso_tight_id_hww[{4}][0], ({3}.isEl) ? electron_sf_hww_wp[{4}]{2} : 0 }}}}}}, common::Variation::{5}) )".format(self.lep1_str, self.lep1_fwkIdx, llIdIso_sfIdx, self.lep2_str, self.lep2_fwkIdx, llIdIso_strCommon)

        # muons
        if systematic == "muidup":
            llIdIso_sfIdx = "[2]" 
            llIdIso_strCommon="UP"
        if systematic == "muiddown":
            llIdIso_sfIdx = "[1]"
            llIdIso_strCommon="DOWN"
        if systematic == "muidup" or systematic == "muiddown":
            # if we compute muon id error, the muon iso SF should not be inside the combineScaleFactors (above, for electron id error, it can be inside because it won't be use together with the error
            llIdIso_sf = "((({0}.isEl) ? 1 : muon_sf_iso_tight_id_hww[{1}][0]) * (({3}.isEl) ? 1 : muon_sf_iso_tight_id_hww[{4}][0]) * (common::combineScaleFactors<2>({{{{{{({0}.isEl) ? electron_sf_hww_wp[{1}][0] :muon_sf_id_hww[{1}][0], ({0}.isEl) ? 0. :muon_sf_id_hww[{1}]{2}}}, {{ ({3}.isEl) ? electron_sf_hww_wp[{4}][0] :muon_sf_id_hww[{4}][0], ({3}.isEl) ? 0. :muon_sf_id_hww[{4}]{2} }}}}}}, common::Variation::{5}) ))".format(self.lep1_str, self.lep1_fwkIdx, llIdIso_sfIdx, self.lep2_str, self.lep2_fwkIdx, llIdIso_strCommon)
        if systematic == "muisoup":
            llIdIso_sfIdx = "[2]" 
            llIdIso_strCommon="UP"
        if systematic == "muisodown":
            llIdIso_sfIdx = "[1]"
            llIdIso_strCommon="DOWN"
        if systematic == "muisoup" or systematic == "muisodown":
            llIdIso_sf = "((({0}.isEl) ? 1 : muon_sf_id_hww[{1}][0]) * (({3}.isEl) ? 1 : muon_sf_id_hww[{4}][0]) * (common::combineScaleFactors<2>({{{{{{({0}.isEl) ? electron_sf_hww_wp[{1}][0] :muon_sf_iso_tight_id_hww[{1}][0], ({0}.isEl) ? 0. :muon_sf_iso_tight_id_hww[{1}]{2}}}, {{ ({3}.isEl) ? electron_sf_hww_wp[{4}][0] :muon_sf_iso_tight_id_hww[{4}][0], ({3}.isEl) ? 0. :muon_sf_iso_tight_id_hww[{4}]{2} }}}}}}, common::Variation::{5}) ))".format(self.lep1_str, self.lep1_fwkIdx, llIdIso_sfIdx, self.lep2_str, self.lep2_fwkIdx, llIdIso_strCommon)

        # BTAG SF
        jjBtag_sfIdx = "[0]"
        jjBtag_strCommon="NOMINAL"
        if systematic == "jjbtagup":
            jjBtag_sfIdx = "[2]" 
            jjBtag_strCommon="UP"
        if systematic == "jjbtagdown":
            jjBtag_sfIdx = "[1]"
            jjBtag_strCommon="DOWN"
        # propagate jecup etc to the framework objects
        sys_fwk = ""
        if "jec" in systematic or "jer" in systematic:
            sys_fwk = "_" + systematic
        jjBtag_sf = "(common::combineScaleFactors<2>({{{{{{ jet{0}_sf_csvv2_{1}[{2}][0] , jet{0}_sf_csvv2_{1}[{2}]{3} }}, {{ jet{0}_sf_csvv2_{1}[{4}][0] , jet{0}_sf_csvv2_{1}[{4}]{3} }}}}}}, {{{{1, 0}}, {{0, 1}}}}, common::Variation::{5}) )".format(sys_fwk, self.btagWP_str, self.jet1_fwkIdx, jjBtag_sfIdx, self.jet2_fwkIdx, jjBtag_strCommon)

        # PU WEIGHT
        puWeight = "event_pu_weight"
        if systematic == "puup":
            puWeight = "event_pu_weight_up"
        if systematic == "pudown":
            puWeight = "event_pu_weight_down"

        # PDF weight
        pdfWeight = ""
        normalization = "nominal"
        if systematic == "pdfup" : # do not change the name of "pdfup", use latter for the proper normalization
            pdfWeight = "event_pdf_weight_up"
            normalization = "pdf_up"
        if systematic == "pdfdown":
            pdfWeight = "event_pdf_weight_down"
            normalization = "pdf_down"

        # TRIGGER EFFICIENCY
        trigEff = "({0}.trigger_efficiency)".format(self.baseObject)
        if systematic == "trigeffup":
            trigEff = "({0}.trigger_efficiency_upVariated)".format(self.baseObject)
        if systematic == "trigeffdown":
            trigEff = "({0}.trigger_efficiency_downVariated)".format(self.baseObject)
        # Include dZ filter efficiency for ee and mumu
        trigEff += "*(({0}.isElEl && runOnMC) ? 0.995 : 1)".format(self.baseObject)
        trigEff += "*(({0}.isMuMu && runOnMC) ? 0.95 : 1)".format(self.baseObject)

        # Append the proper extension to the name plot if needed (scale name are down at the end of the code)
        self.systematicString = ""
        if not systematic == "nominal" and not "scale" in systematic:
            self.systematicString = "__" + systematic

        available_weights = {'trigeff' : trigEff, 'jjbtag' : jjBtag_sf, 'llidiso' : llIdIso_sf, 'pu' : puWeight}

        #########
        # PLOTS #
        #########
        self.basic_plot = []
        self.csv_plot = []
        
        # HH stuff
        self.bdtinput_plot = []
        self.cleancut_plot = []
        self.drllcut_plot = []
        self.drjjcut_plot = []
        self.dphilljjcut_plot = []
        self.isElEl_plot = []
        self.bdtoutput_plot = []
        self.mjj_vs_bdt_plot = []

        self.mll_plot = []
        self.mjj_plot = []

        self.flavour_plot = []
        # MEM stuff
        self.jet_tf_plot = []
        self.mu_tf_plot = []
        self.el_tf_plot = []
        self.momemta_weights_skimmer_plot = []
        self.momemta_weights_plot = []
        
        #MIS stuff 
        self.mis_plot = []

        self.llidisoWeight_plot = []
        self.mumuidisoWeight_plot = []
        self.elelidisoWeight_plot = []
        self.jjbtagWeight_plot = []
        self.trigeffWeight_plot = []
        self.puWeight_plot = []
        self.scaleWeight_plot = []
        self.pdfWeight_plot = []
        self.gen_plot = []
        self.evt_plot = []

        self.other_plot = []
        self.vertex_plot = []
        self.ht_plot = []


        self.forSkimmer_plot = []

        # Protect against the fact that data do not have jecup collections, in the nominal case we still have to check that data have one candidate
        sanityCheck = self.sanityCheck
        if systematic != "nominal":
            sanityCheck = self.joinCuts("!event_is_data", self.sanityCheck)
        # Trigger matching for data
        trigerMatching = "(!(%s.hlt_idx == -1 || %s.hlt_idx == -1) || !event_is_data)"%(self.lep1_str, self.lep2_str)
        

        for cat in categories:

            catCut = self.dict_cat_cut[cat]
            self.totalCut_noFlavour = self.joinCuts(sanityCheck, extraCut, dict_stage_cut[stage], trigerMatching)
            self.totalCut = self.joinCuts(sanityCheck, catCut, extraCut, dict_stage_cut[stage], trigerMatching)
            self.llFlav = cat
            self.extraString = stage + extraString

            self.mll_plot.append({
                        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 10, 250)'
                })
            self.mjj_plot.append({
                        'name': 'jj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str+".M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 10, 410)'
                })
            
            # Plot to compute yields (ensure we have not over/under flow)
            self.isElEl_plot.append({
                        'name': 'isElEl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "%s.isElEl"%self.baseObject,
                        'plot_cut': self.totalCut,
                        'binning': '(2, 0, 2)'
                })
            
            # BDT output plots
            for bdtName in bdtNames:
                bdtRange = (-0.6, 0.6) # default BDT range
                # Special BDT ranges
                if "BDT_SM" in bdtName: bdtRange = (-0.5, 0.5)
                if "BDT_2" in bdtName: bdtRange = (-0.5, 0.6)

                self.bdtoutput_plot.append({
                        'name': 'MVA_%s_%s_%s_%s%s' % (bdtName, self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': BDToutputsVariable[bdtName],
                        'plot_cut': self.totalCut,
                        'binning': '(50, {}, {})'.format(bdtRange[0], bdtRange[1])
                })
                
            # Weight Plots
            self.jjbtagWeight_plot.append(
                        {'name': 'jjbtag_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["jjbtag"],
                        'plot_cut': self.totalCut, 'binning':'(100, 0, 1.5)', 'weight': 'event_weight'})
            self.llidisoWeight_plot.append(
                        {'name': 'llidiso_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["llidiso"],
                        'plot_cut': self.totalCut, 'binning': '(50, 0.7, 1.3)', 'weight': 'event_weight'})
            self.llidisoWeight_plot.append(
                        {'name': 'mumuidiso_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["llidiso"],
                        'plot_cut': self.joinCuts(self.totalCut, "%s.isMuMu" % self.baseObject), 'binning': '(50, 0.7, 1.3)', 'weight': 'event_weight'})
            self.llidisoWeight_plot.append(
                        {'name': 'elelidiso_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["llidiso"],
                        'plot_cut': self.joinCuts(self.totalCut, "%s.isElEl" % self.baseObject), 'binning': '(50, 0.7, 1.3)', 'weight': 'event_weight'})
            self.trigeffWeight_plot.append(
                        {'name': 'trigeff_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["trigeff"],
                        'plot_cut': self.totalCut, 'binning': '(50, 0, 1.2)', 'weight': 'event_weight'})
            self.puWeight_plot.append(
                        {'name': 'pu_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': available_weights["pu"],
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 4)', 'weight': 'event_weight'})
            self.scaleWeight_plot.extend([
                        {'name': 'scale0_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[0])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'},
                        {'name': 'scale1_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[1])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'},
                        {'name': 'scale2_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[2])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'},
                        {'name': 'scale3_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[3])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'},
                        {'name': 'scale4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[4])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'},
                        {'name': 'scale5_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString,  self.systematicString), 'variable': "std::abs(event_scale_weights[5])",
                        'plot_cut': self.totalCut, 'binning': '(100, 0, 2)', 'weight': 'event_weight'}])
                    
            # BASIC PLOTS
            self.basic_plot.extend([
                {
                        'name': 'lep1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 15, 400)'
                },
                {
                        'name': 'lep2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 10, 200)'
                },
                {
                        'name': 'jet1_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 20, 400)'
                },
                {
                        'name': 'jet2_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 20, 300)'
                },
                {
                        'name': 'met_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "%s.Pt()"%self.met_str,
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 450)'
                }
            ])
            self.csv_plot.extend([
                {
                        'name': 'jet1_CSV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".CSV",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 1)'
                },
                {
                        'name': 'jet2_CSV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".CSV",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 1)'
                }
            ])
            self.cleancut_plot.extend([
                #{
                #        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': self.ll_str+".M()",
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0, 250)'
                #},
                {
                        'name': 'll_DR_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_l_l",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'jj_DR_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_j_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'llmetjj_DPhi_ll_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_ll_jj)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                }
            ])
            self.drllcut_plot.append(
                {
                        'name': 'll_DR_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_l_l",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                })
            self.drjjcut_plot.append(
                {
                        'name': 'jj_DR_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_j_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                })
            self.dphilljjcut_plot.append(
                {
                        'name': 'llmetjj_DPhi_ll_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_ll_jj)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                })

            self.bdtinput_plot.extend([
                {
                        'name': 'll_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 10, 250)'
                },
                {
                        'name': 'll_DR_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_l_l",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'jj_DR_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_j_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'llmetjj_DPhi_ll_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_ll_jj)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                },
                {
                        'name': 'll_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.ll_str+".Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 450)'
                },
                {
                        'name': 'jj_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jj_str+".Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 450)'
                },
                {
                        'name': 'llmetjj_minDR_l_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".minDR_l_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 5)'
                },
                {
                        'name': 'llmetjj_MTformula_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".MT_formula", # std::sqrt(2 * ll[ill].p4.Pt() * met[imet].p4.Pt() * (1-std::cos(dphi)));
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 500)'
                },
                {
                        'name': 'llmetjj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 100, 1500)'
                },
                {
                        'name': 'cosThetaStar_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject + ".cosThetaStar_CS",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 1)'
                },
            ])

            self.other_plot.extend([
                {
                    'name': 'lep1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep1_str+".p4.Eta()",
                    'plot_cut': self.totalCut,
                    'binning': '(25, -2.5, 2.5)'
                },
                {
                    'name': 'lep1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep1_str+".p4.Phi()",
                    'plot_cut': self.totalCut,
                    'binning': '(25, -3.1416, 3.1416)'
                },
                {
                    'name': 'lep1_charge_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep1_str+".charge",
                    'plot_cut': self.totalCut,
                    'binning': '(4, -2, 2)'
                },
                #{
                #    'name': 'lep1_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #    'variable': get_lepton_SF(self.lep1_str, self.lepid1, self.lepiso1, "nominal"),
                #    'plot_cut': self.totalCut,
                #    'binning': '(50, 0.8, 1.2)'
                #},
                {
                    'name': 'lep1_Iso_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "({0}.isEl) ? electron_relativeIsoR03_withEA[{1}] : muon_relativeIsoR04_deltaBeta[{1}]".format(self.lep1_str, self.lep1_fwkIdx),
                    'plot_cut': self.totalCut,
                    'binning': '(50, 0, 0.4)'
                },
                {
                    'name': 'lep2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep2_str+".p4.Eta()",
                    'plot_cut': self.totalCut,
                    'binning': '(25, -2.5, 2.5)'
                },
                {
                    'name': 'lep2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep2_str+".p4.Phi()",
                    'plot_cut': self.totalCut,
                    'binning': '(25, -3.1416, 3.1416)'
                },
                {
                    'name': 'lep2_charge_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': self.lep2_str+".charge",
                    'plot_cut': self.totalCut,
                    'binning': '(4, -2, 2)'
                },
                #{
                #    'name': 'lep2_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #    'variable': get_lepton_SF(self.lep2_str, self.lepid2, self.lepiso2, "nominal"),
                #    'plot_cut': self.totalCut,
                #    'binning': '(50, 0.8, 1.2)'
                #},
                {
                        'name': 'lep2_Iso_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "({0}.isEl) ? electron_relativeIsoR03_withEA[{1}] : muon_relativeIsoR04_deltaBeta[{1}]".format(self.lep2_str, self.lep2_fwkIdx),
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 0.4)'
                },
                {
                        'name': 'jet1_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(25, -2.5, 2.5)'
                },
                {
                        'name': 'jet1_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(25, -3.1416, 3.1416)'
                },
                {
                        'name': 'jet1_JP_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".JP",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.5)'
                },
                {
                        'name': 'jet2_eta_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Eta()",
                        'plot_cut': self.totalCut,
                        'binning': '(25, -2.5, 2.5)'
                },
                {
                        'name': 'jet2_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(25, -3.1416, 3.1416)'
                },
                {
                        'name': 'jet2_JP_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".JP",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.5)'
                },
                #{
                #        'name': 'jet1_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': get_csvv2_sf(self.btagWP1, self.jet1_fwkIdx),
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0.5, 1.5)'
                #},
                #{
                #        'name': 'jet2_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': get_csvv2_sf(self.btagWP2, self.jet2_fwkIdx),
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0.5, 1.5)'
                #}
                {
                        'name': 'met_phi_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "met_p4.Phi()",
                        'plot_cut': self.totalCut,
                        'binning': '(25, -3.1416, 3.1416)'
                },
                {
                        'name': 'll_DPhi_l_l_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_l_l)",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                #{
                #        'name': 'll_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': get_leptons_SF(self.ll_str, self.lepid1, self.lepid2, self.lepiso1, self.lepiso2, "nominal"),
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0.8, 1.2)'
                #}
                {
                        'name': 'jj_DPhi_j_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_j_j)",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'jj_CSVprod_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".CSV * " + self.jet2_str+".CSV",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 1)'
                },
                {
                        'name': 'jj_CSVsum_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".CSV + " + self.jet2_str+".CSV",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 2)'
                },
                #{
                #        'name': 'jj_scaleFactor_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': "{0} * {1}".format(get_csvv2_sf(self.btagWP1, self.jet1_fwkIdx), get_csvv2_sf(self.btagWP2, self.jet2_fwkIdx)),
                #        'plot_cut': self.totalCut,
                #        'binning': '(50, 0.5, 1.5)'
                #} 
                #{
                #        'name': 'llmetjj_n_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                #        'variable': "Length$(%s)"%self.mapIndices,
                #        'plot_cut': self.totalCut,
                #        'binning': '(18, 0, 18)'
                #},
                {
                        'name': 'llmetjj_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 250)'
                },
                {
                        'name': 'llmetjj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".p4.M()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 1000)'
                },
                {
                        'name': 'llmetjj_DPhi_ll_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_ll_met)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_minDPhi_l_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".minDPhi_l_met",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_maxDPhi_l_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".maxDPhi_l_met",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_MT_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".MT", # ll[ill].p4 + met[imet].p4).M()
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 600)'
                },
                {
                        'name': 'llmetjj_projMET_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".projectedMet)",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 400)'
                },
                {
                        'name': 'llmetjj_DPhi_jj_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_jj_met)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_minDPhi_j_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".minDPhi_j_met",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_maxDPhi_j_met_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".maxDPhi_j_met",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_maxDR_l_j_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".maxDR_l_j",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'llmetjj_DR_ll_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_ll_jj",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'llmetjj_DR_llmet_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".DR_llmet_jj",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 6)'
                },
                {
                        'name': 'llmetjj_DPhi_llmet_jj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".DPhi_llmet_jj)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 3.1416)'
                },
                {
                        'name': 'llmetjj_cosThetaStar_CS_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "abs("+self.baseObject+".cosThetaStar_CS)",
                        'plot_cut': self.totalCut,
                        'binning': '(25, 0, 1)'
                },
                {
                        'name': 'lljj_pt_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".lljj_p4.Pt()",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 0, 500)'
                },
                {
                        'name': 'lljj_M_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.baseObject+".lljj_p4.M()",
                        'plot_cut': self.totalCut,
                        'binning': '(75, 0, 1000)'
                }
            ])
            # gen level plots for jj 
            #for elt in self.plots_jj:
            #    tempPlot = copy.deepcopy(elt)
            #    if "p4" in tempPlot["variable"]:
            #        tempPlot["variable"] = tempPlot["variable"].replace(self.jj_str,"hh_gen_BB")
            #        tempPlot["name"] = "gen"+tempPlot["name"]
            #        self.plots_gen.append(tempPlot)
            self.gen_plot.extend([
                {
                    'name': 'gen_mHH',
                    'variable': 'hh_gen_mHH',
                    'plot_cut': self.totalCut,
                    'binning': '(50, 0, 1200)'
                },
                {
                    'name': 'gen_costhetastar',
                    'variable': 'hh_gen_costhetastar',
                    'plot_cut': self.totalCut,
                    'binning': '(50, -1, 1)'
                },
            ])
            self.evt_plot.extend([ 
                {
                    'name': 'nLeptonsHWW_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nLeptonsHWW",
                    'plot_cut': self.totalCut,
                    'binning': '(6, 0, 6)'
                },
                {
                    'name': 'nMuonsHWW_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nMuonsHWW",
                    'plot_cut': self.totalCut,
                    'binning': '(4, 0, 4)'
                },
                {
                    'name': 'nElectronsHWW_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nElectronsHWW",
                    'plot_cut': self.totalCut,
                    'binning': '(4, 0, 4)'
                },
                {
                    'name': 'nJetsL_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nJetsL",
                    'plot_cut': self.totalCut,
                    'binning': '(10, 0, 10)'
                },
                {
                    'name': 'nJetsT_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nJetsT",
                    'plot_cut': self.totalCut,
                    'binning': '(10, 0, 10)'
                },
                {
                    'name': 'nBJetsL_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nBJetsL",
                    'plot_cut': self.totalCut,
                    'binning': '(6, 0, 6)'
                },
                {
                    'name': 'nBJetsM_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nBJetsM",
                    'plot_cut': self.totalCut,
                    'binning': '(6, 0, 6)'
                },
                {
                    'name': 'nBJetsT_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "hh_nBJetsT",
                    'plot_cut': self.totalCut,
                    'binning': '(6, 0, 6)'
                }
                ])
#                {
#                    'name': 'nLepAll_%s_jetID_%s_btag_%s%s'%(self.llFlav, self.jjIDCat, self.jjBtagCat, self.suffix),
#                    'variable': "hh_nLeptons",
#                    'plot_cut': self.totalCut,
#                    'binning': '(5, 2, 7)'
#                },
#                {
#                    'name': 'nElAll_%s_jetID_%s_btag_%s%s'%(self.llFlav, self.jjIDCat, self.jjBtagCat, self.suffix),
#                    'variable': "hh_nElectrons",
#                    'plot_cut': self.totalCut,
#                    'binning': '(6, 0, 6)'
#                },
#                {
#                    'name': 'nMuAll_%s_jetID_%s_btag_%s%s'%(self.llFlav, self.jjIDCat, self.jjBtagCat, self.suffix),
#                    'variable': "hh_nMuons",
#                    'plot_cut': self.totalCut,
#                    'binning': '(6, 0, 6)'
#                },
#                {
#                    'name': 'nJet_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
#                    'variable': "Length$(%s)"%self.jetMapIndices,
#                    'plot_cut': self.totalCut,
#                    'binning': '(5, 2, 7)'
#                },
#                {
#                    'name': 'nJetAll_%s_jetID_%s_btag_%s%s'%(self.llFlav, self.jjIDCat, self.jjBtagCat, self.suffix),
#                    'variable': "hh_nJets",
#                    'plot_cut': self.totalCut,
#                    'binning': '(10, 2, 12)'
#                },
#                {
#                    'name': 'nBJetLooseCSV_%s_jetID_%s_btag_%s%s'%(self.llFlav, self.jjIDCat, self.jjBtagCat, self.suffix),
#                    'variable': "hh_nBJetsL",
#                    'plot_cut': self.totalCut,
#                    'binning': '(6, 0, 6)'
#                }
#            ])
            self.flavour_plot.extend([
                {
                    'name': 'gen_bb_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_bb"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_bl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_bl"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_bc_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_bc"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_cc_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_cc"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_cl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_cl"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_ll_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.gen_ll"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_bx_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "({0}.gen_bl || {0}.gen_bc)".format(self.baseObject),
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'gen_xx_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "({0}.gen_ll || {0}.gen_cc || {0}.gen_cl)".format(self.baseObject),
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
            ])
            self.jet_tf_plot.extend([
                {     
                    'name': 'tf_bjet1_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet1_str),
                    'binning': '(' + bjet_nBinsX + ', ' + bjet_binningX + ', ' + bjet_nBinsY + ', ' + bjet_binningY + ')',
                },
                {
                    'name': 'tf_bjet1_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.jet1_str)),
                    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                },
                {
                    'name': 'tf_bjet1_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.jet1_str)),
                    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                },
                {     
                    'name': 'tf_bjet2_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet2_str),
                    'binning': '(' + bjet_nBinsX + ', ' + bjet_binningX + ', ' + bjet_nBinsY + ', ' + bjet_binningY + ')',
                },
                {
                    'name': 'tf_bjet2_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.jet2_str)),
                    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                },
                {
                    'name': 'tf_bjet2_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.jet2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.jet2_str)),
                    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                },
                #{     
                #    'name': 'tf_bjet1_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet1_str),
                #    'binning': '(' + bjet_nBinsX + ', ' + bjet_binningX + ', ' + bjet_nBinsY + ', ' + bjet_binningY + ')',
                #},
                #{
                #    'name': 'tf_bjet1_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.jet1_str)),
                #    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                #},
                #{
                #    'name': 'tf_bjet1_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.jet1_str)),
                #    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                #},
                #{     
                #    'name': 'tf_bjet2_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet2_str),
                #    'binning': '(' + bjet_nBinsX + ', ' + bjet_binningX + ', ' + bjet_nBinsY + ', ' + bjet_binningY + ')',
                #},
                #{
                #    'name': 'tf_bjet2_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.jet2_str)),
                #    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                #},
                #{
                #    'name': 'tf_bjet2_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.jet2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.2'%self.jet2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.jet2_str)),
                #    'binning': '(' + bjet_BA_nBinsX + ', ' + bjet_BA_binningX + ', ' + bjet_BA_nBinsY + ', ' + bjet_BA_binningY + ')',
                #},
            ])
            self.mu_tf_plot.extend([
                {     
                    'name': 'tf_mu1_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isMu'%self.lep1_str),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                {     
                    'name': 'tf_mu1_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isMu'%self.lep1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep1_str)),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                {     
                    'name': 'tf_mu1_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isMu'%self.lep1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep1_str)),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                {     
                    'name': 'tf_mu2_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isMu'%self.lep2_str),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                {     
                    'name': 'tf_mu2_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isMu'%self.lep2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep2_str)),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                {     
                    'name': 'tf_mu2_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isMu'%self.lep2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep2_str)),
                    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                },
                #{     
                #    'name': 'tf_mu1_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isMu'%self.lep1_str),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
                #{     
                #    'name': 'tf_mu1_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isMu'%self.lep1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep1_str)),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
                #{     
                #    'name': 'tf_mu1_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isMu'%self.lep1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep1_str)),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
                #{     
                #    'name': 'tf_mu2_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isMu'%self.lep2_str),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
                #{     
                #    'name': 'tf_mu2_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isMu'%self.lep2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep2_str)),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
                #{     
                #    'name': 'tf_mu2_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isMu'%self.lep2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep2_str)),
                #    'binning': '(' + mu_nBinsX + ', ' + mu_binningX + ', ' + mu_nBinsY + ', ' + mu_binningY + ')',
                #},
            ])
            self.el_tf_plot.extend([
                {     
                    'name': 'tf_el1_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isEl'%self.lep1_str),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                {     
                    'name': 'tf_el1_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isEl'%self.lep1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep1_str)),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                {     
                    'name': 'tf_el1_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep1_str, '%s.isEl'%self.lep1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep1_str)),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                {     
                    'name': 'tf_el2_matchedToAfterFSR_allEta_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isEl'%self.lep2_str),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                {     
                    'name': 'tf_el2_matchedToAfterFSR_barrel_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isEl'%self.lep2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep2_str)),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                {     
                    'name': 'tf_el2_matchedToAfterFSR_endcap_%s'%self.suffix,
                    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_matched'%self.lep2_str, '%s.isEl'%self.lep2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep2_str)),
                    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                },
                #{     
                #    'name': 'tf_el1_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isEl'%self.lep1_str),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
                #{     
                #    'name': 'tf_el1_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isEl'%self.lep1_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep1_str)),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
                #{     
                #    'name': 'tf_el1_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep1_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep1_str, '%s.isEl'%self.lep1_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep1_str)),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
                #{     
                #    'name': 'tf_el2_matchedToBeforeFSR_allEta',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isEl'%self.lep2_str),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
                #{     
                #    'name': 'tf_el2_matchedToBeforeFSR_barrel',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isEl'%self.lep2_str, 'abs({0}.p4.Eta()) <= 1.3'.format(self.lep2_str)),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
                #{     
                #    'name': 'tf_el2_matchedToBeforeFSR_endcap',
                #    'variable': '{0}.tt_parton_p4.E() ::: {0}.p4.E() - {0}.tt_parton_p4.E()'.format(self.lep2_str),
                #    'plot_cut': self.joinCuts(self.totalCut, '%s.tt_parton_DR < 0.1'%self.lep2_str, '%s.isEl'%self.lep2_str, 'abs({0}.p4.Eta()) > 1.3'.format(self.lep2_str)),
                #    'binning': '(' + el_nBinsX + ', ' + el_binningX + ', ' + el_nBinsY + ', ' + el_binningY + ')',
                #},
            ])
            ############
            # WARNING : do not put *W*eight in the plot family name, otherwise no reweighting will be applied, *w*eight is ok
            ###########
            def generateWeightPlot(name):
                return [
                        {
                        'name': name+'_minLog_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "-log10({0}_weights.at(0).first)".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(80, 10, 40)'
                        }, 
                        {
                        'name': name+'_minLog_weight_up_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "-log10({0}_weights.at(0).first + {0}_weights.at(0).second)".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(80, 10, 40)'
                        }, 
                        {
                        'name': name+'_minLog_weight_down_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "-log10({0}_weights.at(0).first - {0}_weights.at(0).second)".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(80, 10, 40)'
                        }, 
                        {
                        'name': name+'_weightRelError_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "{0}_weights.at(0).second / {0}_weights.at(0).first".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(100, 0, 1)'
                        },
                        {
                        'name': name+'_IntegStatus_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "{0}_integStatus".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(2, 0, 2)'
                        },
                        {
                        'name': name+'_time_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "{0}_time".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(90, 0, 3)'
                        },
                        ]
            def generateWeightPlot_skimmer(name):
                return [
                        {
                        'name': name+'_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "{0}_weights.at(0).first".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(80, 0, 1)'
                        },
                        {
                        'name': name+'_weightError_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "{0}_weights.at(0).second".format(name),
                        'plot_cut': self.totalCut,
                        'binning': '(80, 10, 40)'
                        }
                        ]
            self.momemta_weights_plot.extend(generateWeightPlot('pp_Z_llbb_simple_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('pp_Z_llbb_simple_tfJetAllEta'))
            self.momemta_weights_plot.extend(generateWeightPlot('pp_zz_llbb_simple_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('pp_zh_llbb_simple_tfJetAllEta'))
            self.momemta_weights_plot.extend(generateWeightPlot('pp_zh_llbb_simple_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('pp_zz_llbb_simple_tfJetAllEta'))
            self.momemta_weights_plot.extend(generateWeightPlot('pp_tt_llbb_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('pp_tt_llbb_tfJetAllEta'))
            self.momemta_weights_plot.extend(generateWeightPlot('twminus_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('twminus_tfJetAllEta'))
            self.momemta_weights_plot.extend(generateWeightPlot('twplus_tfJetAllEta'))
            self.momemta_weights_skimmer_plot.extend(generateWeightPlot_skimmer('twplus_tfJetAllEta'))
            self.mis_plot.extend([
                        {
                        'name': 'nExtraJet_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "Length$(%s.iExtraJets)"%self.baseObject,
                        'plot_cut': self.totalCut,
                        'binning': '(10, 0, 10)'
                        },
                        #{
                        #'name': 'M_j_j_extraj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        #'variable': "%s.M_j_j_extraj[0]"%self.baseObject,
                        #'plot_cut': self.joinCuts(self.totalCut, "Length$(%s.iExtraJets) > 0"),
                        #'binning': '(80, 0, 800)'
                        #},
                        #{
                        #'name': 'min_DR_j_extraj_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        #'variable': "%s.min_DR_j_extraj[0]"%self.baseObject,
                        #'plot_cut': self.joinCuts(self.totalCut, "Length$(%s.iExtraJets) > 0"),
                        #'binning': '(25, 0, 4)'
                        #}
                ])

            self.vertex_plot.append({
                        'name': 'nPV_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "vertex_n",
                        'plot_cut': self.totalCut,
                        'binning': '(40, 0, 40)'
                })
            self.ht_plot.append({
                        'name': 'ht_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': "event_ht",
                        'plot_cut': self.totalCut,
                        'binning': '(100, 0, 800)'
                })
            self.forSkimmer_plot.extend([
                {
                        'name': 'lep1_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep1_str+".p4",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 15, 400)'
                },
                {
                        'name': 'lep2_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.lep2_str+".p4",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 15, 400)'
                },
                {
                        'name': 'jet1_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet1_str+".p4",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 15, 400)'
                },
                {
                        'name': 'jet2_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                        'variable': self.jet2_str+".p4",
                        'plot_cut': self.totalCut,
                        'binning': '(50, 15, 400)'
                },
                {
                'name': 'extraJet_p4_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                'variable': self.extrajet_str+".p4",
                'plot_cut': self.joinCuts(self.totalCut, self.extrajet_cut),
                'binning': '(10, 0, 10)'
                },
                {
                    'name': 'event_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "event_weight",
                    'plot_cut': self.totalCut,
                    'binning': '(500, -10000, 10000)'
                },
                {
                    'name': 'total_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "event_weight * (%s) * (%s) * (%s) * (%s)"%(available_weights["jjbtag"], available_weights["llidiso"], available_weights["pu"], available_weights["trigeff"]),
                    'plot_cut': self.totalCut,
                    'binning': '(5, -2, 2)'
                },
                {
                    'name': 'event_pu_weight_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "event_pu_weight",
                    'plot_cut': self.totalCut,
                    'binning': '(50, 0, 6)'
                },
                {
                    'name': 'isElEl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.isElEl"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'isMuMu_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.isMuMu"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'isElMu_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.isElMu"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'isMuEl_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "%s.isMuEl"%self.baseObject,
                    'plot_cut': self.totalCut,
                    'binning': '(2, 0, 2)'
                },
                {
                    'name': 'event_number_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "event_event",
                    'plot_cut': self.totalCut,
                    'binning': '(300, 0, 300000)'
                },
                {
                    'name': 'event_run_%s_%s_%s%s'%(self.llFlav, self.suffix, self.extraString, self.systematicString),
                    'variable': "event_run",
                    'plot_cut': self.totalCut,
                    'binning': '(300, 0, 300000)'
                }
            ])

        plotsToReturn = []
        
        for plotFamily in requested_plots:
            
            if "scale" in systematic:
                
                scaleIndices = ["0", "1", "2", "3", "4", "5"]
                
                for scaleIndice in scaleIndices:
                    
                    scaleWeight = "event_scale_weights[%s]" % scaleIndice
                    
                    for plot in getattr(self, plotFamily+"_plot"):
                        tempPlot = copy.deepcopy(plot)
                        # Two different ways to normalise the variations
                        if "Uncorr" not in systematic:
                            tempPlot["normalize-to"] = "scale_%s" % scaleIndice
                        tempPlot["name"] += "__" + systematic + scaleIndice
                        if not "Weight" in plotFamily:
                            tempPlot["weight"] = "event_weight" + " * " + scaleWeight
                            for weight in weights:
                                tempPlot["weight"] += " * " + available_weights[weight]
                        else:
                            print "No other weight than event_weight for ", plotFamily 
                        plotsToReturn.append(tempPlot)
            
            elif "pdf" in systematic:
                
                for plot in getattr(self, plotFamily+"_plot"):
                    if not "Weight" in plotFamily:
                        plot["weight"] = "event_weight" + " * " + pdfWeight
                        plot["normalize-to"] = normalization
                        for weight in weights:
                            plot["weight"] += " * " + available_weights[weight]
                    else:
                        print "No other weight than event_weight for ", plotFamily 
                    plotsToReturn.append(plot)
            
            else:
                
                for plot in getattr(self, plotFamily+"_plot"):
                    if not "Weight" in plotFamily:
                        plot["weight"] = "event_weight"
                        plot["normalize-to"] = normalization
                        for weight in weights:
                            plot["weight"] += " * " + available_weights[weight]
                    else:
                        print "No other weight than event_weight for ", plotFamily 
                    plotsToReturn.append(plot)

        return plotsToReturn


    def joinCuts(self, *cuts):
        if len(cuts) == 0:
            return ""
        elif len(cuts) == 1:
            return cuts[0]
        else:
            totalCut = "("
            for cut in cuts:
                cut = cut.strip().strip("&")
                if cut == "":
                    continue
                totalCut += "(" + cut + ")&&" 
            totalCut = totalCut.strip("&") + ")"
            return totalCut

