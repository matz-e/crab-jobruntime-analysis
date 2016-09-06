import FWCore.ParameterSet.Config as cms

process = cms.Process("h2taus")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'file:/home/t3cms/calpas/h2taus/CMSSW_8_0_16/src/miniAOD/miniAnalyzer/SUSYGluGluToHToTauTau_M-160_13TeV_RunIISpring16MiniAODv1.root'
'file:/home/t3cms/calpas/h2taus/CMSSW_8_0_16SW_8_0_16/src/miniAOD/miniAnalyzer/SUSYGluGluToHToTauTau_M-160_13TeV_RunIISpring16MiniAODv2.root'
#'/store/mc/RunIISpring16MiniAODv2/SUSYGluGluToHToTauTau_Mau_M-160_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/90000/66445A95-3151-E611-AA07-0090FAA579F0.root'
    )
)

#METSignificance recomputation
process.load("RecoMET.METProducers.METSignificance_cfi")
process.load("RecoMET.METProducers.METSignificanceParams_cfi")
process.METSequence = cms.Sequence(process.METSignificance)

#MVA electron ID
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data forma
switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff']
#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)


process.h2taus      = cms.EDAnalyzer('miniAnalyzer',
    vertices        = cms.InputTag("offlineSlimmedPrimaryVertices"),
    muons           = cms.InputTag("slimmedMuons"),
    electrons       = cms.InputTag("slimmedElectrons"),
    taus            = cms.InputTag("slimmedTaus"),
    jets            = cms.InputTag("slimmedJets"),
    pu              = cms.InputTag("slimmedAddPileupInfo"),
    rho             = cms.InputTag("fixedGridRhoFastjetAll"),
    eleMediumIdMap  = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90"),
    eleTightIdMap   = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80"),
    mvaValuesMap    = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
    mets            = cms.InputTag("slimmedMETs"),
    metspuppi       = cms.InputTag("slimmedMETsPuppi"),
    metCov          = cms.InputTag("METSignificance", "METCovariance"),
    #bits            = cms.InputTag("TriggerResults","","HLT"),
    bits            = cms.InputTag("TriggerResults::HLT2"),
    objects         = cms.InputTag("selectedPatTrigger"),
    prescales       = cms.InputTag("patTrigger"),
    mutauFilterName = cms.vstring(
    "HLT_IsoMu18_v3",
    "HLT_IsoMu20_v4",
    "HLT_IsoMu22_v3",
    "HLT_IsoMu22_eta2p1_v2",
    "HLT_IsoMu24_v2",
    "HLT_IsoMu27_v4",
    "HLT_IsoTkMu18_v3",
    "HLT_IsoTkMu20_v5",
    "HLT_IsoTkMu22_eta2p1_v2",
    "HLT_IsoTkMu22_v3",
    "HLT_IsoTkMu24_v2",
    "HLT_IsoTkMu27_v4",
    "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v5",
    "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v5",
    "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2",
    "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2",
    "HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v2",
    ),
    etauFilterName = cms.vstring(
    "HLT_Ele23_WPLoose_Gsf_v4",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_v2",
    "HLT_Ele25_WPTight_Gsf_v2",
    "HLT_Ele25_eta2p1_WPLoose_Gsf_v2",
    "HLT_Ele25_eta2p1_WPTight_Gsf_v2",
    "HLT_Ele27_WPLoose_Gsf_v2",
    "HLT_Ele27_WPTight_Gsf_v2",
    "HLT_Ele27_eta2p1_WPLoose_Gsf_v3",
    "HLT_Ele27_eta2p1_WPTight_Gsf_v3",
    "HLT_Ele32_eta2p1_WPTight_Gsf_v3",
    "HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v3",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v2",
    "HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2",
    "HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v2",
    ),
    tautauFilterName = cms.vstring(
    "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v2",
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3",
    "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v5",
    ),
    emuFilterName = cms.vstring(
    "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v4",
    "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v4",
    "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4",
    "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v4",
    "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v2",
    "HLT_IsoMu18_v3",
    "HLT_IsoMu20_v4",
    "HLT_IsoMu22_v3",
    "HLT_IsoMu22_eta2p1_v2",
    "HLT_IsoMu24_v2",
    "HLT_IsoMu27_v4",
    "HLT_IsoTkMu18_v3",
    "HLT_IsoTkMu20_v5",
    "HLT_IsoTkMu22_eta2p1_v2",
    "HLT_IsoTkMu22_v3",
    "HLT_IsoTkMu24_v2",
    "HLT_IsoTkMu27_v4",
    "HLT_Ele23_WPLoose_Gsf_v4",
    "HLT_Ele24_eta2p1_WPLoose_Gsf_v2",
    "HLT_Ele25_WPTight_Gsf_v2",
    "HLT_Ele25_eta2p1_WPLoose_Gsf_v2",
    "HLT_Ele25_eta2p1_WPTight_Gsf_v2",
    "HLT_Ele27_WPLoose_Gsf_v2",
    "HLT_Ele27_WPTight_Gsf_v2",
    "HLT_Ele27_eta2p1_WPLoose_Gsf_v3",
    "HLT_Ele27_eta2p1_WPTight_Gsf_v3",
    "HLT_Ele32_eta2p1_WPTight_Gsf_v3",
    ),
 )


process.p = cms.Path(process.METSequence * 
     process.egmGsfElectronIDSequence * 
     process.Pathh2taus)



process.TFileService = cms.Service("TFileService", fileName = cms.string('output.root'))
