from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'DYJetsM50'
config.section_('JobType')
config.JobType.psetName = '../python/ConfFile_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['output.root']
config.JobType.maxMemoryMB = 2500
config.section_('Data')
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
config.Data.totalUnits = 90000000
config.Data.unitsPerJob = 10000
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/calpas/hto2taus/flattuple/v2'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_PT_NCG_Lisbon'

