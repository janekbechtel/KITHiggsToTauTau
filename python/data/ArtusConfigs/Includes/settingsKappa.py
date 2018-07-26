#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  # define frequently used conditions
  isMC = not re.search("(?<!PFembedded).Run201", nickname)
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["GenParticles"] = "genParticles" if isMC else ""
  config["GenTaus"] = "genTaus" if isMC else ""
  config["GenTauJets"] = "tauGenJets" if isMC else ""
  config["GenMet"] = "" "genmetTrue" if isMC else ""
  config["GenJets"] = ""
  config["Electrons"] = "electrons"
  config["ElectronMetadata"] = "electronMetadata"
  config["Muons"] = "muons"
  config["Taus"] = "taus"
  config["TauMetadata"] = "taus"
  
  if re.search("MINIAOD|USER", nickname): config["TaggedJets"] = "ak4PF"
  
  if re.search("13TeV", nickname): config["PileupDensity"] = "pileupDensity"
  
  config["Met"] = "met"

  #config["MvaMets"] = "MVAMET"
  #config["PFChargedHadronsPileUp"] = "pfPileUpChargedHadrons"
  #config["PFChargedHadronsNoPileUp"] = "pfNoPileUpChargedHadrons"
  #config["PFChargedHadronsNoPileUp"] = "pfAllChargedParticles"
  #config["PFNeutralHadronsNoPileUp"] = "pfNoPileUpNeutralHadrons"
  #config["PFPhotonsNoPileUp"] = "pfNoPileUpPhotons"
  #config["PackedPFCandidates"] = "packedPFCandidates"
  config["BeamSpot"] = "offlineBeamSpot"
  config["VertexSummary"] = "goodOfflinePrimaryVerticesSummary"
  config["EventMetadata"] = "eventInfo"
  config["LumiMetadata"] = "lumiInfo"
  config["GenEventInfoMetadata"] = "genEventInfoMetadata"
  config["FilterMetadata"] = ""
  config["FilterSummary"] = ""
  config["JetMetadata"] = "jetMetadata"
  config["BeamSpot"] = "offlineBeamSpot"
  config["TriggerInfos"] = "triggerObjectMetadata"
  config["TriggerObjects"] = "triggerObjects"
  

  return config
