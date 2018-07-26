#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU

def build_config(nickname):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("(DY.?JetsToLL|EWKZ2Jets)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsVetoMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJEC",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter_mt",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsMVATestMethods"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["Channel"] = "MT"
  config["MinNMuons"] = 1
  config["MinNTaus"] = 1
  # HltPaths_comment: The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer.
  if re.search("Run2016|Summer16|Embedding2016", nickname): config["HltPaths"] = [
          "HLT_IsoMu22",
          "HLT_IsoTkMu22",
          "HLT_IsoMu22_eta2p1",
          "HLT_IsoTkMu22_eta2p1",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"]
  
  config["NoHltFiltering"] = False
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["MuonLowerPtCuts"] = ["20.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["30.0"]
  config["TauUpperAbsEtaCuts"] = ["2.3"]
  config["TriggerObjectLowerPtCut"] = -1.0
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["DiTauPairLepton1LowerPtCuts"] = ["HLT_IsoMu24_v:25.0", "HLT_IsoTkMu24_v:25.0"]
  config["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
          "HLT_IsoMu22_v",
          "HLT_IsoTkMu22_v",
          "HLT_IsoMu22_eta2p1_v",
          "HLT_IsoTkMu22_eta2p1_v"]
          #"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
          #"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"]
  config["DiTauPairNoHLT"] = False
  config["DiTauPairHLTLast"] = True
  config["HLTBranchNames"] = [
          "trg_singlemuon:HLT_IsoMu22_v",
          "trg_singlemuon:HLT_IsoTkMu22_v",
          "trg_singlemuon:HLT_IsoMu22_eta2p1_v",
          "trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
          "trg_mutaucross_emb:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
          "trg_mutaucross_emb:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"]

  config["MuonTriggerFilterNames"] = [
          "HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_v:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_eta2p1_v:hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"]
  config["TauTriggerFilterNames"] = [
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltPFTau20TrackLooseIsoAgainstMuon",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIsoAgainstMuon",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"]
  config["EventWeight"] = "eventWeight"
  config["SaveRooWorkspaceTriggerWeightAsOptionalOnly"] = "true"
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_9_embedded.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_9_embedded.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
          "0:muonEffTrgWeight",
          "0:isoWeight",
          "0:idWeight",
          "0:triggerWeight"
          ]
    config["EmbeddedWeightWorkspaceObjectNames"]=[
          "0:m_sel_trg_ratio",
          "0:m_iso_ratio",
          "0:m_id_ratio",
          "0:m_trg_ratio"
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta"
          ]
  else:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
    
    config["RooWorkspaceWeightNames"] = [
      "0:triggerWeight_singleMu",
      "0:idIsoWeight",
      "0:trackWeight"
    ]
    config["RooWorkspaceObjectNames"] = [
      "0:m_trgMu22OR_eta2p1_desy_ratio",
      "0:m_idiso0p15_desy_ratio",
      "0:m_trk_ratio"
    ]
    config["RooWorkspaceObjectArguments"] = [
      "0:m_pt,m_eta",
      "0:m_pt,m_eta",
      "0:m_eta"
    ]

  config["SaveMuTauTriggerWeightAsOptionalOnly"] = "true"
  config["MuTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["MuTauTriggerWeightWorkspaceWeightNames"] = [
    "0:triggerWeight_muTauCross",
    "1:triggerWeight_muTauCross"
  ]
  config["MuTauTriggerWeightWorkspaceObjectNames"] = [
    "0:m_trgMu19leg_eta2p1_desy_ratio",
    "1:t_genuine_TightIso_mt_ratio,t_fake_TightIso_mt_ratio"
  ]
  config["MuTauTriggerWeightWorkspaceObjectArguments"] = [
    "0:m_pt,m_eta",
    "1:t_pt,t_eta"
  ]
  config["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu22OR_eta2p1_eff.root"]
  config["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu22OR_eta2p1_eff.root"]
  config["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  config["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  
  config["IdentificationEfficiencyMode"] = "multiply_weights"
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerEfficiencyMode"] = "multiply_weights"
  config["EleTauFakeRateWeightFile"] = ["1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]
  
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["UseUWGenMatching"] = "true"
  
  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.fourVectorQuantities").build_list()
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.syncQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.svfitSyncQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.splitJecUncertaintyQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nVetoMuons",
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "trg_singlemuon",
      "trg_mutaucross_emb",
      "trg_mutaucross",
      "triggerWeight_singleMu_1",
      "triggerWeight_muTauCross_1",
      "triggerWeight_muTauCross_2",
      #~ "lep1ErrD0",
      #~ "lep1ErrDz",
      #~ "lep2ErrD0",
      #~ "lep2ErrDz",
      #~ "PVnDOF",
      #~ #"PVchi2",
      #~ "drel0_1",
      #~ "drel0_2",
      #~ "drelZ_1",
      #~ "drelZ_2",

      "idisoweight_1",
      #"htxs_stage0cat",
      #"htxs_stage1cat",
      "flagMETFilter"
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight"])  

  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1cat"
    ])
  
  config["OSChargeLeptons"] = True
  
  config["Processors"] = [                                    "producer:HltProducer",
                                                              "filter:HltFilter",
                                                              "producer:MetSelector",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MinMuonsCountFilter",
                                                              "producer:ValidElectronsProducer"]
  if not isData:                 config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:               config["Processors"].append(   "producer:HttValidGenTausProducer")

  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidMTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:HttValidVetoMuonsProducer",
                                                              "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:Run2DecayChannelProducer"))
  config["Processors"].extend((                               "producer:DiVetoMuonVetoProducer",
                                                              "producer:TaggedJetCorrectionsProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
                                                              #"producer:TaggedJetUncertaintyShiftProducer"))
  if not isData:                 config["Processors"].append( "producer:MetCorrector") #"producer:MvaMetCorrector"
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if not (isData or isEmbedded): config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  config["Processors"].extend((                               "filter:MinimalPlotlevelFilter",
                                                              "producer:SvfitProducer",
                                                              "producer:ImpactParameterCorrectionsProducer")) #"producer:MVATestMethodsProducer"
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if not (isData or isEmbedded):                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")  

  if not (isData or isEmbedded): config["Processors"].append( "producer:MuTauTriggerWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  
  
  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedMuons"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

                         #"SvfitCacheConsumer"]
                         #"CutFlowTreeConsumer",
                         #"KappaElectronsConsumer",
                         #"KappaTausConsumer",
                         #"KappaTaggedJetsConsumer",
                         #"RunTimeConsumer",
                         #"PrintEventsConsumer"
  
  
  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.nominal").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.JECunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.METunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tauESperDM_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tauMuFakeESperDM_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.tauJetFakeESIncl_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.btagging_shifts").build_config(nickname))

