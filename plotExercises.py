import os
import sys
import time
from array import array
from math import sqrt

import ROOT
from PlotStack4l import PlotStack4l
from ZZStyle import *

#get_ipython().magic(u'jsroot on')

#today=datetime.datetime.today().strftime('%m%d')
#today='1220' # datetime.datetime.today().strftime('%m%d')                       

#now  = datetime.datetime.today()
#now_1 = now - datetime.timedelta(days=1)
#yesterday=now_1.strftime('%m%d')

# voms-proxy-init generated user proxy file to access the xrootd servers
#os.environ['X509_USER_PROXY'] = '/eos/user/b/bockjoo/mySWAN/cmsuser.proxy'
os.environ['X509_USER_PROXY'] = '/home/bockjoo/.cmsuser.proxy'
if os.path.isfile(os.environ['X509_USER_PROXY']):
    pass
else:
    print "os.environ['X509_USER_PROXY'] ",os.environ['X509_USER_PROXY']
    print "You need to put your grid proxy somewhere under /eos/user/<your alpha>/<Username>"
    sys.exit(1)
#os.environ['X509_CERT_DIR'] = '/cvmfs/grid.cern.ch/etc/grid-security/certificates'
#os.environ['X509_VOMS_DIR'] = '/cvmfs/grid.cern.ch/etc/grid-security/vomsdir'
os.environ['X509_CERT_DIR'] = '/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates'
os.environ['X509_VOMS_DIR'] = '/cvmfs/cms.cern.ch/grid/etc/grid-security/vomsdir'
    
#root_file="root://cms-xrd-global.cern.ch//store/user/nvanegas/BckgndW+Jets/tag_1_delphes_events01.root"
#tfil = ROOT.TFile(root_file)
#tfil = ROOT.TFile.Open(root_file)

#print "Listing Tree"

#tfil.ls()



# In[2]:


#inputlist = "filelist_4l_2016_Spring16_AN_Florida_miniaod_one.txt"
inputlist = "filelist_4l_2016_Spring16_AN_Bari_miniaod_read_from_xroot.txt"
inputlist = "filelist_4l_2016_Spring16_AN_Florida_miniaod.txt"
histlabel =  "hMZ_3"
histlabel = "hLogLinXM4l_T_8";
if len(sys.argv) > 1 : histlabel = sys.argv[1]
if len(sys.argv) > 2 : histlabel = sys.argv[1] ; inputlist = sys.argv[2]
# WARNING: depending on histolabel, modify the declaration and the settings of hframe below

thestack = PlotStack4l(inputlist,histlabel)


# In[3]:


if 'plotExercises' == 'plotExercises' :
  thestack.setSamplesNames4l()
  print "\t Analysing samples for " , thestack.whichchannel , " analysis"
    
  print "Histogram label is= " , thestack.histolabel
  #// Final yields
  os.system("[ -d plots ] || mkdir plots")

  #Char_t yieldsOUT[500]
  #sprintf(yieldsOUT,"plots/yields_%s_%s.txt",whichchannel,whichenergy)
  yieldsOUT = ("plots/yields_%s_%s.txt" % (thestack.whichchannel, thestack.whichenergy))
  if ( "hM4l_9" in thestack.histolabel ):
    print "Opening a file for final numbers= " , yieldsOUT 
    thestack.outputyields = open(yieldsOUT, "w")
  #// Execute the analysis

  thestack.plotm4l(thestack.histolabel)

  #// close file for final yields
  if ( "hM4l_9" in thestack.histolabel ) : thestack.outputyields.close()
 
  sys.exit(0)
