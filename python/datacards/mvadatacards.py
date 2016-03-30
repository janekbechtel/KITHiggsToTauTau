# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.mvadatacards_base as datacards


class MVADatacards(datacards.Datacards):
    def __init__(self, higgs_masses=["125"], cb=None):
        super(MVADatacards, self).__init__(cb)

        if cb is None:
            signal_processes = ["ggH", "qqH", "WH", "ZH"]

            # ======================================================================
            # MT channel
            categs = []
            for ntrees in [150,250,350,450]:
				for name in ["up", "down", "mid"]:
					categs.append("mt_Nall_%i_%s"%(ntrees, name))
					categs.append("mt_Nall_%i_4_%s"%(ntrees, name))
					categs.append("mt_all_%i_%s"%(ntrees, name))
					categs.append("mt_all_%i_4_%s"%(ntrees, name))
            self.add_processes(
                    channel="mt",
                    #categories=["mt_"+category for category in ["2jet_vbf", "ztt_loose", "ztt_tight", "inclusive"]],
                    #categories=["mt_"+category for category in ["inclusive"]],
                    categories=categs,
                    bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=signal_processes,
                    analysis=["MVATest"],
                    era=["13TeV"],
                    mass=higgs_masses
            )

            # efficiencies
            self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
            self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)

            self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
            self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)

            # Tau ES
            self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
            self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["mt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)

            # ======================================================================
            # ET channel
            self.add_processes(
                    channel="et",
                    categories=["et_"+category for category in ["2jet_vbf", "ztt_loose", "ztt_tight", "inclusive"]],
                    bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=signal_processes,
                    analysis=["MVATest"],
                    era=["13TeV"],
                    mass=higgs_masses
            )

            # efficiencies
            self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
            self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)

            self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
            self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)

            # Tau ES
            self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
            self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["et"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)

            # ======================================================================
            # EM channel
            self.add_processes(
                    channel="em",
                    categories=["em_"+category for category in ["2jet_vbf", "ztt_loose", "ztt_tight", "inclusive"]],
                    bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=signal_processes,
                    analysis=["MVATest"],
                    era=["13TeV"],
                    mass=higgs_masses
            )

            # efficiencies
            self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
            self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)

            self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
            self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)

            # ======================================================================
            # TT channel
            self.add_processes(
                    channel="tt",
                    categories=["tt_"+category for category in ["2jet_vbf", "ztt_loose", "ztt_tight", "inclusive"]],
                    bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
                    sig_processes=signal_processes,
                    analysis=["MVATest"],
                    era=["13TeV"],
                    mass=higgs_masses
            )

            # efficiencies
            self.cb.cp().channel(["tt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
            self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)

            # Tau ES
            self.cb.cp().channel(["tt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
            self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

            # fake-rate
            self.cb.cp().channel(["tt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)

            # ======================================================================
            # All channels

            # lumi
            self.cb.cp().signals().AddSyst(self.cb, *self.lumi_syst_args)
            self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "W", "VV"]).AddSyst(self.cb, *self.lumi_syst_args)

            # jets
            self.cb.cp().process(["ZTT", "ZL", "ZJ", "TT", "VV", "W"]).AddSyst(self.cb, *self.jec_syst_args)
            self.cb.cp().signals().AddSyst(self.cb, *self.jec_syst_args)
            self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.btag_efficieny_syst_args)

            # MET
            self.cb.cp().AddSyst(self.cb, *self.met_scale_syst_args)

            # QCD systematic
            self.cb.cp().process(["QCD"]).channel(["tt"]).AddSyst(self.cb, *self.qcd_syst_args) # automatically in other channels
            #self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)

            # cross section
            self.cb.cp().process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
            self.cb.cp().process(["TT"]).channel(["mt", "et", "tt"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args) # automatically in other channels determined
            #self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
            self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
            self.cb.cp().process(["W"]).channel(["em", "tt"]).AddSyst(self.cb, *self.wj_cross_section_syst_args) # automatically in other channels determined
            #self.cb.cp().process(["W"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)

            # signal
            self.cb.cp().signals().AddSyst(self.cb, *self.htt_qcd_scale_syst_args)
            self.cb.cp().signals().AddSyst(self.cb, *self.htt_pdf_scale_syst_args)
            self.cb.cp().signals().AddSyst(self.cb, *self.htt_ueps_syst_args)

            if log.isEnabledFor(logging.DEBUG):
                self.cb.PrintAll()

