
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"
#include <boost/regex.hpp>



/**
   \brief TauDecayModeWeightProducer
   Config tags:
   
    Run this producer after the Run2DecayModeProducer

*/

class TauDecayModeWeightProducer : public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual ~TauDecayModeWeightProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings) override;

	void Produce(event_type const& event, product_type& product,
                 setting_type const& settings) const override;
private:

	bool m_isET;
	bool m_isMT;
	bool m_isTT;
};
