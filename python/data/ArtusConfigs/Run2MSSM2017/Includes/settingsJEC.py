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
  config["JetEnergyCorrectionParameters"] = []
  if re.search("Run2017|Embedding2017", nickname):
    config["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V6_DATA_Uncertainty_AK4PFchs.txt"
  else:
    config["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017_V6_MC_Uncertainty_AK4PFchs.txt"
    
  config["JetEnergyCorrectionUncertaintySource"] = ""
  #config["JetEnergyCorrectionUncertaintyShift"] = 0.0
  
  config["JetEnergyCorrectionSplitUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall17/Fall17_17Nov2017F_V6_DATA_UncertaintySources_AK4PFchs.txt" if re.search("Run2017|Fall17", nickname) else ""


  return config
