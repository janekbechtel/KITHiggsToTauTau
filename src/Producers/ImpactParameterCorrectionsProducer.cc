#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ImpactParameterCorrectionsProducer.h"

void ImpactParameterCorrectionsProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drel0_1", [](event_type const& event, product_type const& product) {
		return (product.m_flavourOrderedLeptons.at(0)->dxy / product.m_flavourOrderedLeptons.at(0)->track.errDxy);
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drelZ_1", [](event_type const& event, product_type const& product) {
		return (product.m_flavourOrderedLeptons.at(0)->dz / product.m_flavourOrderedLeptons.at(0)->track.errDz);
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drel0_2", [](event_type const& event, product_type const& product) {
		return (product.m_flavourOrderedLeptons.at(1)->dxy / product.m_flavourOrderedLeptons.at(1)->track.errDxy);
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drelZ_2", [](event_type const& event, product_type const& product) {
		return (product.m_flavourOrderedLeptons.at(1)->dz / product.m_flavourOrderedLeptons.at(1)->track.errDz);
	});
        
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_1_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[d0][abs][0];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_1_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[dZ][abs][0];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_2_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[d0][abs][1];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_2_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[dZ][abs][1];
	});
        
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drel0_1_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[d0][rel][0];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drelZ_1_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[dZ][rel][0];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drel0_2_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[d0][rel][1];
	});
        LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("drelZ_2_calib", [](event_type const& event, product_type const& product) {
		return product.m_DCAcalib[dZ][rel][1];
	});
        
        
	
	// book quantile shifters
	
	
	if (settings.GetQuantileMappingRootfile()!="none"){
		std::string rootfile = settings.GetQuantileMappingRootfile();
		// read config
	        std::string config[2][2][6][2];
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][source] = settings.GetPrompt_e_d0_source();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][target] = settings.GetPrompt_e_d0_target();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][source] = settings.GetPrompt_m_d0_source();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][target] = settings.GetPrompt_m_d0_target();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][source] = settings.GetNonprompt_e_d0_source();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][target] = settings.GetNonprompt_e_d0_target();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][source] = settings.GetNonprompt_m_d0_source();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][target] = settings.GetNonprompt_m_d0_target();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][source] = settings.GetTauh_d0_source();
		config[d0][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][target] = settings.GetTauh_d0_target();
		
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][source] = settings.GetPrompt_e_drel0_source();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][target] = settings.GetPrompt_e_drel0_target();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][source] = settings.GetPrompt_m_drel0_source();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][target] = settings.GetPrompt_m_drel0_target();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][source] = settings.GetNonprompt_e_drel0_source();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][target] = settings.GetNonprompt_e_drel0_target();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][source] = settings.GetNonprompt_m_drel0_source();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][target] = settings.GetNonprompt_m_drel0_target();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][source] = settings.GetTauh_drel0_source();
		config[d0][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][target] = settings.GetTauh_drel0_target();
		
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][source] = settings.GetPrompt_e_dZ_source();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][target] = settings.GetPrompt_e_dZ_target();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][source] = settings.GetPrompt_m_dZ_source();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][target] = settings.GetPrompt_m_dZ_target();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][source] = settings.GetNonprompt_e_dZ_source();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][target] = settings.GetNonprompt_e_dZ_target();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][source] = settings.GetNonprompt_m_dZ_source();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][target] = settings.GetNonprompt_m_dZ_target();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][source] = settings.GetTauh_dZ_source();
		config[dZ][abs][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][target] = settings.GetTauh_dZ_target();
		
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][source] = settings.GetPrompt_e_drelZ_source();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT)][target] = settings.GetPrompt_e_drelZ_target();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][source] = settings.GetPrompt_m_drelZ_source();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT)][target] = settings.GetPrompt_m_drelZ_target();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][source] = settings.GetNonprompt_e_drelZ_source();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)][target] = settings.GetNonprompt_e_drelZ_target();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][source] = settings.GetNonprompt_m_drelZ_source();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)][target] = settings.GetNonprompt_m_drelZ_target();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][source] = settings.GetTauh_drelZ_source();
		config[dZ][rel][Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)][target] = settings.GetTauh_drelZ_target();
		
		for (int dca_direction = 0; dca_direction < 2; dca_direction++){
			for (int dca_reference = 0; dca_reference < 2; dca_reference++){
				for (int gen_match = 1; gen_match < 6; gen_match++){
					if (config[dca_direction][dca_reference][gen_match][source]!="none" && config[dca_direction][dca_reference][gen_match][target]!="none"){
						shifter[dca_direction][dca_reference][gen_match].init(rootfile, config[dca_direction][dca_reference][gen_match][source], config[dca_direction][dca_reference][gen_match][target], true);
						shift[dca_direction][dca_reference][gen_match] = true;
					}
				}
			}
		}
	}
}

void ImpactParameterCorrectionsProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
	// set product defaults
	for (int i=0; i<2; i++){
		for (int j=0; j<2; j++){
			for (int k=0; k<2; k++){
				product.m_DCAcalib[i][j][k] = 0.0;
			}
		}
	}
	
	if (settings.GetQuantileMappingRootfile()!="none"){
		// get uncalibrated impact parameters
		double DCA[2][2][2]; //[d0/dZ][abs/rel][0/1]
		for(int leptonIndex=0; leptonIndex<2; leptonIndex++){
			DCA[d0][abs][leptonIndex] = product.m_flavourOrderedLeptons.at(leptonIndex)->dxy;
			DCA[dZ][abs][leptonIndex] = product.m_flavourOrderedLeptons.at(leptonIndex)->dz;
			DCA[d0][rel][leptonIndex] = product.m_flavourOrderedLeptons.at(leptonIndex)->dxy / product.m_flavourOrderedLeptons.at(0)->track.errDxy;
			DCA[dZ][rel][leptonIndex] = product.m_flavourOrderedLeptons.at(leptonIndex)->dz / product.m_flavourOrderedLeptons.at(0)->track.errDz;
		}
		
		// gen matching
		for(int leptonIndex=0; leptonIndex<2; leptonIndex++){
			int gen_match=0;
			if (settings.GetUseUWGenMatching()){
				KLepton* lepton = product.m_flavourOrderedLeptons.at(leptonIndex);
				KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
				gen_match = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton));
			}
			else{
				KGenParticle* genParticle = product.m_flavourOrderedGenLeptons.at(leptonIndex);
				if (genParticle) gen_match = Utility::ToUnderlyingValue(GeneratorInfo::GetGenMatchingCode(genParticle));
				else gen_match = Utility::ToUnderlyingValue(KappaEnumTypes::GenMatchingCode::IS_FAKE);
			}
			
			// calculate calibrated impact parameters
			for (int dca_direction = 0; dca_direction < 2; dca_direction++){
				for (int dca_reference = 0; dca_reference < 2; dca_reference++){
					if (shift[dca_direction][dca_reference][gen_match]){
						product.m_DCAcalib[dca_direction][dca_reference][leptonIndex] = shifter[dca_direction][dca_reference][gen_match].shift(DCA[dca_direction][dca_reference][leptonIndex]);
					}
					// if one correction is applied, however use uncalibrated value in order to get a partially calibrated distribution
					else if(shift[dca_direction][dca_reference][1] || shift[dca_direction][dca_reference][2] || shift[dca_direction][dca_reference][3] || shift[dca_direction][dca_reference][4] || shift[dca_direction][dca_reference][5]){
						product.m_DCAcalib[dca_direction][dca_reference][leptonIndex] = DCA[dca_direction][dca_reference][leptonIndex];
					}
				}
			}
		}
	}
}