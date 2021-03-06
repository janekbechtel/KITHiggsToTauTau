

#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

/**
   \brief GlobalProducer for MET studies
   
*/
class MetprojectionProducer: public ProducerBase<HttTypes> {
private:
	bool m_isData;
public:
	
	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override {
		return "MetprojectionProducer";
	}

	virtual void Init(setting_type const& settings) override;
	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings) const override;
};

