# Warning: put most recent tags first!
analysis_tags = [ # on which samples do you want ot run
        'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3',
        #'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3skim_addWeight_v1',
        #'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3_skim_addWeight_v2',
        #'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3_flatTrees_with_weight_v2_jecup'
        ]
analysis_tags_for_evt_perJob = [
        #'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3skim_addWeight_v1',
        'v0.1.5+76X_HHAnalysis_v1.0+765_MISearch_2016-08-10.v3',
        ]

Samples = []
SamplesToSplitMore = []
SamplesToSplitAbitMore = []

# NB the Fall15 is not mandatory

# Data
Samples.extend([
    'DoubleEG', # DoubleEG
    'MuonEG', # MuonEG
    'DoubleMuon', # DoubleMuon
    ])

# Main backgrounds:
Samples.extend([
    'ST_tW_top_5f_inclusiveDecays_13TeV-powheg', # tW top
    'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg', # tW atop
    'ST_t-channel_4f_leptonDecays_13TeV-amcatnlo', # sT t-chan
    'TT_TuneCUETP8M1_13TeV-powheg-pythia8', # TT incl NLO
    'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext3', # DY M10-50 NLO merged
    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_extended_ext0_plus_ext1_plus_ext4', # DY M-50 NLO merged 
   ])

# DY LO
Samples.extend([
    # M-50 incl. merged
    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    # M-50, binned HT > 100
    'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1',
    'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1',
    # M-5to50 incl.: forget it...
    'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    # M-5to50, binned HT
    'DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_Fall15MiniAODv2',
    'DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    'DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Fall15MiniAODv2',
    'DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_extended_ext0_plus_ext1',
    ])
#
# Other backgrounds
# VV
Samples.extend([
    #'VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8', # VV(2L2Nu)
    
    'WWToLNuQQ_13TeV-powheg', # WW(LNuQQ)
    'WWTo2L2Nu_13TeV-powheg', # WW(2L2Nu)
    
    'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8', # WZ(3LNu)
    'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8', # WZ(L3Nu)
    'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8', # WZ(LNu2Q)
    'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8', # WZ(2L2Q)
    
    'ZZTo4L_13TeV_powheg_pythia8', # ZZ(4L)
    'ZZTo2L2Nu_13TeV_powheg_pythia8', # ZZ(2L2Nu)
    'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8', # ZZ(2L2Q)
    
    'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8', # WZZ
    ])

# Higgs
Samples.extend([
    # ggH ==> no H(ZZ)?
    'GluGluHToWWTo2L2Nu_M125_13TeV_powheg_JHUgen_pythia8', # H(WW(2L2Nu))
    'GluGluHToBB_M125_13TeV_powheg_pythia8', # H(BB)

    # ZH
    'GluGluZH_HToWWTo2L2Nu_ZTo2L_M125_13TeV_powheg_pythia8', # ggZ(LL)H(WW(2L2Nu))
    'HZJ_HToWW_M125_13TeV_powheg_pythia8', # ZH(WW)
    'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8', # ggZ(LL)H(BB)
    'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8', # Z(LL)H(BB)
    'ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8', # ggZ(NuNu)H(BB)
    
    # VBF
    'VBFHToBB_M-125_13TeV_powheg_pythia8', # VBFH(BB)
    'VBFHToWWTo2L2Nu_M125_13TeV_powheg_JHUgen_pythia8', # VBFH(WW(2L2Nu))

    # WH
    'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8', # W+(LNu)H(BB)
    'WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8', # W-(LNu)H(BB)
    'HWplusJ_HToWW_M125_13TeV_powheg_pythia8', # W+H(WW)
    'HWminusJ_HToWW_M125_13TeV_powheg_pythia8', # W-H(WW)

    # bbH
    'bbHToBB_M-125_4FS_ybyt_13TeV_amcatnlo', # bbH(BB) ybyt
    'bbHToBB_M-125_4FS_yb2_13TeV_amcatnlo', # bbH(BB) yb2
    ])

# Top
Samples.extend([
    'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo', # sT s-channel
    'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8', # TTW(LNu)
    'TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8', # TTW(QQ)
    'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8', # TTZ(2L2Nu)
    'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8', # TTZ(QQ),
    'ttHTobb_M125_13TeV_powheg_pythia8', # ttH(bb)
    'ttHToNonbb_M125_13TeV_powheg_pythia8', # ttH(nonbb)
    'TTTo2L2Nu_13TeV-powheg', # TT(2L2Nu)
    ])

# # TT aMC@NLO
# Samples.append('TTJets_TuneCUETP8M1_amcatnloFXFX')

# Wjets
Samples.extend([
    'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', # JetsLNu
    ])

# MIS signals
Samples.extend([
    'GluGluToHHTo2B2VTo2L2Nu_node_SM_13TeV-madgraph', # SM
    'GluGluToHHTo2B2VTo2L2Nu_node_box_13TeV-madgraph', # box
    'GluGluToHHTo2B2VTo2L2Nu_node_2_13TeV-madgraph', 
    'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTbarDMJets_scalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTbarDMJets_scalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTbarDMJets_scalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'HToZATo2L2B_MH-200_MA-50_13TeV-madgraph',
    'HToZATo2L2B_MH-3000_MA-2000_13TeV-madgraph',
    'HToZATo2L2B_MH-500_MA-300_13TeV-madgraph',
    'HToZATo2L2B_MH-800_MA-700_13TeV-madgraph',
    'SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'SMS-T2tt_mStop-850_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-900_narrow',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-400_narrow',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-650_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow',
    ])
# Which one have to be splitted more (use it if most event pass the selection):
SamplesToSplitMore.extend([
    'GluGluToHHTo2B2VTo2L2Nu_node_SM_13TeV-madgraph',
    'GluGluToHHTo2B2VTo2L2Nu_node_box_13TeV-madgraph',
    'GluGluToHHTo2B2VTo2L2Nu_node_2_13TeV-madgraph',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-900_narrow',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-400_narrow',
    'GluGluToRadionToHHTo2B2VTo2L2Nu_M-650_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-650_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-900_narrow',
    #'GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-400_narrow',
    'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Fall15MiniAODv2',
    'ttHToNonbb_M125_13TeV_powheg_pythia8',
    'ttHTobb_M125_13TeV_powheg_pythia8',
    'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
    'TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_Fall15MiniAODv2',
    'SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'SMS-T2tt_mStop-850_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'TTTo2L2Nu_13TeV-powheg',
    ])
# Which one are in between
SamplesToSplitAbitMore.extend([
    'TT_TuneCUETP8M1_13TeV-powheg-pythia8',
])
