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
  
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["TauEnergyCorrection"] = "smhtt2016" if re.search("Summer16", nickname) else "none"
  config["TauEnergyCorrectionOneProng"] = 0.995
  config["TauEnergyCorrectionOneProngPiZeros"] = 1.011
  config["TauEnergyCorrectionThreeProng"] = 1.006
  if re.search("DY.?JetsToLL|EWKZ2Jets", nickname):
    config["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
    config["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.095
    config["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
    config["TauMuonFakeEnergyCorrectionOneProng"] = 0.998
    config["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.015
    config["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0


  return config
