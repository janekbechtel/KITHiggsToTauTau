#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
#import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  #isEmbedded = datasetsHelper.isEmbedded(nickname)
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLL", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  if re.search("Fall17|Embedding", nickname):
    config["tauJetFakeEsUp"] = {
      "TauJetFakeEnergyCorrection" : 1.0,
      "SvfitCacheFileFolder" : "tauJetFakeEsUp"
    }
    config["tauJetFakeEsDown"] = {
      "TauJetFakeEnergyCorrection" : -1.0,
      "SvfitCacheFileFolder" : "tauJetFakeEsDown"
    }
  
  
  return config
