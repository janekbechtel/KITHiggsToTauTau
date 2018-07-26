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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsElectronID"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["LooseElectronReco"] = "mvanontrig"
  config["LooseElectronID"] = "user"
  config["LooseElectronIDType"] = "mvabased2015andlater"
  config["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
  config["LooseElectronMvaIDCutEB1"] = 0.836695742607
  config["LooseElectronMvaIDCutEB2"] = 0.715337944031
  config["LooseElectronMvaIDCutEE"] = 0.356799721718
  config["LooseElectronIsoType"] = "user"
  config["LooseElectronIso"] = "none"
  config["LooseElectronIsoPtSumOverPtUpperThresholdEB"] = 0.3
  config["LooseElectronIsoPtSumOverPtUpperThresholdEE"] = 0.3
  config["LooseElectronLowerPtCuts"] = ["10.0"]
  config["LooseElectronUpperAbsEtaCuts"] = ["2.5"]
  config["LooseElectronTrackDxyCut"] = 0.045
  config["LooseElectronTrackDzCut"] = 0.2
  config["DirectIso"] = True


  return config
