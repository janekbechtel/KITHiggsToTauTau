
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "quantile_mapping/quantile_mapping/interface/QuantileShifter.h"

class ImpactParameterCorrectionsProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	
	virtual std::string GetProducerId() const override {
		return "ImpactParameterCorrectionsProducer";
	}
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;

private:
	enum DCA_direction{d0, dZ};
	enum DCA_reference{abs, rel};
	enum QS_input{source, target};
	
	QuantileShifter shifter[2][2][6];
	bool shift[2][2][6];
};

