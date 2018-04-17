
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTrigger2017EfficiencyProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

std::string TauTrigger2017EfficiencyProducer::GetProducerId() const
{
	return "TauTrigger2017EfficiencyProducer";
}

void TauTrigger2017EfficiencyProducer::Produce( event_type const& event, product_type & product, 
												setting_type const& settings) const
{
	for(auto weightNames: m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
                    bool mc_weight = MCWeight.at(weightNames.first).at(index);
                    if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::ET)
                    {
                        if(mc_weight)
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getETauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                        else
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getETauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                    }
                    else if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::MT)
                    {
                        if(mc_weight)
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getMuTauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                        else
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getMuTauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                    }
                    if(product.m_decayChannel ==  HttEnumTypes::DecayChannel::TT)
                    {
                        if(mc_weight)
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getDiTauEfficiencyMC(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                        else
                        {
                                product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = TauSFs->getDiTauEfficiencyData(lepton->p4.Pt(),lepton->p4.Eta(),lepton->p4.Phi());
                        }
                    }
		}
	}
}