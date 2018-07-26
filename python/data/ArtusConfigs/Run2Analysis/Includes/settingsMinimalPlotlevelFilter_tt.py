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
  
  config["PlotlevelFilterExpressionQuantities"] = [
    "againstElectronVLooseMVA6_2",
    "extraelec_veto",
    "againstMuonLoose3_2",
    "extramuon_veto",
    "byVLooseIsolationMVArun2v1DBoldDMwLT_1",
    "byVLooseIsolationMVArun2v1DBoldDMwLT_2"
  ]
  config["PlotlevelFilterExpression"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(againstMuonLoose3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byVLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*(byVLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
  
  return config
