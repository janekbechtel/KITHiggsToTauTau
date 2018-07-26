
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetFilterFlagProducer.h"

void MetFilterFlagProducer::Init(setting_type const& settings)
{
    ProducerBase<HttTypes>::Init(settings);
    //FilterBase<HttTypes>::Init(settings);

    LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("flagMETFilter", [](event_type const& event, product_type const& product) {
        return product.m_MetFilter;
    });

    std::vector<std::string> tmpMetFiltersToFlag = settings.GetMetFilterToFlag();
    for(auto filter: tmpMetFiltersToFlag)
    {
        if(filter.at(0) == '!')
        {
            std::string filterName = filter.substr(1);
            m_invertedFilters_flag.push_back(filterName);
            m_metFilters_flag.push_back(filterName);
        }
        else
        {
            m_metFilters_flag.push_back(filter);
        }
    }
}

void MetFilterFlagProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
    for (auto metfilter : m_metFilters_flag)
    {
        int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);                                     
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        //std::cout << "MetFilter Name: " << metfilter << " Decision: " << result << std::endl;
        // check if the filter should be inverted
        if(std::find(m_invertedFilters_flag.begin(),m_invertedFilters_flag.end(), metfilter) != m_invertedFilters_flag.end())
        {
            result = !result;
        }
        product.m_MetFilter = product.m_MetFilter && result;
    }
}

