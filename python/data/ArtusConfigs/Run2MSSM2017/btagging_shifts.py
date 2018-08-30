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
  if not re.search("Run201|Embedding", nickname):
    config["btagEffUp"] = {
      "SvfitCacheFileFolder" : "nominal",
      "BTagShift" : 1.0,
      "BMistagShift" : 0.0
    }
    config["btagEffDown"] = {
      "SvfitCacheFileFolder" : "nominal",
      "BTagShift" : -1.0,
      "BMistagShift" : 0.0
    }
    config["btagMistagUp"] = {
      "SvfitCacheFileFolder" : "nominal",
      "BTagShift" : 0.0,
      "BMistagShift" : 1.0
    }
    config["btagMistagDown"] = {
      "SvfitCacheFileFolder" : "nominal",
      "BTagShift" : 0.0,
      "BMistagShift" : -1.0
    }
  
  
  return config