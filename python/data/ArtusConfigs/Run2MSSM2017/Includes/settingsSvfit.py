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
  
  # SvfitConsumer config
  config["GenerateSvfitInput"] = False			# actually a flag for the SVFit consumer to stage out to a different file specified via the following file name option; the following 4 options are only relevant if True
  config["SvfitOutFile"] = "SvfitCache.root"		# define different output file name base (which is useful to create inputs for offline SVFit calculations. <channel>_<shift><index> is automatically inserted.
  config["SvfitInputCutOff"] = 2000			# Files can be subdevided in order to avoid too large jobs in the offline SVFit calculation. Specifies max. number of events per file.
  config["UpdateSvfitCache"] = False                    # True: use existing caches and complete them; False: recalculate complete cache
  config["UseFirstInputFileNameForSvfit"] = False	# uses kappa nickname instead of filename specified in "SvfitOutFile"
  
  # SvfitProducer config
  config["SvfitCacheMissBehaviour"] = "undefined" # Action if SVFit cache is not found. Choose between 'assert': job fails 'undefined': neither runs SVFit nor fails (used when filling SVFit Caches offline) 'recalculate': run SVFit regularly
  config["SvfitIntegrationMethod"] = "MarkovChain"
  
  SvfitCacheFiles = {
  }
  return config
