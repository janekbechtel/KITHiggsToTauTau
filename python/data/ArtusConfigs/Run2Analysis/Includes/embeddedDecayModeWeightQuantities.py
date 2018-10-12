#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list():
  quantities_list = [
	"embeddedDecayModeWeight",
	"embeddedDecayModeWeight_effUp_pi0Nom",
	"embeddedDecayModeWeight_effDown_pi0Nom",
	"embeddedDecayModeWeight_effNom_pi0Up",
	"embeddedDecayModeWeight_effNom_pi0Down",
	"embeddedDecayModeWeight_effUp_pi0Up",
	"embeddedDecayModeWeight_effUp_pi0Down",
	"embeddedDecayModeWeight_effDown_pi0Up",
	"embeddedDecayModeWeight_effDown_pi0Down"
  ]
  
  return quantities_list
