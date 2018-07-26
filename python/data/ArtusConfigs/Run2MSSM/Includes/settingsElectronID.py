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
  config["ElectronID_documentation"] = "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"
  config["ElectronReco"] = "mvanontrig"
  config["ElectronID"] = "user"
  config["ElectronIDType"] = "mvabased2015andlater"
  
  config["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values" if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
  
  config["ElectronMvaIDCutEB1"] = 0.967083 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.940962684155
  
  config["ElectronMvaIDCutEB2"] = 0.929117 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.899208843708
  
  config["ElectronMvaIDCutEE"] = 0.726311 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.758484721184
  
  config["ElectronIDList"] = [
    "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values",
    "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto",
    "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose",
    "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium",
    "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"
  ]
  
  config["ElectronIsoType"] = "user"
  config["ElectronIso"] = "none"
  config["ElectronIsoSignalConeSize"] = 0.3
  config["ElectronDeltaBetaCorrectionFactor"] = 0.5
  config["ElectronTrackDxyCut"] = 0.045
  config["ElectronTrackDzCut"] = 0.2


  return config
