
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RooWorkspaceWeightProducer.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"
#include <math.h>

RooWorkspaceWeightProducer::RooWorkspaceWeightProducer(
		bool (setting_type::*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)(void) const,
		std::string (setting_type::*GetRooWorkspace)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceWeightNames)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectNames)(void) const,
		std::vector<std::string>& (setting_type::*GetRooWorkspaceObjectArguments)(void) const
):
	GetSaveRooWorkspaceTriggerWeightAsOptionalOnly(GetSaveRooWorkspaceTriggerWeightAsOptionalOnly),
	GetRooWorkspace(GetRooWorkspace),
	GetRooWorkspaceWeightNames(GetRooWorkspaceWeightNames),
	GetRooWorkspaceObjectNames(GetRooWorkspaceObjectNames),
	GetRooWorkspaceObjectArguments(GetRooWorkspaceObjectArguments)
{
}

RooWorkspaceWeightProducer::RooWorkspaceWeightProducer():
		RooWorkspaceWeightProducer(&setting_type::GetSaveRooWorkspaceTriggerWeightAsOptionalOnly,
								   &setting_type::GetRooWorkspace,
								   &setting_type::GetRooWorkspaceWeightNames,
								   &setting_type::GetRooWorkspaceObjectNames,
								   &setting_type::GetRooWorkspaceObjectArguments)
{
}

void RooWorkspaceWeightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	m_saveTriggerWeightAsOptionalOnly = (settings.*GetSaveRooWorkspaceTriggerWeightAsOptionalOnly)();

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);
	TFile f(settings.GetRooWorkspace().c_str());
	gSystem->AddIncludePath("-I$ROOFITSYS/include");
	m_workspace = (RooWorkspace*)f.Get("w");
	f.Close();
	gDirectory = savedir;
	gFile = savefile;
	m_weightNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceWeightNames)()));

	std::map<int,std::vector<std::string>> objectNames = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceObjectNames)()));
	m_functorArgs = Utility::ParseMapTypes<int,std::string>(Utility::ParseVectorToMap((settings.*GetRooWorkspaceObjectArguments)()));
	for(auto objectName:objectNames)
	{
		for(size_t index = 0; index < objectName.second.size(); index++)
		{
			std::vector<std::string> objects;
			boost::split(objects, objectName.second[index], boost::is_any_of(","));
			for(auto object:objects)
			{
				std::cout<<object.c_str()<<std::endl;
				m_functors[objectName.first].push_back(m_workspace->function(object.c_str())->functor(m_workspace->argSet(m_functorArgs[objectName.first][index].c_str())));
			}
		}
	}
}

void RooWorkspaceWeightProducer::Produce( event_type const& event, product_type & product, 
	                     setting_type const& settings) const
{

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="e_eta")
				{
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				if(arg=="m_iso" || arg=="e_iso")
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
			}
			if(weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly)
			{
				product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else
			{
				product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
		}
	}
	if((product.m_weights.find("idweight_1") != product.m_weights.end()) && (product.m_weights.find("isoweight_1") != product.m_weights.end()))
	{
		product.m_weights["identificationWeight_1"] = product.m_weights["idweight_1"]*product.m_weights["isoweight_1"];
		product.m_weights["idweight_1"] = 1.0;
		product.m_weights["isoweight_1"] = 1.0;
	}
	if((product.m_weights.find("idweight_2") != product.m_weights.end()) && (product.m_weights.find("isoweight_2") != product.m_weights.end()))
	{
		product.m_weights["identificationWeight_2"] = product.m_weights["idweight_2"]*product.m_weights["isoweight_2"];
		product.m_weights["idweight_2"] = 1.0;
		product.m_weights["isoweight_2"] = 1.0;
	}
	if(product.m_weights.find("idIsoWeight_1") != product.m_weights.end())
	{
		product.m_weights["identificationWeight_1"] = product.m_weights["idIsoWeight_1"];
		product.m_weights["idIsoWeight_1"] = 1.0;
	}
	if(product.m_weights.find("idIsoWeight_2") != product.m_weights.end())
	{
		product.m_weights["identificationWeight_2"] = product.m_weights["idIsoWeight_2"];
		product.m_weights["idIsoWeight_2"] = 1.0;
	}
}

// ==========================================================================================

EmbeddedWeightProducer::EmbeddedWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveEmbeddedWeightAsOptionalOnly,
								   &setting_type::GetEmbeddedWeightWorkspace,
								   &setting_type::GetEmbeddedWeightWorkspaceWeightNames,
								   &setting_type::GetEmbeddedWeightWorkspaceObjectNames,
								   &setting_type::GetEmbeddedWeightWorkspaceObjectArguments)
{
}

void EmbeddedWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings) const
{
	//~ double tauTrigWeight = 1.0;
	double dR = 0.0;
	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KGenParticle* genTau = product.m_flavourOrderedGenTaus[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			//~ if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				//~ continue;
			//~ if(m_functors.at(weightNames.first).size() != 2)
			//~ {
				//~ LOG(WARNING) << "TauTauTriggerWeightProducer: two object names are required in json config file. Trigger weight will be set to 1.0!";
				//~ break;
			//~ }
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="e_pt") {
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="gt_pt") {
					args.push_back(genTau->p4.Pt());
				}					
				if(arg=="m_eta") {
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="gt_eta") {
					args.push_back(genTau->p4.Eta());
				}				
				if(arg=="gt1_eta")
				{
					KGenParticle* genTau1Tmp = product.m_flavourOrderedGenTaus[0];
					args.push_back(genTau1Tmp->p4.Eta());
				}
				if(arg=="gt2_eta")
				{
					KGenParticle* genTau2Tmp = product.m_flavourOrderedGenTaus[1];
					args.push_back(genTau2Tmp->p4.Eta());
				}
				if(arg=="gt1_pt")
				{
					KGenParticle* genTau1 = product.m_flavourOrderedGenTaus[0];
					args.push_back(genTau1->p4.Pt());
				}
				if(arg=="gt2_pt")
				{
					KGenParticle* genTau2 = product.m_flavourOrderedGenTaus[1];
					args.push_back(genTau2->p4.Pt());
				}
				if(arg=="e_eta")
				{			
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				if(arg=="m_iso" || arg=="e_iso")
				{
					args.push_back(SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, lepton, std::numeric_limits<double>::max()));
				}
				if(arg=="t_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="t_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="t_eta")
				{
					args.push_back(lepton->p4.Phi());
				}
				if(arg=="t_dm")
				{
					KTau* tau = static_cast<KTau*>(lepton);
					args.push_back(tau->decayMode);
				}
				if(arg=="dR")
				{
					KLepton* lep_1 = product.m_flavourOrderedLeptons[0];
					KLepton* lep_2 = product.m_flavourOrderedLeptons[1];
					//~ std::cout<<sqrt(pow((lep_1->p4.Phi()-lep_2->p4.Phi()),2.0)+pow((lep_1->p4.Eta()-lep_2->p4.Eta()),2.0))<<std::endl;
					args.push_back(sqrt(pow((lep_1->p4.Phi()-lep_2->p4.Phi()),2.0)+pow((lep_1->p4.Eta()-lep_2->p4.Eta()),2.0)));
					dR = sqrt(pow((lep_1->p4.Phi()-lep_2->p4.Phi()),2.0)+pow((lep_1->p4.Eta()-lep_2->p4.Eta()),2.0));
				}
			}
			if(weightNames.second.at(index).find("muonEffTrgWeight") != std::string::npos){
				product.m_weights[weightNames.second.at(index)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			if(weightNames.second.at(index).find("doubleTauTrgWeight") != std::string::npos){
				if(dR < 0.5){
				product.m_weights[weightNames.second.at(index)]=1.0;
			}
				else if(dR < 0.75){
				product.m_weights[weightNames.second.at(index)]=1.07622;
			}
				else if(dR < 1.0){
				product.m_weights[weightNames.second.at(index)]=1.12215;
			}
				else if(dR < 1.25){
				product.m_weights[weightNames.second.at(index)]=1.15148;
			}
				else if(dR < 1.5){
				product.m_weights[weightNames.second.at(index)]=1.10009;
			}
				else if(dR < 1.75){
				product.m_weights[weightNames.second.at(index)]=1.05449;
			}
				else if(dR < 2.0){
				product.m_weights[weightNames.second.at(index)]=1.00991;
			}
				else if(dR < 2.25){
				product.m_weights[weightNames.second.at(index)]=1.02122;
			}
				else if(dR < 2.5){
				product.m_weights[weightNames.second.at(index)]=0.992925;
			}
				else if(dR < 2.75){
				product.m_weights[weightNames.second.at(index)]=0.991791;
			}
				else if(dR < 3.0){
				product.m_weights[weightNames.second.at(index)]=0.980743;
			}
				else if(dR < 3.25){
				product.m_weights[weightNames.second.at(index)]=0.975733;
			}
				else if(dR < 3.5){
				product.m_weights[weightNames.second.at(index)]=0.962583;
			}
				else if(dR < 3.75){
				product.m_weights[weightNames.second.at(index)]=0.962583;
			}
				else if(dR < 4.0){
				product.m_weights[weightNames.second.at(index)]=0.868078;
			}
				else if(dR < 4.25){
				product.m_weights[weightNames.second.at(index)]=0.924142;
			}
				else {
				product.m_weights[weightNames.second.at(index)]=1.0;
			}
		}
			else{				
				if(weightNames.second.at(index).find("triggerWeight") != std::string::npos && m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else
				{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
			}
		}
	}
}

// ==========================================================================================


EETriggerWeightProducer::EETriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveEETriggerWeightAsOptionalOnly,
								   &setting_type::GetEETriggerWeightWorkspace,
								   &setting_type::GetEETriggerWeightWorkspaceWeightNames,
								   &setting_type::GetEETriggerWeightWorkspaceObjectNames,
								   &setting_type::GetEETriggerWeightWorkspaceObjectArguments)
{
}

void EETriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings) const
{
	double eTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="e_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="e_eta")
				{
					KElectron* electron = static_cast<KElectron*>(lepton);
					args.push_back(electron->superclusterPosition.Eta());
				}
				eTrigWeight *= (1.0 - m_functors.at(weightNames.first).at(index)->eval(args.data()));
			}
		}
	}
	if(m_saveTriggerWeightAsOptionalOnly)
	{
		product.m_optionalWeights["triggerWeight_1"] = 1-eTrigWeight;
	}
	else{
		product.m_weights["triggerWeight_1"] = 1-eTrigWeight;
	}
}

// ==========================================================================================

MuMuTriggerWeightProducer::MuMuTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveMuMuTriggerWeightAsOptionalOnly,
								   &setting_type::GetMuMuTriggerWeightWorkspace,
								   &setting_type::GetMuMuTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetMuMuTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetMuMuTriggerWeightWorkspaceObjectArguments)
{
}

void MuMuTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings) const
{
	double muTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
			}
			muTrigWeight *= (1.0 - m_functors.at(weightNames.first).at(index)->eval(args.data()));
		}
	}
	if(m_saveTriggerWeightAsOptionalOnly)
	{
		product.m_optionalWeights["triggerWeight_1"] = 1-muTrigWeight;
	}
	else{
		product.m_weights["triggerWeight_1"] = 1-muTrigWeight;
	}
}

// ==========================================================================================

TauTauTriggerWeightProducer::TauTauTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveTauTauTriggerWeightAsOptionalOnly,
								   &setting_type::GetTauTauTriggerWeightWorkspace,
								   &setting_type::GetTauTauTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetTauTauTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetTauTauTriggerWeightWorkspaceObjectArguments)
{
}

void TauTauTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings) const
{
	double tauTrigWeight = 1.0;

	for(auto weightNames:m_weightNames)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons[weightNames.first];
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			if(m_functors.at(weightNames.first).size() != 2)
			{
				LOG(WARNING) << "TauTauTriggerWeightProducer: two object names are required in json config file. Trigger weight will be set to 1.0!";
				break;
			}
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="t_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="t_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
				if(arg=="t_dm")
				{
					KTau* tau = static_cast<KTau*>(lepton);
					args.push_back(tau->decayMode);
				}
			}
			if(genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
			{
				tauTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
			}
			else
			{
				tauTrigWeight = m_functors.at(weightNames.first).at(index+1)->eval(args.data());
			}
			if(m_saveTriggerWeightAsOptionalOnly)
			{
				product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
			}
			else{
				product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
			}
		}
	}
}

// ==========================================================================================

MuTauTriggerWeightProducer::MuTauTriggerWeightProducer() :
		RooWorkspaceWeightProducer(&setting_type::GetSaveMuTauTriggerWeightAsOptionalOnly,
								   &setting_type::GetMuTauTriggerWeightWorkspace,
								   &setting_type::GetMuTauTriggerWeightWorkspaceWeightNames,
								   &setting_type::GetMuTauTriggerWeightWorkspaceObjectNames,
								   &setting_type::GetMuTauTriggerWeightWorkspaceObjectArguments)
{
}

void MuTauTriggerWeightProducer::Produce( event_type const& event, product_type & product,
						   setting_type const& settings) const
{
	double muTrigWeight(1.0), tauTrigWeight(1.0);

	for(auto weightNames:m_weightNames)
	{
		// muon-tau cross trigger scale factors currently depend only on tau pt and eta
		KLepton* lepton = product.m_flavourOrderedLeptons[weightNames.first];
		KLepton* originalLepton = const_cast<KLepton*>(SafeMap::GetWithDefault(product.m_originalLeptons, const_cast<const KLepton*>(lepton), const_cast<const KLepton*>(lepton)));
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = product.m_flavourOrderedGenLeptons[weightNames.first];
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		for(size_t index = 0; index < weightNames.second.size(); index++)
		{
			if(weightNames.second.at(index).find("triggerWeight") == std::string::npos)
				continue;
			if(lepton->flavour() == KLeptonFlavour::TAU && m_functors.at(weightNames.first).size() != 2)
			{
				LOG(WARNING) << "MuTauTriggerWeightProducer: two object names are required for tau leg in json config file. Trigger weight for this leg will be set to 1.0!";
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = 1.0;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = 1.0;
				}
				break;
			}
			auto args = std::vector<double>{};
			std::vector<std::string> arguments;
			boost::split(arguments,  m_functorArgs.at(weightNames.first).at(index) , boost::is_any_of(","));
			for(auto arg:arguments)
			{
				if(arg=="m_pt" || arg=="t_pt")
				{
					args.push_back(lepton->p4.Pt());
				}
				if(arg=="m_eta" || arg=="t_eta")
				{
					args.push_back(lepton->p4.Eta());
				}
			}
			if(lepton->flavour() == KLeptonFlavour::TAU)
			{
				if(genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY)
				{
					tauTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
				}
				else
				{
					tauTrigWeight = m_functors.at(weightNames.first).at(index+1)->eval(args.data());
				}
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = tauTrigWeight;
				}
			}
			else
			{
				muTrigWeight = m_functors.at(weightNames.first).at(index)->eval(args.data());
				if(m_saveTriggerWeightAsOptionalOnly)
				{
					product.m_optionalWeights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = muTrigWeight;
				}
				else{
					product.m_weights[weightNames.second.at(index)+"_"+std::to_string(weightNames.first+1)] = muTrigWeight;
				}
			}
		}
	}
	if (product.m_flavourOrderedLeptons[0]->p4.Pt()>23.0){
		product.m_weights["triggerWeight_1"] = product.m_optionalWeights["triggerWeight_singleMu_1"];
		product.m_weights["triggerWeight_2"] = 1.0;
	}else{
		product.m_weights["triggerWeight_1"] = product.m_optionalWeights["triggerWeight_muTauCross_1"];
		product.m_weights["triggerWeight_2"] = product.m_optionalWeights["triggerWeight_muTauCross_2"];
	}
}
