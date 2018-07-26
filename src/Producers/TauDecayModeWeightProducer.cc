#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauDecayModeWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"


TauDecayModeWeightProducer::~TauDecayModeWeightProducer()
{
}

std::string TauDecayModeWeightProducer::GetProducerId() const
{
	return "TauDecayModeWeightProducer";
}

void TauDecayModeWeightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// Save some time by excluding not needed samples (e.g. HTauTau)
	m_isET = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^et", boost::regex::extended));
	m_isMT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^mt", boost::regex::extended));
	m_isTT = boost::regex_search(settings.GetRootFileFolder(), boost::regex("^tt", boost::regex::extended));

}

void TauDecayModeWeightProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings) const
{

    if (m_isMT || m_isET)
    {
        // Tau DM
        int decayMode = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
		float effCorr_nominal;
		float effCorr_up;
		float effCorr_down;
		float pi0Corr_nominal;
		float pi0Corr_up;
		float pi0Corr_down;
		if (decayMode == 0) {
			effCorr_nominal = 0.975;
			effCorr_up = 0.983;
			effCorr_down = 0.967;
			pi0Corr_nominal = 1.0;
			pi0Corr_up = 1.0;
			pi0Corr_down = 1.0;
		}
		if (decayMode == 1) {
			effCorr_nominal = 0.975;
			effCorr_up = 0.983;
			effCorr_down = 0.967;
			pi0Corr_nominal = 1.051;
			pi0Corr_up = 1.065;
			pi0Corr_down = 1.037;
		}
		if (decayMode == 10) {
			effCorr_nominal = std::pow(0.975,3);
			effCorr_up = std::pow(0.983,3);
			effCorr_down = std::pow(0.967,3);
			pi0Corr_nominal = 1.0;
			pi0Corr_up = 1.0;
			pi0Corr_down = 1.0;
		}				
		product.m_optionalWeights["embeddedDecayModeWeight"] = effCorr_nominal*pi0Corr_nominal;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Nom"] = effCorr_up*pi0Corr_nominal;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Nom"] = effCorr_down*pi0Corr_nominal;
		product.m_optionalWeights["embeddedDecayModeWeight_effNom_pi0Up"] = effCorr_nominal*pi0Corr_up;
		product.m_optionalWeights["embeddedDecayModeWeight_effNom_pi0Down"] = effCorr_nominal*pi0Corr_down;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Up"] = effCorr_up*pi0Corr_up;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Down"] = effCorr_up*pi0Corr_down;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Up"] = effCorr_down*pi0Corr_up;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Down"] = effCorr_down*pi0Corr_down;
	}
    if (m_isTT)
    {
        // Tau DM
        int decayMode_1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->decayMode;
		float effCorr_nominal_1;
		float effCorr_up_1;
		float effCorr_down_1;
		float pi0Corr_nominal_1;
		float pi0Corr_up_1;
		float pi0Corr_down_1;
		if (decayMode_1 == 0) {
			effCorr_nominal_1 = 0.975;
			effCorr_up_1 = 0.983;
			effCorr_down_1 = 0.967;
			pi0Corr_nominal_1 = 1.0;
			pi0Corr_up_1 = 1.0;
			pi0Corr_down_1 = 1.0;
		}
		if (decayMode_1 == 1) {
			effCorr_nominal_1 = 0.975;
			effCorr_up_1 = 0.983;
			effCorr_down_1 = 0.967;
			pi0Corr_nominal_1 = 1.051;
			pi0Corr_up_1 = 1.065;
			pi0Corr_down_1 = 1.037;
		}
		if (decayMode_1 == 10) {
			effCorr_nominal_1 = std::pow(0.975,3);
			effCorr_up_1 = std::pow(0.983,3);
			effCorr_down_1 = std::pow(0.967,3);
			pi0Corr_nominal_1 = 1.0;
			pi0Corr_up_1 = 1.0;
			pi0Corr_down_1 = 1.0;		
		}				
        int decayMode_2 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->decayMode;
		float effCorr_nominal_2;
		float effCorr_up_2;
		float effCorr_down_2;
		float pi0Corr_nominal_2;
		float pi0Corr_up_2;
		float pi0Corr_down_2;
		if (decayMode_2 == 0) {
			effCorr_nominal_2 = 0.975;
			effCorr_up_2 = 0.983;
			effCorr_down_2 = 0.967;
			pi0Corr_nominal_2 = 1.0;
			pi0Corr_up_2 = 1.0;
			pi0Corr_down_2 = 1.0;
		}
		if (decayMode_2 == 1) {
			effCorr_nominal_2 = 0.975;
			effCorr_up_2 = 0.983;
			effCorr_down_2 = 0.967;
			pi0Corr_nominal_2 = 1.051;
			pi0Corr_up_2 = 1.065;
			pi0Corr_down_2 = 1.037;
		}
		if (decayMode_2 == 10) {
			effCorr_nominal_2 = std::pow(0.975,3);
			effCorr_up_2 = std::pow(0.983,3);
			effCorr_down_2 = std::pow(0.967,3);
			pi0Corr_nominal_2 = 1.0;
			pi0Corr_up_2 = 1.0;
			pi0Corr_down_2 = 1.0;		
		}
		product.m_optionalWeights["embeddedDecayModeWeight"] = effCorr_nominal_1*pi0Corr_nominal_1*effCorr_nominal_2*pi0Corr_nominal_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Nom"] = effCorr_up_1*pi0Corr_nominal_1*effCorr_up_2*pi0Corr_nominal_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Nom"] = effCorr_down_1*pi0Corr_nominal_1*effCorr_down_2*pi0Corr_nominal_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effNom_pi0Up"] = effCorr_nominal_1*pi0Corr_up_1*effCorr_nominal_2*pi0Corr_up_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effNom_pi0Down"] = effCorr_nominal_1*pi0Corr_down_1*effCorr_nominal_2*pi0Corr_down_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Up"] = effCorr_up_1*pi0Corr_up_1*effCorr_up_2*pi0Corr_up_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effUp_pi0Down"] = effCorr_up_1*pi0Corr_down_1*effCorr_up_2*pi0Corr_down_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Up"] = effCorr_down_1*pi0Corr_up_1*effCorr_down_2*pi0Corr_up_2;
		product.m_optionalWeights["embeddedDecayModeWeight_effDown_pi0Down"] = effCorr_down_1*pi0Corr_down_1*effCorr_down_2*pi0Corr_down_2;
        
    }

	
}
