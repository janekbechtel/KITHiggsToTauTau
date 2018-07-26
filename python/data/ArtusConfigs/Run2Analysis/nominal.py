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
  config["nominal"] = {
    "ElectronEnergyCorrectionShiftEB" : 1.0, 
    "ElectronEnergyCorrectionShiftEE" : 1.0, 
    "JetEnergyCorrectionUncertaintyShift" : 0.0, 
    "MetUncertaintyShift" : False, 
    "MetUncertaintyType" : "", 
    "SvfitCacheFileFolder" : "nominal",
    "TauElectronFakeEnergyCorrection" : 1.0, 
    "TauElectronFakeEnergyCorrectionOneProngPiZerosShift" : 1.0, 
    "TauElectronFakeEnergyCorrectionOneProngShift" : 1.0, 
    "TauEnergyCorrectionOneProngPiZerosShift" : 1.0, 
    "TauEnergyCorrectionOneProngShift" : 1.0, 
    "TauEnergyCorrectionShift" : 1.0, 
    "TauEnergyCorrectionThreeProngShift" : 1.0, 
    "TauJetFakeEnergyCorrection" : 0.0,
    "TauMuonFakeEnergyCorrection" : 1.0, 
    "TauMuonFakeEnergyCorrectionOneProngPiZerosShift" : 1.0, 
    "TauMuonFakeEnergyCorrectionOneProngShift" : 1.0,
    "BTagShift" : 0.0,
    "BMistagShift" : 0.0
  }
  
  return config