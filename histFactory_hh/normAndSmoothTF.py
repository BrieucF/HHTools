#! /usr/bin/env python

import ROOT as R
import argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='Build transfer functions out of 2D histogram created by plotter.')
    parser.add_argument('-i', '--input', type=str, dest='input', default='/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/HHTools/histFactory_hh/tf_genCut0_noRecoCut_lljjorbb_Oct18/condor/output/allTT.root', help='Input file')
    parser.add_argument('-o', '--output', type=str, dest='output', default='/home/fynu/bfrancois/scratch/framework/MIS_prod_data/CMSSW_7_6_5/src/cp3_llbb/HHTools/histFactory_hh/tf_genCut0_noRecoCut_lljjorbb_Oct18/condor/output/allTT_smoothed_notPutToZero.root', help='Output file')
    return parser.parse_args()

def normalizeDeltaE(hist):
    xAxis = hist.GetXaxis()
    yAxis = hist.GetYaxis()

    for i in range(1, xAxis.GetNbins()+1):
        binWidths = []
        for j in range(1, yAxis.GetNbins()+1):
            width = yAxis.GetBinWidth(j)
            if width not in binWidths:
                binWidths.append(width)

        binWidths.sort()
        minWidth = binWidths[0]

        for j in range(1, yAxis.GetNbins()+1):
            oldContent = hist.GetBinContent(i, j)
            widthRatio = yAxis.GetBinWidth(j)/minWidth
            hist.SetBinContent(i, j, oldContent/widthRatio)

    hist.Smooth(1)
    hist.Smooth(1)
    
    for i in range(1, xAxis.GetNbins()+1):
        
        #for j in range(1, yAxis.GetNbins()+1):
            #if xAxis.GetBinUpEdge(i) + yAxis.GetBinUpEdge(j) < 30:
            #    hist.SetBinContent(i, j, 0)

        integral = hist.Integral(i, i, 1, yAxis.GetNbins())

        for j in range(1, yAxis.GetNbins()+1):
            oldContent = hist.GetBinContent(i, j)

            if integral > 0:
                hist.SetBinContent(i, j, oldContent/integral)
            else:
                hist.SetBinContent(i, j, 0)

def normAndSmooth(TFset, inFile, outFile):
    inFile = R.TFile.Open(inFile)
    outFile = R.TFile(outFile, "recreate")
   
    for TF in TFset:
        inputHists = []
        for hist in TF["histNames"]:
            inputHists.append( inFile.Get(hist) )
        
        DeltaEvsE = inputHists[0].Clone( TF["base"] )
        for hist in inputHists[1:]:
            DeltaEvsE.Add(hist)

        DeltaEvsE.GetXaxis().SetTitle("E_{gen}")
        DeltaEvsE.GetYaxis().SetTitle("E_{rec} - E_{gen}")
        
        DeltaEvsE_Norm = DeltaEvsE.Clone( TF["norm"] )
        normalizeDeltaE(DeltaEvsE_Norm)
        
        DeltaEvsE.Write()
        DeltaEvsE_Norm.Write()
    
    outFile.Close()
    inFile.Close()

if __name__ == "__main__":
    options = parseArguments()

    TFset = [
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_bjet2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_bjet2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_bjet2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_bjet2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_bjet2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_bjet1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_bjet2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_bjet_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        #{
        #    "histNames":
        #        [
        #            "tf_bjet1_matchedToBeforeFSR_allEta",
        #            "tf_bjet2_matchedToBeforeFSR_allEta",
        #        ],
        #    "base": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_allEta",
        #    "norm": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_allEta_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_bjet1_matchedToBeforeFSR_barrel",
        #            "tf_bjet2_matchedToBeforeFSR_barrel",
        #        ],
        #    "base": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_barrel",
        #    "norm": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_barrel_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_bjet1_matchedToBeforeFSR_endcap",
        #            "tf_bjet2_matchedToBeforeFSR_endcap",
        #        ],
        #    "base": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_endcap",
        #    "norm": "ERecMinEGenVSEGen_bjet_matchedToBeforeFSR_endcap_Norm"
        #},
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_mu2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_mu2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_mu2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_mu2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_mu2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_mu1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_mu2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_mu_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        #{
        #    "histNames":
        #        [
        #            "tf_mu1_matchedToBeforeFSR_allEta",
        #            "tf_mu2_matchedToBeforeFSR_allEta",
        #        ],
        #    "base": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_allEta",
        #    "norm": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_allEta_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_mu1_matchedToBeforeFSR_barrel",
        #            "tf_mu2_matchedToBeforeFSR_barrel",
        #        ],
        #    "base": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_barrel",
        #    "norm": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_barrel_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_mu1_matchedToBeforeFSR_endcap",
        #            "tf_mu2_matchedToBeforeFSR_endcap",
        #        ],
        #    "base": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_endcap",
        #    "norm": "ERecMinEGenVSEGen_mu_matchedToBeforeFSR_endcap_Norm"
        #},
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_el2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_el2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                    "tf_el2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_nobtag_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_nobtag_csv"
        },
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_el2_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_allEta_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_el2_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_barrel_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_barrel_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        {
            "histNames":
                [
                    "tf_el1_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                    "tf_el2_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
                ],
            "base": "ERecMinEGenVSEGen_el_matchedToAfterFSR_endcap_hh_llmetjj_HWWleptons_btagM_csv",
            "norm": "ERecMinEGenVSEGen_el_matchedToAfterFSR_endcap_Norm_hh_llmetjj_HWWleptons_btagM_csv"
        },
        #{
        #    "histNames":
        #        [
        #            "tf_el1_matchedToBeforeFSR_allEta",
        #            "tf_el2_matchedToBeforeFSR_allEta",
        #        ],
        #    "base": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_allEta",
        #    "norm": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_allEta_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_el1_matchedToBeforeFSR_barrel",
        #            "tf_el2_matchedToBeforeFSR_barrel",
        #        ],
        #    "base": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_barrel",
        #    "norm": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_barrel_Norm"
        #},
        #{
        #    "histNames":
        #        [
        #            "tf_el1_matchedToBeforeFSR_endcap",
        #            "tf_el2_matchedToBeforeFSR_endcap",
        #        ],
        #    "base": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_endcap",
        #    "norm": "ERecMinEGenVSEGen_el_matchedToBeforeFSR_endcap_Norm"
        #},
    ]

    normAndSmooth(TFset, options.input, options.output)

