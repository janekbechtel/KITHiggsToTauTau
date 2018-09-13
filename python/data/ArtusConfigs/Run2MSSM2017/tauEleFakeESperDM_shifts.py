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
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  if isDY:
    config["eleTauEsOneProngZeroPiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["eleTauEsOneProngZeroPiZeroUp"]["TauElectronFakeEnergyCorrectionOneProng"] = 1.029
    
    config["eleTauEsOneProngZeroPiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["eleTauEsOneProngZeroPiZeroDown"]["TauElectronFakeEnergyCorrectionOneProng"] = 1.019
    
    
    config["eleTauEsOneProngOnePiZeroUp"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["eleTauEsOneProngOnePiZeroUp"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.086
    
    config["eleTauEsOneProngOnePiZeroDown"] = {
      "JetEnergyCorrectionUncertaintyShift" : [0.0]
    }
    config["eleTauEsOneProngOnePiZeroDown"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.066
  
  
  return config
