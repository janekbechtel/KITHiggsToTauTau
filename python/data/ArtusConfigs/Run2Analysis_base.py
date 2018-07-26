#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLL", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsKappa",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.lheWeightAssignment",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsSampleStitchingWeights",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.globalProcessors"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["SkipEvents"] = 0
  config["EventCount"] = -1
  config["InputIsData"] = "true" if isData else "false"
  
  config["LumiWhiteList"] = [7582]
  config["EventWhitelist"] = [1473388]
  
  BosonPdgIds = {
      "DY.?JetsToLL|EWKZ2Jets|Embedding(2016|MC)" : [
        23
      ],
      "^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z)(HToTauTau|H2JetsToTauTau)" : [
        25
      ],
      "W.?JetsToLN|EWKW" : [
        24
      ],
      "SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau" : [
        25,
        35,
        36
        ]
  }
  config["BosonPdgIds"] = [0]
  for key, pdgids in BosonPdgIds.items():
    if re.search(key, nickname): config["BosonPdgIds"] = pdgids
  
  config["BosonStatuses"] = [11,62]
  config["DeltaRMatchingRecoElectronGenParticle"] = 0.2
  config["DeltaRMatchingRecoElectronGenTau"] = 0.2
  config["DeltaRMatchingRecoMuonGenParticle"] = 0.2
  config["DeltaRMatchingRecoMuonGenTau"] = 0.2
  config["DeltaRMatchingRecoTauGenParticle"] = 0.2
  config["DeltaRMatchingRecoTauGenTau"] = 0.2
  config["RecoElectronMatchingGenParticlePdgIds"] = [11,13]
  config["RecoMuonMatchingGenParticlePdgIds"] = [11,13]
  config["RecoTauMatchingGenParticlePdgIds"] = [11,13]
  config["RecoElectronMatchingGenParticleMatchAllElectrons"] = "true"
  config["RecoMuonMatchingGenParticleMatchAllMuons"] = "true"
  config["RecoTauMatchingGenParticleMatchAllTaus"] = "true"
  config["MatchAllElectronsGenTau"] = "true"
  config["MatchAllMuonsGenTau"] = "true"
  config["MatchAllTausGenTau"] = "true"
  config["MatchGenTauDecayMode"] = "true"
  config["UpdateMetWithCorrectedLeptons"] = "true"
  config["TopPtReweightingStrategy"] = "Run1"
  
  '''config["MetFilter"] = [
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_goodVertices",
        "Flag_globalTightHalo2016Filter",
        "Flag_BadPFMuonFilter",
        "Flag_BadChargedCandidateFilter"
  ]
  if isData:
    config["MetFilter"].extend((
        "Flag_eeBadScFilter",
        "!Flag_duplicateMuons",
        "!Flag_badMuons"
    ))
  else:
    config["MetFilter"].extend((
        "!Flag_badGlobalMuonTaggerMAOD",
        "!Flag_cloneGlobalMuonTaggerMAOD"
    ))'''
  config["MetFilterToFlag"] = [
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_goodVertices",
        "Flag_globalTightHalo2016Filter",
        "Flag_BadPFMuonFilter",
        "Flag_BadChargedCandidateFilter"
  ]
  if isData:
    config["MetFilterToFlag"].append("Flag_eeBadScFilter")
    config["MetFilter"] = [
        "!Flag_duplicateMuons",
        "!Flag_badMuons"
    ]
  else:
    config["MetFilter"] = [
        "!Flag_badGlobalMuonTaggerMAOD",
        "!Flag_cloneGlobalMuonTaggerMAOD"
    ]
  
  config["OutputPath"] = "output.root"
  
  if isData or isEmbedded:                config["PileupWeightFile"] = "not needed"
  elif re.search(".*Summer16", nickname): config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
  else:                                   config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2015_246908-260627_13TeVFall15MiniAODv2_PromptReco_69mbMinBiasXS.root"
  
  config["BTagScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_moriond17_BtoH.csv" if re.search("Summer16", nickname) else "$CMSSW_BASE/src/Artus/KappaAnalysis/data/CSVv2_76X.csv"
  config["BTagEfficiencyFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies_moriond2017.root" if re.search("Summer16", nickname) else "$CMSSW_BASE/src/Artus/KappaAnalysis/data/tagging_efficiencies.root"
  
  config["MetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/TypeI-PFMet_Run2016BtoH.root"
  config["MetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys.root"
  config["MvaMetShiftCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MEtSys.root"
  config["MvaMetRecoilCorrectorFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/recoilMet/MvaMET_2016BCD.root"
  config["MetCorrectionMethod"] = "meanResolution"
  #config["ZptReweightProducerWeights"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/zpt/zpt_weights_2016_BtoH.root"
  config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["DoZptUncertainties"] = False

  config["ChooseMvaMet"] = False
  
  if isData or isEmbedded:
    if   re.search("Run2016|Embedding2016", nickname):      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"]
    elif re.search("Run2015(C|D)|Embedding2015", nickname): config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt"]
    elif re.search("Run2015B", nickname):                   config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_13TeV_16Dec2015ReReco_Collisions15_50ns_JSON_v2.txt"]
    
  if re.search("Fall15MiniAODv2", nickname):
    config["SimpleMuTauFakeRateWeightLoose"] = [1.0, 1.0, 1.0, 1.0, 1.0]
    config["SimpleMuTauFakeRateWeightTight"] = [1.0, 1.0, 1.0, 1.0, 1.0]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.02, 1.11]
    config["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.30]
  else:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.01, 1.007, 0.87, 1.154, 2.281]
    config["SimpleMuTauFakeRateWeightTight"] = [1.263, 1.364, 0.854, 1.712, 2.324]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.213, 1.375]
    config["SimpleEleTauFakeRateWeightTight"] = [1.402, 1.90]

  
  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.ee").build_config(nickname)

  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.em").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.et").build_config(nickname)
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.mm").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.mt").build_config(nickname)
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tt").build_config(nickname)
  #config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.inclusive").build_config(nickname)
  
  
  return config
