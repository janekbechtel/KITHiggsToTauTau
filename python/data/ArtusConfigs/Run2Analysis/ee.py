#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("(DY.?JetsToLL|EWKZ2Jets)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsVetoElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter_ee"
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsSvfit",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsMVATestMethods"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["Channel"] = "EE"
  config["MinNElectrons"] = 2
  # The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer.
  if isEmbedded: config["HltPaths"] = [
          ""]
  else: config["HltPaths"] = [
          "HLT_Ele25_eta2p1_WPTight_Gsf"]
  config["HLTBranchNames"] = ["trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v"]
  config["NoHltFiltering"] = True if isEmbedded else False
  
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = False
  config["ElectronLowerPtCuts"] = ["13.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.5"]
  config["DeltaRTriggerMatchingElectrons"] = 0.4
  config["DiTauPairMinDeltaRCut"] = 0.3
  if re.search("Run2016|Summer16", nickname): config["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
          "HLT_Ele25_eta2p1_WPTight_Gsf_v"]
  
  config["DiTauPairLepton1LowerPtCuts"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v:26.0", "HLT_Ele25_eta2p1_WPTight_Gsf_v:26.0"]
  #config["DiTauPairLepton2LowerPtCuts"] = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:24.0"]
    
  config["DiTauPairNoHLT"] =  False
  config["EventWeight"] = "eventWeight"
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["RooWorkspaceWeightNames"] = [
    "0:idIsoWeight",
    "1:idIsoWeight"
  ]
  config["RooWorkspaceObjectNames"] = [
    "0:e_idiso0p1_desy_ratio",
    "1:e_idiso0p1_desy_ratio"
  ]
  config["RooWorkspaceObjectArguments"] = [
    "0:e_pt,e_eta",
    "1:e_pt,e_eta"
  ]
  
  config["EETriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["EETriggerWeightWorkspaceWeightNames"] = [
    "0:triggerWeight",
    "1:triggerWeight"
  ]
  config["EETriggerWeightWorkspaceObjectNames"] = [
    "0:e_trgEle25eta2p1WPTight_desy_ratio",
    "1:e_trgEle25eta2p1WPTight_desy_ratio"
  ]
  config["EETriggerWeightWorkspaceObjectArguments"] = [
    "0:e_pt,e_eta",
    "1:e_pt,e_eta"
  ]
  #config["TriggerEfficiencyData"] = []
  '''
  config["TriggerEfficiencyMc"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_dummy.root"]
  config["IdentificationEfficiencyData"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  config["IdentificationEfficiencyMc"] = [
    "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root",
    "1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  '''
  config["IdentificationEfficiencyMode"] = "multiply_weights"
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerEfficiencyMode"] = "correlate_triggers"
  
  if re.search("Run2016|Summer16", nickname):
    config["ElectronTriggerFilterNames"] = [
          "HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter"]
  
  config["InvalidateNonMatchingElectrons"] = True
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  
  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.fourVectorQuantities").build_list()
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.syncQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.svfitSyncQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.splitJecUncertaintyQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "trg_singleelectron",
      "lep1ErrD0",
      "lep1ErrDz",
      "lep2ErrD0",
      "lep2ErrDz"
  ])
  
  config["OSChargeLeptons"] = True
  
  
  config["Processors"] = [                                    "producer:HltProducer",
                                                              "filter:HltFilter",
                                                              "producer:MetSelector",
                                                              "producer:ElectronCorrectionsProducer",
                                                              "producer:ValidElectronsProducer",
                                                              "filter:ValidElectronsFilter",
                                                              "producer:ElectronTriggerMatchingProducer",
                                                              "filter:MinElectronsCountFilter",
                                                              "producer:ValidMuonsProducer",
                                                              "producer:ValidTausProducer",
                                                              "producer:ValidEEPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:TaggedJetCorrectionsProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"]
                                                              #"producer:TaggedJetUncertaintyShiftProducer"]
  if not isData:                 config["Processors"].append( "producer:MetCorrector") #"producer:MvaMetCorrector"
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
                                                              #"producer:SvfitProducer")) #"producer:MVATestMethodsProducer"
  if not isData:                 config["Processors"].extend(("producer:IdentificationWeightProducer",
                                                              "producer:EETriggerWeightProducer",
                                                              #"producer:TriggerWeightProducer",
                                                              "producer:RooWorkspaceWeightProducer"))
  config["Processors"].append(                                "producer:EventWeightProducer")
  
  
  config["AddGenMatchedParticles"] = True
  config["BranchGenMatchedElectrons"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]
                         #"SvfitCacheConsumer"]
                         #"CutFlowTreeConsumer",
                         #"KappaElectronsConsumer",
                         #"KappaTausConsumer",
                         #"KappaTaggedJetsConsumer",
                         #"RunTimeConsumer",
                         #"PrintEventsConsumer"
  
  
  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('ee', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.nominal").build_config(nickname))
