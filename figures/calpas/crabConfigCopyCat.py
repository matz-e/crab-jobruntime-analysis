import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'calpas_test_KillResubmit{0}'
config.General.requestName = 'calpas{0}'
config.General.workArea = 'crabby'
i = 55
while os.path.exists(os.path.join(config.General.workArea, 'crab_' + config.General.requestName.format(i))):
    i += 1
config.General.requestName = config.General.requestName.format(i)
config.General.instance = 'mmascher-dev6.cern.ch'
config.General.activity = 'analysistest'
config.General.transferOutputs = False

config.section_("JobType")
config.JobType.pluginName = 'CopyCat'
config.JobType.psetName = 'pset_tutorial_analysis.py'
config.JobType.copyCatTaskname = '160901_144946:calpas_crab_DYJetsM50'
config.JobType.copyCatInstance = 'prod'

config.section_("Data")
# config.Data.ignoreLocality = True
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
# config.Data.useParent = True
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 9 * 3600
config.Data.publication = False

# config.section_("Debug")
# config.Debug.collector = 'vocms0115.cern.ch'
# config.Debug.scheddName = 'crab3test-8@vocms058.cern.ch'

config.section_("Site")
config.Site.storageSite = 'T2_IT_Legnaro'
