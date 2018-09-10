
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttElectronCorrectionsProducer.h"


void HttElectronCorrectionsProducer::Init(setting_type const& settings)
{
	ElectronCorrectionsProducer::Init(settings);
	
	eleEnergyCorrection = ToElectronEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetElectronEnergyCorrection())));
}

void HttElectronCorrectionsProducer::AdditionalCorrections(KElectron* electron, event_type const& event,
                                                      product_type& product, setting_type const& settings) const
{
	ElectronCorrectionsProducer::AdditionalCorrections(electron, event, product, settings);
	
	if (eleEnergyCorrection == ElectronEnergyCorrection::FALL2015)
	{
	        electron->p4 = electron->p4 * (1.0);
	}
	else if (eleEnergyCorrection != ElectronEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Electron energy correction of type " << Utility::ToUnderlyingValue(eleEnergyCorrection) << " not yet implemented!";
	}
	
	float eleEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShift();
	float eleEnergyCorrectionShiftEB = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShiftEB();
	float eleEnergyCorrectionShiftEE = static_cast<HttSettings const&>(settings).GetElectronEnergyCorrectionShiftEE();
	
	// Apply scale & smear corrections for electrons
	if (static_cast<HttSettings const&>(settings).GetElectronScaleAndSmearUsed())
	{
			float corrected_energy = electron->getId("electronCorrection:ecalTrkEnergyPostCorr", event.m_electronMetadata);
			float correction_factor = corrected_energy/electron->p4.E();
			electron->p4 = electron->p4 * correction_factor;
			LOG(DEBUG) << "Applying scale & smear. Corrected energy: " << corrected_energy << " correction factor: " << correction_factor;
	}
	// Apply constant electron ES corrections
	//
	if (eleEnergyCorrectionShift != 1.0 && (eleEnergyCorrectionShiftEB != 1.0 || eleEnergyCorrectionShiftEE != 1.0))
	{
		LOG(FATAL) << "Too many different electron energy corrections (all eta, barrel-only, endcap-only)";
	}
	
	if (eleEnergyCorrectionShift != 1.0)
	{
		electron->p4 = electron->p4 * eleEnergyCorrectionShift;
	}
	if (eleEnergyCorrectionShiftEB != 1.0 || eleEnergyCorrectionShiftEE != 1.0)
	{
		if (std::abs(electron->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			electron->p4 = electron->p4 * eleEnergyCorrectionShiftEB;
		}
		else
		{
			electron->p4 = electron->p4 * eleEnergyCorrectionShiftEE;
		}

	}

}
