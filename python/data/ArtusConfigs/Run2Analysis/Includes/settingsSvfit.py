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
  config["UpdateSvfitCache"] = True			# True: use existing caches and complete them; False: recalculate complete cache
  config["UseFirstInputFileNameForSvfit"] = False	# uses kappa nickname instead of filename specified in "SvfitOutFile"
  
  # SvfitProducer config
  config["SvfitCacheMissBehaviour"] = "recalculate" # Action if SVFit cache is not found. Choose between 'assert': job fails 'undefined': neither runs SVFit nor fails (used when filling SVFit Caches offline) 'recalculate': run SVFit regularly
  config["SvfitIntegrationMethod"] = "MarkovChain"
  
  SvfitCacheFiles = {
      "DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root",
      "Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD.root",
      "Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD.root",
      "Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD.root",
      "Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD.root",
      "Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD.root",
      "Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root",
      "Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root",
      "VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root",
      "VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root",
      "W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root",
      "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root",
      "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root",
      "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3.root",
      "WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root",
      "WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root",
      "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root",
      "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root",
      "WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root",
      "WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root",
      "ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root",
      "ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1" : "root://cmsxrootd-1.gridka.de:1094///store/user/swozniew/Svfit/2018-02-07/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
  }
  #for key, SvfitCacheFile in SvfitCacheFiles.items():
  #  if key == nickname: config["SvfitCacheFile"] = SvfitCacheFile

  return config
