#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLL", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  hasBoson = re.search("DY.?JetsToLLM(10to50|50|150)|EWKZ2Jets|^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z)(HToTauTau|H2JetsToTauTau)|SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau", nickname)
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  #config["Processors"] = ["#producer:PrintGenParticleDecayTreeProducer",
  #				"#filter:RunLumiEventFilter"]
  config["Processors"] = ["filter:JsonFilter"] if (isData or re.search("Embedding201", nickname)) else [] #["filter:RunLumiEventFilter"]
  config["Processors"].append(                      "producer:NicknameProducer")
  if not isData:
    if hasBoson:       config["Processors"].extend(("producer:GenBosonFromGenParticlesProducer",
                                                    "producer:GenBosonDiLeptonDecayModeProducer",
                                                    "producer:ValidGenTausProducer",
                                                    "producer:GenDiLeptonDecayModeProducer"))
    config["Processors"].extend((                   "producer:GenParticleProducer",
                                                    "producer:RecoElectronGenParticleMatchingProducer",
                                                    "producer:RecoElectronGenTauMatchingProducer",
                                                    "producer:RecoMuonGenParticleMatchingProducer",
                                                    "producer:RecoMuonGenTauMatchingProducer",
                                                    "producer:RecoTauGenParticleMatchingProducer",
                                                    "producer:RecoTauGenTauMatchingProducer",
                                                    "producer:MatchedLeptonsProducer",
                                                    "producer:CrossSectionWeightProducer",
                                                    "producer:GeneratorWeightProducer",
                                                    "producer:NumberGeneratedEventsWeightProducer"))
    if not isEmbedded: config["Processors"].append( "producer:PUWeightProducer")
  config["Processors"].extend((                     "#filter:MetFilter",
                                                    "producer:MetFilterFlagProducer"))
  return config
