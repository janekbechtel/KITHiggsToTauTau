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
    # grouped JEC uncs documented in https://indico.cern.ch/event/740094/contributions/3055870/attachments/1680587/2699877/RegionalJES.pdf
    config["jecUncEta0to5Up"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "SinglePionECAL",
            "SinglePionHCAL",
            "AbsoluteFlavMap",
            "AbsoluteMPFBias",
            "AbsoluteScale",
            "AbsoluteStat",
            "Fragmentation",
            "FlavorQCD",
            "TimePtEta",
            "PileUpDataMC",
            "RelativeFSR",
            "RelativeStatFSR",
            "PileUpPtRef"
        ]
    }
    config["jecUncEta0to5Down"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "SinglePionECAL",
            "SinglePionHCAL",
            "AbsoluteFlavMap",
            "AbsoluteMPFBias",
            "AbsoluteScale",
            "AbsoluteStat",
            "Fragmentation",
            "FlavorQCD",
            "TimePtEta",
            "PileUpDataMC",
            "RelativeFSR",
            "RelativeStatFSR",
            "PileUpPtRef"
        ]
    }
    config["jecUncEta0to3Up"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "PileUpPtEC1",
            "PileUpPtEC2",
            "PileUpPtBB",
            "RelativeJEREC1",
            "RelativeJEREC2",
            "RelativePtEC1",
            "RelativePtEC2",
            "RelativeStatEC",
            "RelativePtBB"
        ]
    }
    config["jecUncEta0to3Down"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "PileUpPtEC1",
            "PileUpPtEC2",
            "PileUpPtBB",
            "RelativeJEREC1",
            "RelativeJEREC2",
            "RelativePtEC1",
            "RelativePtEC2",
            "RelativeStatEC",
            "RelativePtBB"
        ]
    }
    config["jecUncEta3to5Up"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeStatHF",
            "RelativePtHF",
            "PileUpPtHF",
            "RelativeJERHF"
        ]
    }
    config["jecUncEta3to5Down"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeStatHF",
            "RelativePtHF",
            "PileUpPtHF",
            "RelativeJERHF"
        ]
    }
    config["jecUncRelativeBalUp"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeBal"
        ]
    }
    config["jecUncRelativeBalDown"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeBal"
        ]
    }
    config["jecUncRelativeSampleUp"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : 1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeSample"
        ]
    }
    config["jecUncRelativeSampleDown"] = {
      "UseGroupedJetEnergyCorrectionUncertainty" : True,
      "JetEnergyCorrectionUncertaintyShift" : -1.0,
      "SvfitCacheFileFolder" : "nominal",
      "UseJECShiftsForBJets" : True,
      "JetEnergyCorrectionSplitUncertaintyParameterNames" : [
            "RelativeSample"
        ]
    }
  
  return config
