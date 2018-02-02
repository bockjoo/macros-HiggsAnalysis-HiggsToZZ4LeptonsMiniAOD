
# coding: utf-8

# In[1]:
# References
# [1] http://indico.hep.manchester.ac.uk/getFile.py/access?resId=0&materialId=slides&confId=267

# ported from https://archer.ihepa.ufl.edu:9999/view/cmsdas2018/macros-HiggsAnalysis-HiggsToZZ4LeptonsMiniAOD/PlotStack4l.C


from ROOT import *
import ROOT
import os
from array import array
from math import *
import datetime
import time
#float_array = array("f",values)
#get_ipython().magic(u'jsroot on')

##ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include/")
##ROOT.gSystem.AddIncludePath("-Iinclude/")
#ROOT.gSystem.Load("/cvmfs/sft.cern.ch/lcg/releases/LCG_85swan3/vdt/0.3.6/x86_64-slc6-gcc49-opt/lib/libvdt.so")
##ROOT.gSystem.Load("../../lib/libHiggsAnalysisCombinedLimit.so")
#ROOT.gSystem.Load("/softraid/bockjoo/combine_LCG85_swan3/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")
##ROOT.gSystem.Load("include/HiggsCSandWidth_cc.so")
##ROOT.gSystem.Load("include/HiggsCSandWidthSM4_cc.so")
#ROOT.gSystem.Load("/softraid/bockjoo/combine_LCG85_swan3/HiggsAnalysis/CombinedLimit/HiggsCSandWidth/include/HiggsCSandWidth_cc.so")
#ROOT.gSystem.Load("/softraid/bockjoo/combine_LCG85_swan3/HiggsAnalysis/CombinedLimit/HiggsCSandWidth/include/HiggsCSandWidthSM4_cc.so")

## Setup python 
# import CMS tdrStyle
from tdrStyle import *
setTDRStyle()

# import some more python modules
import sys,glob
from array import array
import string
from scipy.special import erf
import math
#from bandUtils import *
from ZZStyle import *


# In[2]:


class PlotStack4l:
 #
 # Usage: thestack = PlotStack4l() ; thestack.plotstack4l()
 #

 #  //TSystem LoadLib;
 #  //LoadLib.Load("/cmshome/nicola/slc6/MonoHiggs/Analysis13TeV/CMSSW_7_2_0/lib/slc6_amd64_gcc481/libHiggsHiggs_CS_and_Width.so");
 #  //getMassWindow(500.);

 #  //inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod_m4l_MC.txt";
 #  //inputfile="filelist_4e_2016_Spring16_AN_Bari_miniaod_met_step3.txt";
 #  //inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod.txt";
 #inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod_met_step8.txt"
 inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod_read_from_xroot.txt"
 inputfile="filelist_4l_2016_Spring16_AN_FNAL_miniaod.txt"
 inputfile="filelist_4l_2016_Spring16_AN_FNAL_miniaod_xrootd.txt "
 inputfile="filelist_4l_2016_Spring16_AN_Florida_miniaod.txt" # Same as filelist_4l_2016_Spring16_AN_Bari_miniaod.txt

 #  //inputfile="test4mu_13TeV.txt";
    
 def __init__(self,inputlist,histlabel, nrebin ):
  # string
  self.Vdatasetnamebkg = []
  self.Vdatasetnamesig = []
  self.Vdatasetnamedata = []
  self.Vdatasetnamebkgdata = []
  self.Vlabelbkg = []
  self.Vlabelsig = []
  self.Vlabeldata = []
  self.Vlabelbkgdata = []
  # float
  self.Vxsectionbkg = []
  self.Vxsectionsig = []
  self.Vxsectiondata = []
  self.Vxsectionbkgdata = []
  # color_t
  self.Vcolorbkg = []
  self.Vcolorsig = [] #/*, Vcolordata*/
  
  self.Nbins = nrebin ; self.Xmin = 0.0; self.Xmax = 999.0
  self.nRebinZ_X = 0.0; self.Ymax = 999.0
  self.histosdir = "/"
  #self.inputfile = "filelist_4l_2016_Spring16_AN_FNAL_miniaod.txt"
  #self.inputfile = "filelist_4l_2016_Spring16_AN_FNAL_miniaod_xrootd.txt"
  #self.inputfile = "filelist_4l_2016_Spring16_AN_Florida_miniaod.txt"

  self.inputfile = inputlist
  self.whichchannel = ""
  self.whichenergy = ""
  self.whichsample = ""
  self.histotitle =""

  self.outputyields ="" # ofstream

  self.LoadLib =ROOT.TSystem() 
  self.histolabel = histlabel

  self.useLogY = True
  self.useLogX = False
  self.useRatio = True
  self.useDYJets=True
  self.useDYJetsFromData=False  
  self.nRebin=1

  self.errorZZ=0.
  self.errorH125=0.
  self.errorH126=0.
  self.errorH200=0.
  self.errorH350=0.
  self.errorH500=0.
  self.errorH800=0.
  self.fullPathToTheGridProxy = ''
  if "X509_USER_PROXY" in os.environ:
   if os.path.isfile(os.environ['X509_USER_PROXY']):
    self.fullPathToTheGridProxy = os.environ['X509_USER_PROXY']
    pass
  self.prefixForGlobalXrootdRedirector = 'root://cms-xrd-global.cern.ch/'
  self.outputyields = '/dev/null'

 def plotstack4l (self): # the main method or an example usage
  #//TSystem LoadLib
  #//LoadLib.Load("/cmshome/nicola/slc6/MonoHiggs/Analysis13TeV/CMSSW_7_2_0/lib/slc6_amd64_gcc481/libHiggsHiggs_CS_and_Width.so")
  #//getMassWindow(500.)
    
  #//inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod_m4l_MC.txt"
  #//inputfile="filelist_4e_2016_Spring16_AN_Bari_miniaod_met_step3.txt"
  #//inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod.txt"
  #inputfile="filelist_4l_2016_Spring16_AN_Bari_miniaod_met_step8.txt"
  #//inputfile="test4mu_13TeV.txt"
  #inputfile = self.inputfile
  print "INFO storing sample names to variables for ",self.inputfile
  self.setSamplesNames4l()
  print "\t Analysing samples for " , self.whichchannel , " analysis" 
  #return

  #//WARNING: depending on histolabel, modify the declaration and the settings of hframe below
  #//also choose a sensible value for nRebin

  #//std::string histolabel = "hPUvertices";    #// numPU
  #//std::string histolabel = "hPUvertices_ReWeighted";    #// numPY reweighted

  #// Step 0
  #// std::string histolabel = "hPFMET_0" #// PFMET
  
  #// Step 1  loose iso
  #//std::string histolabel = "hPFMET_1" #// PFMET                                                                                   

  #//std::string histolabel = "hPtLep_0" #// pt not cuts (only pt>5)
  #//std::string histolabel = "hIsoLep_0" #// PF isol _ delta B
  #//std::string histolabel = "hSipLep_0" #// SIP
  #//std::string histolabel = "hDxyLep_0" #// d_xy
  #//std::string histolabel = "hDzLep_0" #// d_z
  #//std::string histolabel = "hMuHitLep_0" #// n. muon hits
  #//std::string histolabel = "hPxHitLep_0" #// n. pixel hits
  #//std::string histolabel = "hTKLayLep_0" #// n. tracker layers
  #//std::string histolabel = "hTKIsoLep_0" #// track isolation = sumpT

  #// ****** Standard candle: Z1 selection: step 3 ******

  #// std::string histolabel = "hMZ_3";    #// Z mass 
  #//std::string histolabel = "hMZBB_3";    #// Z mass 
  #//std::string histolabel = "hMZEE_3";    #// Z mass 
  #//std::string histolabel = "hPtZ_3" #// Z pt 
  #//std::string histolabel = "hYZ_3" #// Z Y

  #//std::string histolabel = "hPtLep_3";    #// pT lepton from Z 
  #//std::string histolabel = "hIsoLep_3";    #// isolation of lowest pT lepton from Z 
  #//std::string histolabel = "hSipLep_3";  #// sip the lowest pT lepton from Z
  #//std::string histolabel = "hIpLep_3";   #// IP of the lowest pT lepton from Z
  #//std::string histolabel = "hIpErLep_3";   #// Iperror of the lowest pT lepton from Z

  #//std::string histolabel = "hIso_3";    #// worst isolation value of lepton not coming from Z1
  #//std::string histolabel = "hSip_3";  #// worst sip value of lepton not coming from Z1
  #//std::string histolabel = "hIp_3";   #// worst IP value of lepton not coming from Z1

  #//std::string histolabel = "hMjj_3" #// mass of di-jet for VBF analysis
  #//std::string histolabel = "hDjj_3" #// delta eta between jets for VBF analysis
  #//std::string histolabel = "hVD_3" #// Fisher discriminant for VBF analysis

  #// std::string histolabel = "hPFMET_3" #// PFMET
  #// std::string histolabel = "hLogLinXPFMET_3" #//PF MET log
  #// ****** After cuts on ,Z1, mZ2 and pT >20/10: step 5 ******

  #//std::string histolabel = "hMZ1_5";    #// Z1 mass   
  #//std::string histolabel = "hMZ2_5";    #// Z2 mass 
  #//std::string histolabel = "hM4l_5";    #// 4l mass 

  #//std::string histolabel = "hIso_5";    #// worst isolation 
  #//std::string histolabel = "hSip_5";  #// worst sip 
  #//std::string histolabel = "hIp_5";   #// worst IP


  #// After full selection
  #//std::string histolabel = "hM4l_7" #// 4l mass after full selection but m4l > 70

  #//std::string histolabel = "hM4l_8" #// 4l mass after full selection
  #//std::string histolabel = "hM4l_9" #// 4l mass after full selection
  
  #//std::string histolabel = "hM4l_8_100_800" #// 4l mass in the range [100,800] after full selection
  #//std::string histolabel = "hMZ1_8" #// Z1 mass after full selection
  #//std::string histolabel = "hMZ2_8" #// Z2 mass after full selection
  #//std::string histolabel = "hMZ1_noFSR_8" #// Z1 mass after full selection without FSR recovery
  #//std::string histolabel = "hMZ2_noFSR_8" #// Z2 mass after full selection without FSR recovery
  #//std::string histolabel = "hPtZ1_8" #// Z1 pt after full selection
  #//std::string histolabel = "hPtZ2_8" #// Z2 pt after full selection
  #//std::string histolabel = "hYZ1_8" #// Z1 rapidity after full selection
  #//std::string histolabel = "hYZ2_8" #// Z2 rapidity after full selection
  #//std::string histolabel = "hIso_8" #// worst isolated lepton: isolation value after full selection
  #//std::string histolabel = "hSip_8" #// worst sip lepton: sip value after full selection
  #//std::string histolabel = "hMELA_8" #// MELA discriminant after full selection 
  #//std::string histolabel = "hPFMET_8" #// PFMET
  #//std::string histolabel = "hLogLinXPFMET_8" #//PF MET log
  #//std::string histolabel = "hM4l_T_8" #// Transverse mass
  #self.histolabel = "hLogLinXM4l_T_8" #//PF MET log
  #//std::string histolabel = "DPHI_8" #// DeltaPhi - 4l + MET

  #//std::string histolabel = "hDjj_8" #// delta eta between jets for VBF analysis
  #//std::string histolabel = "hMjj_8" #// dimass between jets for VBF analysis

  #//std::string histolabel = "hPFMET_10"
  #//std::string histolabel = "hNbjets" #// Number of b-jets
  #//std::string histolabel = "hNgood" #// Number of good leptons  

  print "Histogram label is= " , self.histolabel 
  
  #// Final yields
  os.system("[ -d plots ] || mkdir plots")

  #Char_t yieldsOUT[500]
  #sprintf(yieldsOUT,"plots/yields_%s_%s.txt",whichchannel,whichenergy)
  yieldsOUT = ("plots/yields_%s_%s.txt" % (self.whichchannel, self.whichenergy))
  if ( "hM4l_9" in self.histolabel ):
    print "Opening a file for final numbers= " , yieldsOUT 
    self.outputyields = open(yieldsOUT, "w")
    

  
  #// Execute the analysis

  self.plotm4l(self.histolabel)
  
  #// close file for final yields
  if ( "hM4l_9" in self.histolabel ) : self.outputyields.close()
    

 def setSamplesNames4l(self):

  infile = open(self.inputfile, "r")
  if (infile == 0): print "Cannot open " , self.inputfile ; return; 

  if ( "2011" in self.inputfile ):
    self.whichenergy="7TeV"
    self.whichsample="7TeV"
  elif ( "RunI_" in self.inputfile ):
    self.whichenergy="RunI_"
    self.whichsample="8TeV"
  elif ( "2015" in self.inputfile ):
    self.whichenergy="13TeV"
    self.whichsample="13TeV"
  elif ( "2016" in self.inputfile ):
    self.whichenergy="13TeV"
    self.whichsample="13TeV"

  print "Doing plot for " , self.whichenergy , "  and " , self.whichsample 
  
  if ( "4l" in self.inputfile ):
    print "Plotting 4e+4mu+2e2mu combined in 4lepton plots" 
    self.whichchannel="4l"
    self.histosdir="histos4mu_25ns"
    print "This is " , self.whichchannel
  elif ( "4mu" in self.inputfile ):
    print "Plotting 4mu" 
    self.whichchannel="4#mu"
    self.histosdir="histos4mu_25ns"
  elif ( "4e" in self.inputfile ):
    print "Plotting 4e" 
    self.whichchannel="4e"
    self.histosdir="histos4e_25ns"
  elif ( "2e2mu" in self.inputfile ):
    print "Plotting 2e2mu" 
    self.whichchannel="2e2#mu"
    self.histosdir="histos2e2mu_25ns"
    
  #global self.Vdatasetnamedata
  #global self.Vlabeldata
  #self.Vdatasetnamebkg = []
  #self.Vdatasetnamesig = []
  #inputfilename=""
  #for inputfilename in infile:
  #  print "Reading |" , inputfilename.strip(),"|"
  #  print "Reading |" , "root://cmseos.fnal.gov//store/group/lpchzz4leptons/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root","|"
  #  break
  #return

  for unstrippedinputfilename in infile:
    inputfilename = unstrippedinputfilename.strip()
    if inputfilename.startswith('/store') :
      #print "The input file starts with /store. Using xrootd "
      #self.setupGridProxy()
      inputfilename = self.prefixForGlobalXrootdRedirector + inputfilename
    print "Reading |" , inputfilename,"|" 
    # DATA
    #if(inputfilename.find("_DoubleMuon_")<200): #// as many times as it occurs in the input file
    if( "_DoubleMuon_" in inputfilename ):
      self.Vdatasetnamedata.append(inputfilename)
      self.Vlabeldata.append("Double Muon - 2016")
      self.Vxsectiondata.append(1.) #//pb
      
             
    #if(inputfilename.find("_DoubleEG_")<200): #// as many times as it occurs in the input file
    if( "_DoubleEG_" in inputfilename ):
      self.Vdatasetnamedata.append(inputfilename)
      self.Vlabeldata.append("Double EGamma - 2016")
      self.Vxsectiondata.append(1.) #//pb
       
    
    #if(inputfilename.find("_SingleElectron_")<200): #// as many times as it occurs in the input file
    if( "_SingleElectron_" in inputfilename ):
      self.Vdatasetnamedata.append(inputfilename)
      self.Vlabeldata.append("Single Electron - 2016")
      self.Vxsectiondata.append(1.) #//pb
       

    #if(inputfilename.find("_SingleMuon_")<200): #// as many times as it occurs in the input file
    if( "_SingleMuon_" in inputfilename ):
      self.Vdatasetnamedata.append(inputfilename)
      self.Vlabeldata.append("Single Muon - 2016")
      self.Vxsectiondata.append(1.) #//pb
       
    
    #if(inputfilename.find("_MuonEG_")<200): #// as many times as it occurs in the input file
    if( "_MuonEG_" in inputfilename ):
      self.Vdatasetnamedata.append(inputfilename)
      self.Vlabeldata.append("Muon EGamma - 2016")
      self.Vxsectiondata.append(1.) #//pb
        
       

    #//Z+X from data
    #if(inputfilename.find("Z+X")<85):
    if( "Z+X" in inputfilename ):
      self.self.Vdatasetnamebkgdata.append(inputfilename)
      self.self.Vlabelbkgdata.append("Z+X")
      self.self.Vxsectionbkgdata.append(1.) #//pb
    #// SIGNAL
    elif( "Higgs_scalar" in inputfilename or "Higgs_scalar_nohdecay" in inputfilename ):
      #// if( (inputfilename.find("1GeV")<200) ):
      #// 	self.Vdatasetnamesig.append(inputfilename)
      #// 	self.Vlabelsig.append("m_{DM=1 GeV/c^{2, Zprime")
      #// 	self.Vxsectionsig.append(1.) #//pb
      #// 	self.Vcolorsig.append(ROOT.kOrange-3)
      #// 
      #// if( (inputfilename.find("10GeV")<200) ):
      #// 	self.Vdatasetnamesig.append(inputfilename)
      #// 	self.Vlabelsig.append("m_{DM=10 GeV/c^{2, Zprime")
      #// 	self.Vxsectionsig.append(1.) #//pb
      #// 	self.Vcolorsig.append(ROOT.kOrange-3)
      #// 
      #// if( (inputfilename.find("100GeV")<200) ):
      #// 	self.Vdatasetnamesig.append(inputfilename)
      #// 	self.Vlabelsig.append("m_{DM=100 GeV/c^{2, Zprime")
      #// 	self.Vxsectionsig.append(1.) #//pb
      #// 	self.Vcolorsig.append(ROOT.kOrange-3)
      #// 
      #// if( (inputfilename.find("500GeV")<200) ):
      #// 	self.Vdatasetnamesig.append(inputfilename)
      #// 	self.Vlabelsig.append("m_{DM=500 GeV/c^{2, Zprime")
      #// 	self.Vxsectionsig.append(1.) #//pb
      #// 	self.Vcolorsig.append(ROOT.kOrange-3)
      #// 
      #// if( (inputfilename.find("1000GeV")<200) ):
      #// 	self.Vdatasetnamesig.append(inputfilename)
      #// 	self.Vlabelsig.append("m_{DM=1 TeV/c^{2, Zprime")
      #// 	self.Vxsectionsig.append(1.) #//pb
      #// 	self.Vcolorsig.append(ROOT.kOrange-3)
      #// 
      pass
    #// 2HDM
    elif( "2HDM_MZp" in inputfilename ):
        #if( (inputfilename.find("600")<200) ):
        if( "600" in inputfilename ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=600 GeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        if( "800" in inputfilename ):
            #if( (inputfilename.find("800")<200) ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=800 GeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        if( "1000" in inputfilename ):
            #if( (inputfilename.find("1000")<200) ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=1000 GeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        if( "1200" in inputfilename ):
            #if( (inputfilename.find("1200")<200) ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=1.2 TeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        if( "1400" in inputfilename ):
            #if( (inputfilename.find("1400")<200) ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=1.4 TeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        #if( (inputfilename.find("1700")<200) ):
        if( "1700" in inputfilename ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=1.7 TeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb
            self.Vcolorsig.append(ROOT.kOrange-3)
     
        #if( "2000" in inputfilename ):
        #if( (inputfilename.find("2000")<200) ):
        if( "2000" in inputfilename ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=2. TeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb                                                                                                                                                     
            self.Vcolorsig.append(ROOT.kOrange-3)
      
        #if( (inputfilename.find("2500")<200) ):
        if( "2500" in inputfilename ):
            self.Vdatasetnamesig.append(inputfilename)
            self.Vlabelsig.append("m_{Z'}=2.5 TeV/c^{2}, Zprime")
            self.Vxsectionsig.append(1.) #//pb                                                                                                                                                     
            self.Vcolorsig.append(ROOT.kOrange-3)

    #------>        
    #// ZpBaryonic
    #elif( "2HDM_MZp" in inputfilename )
    elif( "ZpBaryonic_MZp" in inputfilename and "MChi-1_" in inputfilename ):
      #if( (inputfilename.find("10000_")<200) ):
      if( "10000_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=10 TeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("1000_")<200) ):
      if( "1000_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=1 TeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("100_")<200) ):
      if( "100_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=100 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("10_")<200) ):
      if( "10_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=10 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("2000_")<200) ):
      if( "2000_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B=2}} TeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("200_")<200) ):
      if( "200_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=200 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("20_")<200) ):
      if( "20_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=20 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("300_")<200) ):
      if( "300_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=300 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("500_")<200) ):
      if( "500_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=500 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)
      #if( (inputfilename.find("50_")<200) ):
      if( "50_" in inputfilename ):
        self.Vdatasetnamesig.append(inputfilename)
        self.Vlabelsig.append("m_{Z'_{B}}=50 GeV, m_{#chi}=1 GeV")
        self.Vxsectionsig.append(1.) #//pb
        self.Vcolorsig.append(ROOT.kOrange-3)        
    #// background higgs
    elif("GluGluHToZZTo4L" in inputfilename or 
        "SMHiggsToZZTo4L" in inputfilename   or 
        "VBF_HToZZTo4L" in inputfilename     or
        "VBF_ToHToZZTo4L" in inputfilename   or
        "TTbarH_HToZZTo4L" in inputfilename  or
        "ttH_HToZZ_4L" in inputfilename  or
        "ZH_HToZZ_4LFilter" in inputfilename  or 
        "ZH_ll_h2l2v" in inputfilename or
        "WplusH_HToZZTo4L" in inputfilename or
        "WminusH_HToZZTo4L" in inputfilename  or 
        "WH_ZH_HToZZ_4LFilter" in inputfilename ):  #// provided that signal samples contain 'GluGluHToZZTo4L'
      #//self.Vdatasetnamebkg.append(inputfilename)
      if( "M125" in inputfilename and "GluGluHToZZTo4L_M125_13TeV_powheg" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ggH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange-3)
        #//print "ggH" 
      

      #if( (inputfilename.find("M125")<200 and (inputfilename.find("VBF")<200)) ):
      if( "M125" in inputfilename and "VBF" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("VBF H, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange-2)
        #//print "VBF H" 
      
      
      #if( (inputfilename.find("M125")<200 and (inputfilename.find("ZH_HToZZ_4L")<200)) ):
      if( "M125" in inputfilename and "ZH_HToZZ_4L" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ZH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange-1)
        #//print "VH" 
      
      
      #if( (inputfilename.find("ZH_ll_h2l2v")<200)):
      if( "ZH_ll_h2l2v" in inputfilename ):
          self.Vdatasetnamebkg.append(inputfilename)
          self.Vlabelbkg.append("ZH,ll,2l2#nu, m_{H}=125 GeV")
          self.Vxsectionbkg.append(1.) #//pb                                                                                                                                                          
          self.Vcolorbkg.append(ROOT.kOrange-1)
          #//print "ZH" ;               
      


      #if( (inputfilename.find("M125")<200 and (inputfilename.find("WplusH")<200)) ):
      if( "M125" in inputfilename and "WplusH" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WplusH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange+2)
        #//print "VH" 
      
      #if( (inputfilename.find("M125")<200 and (inputfilename.find("WminusH")<200)) ):
      if( "M125" in inputfilename and "WminusH" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WminusH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange+3)
        #//print "VH" 
      
      
      #if( (inputfilename.find("M125")<200 and (inputfilename.find("WH")<200)) ):
      if( "M125" in inputfilename and "WH" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange-1)
        #//print "VH" 
      
      
      #if( (inputfilename.find("M125")<200 and (inputfilename.find("ttH")<200)) ):
      if( "M125" in inputfilename and "ttH" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ttH, m_{H}=125 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange)
        #//print "ttH" 
      
      
      
      #if( (inputfilename.find("M-126")<200 and !(inputfilename.find("GluGluToHToZZTo4L")<200)) ):
      if( "M-126" in inputfilename and "GluGluToHToZZTo4L" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ggH, m_{H}=126 GeV")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kOrange-3)
        
    #// BACKGROUND from other sources
    else:  #// provided that everything that is neither data nor signal is background
      #//self.Vdatasetnamebkg.append(inputfilename)
      
      #// qqZZ to 4l
      if ( "_ZZTo4L_13TeV_powheg_pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*},ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      if ( "_ZZ_TuneCUETP8M1_13TeV-pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*},ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 4mu
      if ( "_ZZTo4mu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*},ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      
      
      #// qqZZ to 4e
      if ( "_ZZTo4e" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 4tau
      if ( "_ZZTo4tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z\\#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 2e2mu
      if ( "_ZZTo2e2mu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 2mu2tau
      if ( "_ZZTo2mu2tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 2e2tau
      if ( "_ZZTo2e2tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// qqZZ to 2l2nu
      if ( "_ZZTo2L2Nu_13TeV_powheg_pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*},ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
      

      #// ggZZ 2L2L'
      if ( "GluGluToZZTo2L2L" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("GluGluToZZTo2L2L_8TeV-gg2zz-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        

      #// ggZZ 4L
      if ( "GluGluToZZTo4L" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("GluGluToZZTo4L_8TeV-gg2zz-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
           
    
      
      #// ggZZ 4e
      if ( "GluGluToZZTo4e" in inputfilename or "GluGluToContinToZZTo4e" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
           
        
       #// ggZZ 4mu
      if ( "GluGluToZZTo4mu" in inputfilename or "GluGluToContinToZZTo4mu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        
 
      #// ggZZ 4tau
      if ( "GluGluToZZTo4tau" in inputfilename or "GluGluToContinToZZTo4tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        

       #// ggZZ 2e2mu
      if ( "GluGluToZZTo2e2mu" in inputfilename or "GluGluToContinToZZTo2e2mu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        
 
       #// ggZZ 2e2tau
      if ( "GluGluToZZTo2e2tau" in inputfilename or "GluGluToContinToZZTo2e2tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        

      #// ggZZ 2mu2tau
      if ( "GluGluToZZTo2mu2tau" in inputfilename or "GluGluToContinToZZTo2mu2tau" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        

      #// ggZZ 2l2nu
      if ("GluGluToContinToZZTo2e2nu" in inputfilename or 
         "GluGluToContinToZZTo2mu2nu" in inputfilename or
         "GluGluToContinToZZTo2tau2nu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z#gamma^{*}],ZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kPink+5)
        



      #// WZ
      if ( "WZTo" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kCyan-2)
       
      
      #// WWT2L2Nu
      if ( "WWTo" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WW")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kCyan+3)
       

      #// DYJetsToLL_TuneZ2_M-50_8TeV-madgraph-tauola 
      #if( inputfilename.find("DYJetsToLL_TuneZ2_M-50")<200 or inputfilename.find("DYJetsToLL_M-50")<200 ):
      if( "DYJetsToLL_TuneZ2_M-50" in inputfilename or "DYJetsToLL_M-50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z+jets")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kAzure+2)
       

      #// DYJetsToLL_M-10To50
      if ( "DYJetsToLL_M-10To50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z+jets")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kAzure+2)
       

      
      #// DYlighJetsToLL_TuneZ2_M-50_8TeV-madgraph-tauola 
      if ( "DYlightJetsToLL_TuneZ2_M-50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zlight")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kAzure+6)
         

      #// DYlighJetsToLL_TuneZ2_M-10To50_8TeV-madgraph-tauola 
      if ( "DYlightJetsToLL_TuneZ2_M-10To50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zlight")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kAzure+6)
         
    
      
      #// DYbbJetsToLL_TuneZ2_M-50_8TeV-madgraph-tauola 
      if ( "DYbbJetsToLL_TuneZ2_M-50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zbb")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kAzure+2)
       
      
      #// DYbbJetsToLL_TuneZ2_M-10To50
      if ( "DYbbJetsToLL_TuneZ2_M-10To50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zbb")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kAzure+2)


      #// DYccJetsToLL_TuneZ2_M-50_8TeV-madgraph-tauola 
      if ( "DYccJetsToLL_TuneZ2_M-50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zcc")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kRed+0)
       
      
      #// DYccJetsToLL_TuneZ2_M-10To50
      if ( "DYccJetsToLL_TuneZ2_M-10To50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Zcc")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kRed+0)
       


    
      #// #// DYToEE_M-10To20_TuneZ2_8TeV-pythia6
      #// if inputfilename in ( ):
      #// 	self.Vdatasetnamebkg.append(inputfilename)
      #// 	self.Vlabelbkg.append("DYToEE_M-10To20_TuneZ2_8TeV-pythia6")
      #// 	self.Vxsectionbkg.append(1.) #//pb
      #// 	self.Vcolorbkg.append(ROOT.kAzure+9)
      #//        

      #//       #// DYToMuMu_M-20_TuneZ2_8TeV-pythia6
      #// if inputfilename in ( ):
      #// 	self.Vdatasetnamebkg.append(inputfilename)
      #// 	self.Vlabelbkg.append("DYToMuMu_M-20_TuneZ2_8TeV-pythia")
      #// 	self.Vxsectionbkg.append(1.) #//pb
      #// 	self.Vcolorbkg.append(ROOT.kAzure-7)
      #//        

      #// ZToEE_NNPDF30_13TeV-powheg_M
      if ( "ZToEE_NNPDF30_13TeV-powheg_M" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Z+jets")
        self.Vxsectionbkg.append(1.)
        self.Vcolorbkg.append(ROOT.kAzure-9)
       


      #// QCD_Pt-30to40_doubleEMEnriched_TuneZ2_8TeV-pythia6 
      if ( "30to40_doubleEMEnriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-30to40_doubleEMEnriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal+8)
      
      #// QCD_Pt-40_doubleEMEnriched_TuneZ2_8TeV-pythia6
      if ( "-40_doubleEMEnriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-40_doubleEMEnriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal+8)
      


      #// QCD_Pt-15to20_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-15to20_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-15to20_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)
      

      #// QCD_Pt-20to30_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-20to30_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-20to30_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)
      

      #// QCD_Pt-30to50_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-30to50_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-30to50_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)
      

      #// QCD_Pt-50to80_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-50to80_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-50to80_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)
      

      #// QCD_Pt-80to120_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-80to120_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-80to120_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)


      #// QCD_Pt-120to150_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-120to150_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-120to150_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)
      

      #// QCD_Pt-150_MuPt5Enriched_TuneZ2_8TeV-pythia6 
      if ( "QCD_Pt-150_MuPt5Enriched_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-150_MuPt5Enriched_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-8)


      #// QCD_Pt-20to30_BCtoE_TuneZ2_8TeV-pythia6
      if ( "QCD_Pt-20to30_BCtoE_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-20to30_BCtoE_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)


      #// QCD_Pt-30to80_BCtoE_TuneZ2_8TeV-pythia6
      if ( "QCD_Pt-30to80_BCtoE_TuneZ2_8TeV-pythia6" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt-30to80_BCtoE_TuneZ2_8TeV-pythia6")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

        #// NEW QCD Pythia 8
      if ( "QCD_Pt_1000to1400" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_10to15" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)


      if ( "QCD_Pt_120to170" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_1400to1800" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_15to30" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)


      if ( "QCD_Pt_170to300" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_1800to2400" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_2400to3200" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_300to470" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_30to50" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_3200toInf" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_470to600" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      
      
      if ( "QCD_Pt_50to80" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_5to10" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_5to10_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_600to800" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      

      if ( "QCD_Pt_800to1000" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)


      if ( "QCD_Pt_80to120" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-2)
      


      #// TTbar 
      if ( "TT_Tune" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("t#bar{t} + jets")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-6)
       
      #// TTTo2L2Nu2B_8TeV-powheg-pythia6 
      if ( "TTTo2L2Nu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("t#bar{t}")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kTeal-6)
       
      
      #// Single Top
      #// T_TuneZ2_s-channel_8TeV-madgraph
      if ( "T_s-channel" in inputfilename or "T_TuneZ2_s-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("T_TuneZ2_s-channel_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       
      
      #// T_TuneZ2_t-channel_8TeV-madgraph
      if ( "T_t-channel" in inputfilename or "T_TuneZ2_t-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("T_TuneZ2_t-channel_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       
      
      #// T_TuneZ2_tW-channel_8TeV-madgraph
      if ( "T_tW" in inputfilename or "T_TuneZ2_tW-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("T_TuneZ2_tW-channel-DR_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       

      #// Tbar_TuneZ2_s-channel_8TeV-madgraph
      if ( "Tbar_s-channel" in inputfilename or "Tbar_TuneZ2_s-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Tbar_TuneZ2_s-channel_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       
      
      #// Tbar_TuneZ2_t-channel_8TeV-madgraph
      if ( "Tbar_t-channel" in inputfilename or "Tbar_TuneZ2_t-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Tbar_TuneZ2_t-channel_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       
      
      #// Tbar_TuneZ2_tW-channel-DR_8TeV-madgraph
      if ( "Tbar_tW-channel" in inputfilename or "Tbar_TuneZ2_tW-channel" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("Tbar_TuneZ2_tW-channel-DR_8TeV-powheg-tauola")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kViolet)
       


      #// W+jets
      #// WJetsToLNu_TuneZ2_8TeV-madgraph-tauola 
      if ( "_WJetsToLNu" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("W+Jets")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)

      #/// VVV
      if ( "ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("ZZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)
       
      
      if ( "WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WWZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)
       
      
      if ( "WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("WZZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)
       
      
      #// TTV
      if ( "TTWJets" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("TTW")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)


      if ( "TTZ" in inputfilename ):
        self.Vdatasetnamebkg.append(inputfilename)
        self.Vlabelbkg.append("TTZ")
        self.Vxsectionbkg.append(1.) #//pb
        self.Vcolorbkg.append(ROOT.kSpring)

    
  infile.close()

 def setupGridProxy (self) :
   if not os.path.isfile(os.environ['X509_USER_PROXY']): os.environ['X509_USER_PROXY'] = self.fullPathToTheGridProxy
   if os.path.isfile(os.environ['X509_USER_PROXY']):
    pass
   else:
    print "os.environ['X509_USER_PROXY'] ",os.environ['X509_USER_PROXY']
    print "You need to put your grid proxy somewhere under /eos/user/<your alpha>/<Username>"
    return 1 # sys.exit(1)
   #os.environ['X509_CERT_DIR'] = '/cvmfs/grid.cern.ch/etc/grid-security/certificates'
   #os.environ['X509_VOMS_DIR'] = '/cvmfs/grid.cern.ch/etc/grid-security/vomsdir'
   os.environ['X509_CERT_DIR'] = '/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates'
   os.environ['X509_VOMS_DIR'] = '/cvmfs/cms.cern.ch/grid/etc/grid-security/vomsdir'
    
   # root_file="root://cms-xrd-global.cern.ch//store/user/nvanegas/BckgndW+Jets/tag_1_delphes_events01.root"
   # tfile = ROOT.TFile(root_file)
   # tfile = ROOT.TFile.Open(root_file)

   #print "Listing Tree"

   #tfile.ls()
   return 0

 def plotm4l(self,histlabel) :
   print "plotm4l histlabel = ",histlabel
   style = getStyle("ZZ")


   #//style.SetMarkerSize(0.8)
   style.cd()
   style.SetNdivisions(508, "X")
   style.SetNdivisions(508, "Y")
   style.SetMarkerSize(0.8)

   c1 = ROOT.TCanvas("c1","c1",600,600)
   if (self.useRatio==True) : c1=ROOT.TCanvas("c1","c1",600,800)
   else : c1=ROOT.TCanvas("c1","c1",600,600)

   c1.cd()
   c1.SetTicks(1,1)

   ll = ROOT.TPaveText (0.15, 0.95, 0.95, 0.99, "NDC")
   ll.SetTextSize(0.027)
   ll.SetTextFont(42)
   ll.SetFillColor(0)
   ll.SetBorderSize(0)
   ll.SetMargin(0.01)
   ll.SetTextAlign(12) #// align left

   text = "CMS Preliminary"
   #//text = "CMS"
   ll.AddText(0.01,0.5,text)
   print "Energy= " , self.whichenergy 
   if ( "RunI" in self.whichenergy ):
     text = "#sqrt{s} = 7 TeV, L = 5.05 fb^{-1}  #sqrt{s} = 8 TeV, L = 19.71 fb^{-1}" 
     ll.AddText(0.3, 0.6, text)

   elif ( "7TeV" in self.whichenergy ):
     text = "#sqrt{s} = 7 TeV, L = 5.05 fb^{-1}" 
     ll.AddText(0.65, 0.6, text)

   elif ( "8TeV" in self.whichenergy ):
     text = "#sqrt{s} = 8 TeV, L = 19.71 fb^{-1}" 
     ll.AddText(0.65, 0.6, text)

   elif ( "13TeV" in self.whichenergy ):
     text = "#sqrt{s} = 13 TeV, L = 35.9 fb^{-1}" 
     #//text = "#sqrt{s = 13 TeV, L = 14.77 fb^{-1" 
     ll.AddText(0.65, 0.6, text)
 
   #//ll.Draw()
   # Things I can draw: ll  c1 
   #leg0 = ROOT.TLegend(0.6,0.40,0.8,0.90,NULL,"brNDC")
   leg0 = ROOT.TLegend(0.6,0.40,0.8,0.90,"","brNDC")
   leg0.SetTextSize(0.020)
   leg0.SetLineColor(0)
   leg0.SetLineWidth(1)
   leg0.SetFillColor(ROOT.kWhite)
   leg0.SetBorderSize(0)

   legend = ROOT.TLegend( 0.55, 0.7, 0.9, 0.92)
   legend.SetFillColor(ROOT.kWhite)
   legend.SetTextSize(0.020)

   ZZBgColor = ROOT.kAzure-9

   if(self.useLogY) : c1.SetLogy(1)
   else        : c1.SetLogy(0)

   if(self.useLogX) : c1.SetLogx(1)
   else        : c1.SetLogx(0)

   # Things I can draw: ll  c1 leg0 legend

   print " Vdatasetnamedata " ,  len(self.Vdatasetnamedata) 
   print "INFO: trying to open the first file |", self.Vdatasetnamedata[0],"|"
   #print "INFO: trying to open the first file |","root://cmseos.fnal.gov//store/group/lpchzz4leptons/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root","|"
   #ff=ROOT.TFile() # ff=NULL
   print "INFO X509_USER_PROXY = ", os.environ['X509_USER_PROXY'] 
   print "INFO X509_CERT_DIR = ", os.environ['X509_CERT_DIR']
   print "INFO X509_VOMS_DIR = ", os.environ['X509_VOMS_DIR']

   #ff = ROOT.TFile.Open(self.Vdatasetnamedata[0]);
   #ff = ROOT.TFile.Open("root://cmseos.fnal.gov//store/group/lpchzz4leptons/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root")
   #ff = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/defilip/MonoHiggs/80X/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_part1_1.root")
   #ff = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/user/defilip/MonoHiggs/80X/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root")
   #print "INFO result of file open ",ff
   #ff.ls()
   #return

   # thefile = '/store/user/defilip/MonoHiggs/80X/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root'
   if self.Vdatasetnamedata[0].startswith('/store') :
      print "The input file starts with /store. Using xrootd and Setting up the User Grid Proxy if it exists in the Class Init"
      if self.setupGridProxy() <> 0 :
         print "ERROR proxy setup failed. Please execute the voms-proxy-init and reconfigure the fullPathToTheGridProxy"
         sys.exit(1)

   if(len(self.Vdatasetnamedata)>0):
     ff = ROOT.TFile.Open(self.Vdatasetnamedata[0]);  #// just a random file, to determine the binning
   elif(len(self.Vdatasetnamebkg)>0):  
     ff = ROOT.TFile.Open(self.Vdatasetnamebkg[0])
   elif(len(self.Vdatasetnamesig)>0):  
     ff = ROOT.TFile.Open(self.Vdatasetnamesig[0])
   
   hfourlepbestmass_4l_afterSel_new = ff.Get(histlabel) # TH1F
   #print "DEBUG histlabel = ",histlabel, " hfourlepbestmass_4l_afterSel_new  = ",hfourlepbestmass_4l_afterSel_new 
   #ff.ls()
   #return

   # Things I can draw: ll  c1 leg0 legend hfourlepbestmass_4l_afterSel_new
   #        histlabel Object: hfourlepbestmass_4l_afterSel_new
   #ll.Draw()
   #leg0.Draw("same")
   ##legend.Draw("same")
   #hfourlepbestmass_4l_afterSel_new.Draw("same")
   #c1.Draw()
    
   #self.Nbins =hfourlepbestmass_4l_afterSel_new.GetNbinsX() / self.nRebin
   #self.Xmin= hfourlepbestmass_4l_afterSel_new.GetXaxis().GetXmin()


   self.Nbins =hfourlepbestmass_4l_afterSel_new.GetNbinsX() / self.nRebin
   self.Xmin= hfourlepbestmass_4l_afterSel_new.GetXaxis().GetXmin()
   #print "DEBUG Xmin = ",self.Xmin
   #return
   #self.Nbins =hfourlepbestmass_4l_afterSel_new.GetNbinsX() / self.nRebin
   self.Xmax= hfourlepbestmass_4l_afterSel_new.GetXaxis().GetXmax() 
   self.Ymax= hfourlepbestmass_4l_afterSel_new.GetBinContent(hfourlepbestmass_4l_afterSel_new.GetMaximumBin()) * 580.
   print "NBinsX= " , self.Nbins , " Ymax = " , self.Ymax 

   #// logaritmic bin width                                                                                                                                              
   NMBINS = self.Nbins
   MMIN = self.Xmin
   MMAX = self.Xmax

   logMbins_list = [] # size [NMBINS+1] double
   print "NMBinsX= " , NMBINS 

   if ( "hLogX" in histlabel ):
     for ibin in xrange(NMBINS+1) :
       logMbins_list.append(exp(log(MMIN) + (log(MMAX)-log(MMIN))*ibin/NMBINS))
       print logMbins[ibin]
   elif ( "hLogLinX" in histlabel ):
         #//logMbins[6]={0.,25.,50.,200., 500.,1000.
         for ibin in xrange(NMBINS+1) :
             logMbins_list.append(hfourlepbestmass_4l_afterSel_new.GetBinLowEdge(ibin+1))

   logMbins = array("f",logMbins_list)
   print "DEBUG logMbins = ",logMbins


   # In[6]: hframe2 is for the ratio
   hframe= ROOT.TH2F("hframe","hframe",80,70.,1000.,500,5.,700.);#// 4l analysis mass nrebin=10 GeV # for the histlabel plot ? 
   hframe2= ROOT.TH2F("hframe2","hframe2",80,70.,1000.,1000, 0.5, 20.);#// 4l analysis mass # for the histlable ratio plot ?

   if ( "hPFMET_0" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",5000, 0., 5000., 1000, 0.00001, 10000000000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0., 1000., 1000, 0.5, 2.);#// PFMET


   if ( "hPtLep_0" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,5.,200.,500,0.01,10000000.);#// pT                                                                 
     hframe2= ROOT.TH2F("hframe2","hframe2",80,5.,200.,500, 0.5, 2.);#// pT                                                                           


   if ( "hIsoLep_0" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,0.,10.,500,0.01,10000000.);#// Isolation                                                                  
     hframe2= ROOT.TH2F("hframe2","hframe2",80,0.,10.,500, 0.5, 2.);#// Isolation                                                                     


   if ( "hTKIsoLep_0" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,0.,10.,500,0.01,10000000.);#// Tracker Isolation
     hframe2= ROOT.TH2F("hframe2","hframe2",80,0.,10.,500, 0.5, 2.);#// Tk Isolation                                                                  


   if ( "hPFMET_1" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",5000, 0., 5000., 1000, 0.00001, 10000000000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0., 1000., 1000, 0.5, 2.);#// PFMET


   if ( "hM4l_7" in histlabel and 
       ( "4e" in self.whichchannel or "4#mu" in self.whichchannel or  "2e2#mu" in self.whichchannel)):
     #//hframe= ROOT.TH2F("hframe","hframe",80,70.,270.,500,0.004,42.);#// 4l analysis mass nrebin=2 GeV
     if (not self.useLogY) : hframe= ROOT.TH2F("hframe","hframe",80,70.,300.,500,0.0004,42.)
     else : hframe= ROOT.TH2F("hframe","hframe",80,70.,300.,500,0.0004,100000.)
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 70., 300., 1000, 0.5, 1.5);#// 

   if ( "hM4l_7" in histlabel and "4l" in self.whichchannel):
     if (not self.useLogY) : hframe= ROOT.TH2F("hframe","hframe",80,70.,300.,500,0.004,110.);#// 4l analysis mass nrebin=3
     else : hframe= ROOT.TH2F("hframe","hframe",80,70.,300.,500,0.0004,300.)
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 70., 300., 1000, 0.5, 1.5);#// 


   if ( "hM4l_8" in histlabel and ("4l" in self.whichchannel)):
     hframe= ROOT.TH2F("hframe","hframe",80,70.,182.,500,0.00000004,350000000.);#// 4l analysis mass nrebin=3
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 70., 182., 1000, 0.5, 2.);#// 



   if ( "hM4l_9" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,70.,182.,500,0.000004,35.);#// 4l analysis mass nrebin=3
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 70., 182., 1000, 0.5, 2.);#// 



   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,2600000.);#// mZ1 ee/mumu
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee/mumu

   if ( "hMZ_3" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.01,8000.);#// mZ1 mumu
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 mumu

   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,400000.);#// mZ1 mumu  7TeV
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 mumu 7TeV

   if ( "hMZ_3" in histlabel and  "4e" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,15000.);#// mZ1 ee                                       
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee


   if ( "hMZ_3" in histlabel and  "2e2#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,20000.);#// mZ1 ee/mumu  
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee/mumu
    
   if ( "hMZ_3" in histlabel and "4l" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,20000.);#// mZ1 4l
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 4l

   if ( "hPtLep_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,5.,300.,500,0.001,10000.);#// pT                                          
     hframe2= ROOT.TH2F("hframe2","hframe2",80,5.,200.,500, 0.5, 2.);#// pT                                           


   if ( "hIsoLep_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,0.,5.,500,0.001,100000.);#// Isolation                                    
     hframe2= ROOT.TH2F("hframe2","hframe2",80,0.,5.,500, 0.5, 2.);#// Isolation                                      


   if ( "hSipLep_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600, 0., 5., 1000, 0.0004, 1000000000.);#// sip
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 0., 5., 1000, 0.5, 2.);#// sip

   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,1100000.);#// mZ1 ee
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee
   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,700000.);#// mZ1 ee BB
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee BB
   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,100000.);#// mZ1 ee EE
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee EE

   #//hframe= ROOT.TH2F("hframe","hframe",80,60.,120.,500,0.4,300000.);#// mZ1 ee 7TeV
   #//hframe2= ROOT.TH2F("hframe2","hframe2",6000, 60., 120., 1000, 0.5, 2.);#// mZ1 ee 7TeV


   if ( "hMjj_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,20.,500.,600,0.0004,10E7);#//mass jet jet
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 20., 500., 1000, 0.5, 2.);#// mass jet jet


   if ( "hDjj_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,0.,10.,600,0.0004,10E7);#//delta eta jet jet
     hframe2= ROOT.TH2F("hframe2","hframe2",600, 0., 10., 1000, 0.5, 2.);#// delta eta jet jet


   if ( "hVD_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,0.,2.,600,4E-4,5E11);#// fisher
     hframe2= ROOT.TH2F("hframe2","hframe2",600, 0., 2., 1000, 0.5, 2.);#// fisher


   #// hframe= ROOT.TH2F("hframe","hframe",Nbins*nRebin, Xmin, Xmax, self.Nbins*nRebin, 0.0004, Ymax);#//mass

   if ( "hSip_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600, 0., 10., 1000, 0.0004, 1000000000.);#// sip
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 0., 10., 1000, 0.5, 2.);#// sip

   if ( "hIp_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600, 0., 2., 1000, 0.000004, 1000000000.);#// Ip
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 0., 2., 1000, 0.5, 2.);#// Ip

   #//TH2F *hframe= ROOT.TH2F("hframe","hframe",600, 0., 10., 1000, 0.04, 10000000.);#// chi2
   #//TH2F *hframe= ROOT.TH2F("hframe","hframe",600, 0., 1., 1000, 0.004, 6.);#// prob
   #// TH2F *hframe= ROOT.TH2F("hframe","hframe",600, 0., 0.35, 1000, 0.04, 10000000.);#// prob

   if ( "hIso_3" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",6000, 0., 3., 1000, 0.0004, 1000000000.);#// iso
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 0., 3., 1000, 0.5, 2.);#// iso


   if ( "hPFMET_3" in histlabel or ( "hLogXPFMET_3" in histlabel or "hLogLinXPFMET_3" in histlabel ) ):
     print "Plotting PFMET at step 3" 
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 100000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 10., 1000., 1000, 0.5, 1.5);#// PFMET


   if ( ( "hPFMET_3" in histlabel or (  "hLogXPFMET_3" in histlabel or "hLogLinXPFMET_3" in histlabel ) ) and "4l" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 100000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0., 1000., 1000, 0.5, 1.5);#// PFMET                                                                                 


   if ( "hMZ1_5" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0001,100000.);#// mZ1 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 160., 1000, 0.5, 2.);#// mZ1 


   if ( "hMZ2_5" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0000000001,1000000.);#// mZ2 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 200., 1000, 0.5, 2.);#// mZ2 


   if ( "hMZ1_8" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0001,100000.);#// mZ1 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 160., 1000, 0.5, 2.);#// mZ1 


   if ( "hMZ2_8" in histlabel and "4#mu" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0001,100000.);#// mZ2 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 160., 1000, 0.5, 2.);#// mZ2 


   # added for plotExercises.py hMZ1_8 and plotExercises.py hMZ2_8
   if ( "hMZ1_8" in histlabel and "4l" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0001,100000.);#// mZ1 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 160., 1000, 0.5, 2.);#// mZ1 
   if ( "hMZ2_8" in histlabel and "4l" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",80,40.,200.,500,0.0001,100000.);#// mZ2 
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 40., 160., 1000, 0.5, 2.);#// mZ2 


   if ( "hM4l_T_8" in histlabel or  "hLogLinXM4l_T_8" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,10.,1000.,500,0.00000004,100000000.);#// transverse mass , M4l+MET
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 10., 1200., 1000, 0.5, 1.5);#// 


   if ( "DPHI_8" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",80,0,3.14,500,0.00001,10E8);#// deltaphi 4l,MET
     hframe2= ROOT.TH2F("hframe2","hframe2",80,0,3.14, 1000, 0.5, 1.5);#// 


   if ( "hMELA_8" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,0.,1.,600,0.,20.);#// MELA at final stage
     hframe2= ROOT.TH2F("hframe2","hframe2",600, 0., 1., 1000, 0.5, 2.);#// MELA at final stage


   if ( "hPFMET_8" in histlabel or  "hPFMET_10" in histlabel):
     #//hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.0000004, 50000.);#// PFMET
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 100000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0.,1000., 1000, 0.5, 2.);#// PFMET


   if ( "hPFMET_8" in histlabel or ( "hLogXPFMET_8" in histlabel or "hLogLinXPFMET_8" in histlabel ) ):
     print "Plotting PFMET at step 8" 
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 1000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 10., 1000., 1000, 0.5, 1.5);#// PFMET


   if ( ( "hPFMET_8" in histlabel or (  "hLogXPFMET_8" in histlabel or "hLogLinXPFMET_8" in histlabel ) ) and "4l" in self.whichchannel):
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 1000000.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0., 1000., 1000, 0.5, 1.5);#// PFMET                                                                                 


   if ( "hPFMET_9" in histlabel ):
     #//hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.0000004, 50000.);#// PFMET
     hframe= ROOT.TH2F("hframe","hframe",1000, 0., 1000., 1000, 0.000001, 100.);#// PFMET
     hframe2= ROOT.TH2F("hframe2","hframe2",1000, 0.,1000., 1000, 0.5, 2.);#// PFMET


   if ( "hMjj_8" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,20.,500.,600,0.000004,10E4);#//mass jet jet
     hframe2= ROOT.TH2F("hframe2","hframe2",6000, 20., 500., 1000, 0.5, 2.);#// mass jet jet


   if ( "hDjj_8" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,0.,10.,600,0.000004,10E4);#//delta eta jet jet
     hframe2= ROOT.TH2F("hframe2","hframe2",600, 0., 10., 1000, 0.5, 2.);#// delta eta jet jet


   if ( "hNbjets" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,-0.5,9.,600,0.000004,10E3);#// number of b-jets
     hframe2= ROOT.TH2F("hframe2","hframe2",600, -0.5, 9., 1000, 0.5, 2.);#// number of b-jets
     hframe.SetXTitle("# bjets")


   if ( "hNgood" in histlabel ):
     hframe= ROOT.TH2F("hframe","hframe",600,3.5,10.5,600,0.000004,10E5);#// number of good leptons
     hframe2= ROOT.TH2F("hframe2","hframe2",600, 3.5, 9., 1000, 0.5, 2.);#// number of good leptons
     hframe.SetXTitle("# good lept.")


   #//TH2F *hframe= ROOT.TH2F("hframe","hframe",6000, 0., 200., 1000, 0.004, 700000.);#// ptZ


   if (self.nRebin==1):
     if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ): hframe.SetYTitle("Events / GeV")
     else : hframe.SetYTitle("Events/1 GeV")

   if (self.nRebin==2) : hframe.SetYTitle("Events/2 GeV")
   if (self.nRebin==1 and  "hNbjets" in histlabel ) : hframe.SetYTitle("Events")
   if (self.nRebin==1 and  "hNgood" in histlabel ) : hframe.SetYTitle("Events")

   if (self.nRebin==3) : hframe.SetYTitle("Events/3 GeV")
   if (self.nRebin==10) : hframe.SetYTitle("Events/10 GeV")
   if ( "hSip_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.12") #// self.nRebin=2 sip
   if (self.nRebin==4 and  "hSip_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.24") #// self.nRebin=4 sip

   if ( "hIso_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.04") #//nrebin=4 iso
   if (self.nRebin==5 and  "hIso_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.05") #//nrebin=5 iso

   if (self.nRebin==2 and  "hMjj_3" in histlabel ) : hframe.SetYTitle("Events/5 GeV") #// self.nRebin=2 mass jet jet
   if (self.nRebin==2 and  "hDjj_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.4") #// self.nRebin=2 deltetaeta
   if (self.nRebin==2 and  "hVD_3" in histlabel ) : hframe.SetYTitle("Events/bin=0.1") #// self.nRebin=2 fisher
   if (self.nRebin==10 and  "hMELA_8" in histlabel ) : hframe.SetYTitle("Events / 0.033") #// MELA
   if (self.nRebin==5 and ( "hPFMET_8" in histlabel or "hPFMET_3" in histlabel )) : hframe.SetYTitle("Events/5 GeV") #// PFMET


   if ( "hM4l_7" in histlabel or  "hM4l_8" in histlabel  or  "hM4l_9" in histlabel  ):
     self.histotitle = ("m_{%s} [GeV]" % self.whichchannel)
     hframe.SetXTitle(self.histotitle)


   if ( "hM4l_T_8" in histlabel or  "hLogLinXM4l_T_8" in histlabel ):
     self.histotitle = ("m_{T} (%s+MET) [GeV]" % self.whichchannel)
     hframe.SetXTitle(self.histotitle)


   if ( "DPHI_8" in histlabel ):
     self.histotitle = ("#Delta#phi (%s,MET) [rad]" % self.whichchannel)
     hframe.SetXTitle(self.histotitle)
     hframe.SetYTitle("Events / 0.2 rad")



   #//hframe.SetXTitle("M_{Z2 [GeV]")
   # >>> 448       
   if (( "hMZ_3" in histlabel or  "hMZ1_8" in histlabel) and "4#mu" in self.whichchannel): 
     hframe.SetXTitle("M_{Z#rightarrow#mu#mu} [GeV]")
   if (( "hMZ_3" in histlabel or  "hMZ1_8" in histlabel) and "4e" in self.whichchannel): 
     hframe.SetXTitle("M_{Z#rightarrow ee} [GeV]")
        
   #//hframe.SetXTitle("M_{Z#rightarrow ee (BB)  [GeV]")
   #//hframe.SetXTitle("M_{Z#rightarrow ee (EE)  [GeV]")
   #// hframe.SetXTitle("Sign. 3DIP")
   #// hframe.SetXTitle("R^{iso_{12 [GeV/c^{2]")
   if ( "hIso_3" in histlabel and  "4e" in self.whichchannel) : hframe.SetXTitle("electron worst rel. iso.")
   if ( "hIso_3" in histlabel and  "4#mu" in self.whichchannel) : hframe.SetXTitle("muon worst iso.")
   if ( "hIso_3" in histlabel and  "2e2#mu" in self.whichchannel) : hframe.SetXTitle("lepton worst iso.")
   #//hframe.SetXTitle("lepton worst iso.")
   if ( "hSip_3" in histlabel and  "4e" in self.whichchannel) : hframe.SetXTitle("electron worst SIP_{3D}")
   if ( "hSip_3" in histlabel and  "4#mu" in self.whichchannel) : hframe.SetXTitle("muon worst sign. 3DIP")
   if ( "hSip_3" in histlabel and  "2e2#mu" in self.whichchannel) : hframe.SetXTitle("lepton worst sign. 3DIP")
   #//hframe.SetXTitle("lepton worst sign. 3DIP")
   #// hframe.SetXTitle("Prob(#chi^{2/ndof.) of 4#mu vertex fitter (best 4#mu comb.)")
   #// hframe.SetXTitle("#chi^{2/ndof. of 4#mu vertex fitter (best 4#mu comb.)")
   if ( "hMjj_3" in histlabel or  "hMjj_8" in histlabel ) : hframe.SetXTitle("di jet mass") #//Mjj
   if ( "hDjj_3" in histlabel or  "hDjj_3" in histlabel ) : hframe.SetXTitle("#Delta#eta jets") #//deltaetajj
   #//if ( "hVD_3" in histlabel ) : hframe.SetXTitle("Fisher discriminant") #// fisher
   if ( "hVD_3" in histlabel ) : hframe.SetXTitle("D_{jet}") #// fisher

   if ( "hMELA_8" in histlabel ) : hframe.SetXTitle("D_{bkg}^{kin}") #// MELA
   if ( "PFMET_8" in histlabel or  "PFMET_3" in histlabel ) : hframe.SetXTitle("PF MET (GeV)") #// PFMET


   hframe.GetXaxis().SetLabelOffset(0.007)
   hframe.GetXaxis().SetTitleOffset(0.9)
   hframe.GetYaxis().SetLabelOffset(0.007)

   hframe.Draw() #; c1.Draw()


   # In[7]:
   # Data  
   # Use TH1F for a custom binning using the bin array (logMbins) created above or a fixed binsize binning
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : htotaldata    = ROOT.TH1F("htotaldata","htotaldata",NMBINS, logMbins)
   else : htotaldata = ROOT.TH1F("htotaldata", "htotaldata",self.Nbins ,self.Xmin,self.Xmax)

   htotaldata.SetMarkerColor(1)
   htotaldata.SetMarkerStyle(20)
   htotal=ROOT.THStack("Nicola","")

   # MC
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ):
     htotalHisto         = ROOT.TH1F("htotalHisto","htotalHisto",NMBINS, logMbins) # for hframe
     htotalHistoRatio    = ROOT.TH1F("htotalHistoRatio","htotalHistoRatio",NMBINS, logMbins)  # for hframe2 ?
   else :
     htotalHisto = ROOT.TH1F("htotalHisto", "htotalHisto",self.Nbins , self.Xmin, self.Xmax) # for hframe
     htotalHistoRatio = ROOT.TH1F("htotalHistoRatio", "htotalHistoRatio",self.Nbins , self.Xmin, self.Xmax) # for hframe2
    


   # In[8]:
   # background MC weighted and non-weighted
   nEvent_4l_w_totalbkgMC = ROOT.TH1D("nEvent_4l_w_totalbkgMC", "nEventComplete MC Weighted", 22, 0., 22.)
   nEvent_4l_w_totalbkgMC.Sumw2()
   nEvent_4l_totalbkgMC = ROOT.TH1D("nEvent_4l_totalbkgMC", "nEventComplete MC", 22, 0., 22.)
   nEvent_4l_totalbkgMC.Sumw2()
   listtotalbkgMC_w = ROOT.TList()
   listtotalbkgMC = ROOT.TList()

   #// data
   nEvent_4l_w_data = ROOT.TH1D("nEvent_4l_w_data", "nEventComplete data Weighted", 22, 0., 22.)
   nEvent_4l_w_data.Sumw2()
   listdata = ROOT.TList()


   # In[9]:
   #f0 = ROOT.TFile.Open(self.Vdatasetnamedata[0])
   #nEvent_4l_w_new = f0.Get("nEvent_4l_w")
   #for i in xrange(1,nEvent_4l_w_new.GetNbinsX()+1,1):
   #   nEvent_4l_w_data.GetXaxis().SetBinLabel(i,nEvent_4l_w_new.GetXaxis().GetBinLabel(i))
   ndata=0
   # Loop through all datasets
   for  datasetIdData in xrange( len(self.Vdatasetnamedata) ) :
     dataset = ("%s" % self.Vdatasetnamedata[datasetIdData])
     #print "Root-ple= " , dataset 
     f1 = ROOT.TFile.Open(dataset)
     nEvent_4l_w_new = f1.Get("nEvent_4l_w")
     #if ndata == 0 : nEvent_4l_w_data = nEvent_4l_w_new
     hfourlepbestmass_4l_afterSel_new = f1.Get(histlabel)

     if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_new = f1.Get(histlabel)    
     else : hfourlepbestmass_4l_afterSel_new_new=hfourlepbestmass_4l_afterSel_new.Rebin(self.nRebin, histlabel)

     hfourlepbestmass_4l_afterSel_new_new.SetMarkerColor(1)
     hfourlepbestmass_4l_afterSel_new_new.SetMarkerStyle(20)
     hfourlepbestmass_4l_afterSel_new_new.SetMarkerSize(0.95)
     #print "Adding data " , dataset
     htotaldata.Add(hfourlepbestmass_4l_afterSel_new_new)
     
     #print "Label= " , self.Vlabeldata[datasetIdData],"  Entries= " , hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1) 
     if (datasetIdData==(len(self.Vdatasetnamedata)-1)):
       leg0.AddEntry(hfourlepbestmass_4l_afterSel_new_new,"Data 2016", "P")
       legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new,"DATA 2016", "P")
       #//htotaldata.Draw("EPsame")
     ndata=ndata+1
     nEvent_4l_w_data.Add(nEvent_4l_w_new)
     #listdata.append(nEvent_4l_w_new)
   print "INFO Number of Datasets = ",ndata
   #GOOD return
   #nEvent_4l_w_data = nEvent_4l_w_new.Clone("nEvent_4l_w_data")
   ##nEvent_4l_w_data = hfourlepbestmass_4l_afterSel_new_new.Clone("nEvent_4l_w_data")
   #print "DEBUG 1 nEvent_4l_w_data ",nEvent_4l_w_data
   #nEvent_4l_w_data.Reset()
   #print "DEBUG 2 nEvent_4l_w_data ",nEvent_4l_w_data
   #ORIGINAL in C nEvent_4l_w_data.Merge(listdata) # BAD
   #nEvent_4l_w_data.Merge(listdata)
   #print "DEBUG 2 nEvent_4l_w_data ",nEvent_4l_w_data
    


   # In[10]:
   print ( "Data= " , htotaldata.Integral() , " and in the bins= ",
         htotaldata.GetBinContent(1) , " err= " , htotaldata.GetBinError(1) , " " ,
         htotaldata.GetBinContent(2) , " err= " , htotaldata.GetBinError(2) , " " ,
         htotaldata.GetBinContent(3) , " err= " , htotaldata.GetBinError(3) , " " ,
         htotaldata.GetBinContent(4) , " err= " , htotaldata.GetBinError(4) , " " ,
         htotaldata.GetBinContent(5) , " err= " , htotaldata.GetBinError(5) )


   # In[11]:
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ):
     print "Plotting htotaldata with log bins" 
   else :
     #// Set Errors as in http:#//www-cdf.fnal.gov/physics/statistics/notes/pois_eb.txt
     arraysize = [] ; x = [] ; y = [] ; exl = [] ; exh = [] ; eyl = [] ; eyh = []        
     totaldataentries=0. ; totaldataentries100=0.
     arraysize.append( htotaldata.GetNbinsX() )
     for nbins in xrange(1,htotaldata.GetNbinsX()+1): #for (int nbins=1;nbins<=htotaldata.GetNbinsX(); nbins++):
       #// print "BinCenter=" , htotaldata.GetBinCenter(nbins) , " BinContent=" , htotaldata.GetBinContent(nbins) , " BinErrorContent=" , htotaldata.GetBinError(nbins) 
       exl.append ( 0. )
       exh.append ( 0. )
       totaldataentries = totaldataentries + htotaldata.GetBinContent(nbins)
       if (htotaldata.GetBinCenter(nbins)>100. and htotaldata.GetBinCenter(nbins)<800.) : 
        totaldataentries100 = totaldataentries100 + htotaldata.GetBinContent(nbins)
       if (htotaldata.GetBinContent(nbins)>0):
         x.append( htotaldata.GetBinCenter(nbins) )
         eyh.append(  0.5 + sqrt(htotaldata.GetBinContent(nbins)+0.25) )
         eyl.append( -0.5 + sqrt(htotaldata.GetBinContent(nbins)+0.25) )
       else :
         x.append ( 0. )
         eyl.append ( 0. )
         eyh.append ( 0. )
       y.append( htotaldata.GetBinContent(nbins) )


     print "Total data= " , totaldataentries 
     
     x = array("f",x) ; y = array("f",y) ; exl = array("f",exl) ; exh = array("f",exh)
     eyl = array("f",eyl) ; eyh = array("f",eyh)
     Nbins = self.Nbins
     gr = ROOT.TGraphAsymmErrors(Nbins,x,y,exl,exh,eyl,eyh)
     gr.SetMarkerColor(1)
     gr.SetMarkerStyle(20)
     gr.SetMarkerSize(0.95)
   
   # Things I can draw: c1 ll leg0 legend hfourlepbestmass_4l_afterSel_new hfourlepbestmass_4l_afterSel_new_new
   # htotaldata gr



   # In[12]:
   #// Z+X from data
   if (self.useDYJets==False and self.useDYJetsFromData==True):
     if ( "hM4l_7" in histlabel or  "hPFMET_8" in histlabel ):       
       for datasetIdbkgData in xrange(len(self.Vdatasetnamebkgdata)): #for (unsigned int datasetIdbkgData=0; datasetIdbkgData<self.self.Vdatasetnamebkgdata.size(); datasetIdbkgData++):
         dataset = ("%s" % self.Vdatasetnamebkgdata[datasetIdbkgData])
         print "bkg Root-ple= " , dataset 
         f3 = ROOT.TFile.Open(dataset)
         hfourlepbestmass_4l_afterSel_new = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new", "Mass of four leptons after fullselection", 1000, 0,1000.)
         if ( "hPFMET_8" in histlabel ):
           hfourlepbestmass_4l_afterSel_new = f3.Get("h_MassZplusX_FR")
           self.nRebinZ_X=self.nRebin
           hfourlepbestmass_4l_afterSel_new_new=hfourlepbestmass_4l_afterSel_new.Rebin(self.nRebinZ_X, "h_MassZplusX_FR");      

         hfourlepbestmass_4l_afterSel_new_new.SetLineColor(ROOT.kCyan-2)
         hfourlepbestmass_4l_afterSel_new_new.SetFillColor(ROOT.kCyan-2)
         hfourlepbestmass_4l_afterSel_new_new.SetMarkerStyle(24)
         hfourlepbestmass_4l_afterSel_new_new.SetLineWidth(1)

         temp = ("%s" % self.histosdir)

         if ( "hM4l_7" in histlabel ):
           print "Adding Z+X for m4l > 70. GeV" 
           print "N bins Z+X= " , hfourlepbestmass_4l_afterSel_new_new.GetNbinsX()
           print "Z+X entries= " , hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1) 
           htotal.Add(hfourlepbestmass_4l_afterSel_new_new)
           htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_new)
           if ( temp in self.Vdatasetnamebkgdata[datasetIdbkgData] ):
             print "Adding legend for Z+X" 
             legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new,self.Vlabelbkgdata[datasetIdbkgData], "F"); 

         elif ( temp in self.Vdatasetnamebkgdata[datasetIdbkgData] and 
            ( "hM4l_8" in histlabel or  "hPFMET_8" in histlabel )):
           print "Adding Z+X" 
           #//print "Z+X entries= " , hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1) 
           htotal.Add(hfourlepbestmass_4l_afterSel_new_new)
           htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_new)
           if ( temp in self.Vdatasetnamebkgdata[datasetIdbkgData] and 
               ( self.whichenergy in self.Vdatasetnamebkgdata[datasetIdbkgData] or self.whichsample in self.Vdatasetnamebkgdata[datasetIdbkgData]) ):
             print "Adding legend for Z+X" 
             legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new,self.Vlabelbkgdata[datasetIdbkgData], "F");


   # =============================>
   #//print "Total Z+X is= " , htotal.GetHistogram().GetEntries()
   print "Total Z+X is= " , htotalHisto.Integral(0,-1)  
   #//outputyields , "Z+X "   , htotal.GetHistogram().GetEntries() , " +/- 0"


   # In[13]:


   # Things I can draw: c1 ll leg0 legend hfourlepbestmass_4l_afterSel_new hfourlepbestmass_4l_afterSel_new_new
   # htotaldata gr htotal htotalHisto  
   #htotal.Draw() ; c1.Draw()
   #htotalHisto.Draw() ; c1.Draw()
   #htotalHisto.Print()
   # htotal is the stack
   #htotal.Draw() ; c1.Draw()
   #htotalHisto.Draw() ; c1.Draw()


   whichchannel = self.whichchannel
   if ( "4#mu" in self.whichchannel ) : whichchannel = "4mu"
   if ( "2e2#mu" in self.whichchannel) : whichchannel = "2e2mu"
   # In[14]:
   if ( "hM4l_9" in histlabel ) : # if ( "hM4l_9" in self.histolabel ):
     os.system("[ -d plots ] || mkdir plots")
     yieldsOUT = ("plots/yields_%s_%s.txt" % (whichchannel, self.whichenergy))
     print "Opening a file for final numbers= " , yieldsOUT 
     self.outputyields = open(yieldsOUT, "w")
     self.outputyields.write( ( "%s %f %s" ) % ( "Z+X " , htotalHisto.Integral(0,-1) , " +/- 0" ) )


   # In[15]:
   #hfourlepbestmass_4l_afterSel_new_qqZZ
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_qqZZ    = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qqZZ","hfourlepbestmass_4l_afterSel_new_qqZZ",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_qqZZ = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qqZZ", "hfourlepbestmass_4l_afterSel_new_qqZZ",self.Nbins , self.Xmin, self.Xmax)
   nEvent_4l_w_qqZZ = ROOT.TH1D("nEvent_4l_w_qqZZ", "nEventComplete qqZZ Weighted", 22, 0., 22.)
   nEvent_4l_qqZZ = ROOT.TH1D("nEvent_4l_qqZZ", "nEventComplete qqZZ", 22, 0., 22.)
   nEvent_4l_w_qqZZ.Sumw2()
   nEvent_4l_qqZZ.Sumw2()
   listqqZZ_w = ROOT.TList()
   listqqZZ = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_ggZZ
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_ggZZ = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ggZZ","hfourlepbestmass_4l_afterSel_new_ggZZ",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_ggZZ = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ggZZ", "hfourlepbestmass_4l_afterSel_new_ggZZ",self.Nbins , self.Xmin, self.Xmax)
   nEvent_4l_w_ggZZ = ROOT.TH1D("nEvent_4l_w_ggZZ", "nEventComplete ggZZ Weighted", 22, 0., 22.)
   nEvent_4l_ggZZ = ROOT.TH1D("nEvent_4l_ggZZ", "nEventComplete ggZZ", 22, 0., 22.)
   nEvent_4l_w_ggZZ.Sumw2()
   nEvent_4l_ggZZ.Sumw2()
   listggZZ_w = ROOT.TList()
   listggZZ = ROOT.TList()
    
   #hfourlepbestmass_4l_afterSel_new_ZZ
   if (  "hLogX" in histlabel  or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_ZZ    = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ZZ","hfourlepbestmass_4l_afterSel_new_ZZ",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_ZZ = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ZZ", "hfourlepbestmass_4l_afterSel_new_ZZ",self.Nbins , self.Xmin, self.Xmax)
   nEvent_4l_w_ZZ = ROOT.TH1D("nEvent_4l_w_ZZ", "nEventComplete ZZ Weighted", 22, 0., 22.)
   nEvent_4l_ZZ = ROOT.TH1D("nEvent_4l_ZZ", "nEventComplete ZZ", 22, 0., 22.)
   nEvent_4l_w_ZZ.Sumw2()
   nEvent_4l_ZZ.Sumw2()
   listZZ_w = ROOT.TList()
   listZZ = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_qcdDEM
   if (  "hLogX" in histlabel  or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_qcdDEM    = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdDEM","hfourlepbestmass_4l_afterSel_new_qcdDEM",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_qcdDEM = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdDEM", "hfourlepbestmass_4l_afterSel_new_qcdDEM",self.Nbins , self.Xmin, self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_qcdMu
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_qcdMu = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdMu", "hfourlepbestmass_4l_afterSel_new_qcdMu",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_qcdMu= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdMu", "hfourlepbestmass_4l_afterSel_new_qcdMu",self.Nbins , self.Xmin, self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_qcdBC
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_qcdBC = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdBC", "hfourlepbestmass_4l_afterSel_new_qcdBC",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_qcdBC = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcdBC", "hfourlepbestmass_4l_afterSel_new_qcdBC",self.Nbins , self.Xmin, self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_qcd
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_qcd = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcd", "hfourlepbestmass_4l_afterSel_new_qcd",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_qcd= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_qcd", "hfourlepbestmass_4l_afterSel_new_qcd",self.Nbins , self.Xmin, self.Xmax)
   nEvent_4l_w_QCD = ROOT.TH1D("nEvent_4l_w_QCD", "nEventComplete QCD Weighted", 22, 0., 22.)
   nEvent_4l_QCD = ROOT.TH1D("nEvent_4l_QCD", "nEventComplete QCD", 22, 0., 22.)
   nEvent_4l_w_QCD.Sumw2()
   nEvent_4l_QCD.Sumw2()
   listQCD_w = ROOT.TList()
   listQCD = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_singlet
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_singlet = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_singlet", "hfourlepbestmass_4l_afterSel_new_singlet",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_singlet = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_singlet", "hfourlepbestmass_4l_afterSel_new_singlet",self.Nbins , self.Xmin, self.Xmax)
   nEvent_4l_w_ST = ROOT.TH1D("nEvent_4l_w_ST", "nEventComplete ST Weighted", 22, 0., 22.)
   nEvent_4l_w_ST.Sumw2()
   nEvent_4l_ST = ROOT.TH1D("nEvent_4l_ST", "nEventComplete ST", 22, 0., 22.)
   nEvent_4l_ST.Sumw2()
   listST_w = ROOT.TList()
   listST = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_DY
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_DY = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DY", "hfourlepbestmass_4l_afterSel_new_DY",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_DY = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DY", "hfourlepbestmass_4l_afterSel_new_DY",self.Nbins, self.Xmin, self.Xmax);    

   #hfourlepbestmass_4l_afterSel_new_DYlight
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_DYlight = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYlight", "hfourlepbestmass_4l_afterSel_new_DYlight",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_DYlight = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYlight", "hfourlepbestmass_4l_afterSel_new_DYlight",self.Nbins, self.Xmin, self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_DYbb
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_DYbb = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYbb", "hfourlepbestmass_4l_afterSel_new_DYbb",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_DYbb= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYbb", "hfourlepbestmass_4l_afterSel_new_DYbb",self.Nbins, self.Xmin, self.Xmax);        

   #hfourlepbestmass_4l_afterSel_new_DYcc
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_DYcc = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYcc", "hfourlepbestmass_4l_afterSel_new_DYcc",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_DYcc = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_DYcc", "hfourlepbestmass_4l_afterSel_new_DYcc",self.Nbins, self.Xmin, self.Xmax);        
   nEvent_4l_w_DY = ROOT.TH1D("nEvent_4l_w_DY", "nEventComplete DY Weighted", 22, 0., 22.)
   nEvent_4l_w_DY.Sumw2()
   nEvent_4l_DY = ROOT.TH1D("nEvent_4l_DY", "nEventComplete DY", 22, 0., 22.)
   nEvent_4l_DY.Sumw2()
   listDY_w = ROOT.TList()
   listDY = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_WW
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_WW = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WW", "hfourlepbestmass_4l_afterSel_new_WW",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_WW = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WW", "hfourlepbestmass_4l_afterSel_new_WW",self.Nbins, self.Xmin, self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_WZ
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_WZ = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WZ", "hfourlepbestmass_4l_afterSel_new_WZ",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_WZ= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WZ", "hfourlepbestmass_4l_afterSel_new_WZ",self.Nbins,self.Xmin,self.Xmax);                        

   #hfourlepbestmass_4l_afterSel_new_Wj
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_Wj = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_Wj", "hfourlepbestmass_4l_afterSel_new_Wj",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_Wj= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_Wj", "hfourlepbestmass_4l_afterSel_new_Wj",self.Nbins, self.Xmin, self.Xmax)
   nEvent_4l_w_WZ_WW_Wj = ROOT.TH1D("nEvent_4l_w_WZ_WW_Wj", "nEventComplete WZ_WW_Wj Weighted", 22, 0., 22.)
   nEvent_4l_WZ_WW_Wj = ROOT.TH1D("nEvent_4l_WZ_WW_Wj", "nEventComplete WZ_WW_Wj", 22, 0., 22.)
   nEvent_4l_w_WZ_WW_Wj.Sumw2()
   nEvent_4l_WZ_WW_Wj.Sumw2()
   listWZ_WW_Wj_w = ROOT.TList()
   listWZ_WW_Wj = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_TT
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_TT = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_TT", "hfourlepbestmass_4l_afterSel_new_TT",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_TT= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_TT", "hfourlepbestmass_4l_afterSel_new_TT",self.Nbins, self.Xmin, self.Xmax)
   nEvent_4l_w_TT = ROOT.TH1D("nEvent_4l_w_TT", "nEventComplete TT Weighted", 22, 0., 22.)
   nEvent_4l_TT = ROOT.TH1D("nEvent_4l_TT", "nEventComplete TT", 22, 0., 22.)
   nEvent_4l_w_TT.Sumw2()
   nEvent_4l_TT.Sumw2()
   listTT_w = ROOT.TList()
   listTT = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_VVV
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_VVV = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VVV", "hfourlepbestmass_4l_afterSel_new_VVV",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_VVV= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VVV", "hfourlepbestmass_4l_afterSel_new_VVV",self.Nbins, self.Xmin, self.Xmax)
   nEvent_4l_w_VVV = ROOT.TH1D("nEvent_4l_w_VVV", "nEventComplete VVV Weighted", 22, 0., 22.)
   nEvent_4l_VVV = ROOT.TH1D("nEvent_4l_VVV", "nEventComplete VVV", 22, 0., 22.)
   nEvent_4l_w_VVV.Sumw2()
   nEvent_4l_VVV.Sumw2()
   listVVV_w = ROOT.TList()
   listVVV = ROOT.TList()

   #hfourlepbestmass_4l_afterSel_new_TTV
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_TTV = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_TTV", "hfourlepbestmass_4l_afterSel_new_TTV",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_TTV= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_TTV", "hfourlepbestmass_4l_afterSel_new_TTV",self.Nbins, self.Xmin, self.Xmax)
   nEvent_4l_w_TTV = ROOT.TH1D("nEvent_4l_w_TTV", "nEventComplete TTV Weighted", 22, 0., 22.)
   nEvent_4l_TTV = ROOT.TH1D("nEvent_4l_TTV", "nEventComplete TTV", 22, 0., 22.)
   nEvent_4l_w_TTV.Sumw2()
   nEvent_4l_TTV.Sumw2()
   listTTV_w = ROOT.TList()
   listTTV = ROOT.TList()

   # ====================================>  
   #//print "Total Z+X is= " , htotal.GetHistogram().GetEntries() 
   print "Total Z+X is= " , htotalHisto.Integral(0,-1)  
   #// Higgs as background
   #hfourlepbestmass_4l_afterSel_new_ggH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_ggH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ggH", "hfourlepbestmass_4l_afterSel_new_ggH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_ggH= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ggH", "hfourlepbestmass_4l_afterSel_new_ggH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_VH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_VH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VH", "hfourlepbestmass_4l_afterSel_new_VH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_VH= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VH", "hfourlepbestmass_4l_afterSel_new_VH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_ZH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_ZH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ZH", "hfourlepbestmass_4l_afterSel_new_ZH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_ZH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ZH", "hfourlepbestmass_4l_afterSel_new_ZH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_WH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_WH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WH", "hfourlepbestmass_4l_afterSel_new_WH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_WH= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_WH", "hfourlepbestmass_4l_afterSel_new_WH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_VBFH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_VBFH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VBFH", "hfourlepbestmass_4l_afterSel_new_VBFH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_VBFH= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_VBFH", "hfourlepbestmass_4l_afterSel_new_VBFH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_ttH
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_ttH = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ttH", "hfourlepbestmass_4l_afterSel_new_ttH",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_ttH= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_ttH", "hfourlepbestmass_4l_afterSel_new_ttH",self.Nbins,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_afterSel_new_totSM_H
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_totSM_H = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_totSM_H", "hfourlepbestmass_4l_afterSel_new_totSM_H",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_totSM_H= ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_totSM_H", "hfourlepbestmass_4l_afterSel_new_totSM_H",self.Nbins,self.Xmin,self.Xmax)
   nEvent_4l_w_totSM_H = ROOT.TH1D("nEvent_4l_w_totSM_H", "nEventComplete totSM_H Weighted", 22, 0., 22.)
   nEvent_4l_totSM_H = ROOT.TH1D("nEvent_4l_totSM_H", "nEventComplete totSM_H", 22, 0., 22.)
   nEvent_4l_w_totSM_H.Sumw2()
   nEvent_4l_totSM_H.Sumw2()
   listtotSM_H_w = ROOT.TList()
   listtotSM_H = ROOT.TList()

   #// Total bkg - no Higgs
   #hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H", "hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H",NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H", "hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H",self.Nbins,self.Xmin,self.Xmax)
   nEvent_4l_w_totbkg_noSM_H = ROOT.TH1D("nEvent_4l_w_totbkg_noSM_H", "nEventComplete totbkg_noSM_H Weighted", 22, 0., 22.)
   nEvent_4l_totbkg_noSM_H = ROOT.TH1D("nEvent_4l_totbkg_noSM_H", "nEventComplete totbkg_noSM_H", 22, 0., 22.)
   nEvent_4l_w_totbkg_noSM_H.Sumw2()
   nEvent_4l_totbkg_noSM_H.Sumw2()
   listtotbkg_noSM_H_w = ROOT.TList()
   listtotbkg_noSM_H = ROOT.TList()


   # In[16]:
   ndata = 0
   f2 = []
   hfourlepbestmass_4l_afterSel_new = []
   hfourlepbestmass_4l_afterSel_new_new = []
   for datasetId in xrange(len(self.Vdatasetnamebkg)-1, -1,-1): #for ( int datasetId=len(self.Vdatasetnamebkg)-1; datasetId >=0; datasetId--):  
     dataset = ( "%s" % self.Vdatasetnamebkg[datasetId] )
     print "Counter=" , datasetId , " Root-ple=" , dataset , " Label=" , self.Vlabelbkg[datasetId] 
     # in python dataset is same as datasetnamebkg, but since this is ported from PlotStack4l.C
     datasetnamebkg = self.Vdatasetnamebkg[datasetId]
     f2.append( ROOT.TFile.Open(dataset) )
     hfourlepbestmass_4l_afterSel_new.append(f2[ndata].Get(histlabel))

     nEvent_4l_w_new = f2[ndata].Get("nEvent_4l_w")
     nEvent_4l_new = f2[ndata].Get("nEvent_4l")
     #print "Bin content= " , nEvent_4l_w_new.GetBinContent(5) , " " , nEvent_4l_w_new.GetBinError(5) 
        
     if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ):
       if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ): hfourlepbestmass_4l_afterSel_new_new.append( f2[ndata].Get(histlabel) )
       else : hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin, histlabel) )

       #//hfourlepbestmass_4l_afterSel_new_new=hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin, histlabel /*"hfourlepbestmass_4l_afterSel_new_new"*/)
       hfourlepbestmass_4l_afterSel_new_new[ndata].SetLineColor(self.Vcolorbkg[datasetId])
       hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillColor(self.Vcolorbkg[datasetId])
       hfourlepbestmass_4l_afterSel_new_new[ndata].SetMarkerStyle(24)
       hfourlepbestmass_4l_afterSel_new_new[ndata].SetLineWidth(1)
       theerror=0.0
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0) : theerror = sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()
       print "Label= " , self.Vlabelbkg[datasetId], "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries(), "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1), " +- ", theerror
       # nEvent_4l_w_totalbkgMC->Merge(listtotalbkgMC_w); nEvent_4l_totalbkgMC->Merge(listtotalbkgMC);
       # nEvent_4l_w_totbkg_noSM_H->Merge(listtotbkg_noSM_H_w); nEvent_4l_totbkg_noSM_H->Merge(listtotbkg_noSM_H);
       nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
       nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)

       #// Higgs as background
       if( "GluGluHToZZTo4L" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_ggH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_ggH.SetMarkerColor(ROOT.kOrange-3)
         hfourlepbestmass_4l_afterSel_new_ggH.SetFillColor(ROOT.kOrange-3)
         hfourlepbestmass_4l_afterSel_new_totSM_H.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         print "     ggH Integral= " , hfourlepbestmass_4l_afterSel_new_totSM_H.Integral() 
         nEvent_4l_w_totSM_H.Add(nEvent_4l_w_new) # listtotSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totSM_H.Add(nEvent_4l_new) # listtotSM_H.Add(nEvent_4l_new)
         
       if( "ttH" in datasetnamebkg ) :
         hfourlepbestmass_4l_afterSel_new_ttH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_ttH.SetMarkerColor(ROOT.kOrange)
         hfourlepbestmass_4l_afterSel_new_ttH.SetFillColor(ROOT.kOrange)
         hfourlepbestmass_4l_afterSel_new_totSM_H.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         print "     ttH Integral= " , hfourlepbestmass_4l_afterSel_new_totSM_H.Integral() 
         nEvent_4l_w_totSM_H.Add(nEvent_4l_w_new) # listtotSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totSM_H.Add(nEvent_4l_new) # listtotSM_H.Add(nEvent_4l_new)

       if( "VBF" in datasetnamebkg):
         print "VBF" 
         hfourlepbestmass_4l_afterSel_new_VBFH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_VBFH.SetMarkerColor(ROOT.kOrange-2)
         hfourlepbestmass_4l_afterSel_new_VBFH.SetFillColor(ROOT.kOrange-2)
         hfourlepbestmass_4l_afterSel_new_totSM_H.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         print "     VBF Integral= " , hfourlepbestmass_4l_afterSel_new_totSM_H.Integral() 
         nEvent_4l_w_totSM_H.Add(nEvent_4l_w_new) # listtotSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totSM_H.Add(nEvent_4l_new) # listtotSM_H.Add(nEvent_4l_new)

       if( "WplusH" in datasetnamebkg or  "WminusH" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_WH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_WH.SetMarkerColor(ROOT.kOrange+2)
         hfourlepbestmass_4l_afterSel_new_WH.SetFillColor(ROOT.kOrange+2)
         hfourlepbestmass_4l_afterSel_new_WH.SetLineColor(ROOT.kOrange+2)
         print "     WH" 

         hfourlepbestmass_4l_afterSel_new_VH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_VH.SetMarkerColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_VH.SetFillColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_VH.SetLineColor(ROOT.kOrange-1)

         hfourlepbestmass_4l_afterSel_new_totSM_H.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         nEvent_4l_w_totSM_H.Add(nEvent_4l_w_new) # listtotSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totSM_H.Add(nEvent_4l_new) # listtotSM_H.Add(nEvent_4l_new)

       if( "ZH" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_ZH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_ZH.SetMarkerColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_ZH.SetFillColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_ZH.SetLineColor(ROOT.kOrange-1)

         hfourlepbestmass_4l_afterSel_new_VH.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_VH.SetMarkerColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_VH.SetFillColor(ROOT.kOrange-1)
         hfourlepbestmass_4l_afterSel_new_VH.SetLineColor(ROOT.kOrange-1)

         hfourlepbestmass_4l_afterSel_new_totSM_H.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         print "     ZH Integral= " , hfourlepbestmass_4l_afterSel_new_totSM_H.Integral() 
         nEvent_4l_w_totSM_H.Add(nEvent_4l_w_new) # listtotSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totSM_H.Add(nEvent_4l_new) # listtotSM_H.Add(nEvent_4l_new)

       #// DYJetsToLL check normalization
       if( "DYJetsToLL" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_DY.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_DY.SetMarkerColor(ROOT.kAzure+2)
         hfourlepbestmass_4l_afterSel_new_DY.SetFillColor(ROOT.kAzure+2)
         temp = ("%s" % self.histosdir)
         if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0 and ( "DYJetsToLL_M-50_TuneZ2Star" in datasetnamebkg or  "DYJetsToLL_M-50" in datasetnamebkg)):
           print "     DY Integral = " , hfourlepbestmass_4l_afterSel_new_DY.Integral(0,-1) 
           if (self.useDYJets==True) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
         nEvent_4l_w_DY.Add(nEvent_4l_w_new) # listDY_w.Add(nEvent_4l_w_new)
         nEvent_4l_DY.Add(nEvent_4l_new) # listDY.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       if( "ZToEE" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_DY.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_DY.SetMarkerColor(ROOT.kAzure+2)
         hfourlepbestmass_4l_afterSel_new_DY.SetFillColor(ROOT.kAzure+2)      
         hfourlepbestmass_4l_afterSel_new_DY.SetLineColor(ROOT.kAzure+2)
         temp = ("%s" % self.histosdir)
         if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg and hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0 and "ZToEE_NNPDF30_13TeV-powheg_M_1400_2300" in datasetnamebkg)):
           print "     DY Integral = " , hfourlepbestmass_4l_afterSel_new_DY.Integral(0,-1) 
           if (self.useDYJets==True) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
         nEvent_4l_w_DY.Add(nEvent_4l_w_new) # listDY_w.Add(nEvent_4l_w_new)
         nEvent_4l_DY.Add(nEvent_4l_new) # listDY.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       #// DYlightJetsToLL check normalization
       if( "DYlightJetsToLL" in datasetnamebkg) :
         hfourlepbestmass_4l_afterSel_new_DYlight.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_DYlight.SetMarkerColor(ROOT.kAzure+6)
         #//hfourlepbestmass_4l_afterSel_new_DYlight.SetLineColor(ROOT.kAzure+6)
         #//hfourlepbestmass_4l_afterSel_new_DYlight.SetLineWidth(2)
         hfourlepbestmass_4l_afterSel_new_DYlight.SetFillColor(ROOT.kAzure+6)
         temp = ("%s" % self.histosdir)
         if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or self.whichsample in datasetnamebkg ) and hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0 and "DYlightJetsToLL_TuneZ2_M-50" in datasetnamebkg ):
           print "     DYlight Integral = " , hfourlepbestmass_4l_afterSel_new_DYlight.Integral(0,-1) 
           if (self.useDYJets==False) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
         nEvent_4l_w_DY.Add(nEvent_4l_w_new) # listDY_w.Add(nEvent_4l_w_new)
         nEvent_4l_DY.Add(nEvent_4l_new) # listDY.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       #// DYbb
       if( "DYbbJetsToLL" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_DYbb.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_DYbb.SetMarkerColor(ROOT.kAzure+2)
         #//	hfourlepbestmass_4l_afterSel_new_DYbb.SetLineColor(ROOT.kAzure+2)
         #//	hfourlepbestmass_4l_afterSel_new_DYbb.SetLineWidth(2)
         hfourlepbestmass_4l_afterSel_new_DYbb.SetFillColor(ROOT.kAzure+2)
         temp = ("%s" % self.histosdir)
         if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0 and  "DYbbJetsToLL_TuneZ2_M-50" in datasetnamebkg):
           print "DYbb= " , hfourlepbestmass_4l_afterSel_new_DYbb.Integral(0,-1) 
           if (self.useDYJets==False) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")        
         nEvent_4l_w_DY.Add(nEvent_4l_w_new) # listDY_w.Add(nEvent_4l_w_new)
         nEvent_4l_DY.Add(nEvent_4l_new) # listDY.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       #//DYCC
       if( "DYccJetsToLL" in datasetnamebkg):
         hfourlepbestmass_4l_afterSel_new_DYcc.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         hfourlepbestmass_4l_afterSel_new_DYcc.SetMarkerColor(ROOT.kRed+0)
         #// hfourlepbestmass_4l_afterSel_new_DYcc.SetLineColor(ROOT.kRed+0)
         #// hfourlepbestmass_4l_afterSel_new_DYcc.SetLineWidth(2)
         hfourlepbestmass_4l_afterSel_new_DYcc.SetFillColor(ROOT.kRed+0)
         temp = ("%s" % self.histosdir)
         if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0 and  "DYccJetsToLL_M-50_TuneZ2Star" in datasetnamebkg):
           print "DYcc= " , hfourlepbestmass_4l_afterSel_new_DYcc.Integral(0,-1) 
           if (self.useDYJets==False) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         nEvent_4l_w_DY.Add(nEvent_4l_w_new) # listDY_w.Add(nEvent_4l_w_new)
         nEvent_4l_DY.Add(nEvent_4l_new) # listDY.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       if (self.useDYJetsFromData==False):
         #// WW
         if( "WWTo" in datasetnamebkg):
           hfourlepbestmass_4l_afterSel_new_WW.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
           hfourlepbestmass_4l_afterSel_new_WW.SetMarkerColor(ROOT.kCyan+3)
           hfourlepbestmass_4l_afterSel_new_WW.SetFillColor(ROOT.kCyan+3)
           hfourlepbestmass_4l_afterSel_new_WW.SetLineColor(ROOT.kCyan+3)
           temp = ("%s" % self.histosdir)
           if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_WW.GetEntries()>0. ) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
           nEvent_4l_w_WZ_WW_Wj.Add(nEvent_4l_w_new) # listWZ_WW_Wj_w.Add(nEvent_4l_w_new)
           nEvent_4l_WZ_WW_Wj.Add(nEvent_4l_new) # listWZ_WW_Wj.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         #// WZ     
         if( "WZTo" in datasetnamebkg):  
           hfourlepbestmass_4l_afterSel_new_WZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
           hfourlepbestmass_4l_afterSel_new_WZ.SetMarkerColor(ROOT.kCyan-2)
           hfourlepbestmass_4l_afterSel_new_WZ.SetFillColor(ROOT.kCyan-2)
           hfourlepbestmass_4l_afterSel_new_WZ.SetLineColor(ROOT.kCyan-2)
           temp = ("%s" % self.histosdir)
           if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_WZ.GetEntries()>0. ) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
           nEvent_4l_w_WZ_WW_Wj.Add(nEvent_4l_w_new) # listWZ_WW_Wj_w.Add(nEvent_4l_w_new)
           nEvent_4l_WZ_WW_Wj.Add(nEvent_4l_new) # listWZ_WW_Wj.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         #// TTT
         if( "TTT" in datasetnamebkg): 
           hfourlepbestmass_4l_afterSel_new_TT.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);     
           hfourlepbestmass_4l_afterSel_new_TT.SetMarkerColor(ROOT.kTeal-6)
           hfourlepbestmass_4l_afterSel_new_TT.SetFillColor(ROOT.kTeal-6)
           hfourlepbestmass_4l_afterSel_new_TT.SetLineColor(ROOT.kTeal-6)
           print "     TT+jets= " , hfourlepbestmass_4l_afterSel_new_TT.GetEntries() 
           temp = ("%s" % self.histosdir)
           if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_TT.GetEntries()>0. ) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
           nEvent_4l_w_TT.Add(nEvent_4l_w_new) # listTT_w.Add(nEvent_4l_w_new)
           nEvent_4l_TT.Add(nEvent_4l_new) # listTT.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         #// W+jets
         if( "_WJets" in datasetnamebkg):
           print "Wjets" 
           hfourlepbestmass_4l_afterSel_new_Wj.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])    
           hfourlepbestmass_4l_afterSel_new_Wj.SetMarkerColor(ROOT.kSpring)
           hfourlepbestmass_4l_afterSel_new_Wj.SetFillColor(ROOT.kSpring)
           temp = ("%s" % self.histosdir)
           if( temp in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_Wj.GetEntries()>0. ) : legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")        
           nEvent_4l_w_WZ_WW_Wj.Add(nEvent_4l_w_new) # listWZ_WW_Wj_w.Add(nEvent_4l_w_new)
           nEvent_4l_WZ_WW_Wj.Add(nEvent_4l_new) # listWZ_WW_Wj.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         #/// VVV
         if( "_ZZZ" in datasetnamebkg):
           print "ZZZ" 
           hfourlepbestmass_4l_afterSel_new_VVV.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);        
           hfourlepbestmass_4l_afterSel_new_VVV.SetMarkerColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetFillColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetLineColor(ROOT.kAzure-4)
           temp = ("%s/output_ZZZ" % self.histosdir)
           if( temp in datasetnamebkg and  "ZZZ" in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_VVV.GetEntries()>0. ): 
             legend.AddEntry(hfourlepbestmass_4l_afterSel_new_VVV,"VVV", "F")
             #//print "Label= ZZZ     Entries= " , hfourlepbestmass_4l_afterSel_new_ZZZ.Integral(0,-1) 
             print "     Label= Total VVV     Entries= " , hfourlepbestmass_4l_afterSel_new_VVV.Integral(0,-1) 

           nEvent_4l_w_VVV.Add(nEvent_4l_w_new) # listVVV_w.Add(nEvent_4l_w_new)
           nEvent_4l_VVV.Add(nEvent_4l_new) # listVVV.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         if( "_WWZ" in datasetnamebkg):
           print "WWZ" 
           hfourlepbestmass_4l_afterSel_new_VVV.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);        
           hfourlepbestmass_4l_afterSel_new_VVV.SetMarkerColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetFillColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetLineColor(ROOT.kAzure-4)
           nEvent_4l_w_VVV.Add(nEvent_4l_w_new) # listVVV_w.Add(nEvent_4l_w_new)
           nEvent_4l_VVV.Add(nEvent_4l_new) # listVVV.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)


         if( "_WZZ" in datasetnamebkg):
           print "WZZ" 
           hfourlepbestmass_4l_afterSel_new_VVV.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);        
           hfourlepbestmass_4l_afterSel_new_VVV.SetMarkerColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetFillColor(ROOT.kAzure-4)
           hfourlepbestmass_4l_afterSel_new_VVV.SetLineColor(ROOT.kAzure-4)
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
           nEvent_4l_w_VVV.Add(nEvent_4l_w_new) # listVVV_w.Add(nEvent_4l_w_new)
           nEvent_4l_VVV.Add(nEvent_4l_new) # listVVV.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         #//TTV
         if( "_TTZ" in datasetnamebkg):
           print "TTZ" 
           hfourlepbestmass_4l_afterSel_new_TTV.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);        
           hfourlepbestmass_4l_afterSel_new_TTV.SetMarkerColor(ROOT.kAzure+4);	
           hfourlepbestmass_4l_afterSel_new_TTV.SetFillColor(ROOT.kAzure+4);	
           hfourlepbestmass_4l_afterSel_new_TTV.SetLineColor(ROOT.kAzure+4);	
           temp = ("%s/output_TTZ" % self.histosdir)
           if( temp in datasetnamebkg and  "TTZ" in datasetnamebkg and ( self.whichenergy in datasetnamebkg or  self.whichsample in datasetnamebkg) and hfourlepbestmass_4l_afterSel_new_TTV.GetEntries()>0. ): 
             legend.AddEntry(hfourlepbestmass_4l_afterSel_new_TTV,"TTV", "F")
             print "     Label= Total TTV     Entries= " , hfourlepbestmass_4l_afterSel_new_TTV.Integral(0,-1) 
           nEvent_4l_w_TTV.Add(nEvent_4l_w_new) # listTTV_w.Add(nEvent_4l_w_new)
           nEvent_4l_TTV.Add(nEvent_4l_new) # listTTV.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

         if( "_TTW" in datasetnamebkg):
           print "     TTW" 
           hfourlepbestmass_4l_afterSel_new_TTV.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);        
           hfourlepbestmass_4l_afterSel_new_TTV.SetMarkerColor(ROOT.kAzure+4)
           hfourlepbestmass_4l_afterSel_new_TTV.SetFillColor(ROOT.kAzure+4)
           hfourlepbestmass_4l_afterSel_new_TTV.SetLineColor(ROOT.kAzure+4)
           #//hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
           nEvent_4l_w_TTV.Add(nEvent_4l_w_new) # listTTV_w.Add(nEvent_4l_w_new)
           nEvent_4l_TTV.Add(nEvent_4l_new) # listTTV.Add(nEvent_4l_new)
           nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
           nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

     #// ggZZ
     elif( "GluGluToZZTo" in datasetnamebkg or  "GluGluToContinToZZTo" in datasetnamebkg): #      if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ):
       print "Adding sample ggZZ" 
       hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : self.errorZZ=self.errorZZ+pow(sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries(),2)
       hfourlepbestmass_4l_afterSel_new_ggZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_ggZZ.SetLineColor(1)
       hfourlepbestmass_4l_afterSel_new_ggZZ.SetFillColor(ROOT.kPink+5)
       hfourlepbestmass_4l_afterSel_new_ggZZ.SetLineWidth(1)

       hfourlepbestmass_4l_afterSel_new_ZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineColor(1)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetFillColor(ZZBgColor)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineWidth(1)
       theerror = 0.0 
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : theerror = sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()
       print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries(), "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) , " +- ", theerror
       #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
       if ( "GluGluToContinToZZTo2e2mu" in datasetnamebkg and ( self.whichenergy in datasetnamebkg or self.whichsample in datasetnamebkg) ) : 
         #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_ggZZ,"ggZZ", "F")
         print "     Label= ggZZ     Entries= " , hfourlepbestmass_4l_afterSel_new_ggZZ.Integral(0,-1) 
         print "     Label= Total ZZ     Entries= " , hfourlepbestmass_4l_afterSel_new_ZZ.Integral(0,-1) 

       nEvent_4l_w_ZZ.Add(nEvent_4l_w_new) # listZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_ZZ.Add(nEvent_4l_new) # listZZ.Add(nEvent_4l_new)
       nEvent_4l_ggZZ.Add(nEvent_4l_new) # listqqZZ.Add(nEvent_4l_new)
       nEvent_4l_w_ggZZ.Add(nEvent_4l_w_new) # listqqZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
       nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
       nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
       nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

     # qqZZ
     elif(  "_ZZTo4L" in datasetnamebkg ): #if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ):
       print "Adding sample qqZZ"
       hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel ) )
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : self.errorZZ=self.errorZZ+pow(sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries(),2)
       hfourlepbestmass_4l_afterSel_new_qqZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetLineColor(1)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetFillColor(ROOT.kPink+5)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetLineWidth(1)

       hfourlepbestmass_4l_afterSel_new_ZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineColor(ZZBgColor)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetFillColor(ZZBgColor)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineWidth(1)

       if ( "8TeV" in self.whichsample ) : temp = ( "%s/output_ZZTo2e2mu_%s" % ( self.histosdir,self.whichsample) )
       elif ( "7TeV" in self.whichsample ) : temp = ( "%s/output_ZZTo2e2mu_mll4_%s" % ( self.histosdir,self.whichsample) )
       elif ( "13TeV" in self.whichsample ) : temp = ( "%s/output_ZZTo4L_%s" % ( self.histosdir,self.whichsample) )

       if( temp in datasetnamebkg ):
         if (self.errorZZ>0.) : self.errorZZ=sqrt(self.errorZZ)
         legend.AddEntry(hfourlepbestmass_4l_afterSel_new_ZZ,"Z#gamma^{*}, ZZ", "F")
         print "Label= qqZZ     Entries= " , hfourlepbestmass_4l_afterSel_new_qqZZ.Integral(0,-1) 
         print "Label= qqZZ+ggZZ   Entries= " , hfourlepbestmass_4l_afterSel_new_ZZ.Integral(0,-1), "  Error= " , self.errorZZ
         #self.outputyields = open("plots/test.txt")
         if ( "hM4l_9" in histlabel ) : 
             self.outputyields.write( "%s %f %s %f " % ( "ZZ " , hfourlepbestmass_4l_afterSel_new_ZZ.Integral(0,-1) , " +/- " , self.errorZZ ) )

       theerror = 0.0
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : theerror = sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()
       print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)
       nEvent_4l_w_ZZ.Add(nEvent_4l_w_new) # listZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_ZZ.Add(nEvent_4l_new) # listZZ.Add(nEvent_4l_new)
       nEvent_4l_qqZZ.Add(nEvent_4l_new) # listqqZZ.Add(nEvent_4l_new)
       nEvent_4l_w_qqZZ.Add(nEvent_4l_w_new) # listqqZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
       nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
       nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
       nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

     
     elif(  "_ZZTo2L2Nu" in datasetnamebkg ): #if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ):
       print "Adding sample qqZZ2l2nu" 
       hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel ) )      
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : self.errorZZ=self.errorZZ+pow(sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries(),2)
       #//print sqrt(errorZZ) 
       hfourlepbestmass_4l_afterSel_new_qqZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetLineColor(1)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetFillColor(ROOT.kPink+5)
       hfourlepbestmass_4l_afterSel_new_qqZZ.SetLineWidth(1)

       hfourlepbestmass_4l_afterSel_new_ZZ.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
       #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineColor(ZZBgColor)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetFillColor(ZZBgColor)
       hfourlepbestmass_4l_afterSel_new_ZZ.SetLineWidth(1)

       if ( "13TeV" in self.whichsample ) : temp = ("%s/output_ZZTo2L2Nu_%s" % (self.histosdir,self.whichsample))

       if( temp in datasetnamebkg ):
         if (self.errorZZ>0.) : self.errorZZ=sqrt(self.errorZZ)
         print "Label= qqZZ (with 2l2nu)     Entries= " , hfourlepbestmass_4l_afterSel_new_qqZZ.Integral(0,-1) 
         print "Label= qqZZ+ggZZ (with 2l2nu)  Entries= " , hfourlepbestmass_4l_afterSel_new_ZZ.Integral(0,-1), "  Error= " , self.errorZZ
         if ( "hM4l_9" in histlabel ) : self.outputyields.write( "%s %f %s %f" % ( "ZZ " , hfourlepbestmass_4l_afterSel_new_ZZ.Integral(0,-1) , " +/- " , self.errorZZ ))

       theerror = 0.0
       if (hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()>0.) : theerror = sqrt(hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries())*hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new[ndata].GetEntries()
       print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1), " +- ", theerror
       nEvent_4l_w_ZZ.Add(nEvent_4l_w_new) # listZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_ZZ.Add(nEvent_4l_new) # listZZ.Add(nEvent_4l_new)
       nEvent_4l_qqZZ.Add(nEvent_4l_new) # listqqZZ.Add(nEvent_4l_new)
       nEvent_4l_w_qqZZ.Add(nEvent_4l_w_new) # listqqZZ_w.Add(nEvent_4l_w_new)
       nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
       nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
       nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
       nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

     # =========>
     elif (self.useDYJetsFromData==False): #if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ): 
       if( "_MuPt5Enriched" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
         hfourlepbestmass_4l_afterSel_new_qcdMu.Add(hfourlepbestmass_4l_afterSel_new_new[ndata]);      
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
         hfourlepbestmass_4l_afterSel_new_qcdMu.SetLineColor(1)
         hfourlepbestmass_4l_afterSel_new_qcdMu.SetFillColor(ROOT.kTeal-8)
         hfourlepbestmass_4l_afterSel_new_qcdMu.SetLineWidth(1)

         temp = ("%s/output_QCD_Pt-15to20_MuPt5Enriched" % self.histosdir)
         if( temp in datasetnamebkg ): #// provided that this is the last single-top sample
           legend.AddEntry(hfourlepbestmass_4l_afterSel_new_qcdMu,"QCD MuPt5", "F")
           print "Label= QCD MuPt5    Entries= " , hfourlepbestmass_4l_afterSel_new_qcdMu.Integral(0,-1) 
         print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) 
         nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
         nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       elif( "_doubleEMEnriched" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
         hfourlepbestmass_4l_afterSel_new_qcdDEM.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
         hfourlepbestmass_4l_afterSel_new_qcdDEM.SetLineColor(1)
         hfourlepbestmass_4l_afterSel_new_qcdDEM.SetFillColor(ROOT.kTeal+8)
         hfourlepbestmass_4l_afterSel_new_qcdDEM.SetLineWidth(1)

         temp = ( "%s/output_QCD_Pt-80_doubleEMEnriched" % self.histosdir)
         if( temp in datasetnamebkg ): 
           legend.AddEntry(hfourlepbestmass_4l_afterSel_new_qcdDEM,"QCD doubleEM", "F")
           print "Label= QCD EM    Entries= " , hfourlepbestmass_4l_afterSel_new_qcdMu.Integral(0,-1) 

         print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) 
         #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
         nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       elif( "_BCtoE" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_new.append ( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
         hfourlepbestmass_4l_afterSel_new_qcdBC.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
         hfourlepbestmass_4l_afterSel_new_qcdBC.SetLineColor(1)
         hfourlepbestmass_4l_afterSel_new_qcdBC.SetFillColor(ROOT.kTeal-2)
         hfourlepbestmass_4l_afterSel_new_qcdBC.SetLineWidth(1)
         temp = ( "%s/output_QCD_Pt-20to30_BCtoE" % self.histosdir)
         if( temp in datasetnamebkg): #// provided that this is the last single-top sample
           legend.AddEntry(hfourlepbestmass_4l_afterSel_new_qcdBC,"QCD BCtoE", "F")
           print "Label= QCD BCtoE    Entries= " , hfourlepbestmass_4l_afterSel_new_qcdBC.Integral(0,-1) 
         print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) 
         nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
         nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       elif( "QCD_Pt" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_new.append( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
         hfourlepbestmass_4l_afterSel_new_qcd.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         #//hfourlepbestmass_4l_afterSel_new_new[ndata].SetFillStyle(1001)
         hfourlepbestmass_4l_afterSel_new_qcd.SetLineColor(ROOT.kTeal-2)
         hfourlepbestmass_4l_afterSel_new_qcd.SetFillColor(ROOT.kTeal-2)
         hfourlepbestmass_4l_afterSel_new_qcd.SetLineWidth(1)
         temp = ("%s/output_QCD_Pt_1000to1400" % self.histosdir)
         if( temp in datasetnamebkg and hfourlepbestmass_4l_afterSel_new_qcd.GetEntries()>0.): 
           leg0.AddEntry(hfourlepbestmass_4l_afterSel_new_qcd,"QCD", "F")
           legend.AddEntry(hfourlepbestmass_4l_afterSel_new_qcd,"QCD", "F")
           print "Label= QCD Entries= " , hfourlepbestmass_4l_afterSel_new_qcd.Integral(0,-1) 

         print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) 
         #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_new[ndata],self.Vlabelbkg[datasetId], "F")
         nEvent_4l_w_QCD.Add(nEvent_4l_w_new) # listQCD_w.Add(nEvent_4l_w_new)
         nEvent_4l_QCD.Add(nEvent_4l_new) # listQCD.Add(nEvent_4l_new)
         nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
         nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

       #// single top
       #//elif (datasetId>=12 and datasetId<=14):
       elif( "ST_" in datasetnamebkg or   "Tbar_" in datasetnamebkg ):
         hfourlepbestmass_4l_afterSel_new_new.append( hfourlepbestmass_4l_afterSel_new[ndata].Rebin(self.nRebin,histlabel) )
         hfourlepbestmass_4l_afterSel_new_singlet.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])
         #// hfourlepbestmass_4l_afterSel_new_new[ndata].SetMarkerColor(datasetId+4)
         #//       hfourlepbestmass_4l_afterSel_new_new[ndata].SetMarkerStyle(26)
         #//       hfourlepbestmass_4l_afterSel_new_new[ndata].SetLineWidth(2)
         #//       hfourlepbestmass_4l_afterSel_new_new[ndata].Draw("sameP")
         hfourlepbestmass_4l_afterSel_new_singlet.SetLineColor(self.Vcolorbkg[datasetId])
         hfourlepbestmass_4l_afterSel_new_singlet.SetFillColor(ROOT.kViolet)
         #//hfourlepbestmass_4l_afterSel_new_singlet.SetFillStyle(3004)
         hfourlepbestmass_4l_afterSel_new_singlet.SetLineWidth(1)
         temp = ("%s/output_ST_" % self.histosdir)
         if( temp in datasetnamebkg and  "t-channel" in datasetnamebkg ): #// provided that this is the last single-top sample
           #//hfourlepbestmass_4l_afterSel_new_singlet.Draw("sameP")
           leg0.AddEntry(hfourlepbestmass_4l_afterSel_new_singlet,"Single Top", "F")
           legend.AddEntry(hfourlepbestmass_4l_afterSel_new_singlet,"Single Top", "F")
           print "Label= single t     Entries= " , hfourlepbestmass_4l_afterSel_new_singlet.Integral(0,-1) 
         print "Label= " , self.Vlabelbkg[datasetId] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new[ndata].Integral(0,-1) 
 
         nEvent_4l_w_ST.Add(nEvent_4l_w_new) # listST_w.Add(nEvent_4l_w_new)
         nEvent_4l_ST.Add(nEvent_4l_new) # listST.Add(nEvent_4l_new)
         nEvent_4l_TT.Add(nEvent_4l_new) # listTT.Add(nEvent_4l_new)
         nEvent_4l_w_TT.Add(nEvent_4l_w_new) # listTT_w.Add(nEvent_4l_w_new)
         nEvent_4l_w_totalbkgMC.Add(nEvent_4l_w_new) # listtotalbkgMC_w.Add(nEvent_4l_w_new)
         nEvent_4l_totalbkgMC.Add(nEvent_4l_new) # listtotalbkgMC.Add(nEvent_4l_new)
         nEvent_4l_w_totbkg_noSM_H.Add(nEvent_4l_w_new) # listtotbkg_noSM_H_w.Add(nEvent_4l_w_new)
         nEvent_4l_totbkg_noSM_H.Add(nEvent_4l_new) # listtotbkg_noSM_H.Add(nEvent_4l_new)

     #if( "WZTo" in datasetnamebkg or "WWTo" in datasetnamebkg or "DYJetsToLL" in datasetnamebkg or "DYlightJetsToLL" in datasetnamebkg or "DYbbJetsToLL" in datasetnamebkg or "DYccJetsToLL" in datasetnamebkg or "ZToEE" in datasetnamebkg or "TTT" in datasetnamebkg or "WJetsToLNu" in datasetnamebkg or "M125" in datasetnamebkg or "ZZZ" in datasetnamebkg or "WWZ" in datasetnamebkg or "WZZ" in datasetnamebkg or "TTWJet" in datasetnamebkg or "TTZTo" in datasetnamebkg ):
  
     print "INFO creating The Stack "

     tempp = '!@#$%^&*()' # ( "%s/output_ZZTo2e2mu_%s" % (self.histosdir,self.whichsample) )
     if ( "8TeV" in self.whichsample ) : tempp = ( "%s/output_ZZTo2e2mu_%s" % (self.histosdir,self.whichsample) )
     elif ( "7TeV" in self.whichsample ) : tempp = ( "%s/output_ZZTo2e2mu_mll4_%s" % (self.histosdir,self.whichsample) )    
     elif ( "13TeV" in self.whichsample ) : tempp = ( "%s/output_ZZTo4L_%s" % (self.histosdir,self.whichsample) )
     if( tempp in datasetnamebkg):
       print "Stacking ZZ (ggZZ+qqZZ)" 
       htotal.Add(hfourlepbestmass_4l_afterSel_new_ZZ)
       #//htotal.Add(hfourlepbestmass_4l_afterSel_new_qqZZ)
       htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_ZZ)
       hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_ZZ)

       #nEvent_4l_ZZ.Merge(listZZ)
       #nEvent_4l_w_ZZ.Merge(listZZ_w)
       #nEvent_4l_qqZZ.Merge(listqqZZ)
       #nEvent_4l_w_qqZZ.Merge(listqqZZ_w)
       #nEvent_4l_ggZZ.Merge(listggZZ)
       #nEvent_4l_w_ggZZ.Merge(listggZZ_w);      
     else :       
        temppp = ("%s" % self.histosdir)
        #// Higgs bkg
        if( temppp in datasetnamebkg and ( "output_GluGluHToZZTo4L" in datasetnamebkg or ( "output_GluGluHToZZTo4L" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) : 
            #//if (histlabel.find("hM4l_7")>10):
            print "Adding ggH" 
            #//htotal.Add(hfourlepbestmass_4l_afterSel_new_ggH)
            #//htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_ggH); 	   
            htotal.Add(hfourlepbestmass_4l_afterSel_new_totSM_H);                                                                                                             
            htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_totSM_H)
            #nEvent_4l_totSM_H.Merge(listtotSM_H)
            #nEvent_4l_w_totSM_H.Merge(listtotSM_H_w);	    
            #//

        if( temppp in datasetnamebkg and (           "output_WminusH" in datasetnamebkg or           ( "output_WminusH" in datasetnamebkg and  self.whichenergy in datasetnamebkg)                                               )          )  : 
            #//if (histlabel.find("hM4l_7")>10):
            print "Adding WH" 
            #//htotal.Add(hfourlepbestmass_4l_afterSel_new_WH)
            #//htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_WH)
            #//

        if( temppp in datasetnamebkg and ( "output_ZH" in datasetnamebkg or ( "output_ZH" in datasetnamebkg and  self.whichenergy in datasetnamebkg ) ) ) : 
            #//if (histlabel.find("hM4l_7")>10):
            print "Adding ZH" 
            #//htotal.Add(hfourlepbestmass_4l_afterSel_new_ZH)
            #//htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_ZH)
            #//

        if( temppp in datasetnamebkg and ( "output_ttH" in datasetnamebkg or ( "output_ttH" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
            #//if (histlabel.find("hM4l_7")>10):
            print "Adding ttH" 
            #//htotal.Add(hfourlepbestmass_4l_afterSel_new_ttH)
            #//htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_ttH)
            #//

        if( temppp in datasetnamebkg and ( "output_VBF" in datasetnamebkg or ( "output_VBF" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
            #//if (histlabel.find("hM4l_7")>10):
            print "Adding VBF" 
            #//htotal.Add(hfourlepbestmass_4l_afterSel_new_VBFH)
            #//htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_VBFH)
            #//


        #// other backgrounds
        if (self.useDYJets==True):
          if( temppp in datasetnamebkg and ( "output_DYJetsToLL_M-50_Tune" in datasetnamebkg or "output_ZToEE_NNPDF30_13TeV-powheg_M_1400_2300" in datasetnamebkg or ( "output_DYJetsToLL_TuneZ2_M-50" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
            htotal.Add(hfourlepbestmass_4l_afterSel_new_DY)
            htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_DY)
            #nEvent_4l_DY.Merge(listDY)
            #nEvent_4l_w_DY.Merge(listDY_w)
            hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_DY)


        elif (self.useDYJets==False):
          if( temppp in datasetnamebkg and  "output_DYlightJetsToLL_TuneZ2_M-50" in datasetnamebkg ) :
            htotal.Add(hfourlepbestmass_4l_afterSel_new_DYlight)
            htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_DYlight)
            hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_DYlight)
            #nEvent_4l_DY.Merge(listDY)
            #nEvent_4l_w_DY.Merge(listDY_w)

          if( temppp in datasetnamebkg and  "output_DYbbJetsToLL_TuneZ2_M-50" in datasetnamebkg ) :
            htotal.Add(hfourlepbestmass_4l_afterSel_new_DYbb)
            htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_DYbb)

          if( temppp in datasetnamebkg and  "output_DYccJetsToLL_TuneZ2_M-50" in datasetnamebkg ) :
            htotal.Add(hfourlepbestmass_4l_afterSel_new_DYcc)
            htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_DYcc)



        if( temppp in datasetnamebkg and ( "output_WWTo" in datasetnamebkg or ( "output_WWTo" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_WW)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_WW)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_WW)

        if( temppp in datasetnamebkg and ( "output_WZTo" in datasetnamebkg or ( "output_WZTo" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_WZ);         
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_WZ)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_WZ)
          #nEvent_4l_WZ_WW_Wj.Merge(listWZ_WW_Wj)
          #nEvent_4l_w_WZ_WW_Wj.Merge(listWZ_WW_Wj_w)

        if( temppp in datasetnamebkg and ( "output_TTT" in datasetnamebkg or ( "output_TTT" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_TT);                        
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_TT)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_TT)
          #nEvent_4l_TT.Merge(listTT)
          #nEvent_4l_w_TT.Merge(listTT_w)

        if( temppp in datasetnamebkg and ( "output_WJ" in datasetnamebkg or ( "output_WJ" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_Wj)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_Wj)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_Wj)


        if( temppp in datasetnamebkg and ( "output_ZZZ" in datasetnamebkg or ( "output_ZZZ" in datasetnamebkg and  self.whichenergy in datasetnamebkg) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_VVV)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_VVV)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_VVV)
          #nEvent_4l_VVV.Merge(listVVV)
          #nEvent_4l_w_VVV.Merge(listVVV_w)


        if( temppp in datasetnamebkg and ( "output_TTZ" in datasetnamebkg or ( "output_TTZ" in datasetnamebkg and  self.whichenergy in datasetnamebkg ) ) ) :
          htotal.Add(hfourlepbestmass_4l_afterSel_new_TTV)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_TTV)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_TTV)
          #nEvent_4l_TTV.Merge(listTTV)
          #nEvent_4l_w_TTV.Merge(listTTV_w)



        #//if( "GluGluToZZTo4mu_BackgroundOnly" in datasetnamebkg ) #// provided that this is the last single-top sample      
        #//htotal.Add(hfourlepbestmass_4l_afterSel_new_ggZZ);      

        #//if( temppp in datasetnamebkg  "output_ZZTo2e2mu_8TeV" in datasetnamebkg ): 
        #//	htotal.Add(hfourlepbestmass_4l_afterSel_new_qqZZ)
        #//#//htotal.Add(hfourlepbestmass_4l_afterSel_new_qqZZ)

        if( temppp in datasetnamebkg and  "output_QCD_Pt-15to20_MuPt5Enriched" in datasetnamebkg ): 
          htotal.Add(hfourlepbestmass_4l_afterSel_new_qcdMu)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_qcdMu)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_qcdMu)

        if( temppp in datasetnamebkg and  "output_QCD_Pt-40_doubleEMEnriched" in datasetnamebkg ): 
          htotal.Add(hfourlepbestmass_4l_afterSel_new_qcdDEM)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_qcdDEM)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_qcdDEM)

        if( temppp in datasetnamebkg and  "output_QCD_Pt_20to30_BCtoE" in datasetnamebkg ):     
          htotal.Add(hfourlepbestmass_4l_afterSel_new_qcdBC)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_qcdBC)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_qcdBC)


        if( temppp in datasetnamebkg and  "output_QCD_Pt_1000to1400" in datasetnamebkg ):
          htotal.Add(hfourlepbestmass_4l_afterSel_new_qcd)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_qcd)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_qcd)
          #nEvent_4l_w_QCD.Merge(listQCD_w)
          #nEvent_4l_QCD.Merge(listQCD)


        if( temppp in datasetnamebkg and  "output_ST_" in datasetnamebkg and  "t-channel" in datasetnamebkg ):     	 
          htotal.Add(hfourlepbestmass_4l_afterSel_new_singlet)
          htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_singlet)
          hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Add(hfourlepbestmass_4l_afterSel_new_singlet)

     ndata = ndata + 1 # f2.append( ROOT.TFile.Open(dataset) )


     #// htotal.Add(hfourlepbestmass_4l_afterSel_new_new[ndata])



   #// 
   #nEvent_4l_w_totalbkgMC.Merge(listtotalbkgMC_w)
   #nEvent_4l_totalbkgMC.Merge(listtotalbkgMC);	
   #nEvent_4l_w_totbkg_noSM_H.Merge(listtotbkg_noSM_H_w)
   #nEvent_4l_totbkg_noSM_H.Merge(listtotbkg_noSM_H);	
                


   # In[17]:


   #nEvent_4l_totbkg_noSM_H.Merge(listtotbkg_noSM_H);	
   #c2 = ROOT.TCanvas("c2","c2",600,600)
   ##hfourlepbestmass_4l_afterSel_new_new[119].Draw("hist") ; 
   #htotaldata.Draw("EP")
   ##gr.Draw("EP")
   ##htotal.Draw("hist")
   ##htotalHisto.Draw("hist")
   #c2.Draw()
  
   #Things_I_Can_Draw=[hfourlepbestmass_4l_afterSel_new, hfourlepbestmass_4l_afterSel_new_new, htotaldata, gr, htotal, htotalHisto]
   ##Things_I_Can_Draw=[hfourlepbestmass_4l_afterSel_new_DY , 'hfourlepbestmass_4l_afterSel_new_DYbb' , 'hfourlepbestmass_4l_afterSel_new_DYcc' , 'hfourlepbestmass_4l_afterSel_new_DYlight' , 'hfourlepbestmass_4l_afterSel_new_TT' , 'hfourlepbestmass_4l_afterSel_new_TTV' , 'hfourlepbestmass_4l_afterSel_new_VBFH' , 'hfourlepbestmass_4l_afterSel_new_VH' , 'hfourlepbestmass_4l_afterSel_new_VVV' , 'hfourlepbestmass_4l_afterSel_new_WH' , 'hfourlepbestmass_4l_afterSel_new_WW' , 'hfourlepbestmass_4l_afterSel_new_WZ' , 'hfourlepbestmass_4l_afterSel_new_Wj' , 'hfourlepbestmass_4l_afterSel_new_ZH' , 'hfourlepbestmass_4l_afterSel_new_ZZ' , 'hfourlepbestmass_4l_afterSel_new_ggH' , 'hfourlepbestmass_4l_afterSel_new_ggZZ' , 'hfourlepbestmass_4l_afterSel_new_qcd' , 'hfourlepbestmass_4l_afterSel_new_qcdBC' , 'hfourlepbestmass_4l_afterSel_new_qcdDEM' , 'hfourlepbestmass_4l_afterSel_new_qcdMu' , 'hfourlepbestmass_4l_afterSel_new_qqZZ' , 'hfourlepbestmass_4l_afterSel_new_singlet' , 'hfourlepbestmass_4l_afterSel_new_totSM_H' , 'hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H' , 'hfourlepbestmass_4l_afterSel_new_ttH']
   Things_I_Can_Draw=[hfourlepbestmass_4l_afterSel_new_DY , hfourlepbestmass_4l_afterSel_new_DYbb , hfourlepbestmass_4l_afterSel_new_DYcc , hfourlepbestmass_4l_afterSel_new_DYlight , hfourlepbestmass_4l_afterSel_new_TT , hfourlepbestmass_4l_afterSel_new_TTV , hfourlepbestmass_4l_afterSel_new_VBFH , hfourlepbestmass_4l_afterSel_new_VH , hfourlepbestmass_4l_afterSel_new_VVV , hfourlepbestmass_4l_afterSel_new_WH , hfourlepbestmass_4l_afterSel_new_WW , hfourlepbestmass_4l_afterSel_new_WZ , hfourlepbestmass_4l_afterSel_new_Wj , hfourlepbestmass_4l_afterSel_new_ZH , hfourlepbestmass_4l_afterSel_new_ZZ , hfourlepbestmass_4l_afterSel_new_ggH , hfourlepbestmass_4l_afterSel_new_ggZZ , hfourlepbestmass_4l_afterSel_new_qcd , hfourlepbestmass_4l_afterSel_new_qcdBC , hfourlepbestmass_4l_afterSel_new_qcdDEM , hfourlepbestmass_4l_afterSel_new_qcdMu , hfourlepbestmass_4l_afterSel_new_qqZZ , hfourlepbestmass_4l_afterSel_new_singlet , hfourlepbestmass_4l_afterSel_new_totSM_H , hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H , hfourlepbestmass_4l_afterSel_new_ttH ]
   #c2 = ROOT.TCanvas("c2","c2",600,600)

   #if 1 == 0 :
   #if "hMZ_3" in histlabel :
   if "hMZ_3" in histlabel or "hPFMET_3" in histlabel or "hM4l_7"  in histlabel or "hPFMET_8" in histlabel :
     print "INFO about to draw each background source in 10 seconds each plot is drawn after 5 seconds of sleep"
     c2 = ROOT.TCanvas("c2","c2",600,600)
     c2.cd()
     i=0
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=1
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=2
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=3
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=4
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=5
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=6
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=7
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=8
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=9
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=10
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=11
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=12
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=13
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=14
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=15
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=16
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=17
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=18
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=19
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=20
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=21
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=22
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=23
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=24
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

     i=25
     print Things_I_Can_Draw[i].GetName()
     Things_I_Can_Draw[i].Print()
     Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()
     #
     c1.cd()

   htotalHistoRatio.Sumw2()

   htotalHistoRatio.Divide(htotaldata,htotalHisto,1.,1.)

   ##htotaldata.Draw("EP")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()
   ##htotalHisto.Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()
   #htotalHistoRatio.Draw("EP")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()


   # In[18]:
   #// Signal
   hfourlepbestmass_4l_afterSel_new_signal125 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_signal125", "hfourlepbestmass_4l_afterSel_new_signal125",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_DM1", "hfourlepbestmass_4l_afterSel_new_monoH_DM1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_DM10 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_DM10", "hfourlepbestmass_4l_afterSel_new_monoH_DM10",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_DM100 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_DM100", "hfourlepbestmass_4l_afterSel_new_monoH_DM100",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_DM500 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_DM500", "hfourlepbestmass_4l_afterSel_new_monoH_DM500",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1000 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_DM1000", "hfourlepbestmass_4l_afterSel_new_monoH_DM1000",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1", "hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10", "hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100", "hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500", "hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000", "hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000",self.Nbins ,self.Xmin,self.Xmax)

   #// 2HDM 

   hfourlepbestmass_4l_afterSel_new_monoH_MZP600 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP600", "hfourlepbestmass_4l_afterSel_new_monoH_MZP600",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP800 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP800", "hfourlepbestmass_4l_afterSel_new_monoH_MZP800",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP1000", "hfourlepbestmass_4l_afterSel_new_monoH_MZP1000",self.Nbins ,self.Xmin,self.Xmax)
   #hfourlepbestmass_4l_afterSel_new_monoH_MZP1200
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_monoH_MZP1200 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP1200", "hfourlepbestmass_4l_afterSel_new_monoH_MZP1200", NMBINS, logMbins)
   else : hfourlepbestmass_4l_afterSel_new_monoH_MZP1200 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP1200", "hfourlepbestmass_4l_afterSel_new_monoH_MZP1200",self.Nbins ,self.Xmin,self.Xmax)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP1400", "hfourlepbestmass_4l_afterSel_new_monoH_MZP1400",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP1700", "hfourlepbestmass_4l_afterSel_new_monoH_MZP1700",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP2000", "hfourlepbestmass_4l_afterSel_new_monoH_MZP2000",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500 = ROOT.TH1F("hfourlepbestmass_4l_afterSel_new_monoH_MZP2500", "hfourlepbestmass_4l_afterSel_new_monoH_MZP2500",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp10000_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-10000_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-10000_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp1000_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-1000_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-1000_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-100_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-100_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-10_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-10_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp2000_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-2000_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-2000_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp200_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-200_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-200_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp20_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-20_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-20_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp300_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-300_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-300_MChi-1",self.Nbins ,self.Xmin,self.Xmax)

   #hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1=ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1","hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1", NMBINS, logMbins)
   else : hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1","hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1",self.Nbins ,self.Xmin,self.Xmax)

   nEvent_4l_w_ZpBaryonic_MZp500_MChi1 = ROOT.TH1D("nEvent_4l_w_ZpBaryonic_MZp500_MChi1","nEvent_4l_w_ZpBaryonic_MZp500_MChi1",22,0.,22.)
   nEvent_4l_ZpBaryonic_MZp500_MChi1 = ROOT.TH1D("nEvent_4l_ZpBaryonic_MZp500_MChi1","nEvent_4l_ZpBaryonic_MZp500_MChi1",22,0.,22.)
   nEvent_4l_w_ZpBaryonic_MZp500_MChi1.Sumw2()
   nEvent_4l_ZpBaryonic_MZp500_MChi1.Sumw2()
   listZpBaryonic_MZp500_MChi1_w = ROOT.TList()
   listZpBaryonic_MZp500_MChi1 = ROOT.TList()

   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi1 = ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-50_MChi-1","hfourlepbestmass_4l_newZpBaryonic_MZp-50_MChi-1",self.Nbins ,self.Xmin,self.Xmax)
   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10=ROOT.TH1F("hfourlepbestmass_4l_newZpBaryonic_MZp-50_MChi-10","hfourlepbestmass_4l_newZpBaryonic_MZp-50_MChi-10",self.Nbins ,self.Xmin,self.Xmax)


   # In[19]:


   # lines 1971 - 2325 in PlotStack4l.plotm4l.py
   arraysizesig = []
   arraysizesig.append (self.Nbins)
   print  "Bins= " , arraysizesig[0] 

   #float bincont125[arraysizesig[0]],
   #      bincontgg125[arraysizesig[0]],bincontvbf125[arraysizesig[0]]
   bincont125=[]
   bincontgg125=[]
   bincontvbf125=[]
   #for (int i=0;i<hfourlepbestmass_4l_afterSel_new_signal125.GetNbinsX();i++):
   for i in xrange(hfourlepbestmass_4l_afterSel_new_signal125.GetNbinsX()) : 
     bincont125.append(0.)
     #// bincontgg125[i]=0.
     #// bincontvbf125[i]=0.


   #delete [] arraysizesig

   print "Number of signal samples= " , len(self.Vdatasetnamesig) 

   for datasetIdSig in xrange(len(self.Vdatasetnamesig)-1, -1, -1): # for ( int datasetIdSig=len(self.Vdatasetnamesig)-1; datasetIdSig >=0; datasetIdSig--):  
     dataset = ( "%s" % self.Vdatasetnamesig[datasetIdSig])
     print "Counter=" , datasetIdSig , " Root-ple=" , dataset , " Label=" , self.Vlabelsig[datasetIdSig] 

     datasetnamesig = self.Vdatasetnamesig[datasetIdSig]

     f0 = ROOT.TFile.Open(dataset)

     nEvent_4l_w_new = f0.Get("nEvent_4l_w")
     nEvent_4l_new = f0.Get("nEvent_4l")

     hfourlepbestmass_4l_afterSel_new = f0.Get(histlabel)
     hfourlepbestmass_4l_afterSel_new_new="" #ROOT.TH1()  #NULL

     if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : hfourlepbestmass_4l_afterSel_new_new = f0.Get(histlabel)
     else : hfourlepbestmass_4l_afterSel_new_new=hfourlepbestmass_4l_afterSel_new.Rebin(self.nRebin, histlabel)


     #//hfourlepbestmass_4l_afterSel_new_new.SetLineColor()
     #//hfourlepbestmass_4l_afterSel_new_new.SetFillColor(0)
     #//hfourlepbestmass_4l_afterSel_new_new.SetFillStyle(3244)
     hfourlepbestmass_4l_afterSel_new_new.SetMarkerSize(1.5)
     #//hfourlepbestmass_4l_afterSel_new_new.Draw("same")
     
     print "Label= " , self.Vlabelsig[datasetIdSig] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new.GetEntries() 
     theerror = 0.0
     if (hfourlepbestmass_4l_afterSel_new_new.GetEntries()>0) : theerror = sqrt(hfourlepbestmass_4l_afterSel_new_new.GetEntries())*hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new.GetEntries()
     print "Label= " , self.Vlabelsig[datasetIdSig] , "  Entries= " , hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1), " Error= ", theerror

     if( "Higgs_Zprime_nohdecay" in datasetnamesig and  "1GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_DM1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_Zprime_nohdecay" in datasetnamesig and  "10GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_DM10.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_Zprime_nohdecay" in datasetnamesig and  "100GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_DM100.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_Zprime_nohdecay" in datasetnamesig and  "500GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_DM500.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_Zprime_nohdecay" in datasetnamesig and  "1000GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_DM1000.Add(hfourlepbestmass_4l_afterSel_new_new)

     if( "Higgs_scalar_nohdecay" in datasetnamesig and  "1GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_scalar_nohdecay" in datasetnamesig and  "10GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_scalar_nohdecay" in datasetnamesig and  "100GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_scalar_nohdecay" in datasetnamesig and  "500GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "Higgs_scalar_nohdecay" in datasetnamesig and  "1000GeV" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000.Add(hfourlepbestmass_4l_afterSel_new_new)

     #//2HDM
     if( "2HDM_MZp-600" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP600.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-800" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP800.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-1000" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-1200" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-1400" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-1700" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-2000" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "2HDM_MZp-2500" in datasetnamesig) : hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.Add(hfourlepbestmass_4l_afterSel_new_new)

     #// ZpBaryonic
     if( "ZpBaryonic_MZp-10000_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp10000_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-1000_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp1000_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-100_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-10_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-2000_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp2000_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-200_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp200_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-20_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp20_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-300_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp300_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-500_MChi-1" in datasetnamesig):
       hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
       nEvent_4l_w_ZpBaryonic_MZp500_MChi1.Add(nEvent_4l_w_new) # listZpBaryonic_MZp500_MChi1_w.Add(nEvent_4l_w_new)
       nEvent_4l_ZpBaryonic_MZp500_MChi1.Add(nEvent_4l_new) # listZpBaryonic_MZp500_MChi1.Add(nEvent_4l_new)
       
     if( "ZpBaryonic_MZp-50_MChi-1" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi1.Add(hfourlepbestmass_4l_afterSel_new_new)
     if( "ZpBaryonic_MZp-50_MChi-10" in datasetnamesig) : hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.Add(hfourlepbestmass_4l_afterSel_new_new)


     #//print "Nbins=" , hfourlepbestmass_4l_afterSel_new_new.GetNbinsX() 
     for nbins in xrange(1,hfourlepbestmass_4l_afterSel_new_new.GetNbinsX()+1,1): #     for (int nbins=1;nbins<=hfourlepbestmass_4l_afterSel_new_new.GetNbinsX(); nbins++):
       #// print "BinCenter=" , hfourlepbestmass_4l_afterSel_new_new.GetBinCenter(nbins) , " BinContent=" , hfourlepbestmass_4l_afterSel_new_new.GetBinContent(nbins) , " BinError Content=" , hfourlepbestmass_4l_afterSel_new_new.GetBinError(nbins) 

       if ( "M-125" in datasetnamesig): #// Adding SMHiggs, VBF, TTH, WH, ZH
         if (nbins==1):
           print "Adding samples at 125 GeV" , dataset 
           #//print sqrt(errorH125) , " " , sqrt(hfourlepbestmass_4l_afterSel_new_new.GetEntries())*hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new.GetEntries() 
           if (hfourlepbestmass_4l_afterSel_new_new.GetEntries()>0.) : self.errorH125=errorH125+pow(sqrt(hfourlepbestmass_4l_afterSel_new_new.GetEntries())*hfourlepbestmass_4l_afterSel_new_new.Integral(0,-1)/hfourlepbestmass_4l_afterSel_new_new.GetEntries(),2)
           #//print sqrt(errorH125) 

         bincont125[nbins-1]=bincont125[nbins-1]+float(hfourlepbestmass_4l_afterSel_new_new.GetBinContent(nbins))



       #// only ggF and VBF
       #// if ( "SMHiggsToZZTo4L_M-125" in datasetnamesig): #// Adding VBF only
       #// if (nbins==1) : print "Adding samples at 125 GeV ggF only" , dataset 
       #// 	bincontgg125[nbins-1]=bincontgg125[nbins-1]+float(hfourlepbestmass_4l_afterSel_new_new.GetBinContent(nbins))
       #// 
       #// if ( "VBF_HToZZTo4L_M-125" in datasetnamesig or datasetnamesig.find("VBF_ToHToZZTo4L_M-125")<100): #// Adding VBF only
       #// if (nbins==1) : print "Adding samples at 125 GeV VBF only" , dataset 
       #// 	bincontvbf125[nbins-1]=bincontvbf125[nbins-1]+float(hfourlepbestmass_4l_afterSel_new_new.GetBinContent(nbins))
       #// 


       #//print "BinCont= " , bincont[nbins-1] 

       #// #char temp[328]
       #// temp = ("%s" % self.histosdir)

       #// if (datasetnamesig.find(temp)< 100 and datasetnamesig.find("output_SMHiggsToZZTo4L_M-125") < 180 ):
       #// 	#//print double(bincont125[nbins-1]) 
       #// 	hfourlepbestmass_4l_afterSel_new_signal125.SetBinContent(nbins,double(bincont125[nbins-1]))

       #// 

       #// ongly ggF and VBF
       #// if (datasetnamesig.find(temp)< 100 and datasetnamesig.find("output_SMHiggsToZZTo4L_M125") < 180 ):
       #// 	#//print double(bincontgg125[nbins-1]) 
       #// 	hfourlepbestmass_4l_afterSel_new_signalgg125.SetBinContent(nbins,double(bincontgg125[nbins-1]))
       #// 
       #// if (datasetnamesig.find(temp)< 100 and (datasetnamesig.find("output_VBF_HToZZTo4L_M125") < 180 or datasetnamesig.find("output_VBF_ToHToZZTo4L_M125") < 180) ):
       #// 	#//print double(bincontvbf125[nbins-1]) 
       #// 	hfourlepbestmass_4l_afterSel_new_signalvbf125.SetBinContent(nbins,double(bincontvbf125[nbins-1]))
       #// 





   #nEvent_4l_w_ZpBaryonic_MZp500_MChi1.Merge(listZpBaryonic_MZp500_MChi1_w)
   #nEvent_4l_ZpBaryonic_MZp500_MChi1.Merge(listZpBaryonic_MZp500_MChi1)

   if (self.errorH125>0.) : self.errorH125=sqrt(self.errorH125)

   #// print "Higgs Signal expected at mH=125 is " , hfourlepbestmass_4l_afterSel_new_signal125.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "mH=125 " , hfourlepbestmass_4l_afterSel_new_signal125.Integral(0,-1) , " +/- " , self.errorH125 

   #//print "Signal expected at mH=125 ggF only is " , hfourlepbestmass_4l_afterSel_new_signalgg125.Integral(0,-1) ;		     
   #//print "Signal expected at mH=125 VBF only is " , hfourlepbestmass_4l_afterSel_new_signalvbf125.Integral(0,-1) 

   #// Dark Matter monohiggs signal
   #// print "Mono-Higgs Signal expected at m_DM=1 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_DM1.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "m_DM=1 " , hfourlepbestmass_4l_afterSel_new_monoH_DM1.Integral(0,-1) , " +/- " , self.errorH125 

   #// print "Mono-Higgs Signal expected at m_DM=10 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_DM10.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "m_DM=1 " , hfourlepbestmass_4l_afterSel_new_monoH_DM10.Integral(0,-1) , " +/- " , self.errorH125 

   #// print "Mono-Higgs Signal expected at m_DM=100 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_DM100.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "m_DM=1 " , hfourlepbestmass_4l_afterSel_new_monoH_DM100.Integral(0,-1) , " +/- " , self.errorH125 

   #//  print "Mono-Higgs Signal expected at m_DM=500 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_DM500.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "m_DM=1 " , hfourlepbestmass_4l_afterSel_new_monoH_DM500.Integral(0,-1) , " +/- " , self.errorH125 

   #//  print "Mono-Higgs Signal expected at m_DM=1 TeV is " , hfourlepbestmass_4l_afterSel_new_monoH_DM1000.Integral(0,-1) , " +/- " , self.errorH125 
   #// if ( "hM4l_9" in histlabel ):::::::::::::: 
   #//   outputyields , "m_DM=1 " , hfourlepbestmass_4l_afterSel_new_monoH_DM1000.Integral(0,-1) , " +/- " , self.errorH125 

   #// 2HDM
   print "Mono-Higgs Signal expected for MZP600 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP600.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP600 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP600.Integral(0,-1) , " +/- " , self.errorH125 ) )

   print "Mono-Higgs Signal expected for MZP800 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP800.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP800 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP800.Integral(0,-1) , " +/- " , self.errorH125 ))

   print "Mono-Higgs Signal expected for MZP1000 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP1000 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.Integral(0,-1) , " +/- " , self.errorH125 ))

   print "Mono-Higgs Signal expected for MZP1200 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP1200 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.Integral(0,-1) , " +/- " , self.errorH125 ))

   print "Mono-Higgs Signal expected for MZP1400 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP1400 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.Integral(0,-1) , " +/- " , self.errorH125 ) )

   print "Mono-Higgs Signal expected for MZP1700 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP1700 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.Integral(0,-1) , " +/- " , self.errorH125 ) )

   print "Mono-Higgs Signal expected for MZP2000 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP2000 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.Integral(0,-1) , " +/- " , self.errorH125 ) )

   print "Mono-Higgs Signal expected for MZP2500 GeV is " , hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.Integral(0,-1) , " +/- " , self.errorH125 
   if ( "hM4l_9" in histlabel ) : self.outputyields.write ( "%s %f %s %f" % ( "m_ZP2500 " , hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.Integral(0,-1) , " +/- " , self.errorH125 ) )



   #// hfourlepbestmass_4l_afterSel_new_signal125.SetLineColor(ROOT.kRed-4)
   #// hfourlepbestmass_4l_afterSel_new_signalgg125.SetLineColor(ROOT.kRed-4);		     
   #// hfourlepbestmass_4l_afterSel_new_signalvbf125.SetLineColor(ROOT.kOrange-4)

   hfourlepbestmass_4l_afterSel_new_signal125.SetMarkerSize(0.95)

   hfourlepbestmass_4l_afterSel_new_totSM_H.SetMarkerColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_totSM_H.SetLineColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_totSM_H.SetFillColor(ROOT.kRed-4)

   #//if ( "hM4l_7" in histlabel ):
   #//  htotal.Add(hfourlepbestmass_4l_afterSel
   print "Total higgs 125 rate is= " , hfourlepbestmass_4l_afterSel_new_totSM_H.Integral() 
   #// htotalHisto.Add(hfourlepbestmass_4l_afterSel_new_totSM_H)
   #//hfourlepbestmass_4l_afterSel_new_totSM_H.Draw("hist same")
   legend.AddEntry(hfourlepbestmass_4l_afterSel_new_totSM_H,"H#rightarrowZZ#rightarrow 4l, m_{H}=125 GeV", "F")
   #//


   hfourlepbestmass_4l_afterSel_new_monoH_DM1.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1.SetMarkerColor(ROOT.kGreen-4)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1.SetLineColor(ROOT.kGreen-4)

   hfourlepbestmass_4l_afterSel_new_monoH_DM10.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_DM10.SetMarkerColor(ROOT.kBlue-4)
   hfourlepbestmass_4l_afterSel_new_monoH_DM10.SetLineColor(ROOT.kBlue-4)

   hfourlepbestmass_4l_afterSel_new_monoH_DM100.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_DM100.SetMarkerColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_monoH_DM100.SetLineColor(ROOT.kRed-4)

   hfourlepbestmass_4l_afterSel_new_monoH_DM500.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_DM500.SetMarkerColor(ROOT.kOrange-3)
   hfourlepbestmass_4l_afterSel_new_monoH_DM500.SetLineColor(ROOT.kOrange-3)

   hfourlepbestmass_4l_afterSel_new_monoH_DM1000.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1000.SetMarkerColor(ROOT.kOrange+7)
   hfourlepbestmass_4l_afterSel_new_monoH_DM1000.SetLineColor(ROOT.kOrange+7)

   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1.SetMarkerColor(ROOT.kGreen-4)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1.SetLineColor(ROOT.kGreen-4)

   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10.SetMarkerColor(ROOT.kBlue-4)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10.SetLineColor(ROOT.kBlue-4)

   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100.SetMarkerColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100.SetLineColor(ROOT.kRed-4)

   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500.SetMarkerColor(ROOT.kOrange-3)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500.SetLineColor(ROOT.kOrange-3)

   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000.SetMarkerColor(ROOT.kOrange+7)
   hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000.SetLineColor(ROOT.kOrange+7)

   #// 2HDM
   hfourlepbestmass_4l_afterSel_new_monoH_MZP600.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP600.SetMarkerColor(ROOT.kGreen-4)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP600.SetLineColor(ROOT.kGreen-4)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP800.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP800.SetMarkerColor(ROOT.kBlue-4)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP800.SetLineColor(ROOT.kBlue-4)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.SetMarkerColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.SetLineColor(ROOT.kRed-4)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.SetLineWidth(2)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.SetMarkerColor(ROOT.kOrange-3)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.SetLineColor(ROOT.kOrange-3)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.SetLineWidth(2)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.SetMarkerColor(ROOT.kBlack)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.SetLineColor(ROOT.kBlack)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.SetLineWidth(2)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.SetMarkerColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.SetLineColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.SetLineWidth(2)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.SetMarkerColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.SetLineColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.SetLineWidth(2)

   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.SetMarkerSize(0.95)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.SetMarkerColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.SetLineColor(ROOT.kCyan)
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.SetLineWidth(2)

   #// Z' baryonic
   hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.SetMarkerSize(0.95)
   hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.SetMarkerColor(ROOT.kRed)
   hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.SetLineColor(ROOT.kRed)
   hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.SetLineWidth(2)

   hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.SetMarkerSize(0.95)
   hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.SetMarkerColor(ROOT.kGreen-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.SetLineColor(ROOT.kGreen-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.SetLineWidth(2)

   hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.SetMarkerSize(0.95)
   hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.SetMarkerColor(ROOT.kBlue-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.SetLineColor(ROOT.kBlue-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.SetLineWidth(2)

   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.SetMarkerSize(0.95)
   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.SetMarkerColor(ROOT.kCyan-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.SetLineColor(ROOT.kCyan-4)
   hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.SetLineWidth(2)

   #// MZprime 2HDM
   #// htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP600)
   #// htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1000)
   #// htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1400)
   #// htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1700)

   #//MZprimeBaryonic
   #// htotal.Add(hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1)
   #//htotal.Add(hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1)
   #//htotal.Add(hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1)
   #//legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1,"m_{Z'B=10 GeV, m_{#chi=1 GeV","L")
   #//legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1,"m_{Z'B=100 GeV, m_{#chi=1 GeV","L")
   #//legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1,"m_{Z'B=500 GeV, m_{#chi=1 GeV","L")



   htotal.Draw("hist same")
   if (  "hLogX" in histlabel or  "hLogLinX" in histlabel ) : htotaldata.Draw("E1Psame")
   else : gr.Draw("EPsame")
   # This is necessary for the python notebook
   #c1.Draw()


   #if 1 == 0 :
   if "hMZ_3" in histlabel or "hPFMET_3" in histlabel or "hM4l_7"  in histlabel or "hPFMET_8" in histlabel :
    print "INFO about to draw possible signal sample in 10 seconds each plot is drawn after 5 seconds of sleep"
    Things_I_Can_Draw = [ hfourlepbestmass_4l_afterSel_new_monoH_MZP1200 , hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1 , hfourlepbestmass_4l_afterSel_new_monoH_DM1 , hfourlepbestmass_4l_afterSel_new_monoH_DM10 , hfourlepbestmass_4l_afterSel_new_monoH_DM100 , hfourlepbestmass_4l_afterSel_new_monoH_DM1000 , hfourlepbestmass_4l_afterSel_new_monoH_DM500 , hfourlepbestmass_4l_afterSel_new_monoH_MZP1000 , hfourlepbestmass_4l_afterSel_new_monoH_MZP1400 , hfourlepbestmass_4l_afterSel_new_monoH_MZP1700 , hfourlepbestmass_4l_afterSel_new_monoH_MZP2000 , hfourlepbestmass_4l_afterSel_new_monoH_MZP2500 , hfourlepbestmass_4l_afterSel_new_monoH_MZP600 , hfourlepbestmass_4l_afterSel_new_monoH_MZP800 , hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1 , hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10 , hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100 , hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000 , hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500 , hfourlepbestmass_4l_afterSel_new_signal125 , hfourlepbestmass_4l_newZpBaryonic_MZp10000_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp1000_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp2000_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp200_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp20_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp300_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi1 , hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10 , hfourlepbestmass_4l_afterSel_new_monoH_MZP1200 ,  hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1 ]
    print len(Things_I_Can_Draw)
    c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd()
    i=0 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=1 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=2 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=3 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=4 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=5 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=6 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=7 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=8 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=9 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=10 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=11 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=12 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=13 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=14 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=15 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=16 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=17 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=18 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=19 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=20 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=21 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=22 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=23 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=24 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=25 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=26 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=27 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=28 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=29 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=30 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    i=31 # 0 - 31
    print Things_I_Can_Draw[i].GetName()
    Things_I_Can_Draw[i].Print()
    Things_I_Can_Draw[i].Draw("hist")  ; time.sleep(5)  ; c2 = ROOT.TCanvas("c2","c2",600,600) ; c2.cd() #; c2.Draw()

    c1.cd()

   # In[20]:

   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.Draw("hist same")
   #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1200)
   legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP1200,"m_{Z'}=1200 GeV, m_{A_{0}}=300 GeV","L")
   #//hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.Draw("hist same")
   #//hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.Draw("hist same")

   #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP600)
   #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1000)
   #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_MZP1700)

   #//hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1.Draw("hist same")
   #//hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1.Draw("hist same")
   #//htotal.Add(hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1)
   hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1.Draw("hist same")
   #//hfourlepbestmass_4l_newZpBaryonic_MZp50_MChi10.Draw("hist same")
   #//legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp10_MChi1,"m_{Z'B=10 GeV, m_{#chi=1 GeV","L")
   #//legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp100_MChi1,"m_{Z'B=100 GeV, m_{#chi=1 GeV","L")
   legend.AddEntry(hfourlepbestmass_4l_newZpBaryonic_MZp500_MChi1,"m_{Z'B}=500 GeV, m_{#chi}=1 GeV","L")
   if ( "hMELA_8" in histlabel or "hPFMET_3" in histlabel or "h_hLogXPFMET_3" in histlabel or "hLogLinX" in histlabel or "hPFMET_8" in histlabel or "hMZ_3" in histlabel  or "hMZ1_5" in histlabel  or "hM4l_T_8" in histlabel or "DPHI_8" in histlabel or "hMjj_8" in histlabel or "hDjj_8" in histlabel or "hNbjets" in histlabel or "hNgood" in histlabel ) :
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_signal126);  #// signal stacked on top of background
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_signal126,"m_{H=126 GeV","L")
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_signal126)
     #//print "Plotting 4l+MET" 
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM1)
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM10)
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM100)
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM500)
     #//htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM1000)
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM1,"m_{DM=1 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM10,"m_{DM=10 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM100,"m_{DM=100 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM500,"m_{DM=500 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM1000,"m_{DM=1 TeV, Z'_{H", "L");	

     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1,"m_{DM=1 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM10,"m_{DM=10 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM100,"m_{DM=100 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM500,"m_{DM=500 GeV, Z'_{H", "L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_scalar_DM1000,"m_{DM=1 TeV, Z'_{H", "L");	


     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP600,"m_{Z'=600 GeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP800,"m_{Z'=800 GeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP1000,"m_{Z'=1 TeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP1200,"m_{Z'=1.2 TeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP1400,"m_{Z'=1.4 TeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP1700,"m_{Z'=1.7 TeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP2000,"m_{Z'=2 TeV, m_{A_{0=300 GeV","L")
     #//legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_MZP2500,"m_{Z'=2.5 TeV, m_{A_{0=300 GeV","L");       
     pass
   else : 
     #// if (  "hMjj_3" in histlabel or  "hDjj_3" in histlabel or  "hVD_3" in histlabel ):
     #//   hfourlepbestmass_4l_afterSel_new_signalgg125.Draw("same");   #// signal overimposed
     #//   hfourlepbestmass_4l_afterSel_new_signalvbf125.Draw("same");   #// signal overimposed
     #// 
     #// else : {
     #//  hfourlepbestmass_4l_afterSel_new_signal125.Draw("same")
     #//  legend.AddEntry(hfourlepbestmass_4l_afterSel_new_signal125,"m_{H=125 GeV","L")
     #//hfourlepbestmass_4l_afterSel_new_signal126.Draw("same")
     #//
     pass

   #// if ( "hMjj_3" in histlabel or  "hDjj_3" in histlabel or  "hVD_3" in histlabel ):
   #//   legend.AddEntry(hfourlepbestmass_4l_afterSel_new_signalgg125,"ggH, m_{H=125 GeV","L")
   #//   legend.AddEntry(hfourlepbestmass_4l_afterSel_new_signalvbf125,"qqH, m_{H=125 GeV","L")
   #// 
   #// else : {
   #//  print "Plotting 4l+MET" 
   #//  htotal.Add(hfourlepbestmass_4l_afterSel_new_monoH_DM100)
   #//  legend.AddEntry(hfourlepbestmass_4l_afterSel_new_monoH_DM100,"m_{DM=100 GeV, Z'_{H", "L")
   #//


   #//  #// Zoom
   #// htotal.SetMinimum(0)
   #//   htotal.SetMaximum(12.4) #// 3 GeV bin
   #//   htotal.Draw()
   #//   htotal.GetXaxis().SetRange(23,59) #// 3 GeV bin
   #//   #//htotal.GetYaxis().SetRangeUser(0.,16.)
   #//   htotal.GetYaxis().SetTitle("Events / 3 GeV") #// 3 GeV bin
   #//   sprintf(histotitle,"m_{%s [GeV]",self.whichchannel)
   #//   htotal.GetXaxis().SetTitle(histotitle)
   #//   htotal.GetXaxis().SetLabelSize(0.045)
   #//   htotal.GetXaxis().SetTitleSize(0.05)
   #//   htotal.GetXaxis().SetTitleOffset(1.15)
   #//   htotal.GetXaxis().SetTitleFont(42)
   #//   htotal.GetYaxis().SetLabelSize(0.045)
   #//   htotal.GetYaxis().SetTitleSize(0.05)
   #//   htotal.GetYaxis().SetTitleOffset(1.15)
   #//   htotal.GetYaxis().SetTitleFont(42)
   #//   gr.Draw("EPsame")

   #//   htotal.Draw("same")
   #//   gr.Draw("EPsame")

   #//leg0.Draw("same")
   #//leg1.Draw("same")

   legend.Draw("same")
   ll.Draw("same")

   print "Saving plots for " , whichchannel 
   saveaspdfzoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom.pdf"
   if self.useLogY : saveaspdfzoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom_log.pdf" # std::string saveaspdfzoom = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom_log.pdf" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom.pdf"
   saveaspngzoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom.png"
   if self.useLogY : saveaspngzoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom_log.png" # std::string saveaspngzoom = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom_log.png" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom.png"
   saveasepszoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom.eps"
   if self.useLogY : saveasepszoom = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_zoom_log.eps" # std::string saveasepszoom = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+thest 
   #//   c1.SaveAs(saveaspdfzoom/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.pdf"*/)
   #//   c1.SaveAs(saveaspngzoom/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.png"*/)
   #//   c1.SaveAs(saveasepszoom/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.eps"*/)


   #// full spectrum
   #//  if (self.nRebin==10 and  "hM4l_8" in histlabel):
   #//     print "Plotting the full spectrum" 
   #//     #// htotal.Add(hfourlepbestmass_4l_afterSel_new_signal350)
   #//     #// legend.AddEntry(hfourlepbestmass_4l_afterSel_new_signal350,"m_{H=350 GeV","L")
   #//     htotal.SetMinimum(0)
   #//     htotal.SetMaximum(24.5) #// 10 GeV bin
   #//     htotal.Draw()
   #//     htotal.GetXaxis().SetRange(7,81) #// 10 GeV bin
   #//     #//htotal.GetYaxis().SetRangeUser(0.,16.)
   #//     htotal.GetYaxis().SetTitle("Events / 10 GeV") #// 10 GeV bin    
   #//     sprintf(histotitle,"m_{%s [GeV]",self.whichchannel)
   #//     htotal.GetXaxis().SetTitle(histotitle)
   #//     htotal.GetXaxis().SetLabelSize(0.045)
   #//     htotal.GetXaxis().SetTitleSize(0.05)
   #//     htotal.GetXaxis().SetTitleOffset(1.15)
   #//     htotal.GetXaxis().SetTitleFont(42)
   #//     htotal.GetYaxis().SetLabelSize(0.045)
   #//     htotal.GetYaxis().SetTitleSize(0.05)
   #//     htotal.GetYaxis().SetTitleOffset(1.15)
   #//     htotal.GetYaxis().SetTitleFont(42)
   #//     gr.Draw("EPsame")

   #//     legend.Draw("same")
   #//     ll.Draw("same")


   #//     std::string saveaspdf = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_log.pdf" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+".pdf"
   #//     std::string saveaspng = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_log.png" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+".png"
   #//     std::string saveaseps = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_log.eps" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+".eps"
   #//     #// c1.SaveAs(saveaspdf/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.pdf"*/)
   #// #//     c1.SaveAs(saveaspng/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.png"*/)
   #// #//     c1.SaveAs(saveaseps/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.eps"*/)
   #//   
   # ============================>
   ROOT.gPad.RedrawAxis()

   if (self.useRatio==True):
     #//  c1.Update()
     canvasratio = 0.3
     c1.SetBottomMargin(canvasratio + (1-canvasratio)*c1.GetBottomMargin()-canvasratio*c1.GetTopMargin())
     #//print "Canvas= " , canvasratio + (1-canvasratio)*c1.GetBottomMargin()-canvasratio*c1.GetTopMargin() 

     #// Ratio: data / total bkg 
     canvasratio = 0.16
     ratioPad = ROOT.TPad("BottomPad","",0,0,1,1)
     ratioPad.SetTopMargin((1-canvasratio) - (1-canvasratio)*ratioPad.GetBottomMargin()+canvasratio*ratioPad.GetTopMargin())
     ratioPad.SetFillStyle(4000)
     ratioPad.SetFillColor(4000)
     ratioPad.SetFrameFillColor(4000)
     ratioPad.SetFrameFillStyle(4000)
     ratioPad.SetFrameBorderMode(0)
     ratioPad.SetTicks(1,1)
     #//ratioPad.SetLogx()
     ratioPad.Draw()
     ratioPad.cd()

     #//TH2F *hframe2= ROOT.TH2F("hframe2","hframe2",6000, 0., 2.2, 1000, 0.5, 2.);#// iso

     hframe2.GetYaxis().SetLabelSize(0.020)
     hframe2.GetXaxis().SetLabelSize(0.020)
     #//  hframe2.GetYaxis().SetTitleSize(0.047)
     hframe2.SetYTitle("Data/MC")
     #//  hframe2.GetYaxis().SetRangeUser(-10,10)
     hframe2.GetYaxis().SetNdivisions(503)
     #//hframe2.GetXaxis().SetTitleOffset(1.25)
     hframe2.Draw("")

     htotalHistoRatio.SetMarkerStyle(20)
     htotalHistoRatio.SetMarkerSize(0.95)
     htotalHistoRatio.SetMarkerColor(ROOT.kBlack)
     htotalHistoRatio.Draw("Psame")


     c1.Update()


   #whichchannel=self.whichchannel
   #if ( "4#mu" in self.whichchannel ): self.whichchannel="4mu"
   #if ( "2e2#mu" in self.whichchannel): self.whichchannel="2e2mu"

   saveaspdfratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.pdf"
   if self.useLogY : saveaspdfratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.pdf" #  std::string saveaspdfratio = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.pdf" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.pdf"
   saveaspngratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.png"
   if self.useLogY : saveaspngratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.png" # std::string saveaspngratio = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.png" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.png"
   saveasepsratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.eps"
   if self.useLogY : saveasepsratio =  "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.eps" # std::string saveasepsratio = useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.eps" : "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.eps"
   saveasrootratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.root"
   if self.useLogY : saveasrootratio = "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.root" # std::string saveasrootratio= useLogY ? "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio_log.root": "plots/h_"+histlabel+"_"+whichchannel+"_"+self.whichenergy+"_ratio.root"

   print saveasrootratio 
   c1.SaveAs(saveaspdfratio) #/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.pdf"*/)
   c1.SaveAs(saveaspngratio) #/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.png"*/)
   c1.SaveAs(saveasepsratio) #/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.eps"*/)
   c1.SaveAs(saveasrootratio) #/*"plots/hfourlepbestmass_4l_afterSel_new_m4l.root"*/)


   #// Write final histogram in a file 
   #char htotalfinal[300]
   print whichchannel 
   htotalfinal = ("plots/htotalfinal_%s_%s.root" % ( histlabel,whichchannel) )
   print "\n Writing final histograms in a file " , htotalfinal 
   file1 = ROOT.TFile(htotalfinal, "RECREATE")
   file1.cd()
   htotalHisto.Write()
   htotaldata.Write()
   hfourlepbestmass_4l_afterSel_new_qqZZ.Write()
   hfourlepbestmass_4l_afterSel_new_ggZZ.Write()
   nEvent_4l_w_DY.Write()
   nEvent_4l_w_TT.Write()
   nEvent_4l_w_ZZ.Write()
   nEvent_4l_w_qqZZ.Write()
   nEvent_4l_w_ggZZ.Write()
   nEvent_4l_w_WZ_WW_Wj.Write()
   nEvent_4l_w_TTV.Write()
   nEvent_4l_w_VVV.Write()
   nEvent_4l_w_QCD.Write()
   hfourlepbestmass_4l_afterSel_new_totSM_H.Write()
   hfourlepbestmass_4l_afterSel_new_totbkg_noSM_H.Write()
   nEvent_4l_w_totSM_H.Write()
   nEvent_4l_w_totalbkgMC.Write()
   nEvent_4l_w_totbkg_noSM_H.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP600.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP800.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1000.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1200.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1400.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP1700.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2000.Write()
   hfourlepbestmass_4l_afterSel_new_monoH_MZP2500.Write()
   nEvent_4l_w_ZpBaryonic_MZp500_MChi1.Write()
   nEvent_4l_w_data.Write()
   file1.Write()
   file1.Close()

   #// Write cutflow tables 
   print "\n Writing cut flow tables in tex format \n" 

   #// DY
   #//print "Cont.= " , nEvent_4l_w_DY.GetBinContent(5) , " Err= " , nEvent_4l_w_DY.GetBinError(5) 
   #//print "Cont.= " , nEvent_4l_DY.GetBinContent(5) , " Err= " , nEvent_4l_DY.GetBinError(5) , " " , nEvent_4l_DY.GetBinError(5)*nEvent_4l_w_DY.GetBinContent(5)/nEvent_4l_DY.GetBinContent(5) 

   #// QCD
   #//print "Cont.= " , nEvent_4l_w_QCD.GetBinContent(5) , " Err= " , nEvent_4l_w_QCD.GetBinError(5) 
   #//print "Cont.= " , nEvent_4l_QCD.GetBinContent(5) , " Err= " , nEvent_4l_QCD.GetBinError(5) , " " , nEvent_4l_QCD.GetBinError(5)*nEvent_4l_w_QCD.GetBinContent(5)/nEvent_4l_QCD.GetBinContent(5) 

   print "Cont.= " , nEvent_4l_w_totSM_H.GetBinContent(5) , " Err= " , nEvent_4l_w_totSM_H.GetBinError(5) 
   print "Cont.= " , nEvent_4l_totSM_H.GetBinContent(5) , " Err= " , nEvent_4l_totSM_H.GetBinError(5) , " " , nEvent_4l_totSM_H.GetBinError(5)*nEvent_4l_w_totSM_H.GetBinContent(5)/nEvent_4l_totSM_H.GetBinContent(5) 


   #Char_t outformat[20000]

   print "\\begin{table*}[htbH] \n", "\\begin{center} \n", "\\resizebox{\\textwidth}{!}{% \n" , "\\begin{tabular}{ l | c | c | c | c | c | c | c | c | c | c | c |} \n" ,     "\\hline    \\hline"


   print "Channel: $" , whichchannel ,"$ & $Z\\gamma^{*},ZZ$ & $Z+js$ & $WZ,WW,W+js$ & $t \\bar{t}$ & $t \\bar{t}V$ & $VVV$ & $QCD$ & $SM \\, H$ & $Tot. \\, Bkg$  & Z' baryonic & Obs. \\\\" 
   print "\\hline" 

   outformat = ("HLT & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(5), nEvent_4l_w_ZZ.GetBinError(5),
        nEvent_4l_w_DY.GetBinContent(5), nEvent_4l_w_DY.GetBinError(5),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(5),  nEvent_4l_w_WZ_WW_Wj.GetBinError(5), 
        nEvent_4l_w_TT.GetBinContent(5), nEvent_4l_w_TT.GetBinError(5), 
        nEvent_4l_w_TTV.GetBinContent(5), nEvent_4l_w_TTV.GetBinError(5), 
        nEvent_4l_w_VVV.GetBinContent(5), nEvent_4l_w_VVV.GetBinError(5),
        nEvent_4l_w_QCD.GetBinContent(5), nEvent_4l_w_QCD.GetBinError(5),
        nEvent_4l_w_totSM_H.GetBinContent(5), nEvent_4l_w_totSM_H.GetBinError(5),
        nEvent_4l_w_totalbkgMC.GetBinContent(5), nEvent_4l_w_totalbkgMC.GetBinError(5),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(5), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(5),
        nEvent_4l_w_data.GetBinContent(5)))
   print outformat 

   outformat = ("$l^{+} l^{-}$, $12<m_{l^{+}l^{-}}<120$ & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e $ \\pm $ %.2e & %.2e  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(8), nEvent_4l_w_ZZ.GetBinError(8),
        nEvent_4l_w_DY.GetBinContent(8), nEvent_4l_w_DY.GetBinError(8),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(8),  nEvent_4l_w_WZ_WW_Wj.GetBinError(8), 
        nEvent_4l_w_TT.GetBinContent(8), nEvent_4l_w_TT.GetBinError(8), 
        nEvent_4l_w_TTV.GetBinContent(8), nEvent_4l_w_TTV.GetBinError(8), 
        nEvent_4l_w_VVV.GetBinContent(8), nEvent_4l_w_VVV.GetBinError(8),
        nEvent_4l_w_QCD.GetBinContent(8), nEvent_4l_w_QCD.GetBinError(8),
        nEvent_4l_w_totSM_H.GetBinContent(8), nEvent_4l_w_totSM_H.GetBinError(8),
        nEvent_4l_w_totalbkgMC.GetBinContent(8), nEvent_4l_w_totalbkgMC.GetBinError(8),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(8), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(8),
        nEvent_4l_w_data.GetBinContent(8)))
   print outformat 


   #//%.2e & %.2e & %.2e & %.2e & %.2e & %.2e & %.2e & %.2e & %.2e & %.2e  \\\\",nEvent_4l_w_ZZ.GetBinContent(8),nEvent_4l_w_DY.GetBinContent(8),nEvent_4l_w_WZ_WW_Wj.GetBinContent(8),nEvent_4l_w_TT.GetBinContent(8),nEvent_4l_w_TTV.GetBinContent(8),nEvent_4l_w_VVV.GetBinContent(8),nEvent_4l_w_totSM_H.GetBinContent(8),nEvent_4l_w_totalbkgMC.GetBinContent(8),nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(8),nEvent_4l_w_data.GetBinContent(8))
   #//  print outformat 

   outformat = ("$Z_{1},Z_{2}$  & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %d  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(9), nEvent_4l_w_ZZ.GetBinError(9),
        nEvent_4l_w_DY.GetBinContent(9), nEvent_4l_w_DY.GetBinError(9),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(9),  nEvent_4l_w_WZ_WW_Wj.GetBinError(9), 
        nEvent_4l_w_TT.GetBinContent(9), nEvent_4l_w_TT.GetBinError(9), 
        nEvent_4l_w_TTV.GetBinContent(9), nEvent_4l_w_TTV.GetBinError(9), 
        nEvent_4l_w_VVV.GetBinContent(9), nEvent_4l_w_VVV.GetBinError(9),
        nEvent_4l_w_QCD.GetBinContent(9), nEvent_4l_w_QCD.GetBinError(9),
        nEvent_4l_w_totSM_H.GetBinContent(9), nEvent_4l_w_totSM_H.GetBinError(9),
        nEvent_4l_w_totalbkgMC.GetBinContent(9), nEvent_4l_w_totalbkgMC.GetBinError(9),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(9), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(9),
        int(nEvent_4l_w_data.GetBinContent(9))))
   print outformat 

   #//& %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f  \\\\",nEvent_4l_w_ZZ.GetBinContent(9),nEvent_4l_w_DY.GetBinContent(9),nEvent_4l_w_WZ_WW_Wj.GetBinContent(9),nEvent_4l_w_TT.GetBinContent(9),nEvent_4l_w_TTV.GetBinContent(9),nEvent_4l_w_VVV.GetBinContent(9),nEvent_4l_w_totSM_H.GetBinContent(9),nEvent_4l_w_totalbkgMC.GetBinContent(9),nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(9),nEvent_4l_w_data.GetBinContent(9))
   #// print outformat 

   outformat = ("$p_{T}>20/10$, $m_{l^{+}l^{-}}>4$, $m_{Z_{1}}>40$  & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %d  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(12), nEvent_4l_w_ZZ.GetBinError(12),
        nEvent_4l_w_DY.GetBinContent(12), nEvent_4l_w_DY.GetBinError(12),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(12),  nEvent_4l_w_WZ_WW_Wj.GetBinError(12), 
        nEvent_4l_w_TT.GetBinContent(12), nEvent_4l_w_TT.GetBinError(12), 
        nEvent_4l_w_TTV.GetBinContent(12), nEvent_4l_w_TTV.GetBinError(12), 
        nEvent_4l_w_VVV.GetBinContent(12), nEvent_4l_w_VVV.GetBinError(12),
        nEvent_4l_w_QCD.GetBinContent(12), nEvent_4l_w_QCD.GetBinError(12),
        nEvent_4l_w_totSM_H.GetBinContent(12), nEvent_4l_w_totSM_H.GetBinError(12),
        nEvent_4l_w_totalbkgMC.GetBinContent(12), nEvent_4l_w_totalbkgMC.GetBinError(12),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(12), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(12),
        int(nEvent_4l_w_data.GetBinContent(12))))
   print outformat 

   #//& %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f  \\\\",nEvent_4l_w_ZZ.GetBinContent(12),nEvent_4l_w_DY.GetBinContent(12),nEvent_4l_w_WZ_WW_Wj.GetBinContent(12),nEvent_4l_w_TT.GetBinContent(12),nEvent_4l_w_TTV.GetBinContent(12),nEvent_4l_w_VVV.GetBinContent(12),nEvent_4l_w_totSM_H.GetBinContent(12),nEvent_4l_w_totalbkgMC.GetBinContent(12),nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(12),nEvent_4l_w_data.GetBinContent(12))
   #//print outformat 

   outformat = ("$m_{4l}>70$  & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %d  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(15), nEvent_4l_w_ZZ.GetBinError(15),
        nEvent_4l_w_DY.GetBinContent(15), nEvent_4l_w_DY.GetBinError(15),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(15),  nEvent_4l_w_WZ_WW_Wj.GetBinError(15), 
        nEvent_4l_w_TT.GetBinContent(15), nEvent_4l_w_TT.GetBinError(15), 
        nEvent_4l_w_TTV.GetBinContent(15), nEvent_4l_w_TTV.GetBinError(15), 
        nEvent_4l_w_VVV.GetBinContent(15), nEvent_4l_w_VVV.GetBinError(15),
        nEvent_4l_w_QCD.GetBinContent(15), nEvent_4l_w_QCD.GetBinError(15),
        nEvent_4l_w_totSM_H.GetBinContent(15), nEvent_4l_w_totSM_H.GetBinError(15),
        nEvent_4l_w_totalbkgMC.GetBinContent(15), nEvent_4l_w_totalbkgMC.GetBinError(15),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(15), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(15),
        int(nEvent_4l_w_data.GetBinContent(15))))
   print outformat 
   #//& %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f  \\\\",nEvent_4l_w_ZZ.GetBinContent(15),nEvent_4l_w_DY.GetBinContent(15),nEvent_4l_w_WZ_WW_Wj.GetBinContent(15),nEvent_4l_w_TT.GetBinContent(15),nEvent_4l_w_TTV.GetBinContent(15),nEvent_4l_w_VVV.GetBinContent(15),nEvent_4l_w_totSM_H.GetBinContent(15),nEvent_4l_w_totalbkgMC.GetBinContent(15),nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(15),nEvent_4l_w_data.GetBinContent(15))
   #//print outformat 

   outformat = ("$|m_{4l}-125| \\leq 10$, $N_{l}=4$, $n_{b} \\leq 1$ & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %.2f $ \\pm $ %.2f & %d  \\\\" % (
        nEvent_4l_w_ZZ.GetBinContent(22), nEvent_4l_w_ZZ.GetBinError(22),
        nEvent_4l_w_DY.GetBinContent(22), nEvent_4l_w_DY.GetBinError(22),
        nEvent_4l_w_WZ_WW_Wj.GetBinContent(22),  nEvent_4l_w_WZ_WW_Wj.GetBinError(22), 
        nEvent_4l_w_TT.GetBinContent(22), nEvent_4l_w_TT.GetBinError(22), 
        nEvent_4l_w_TTV.GetBinContent(22), nEvent_4l_w_TTV.GetBinError(22), 
        nEvent_4l_w_VVV.GetBinContent(22), nEvent_4l_w_VVV.GetBinError(22),
        nEvent_4l_w_QCD.GetBinContent(22), nEvent_4l_w_QCD.GetBinError(22),
        nEvent_4l_w_totSM_H.GetBinContent(22), nEvent_4l_w_totSM_H.GetBinError(22),
        nEvent_4l_w_totalbkgMC.GetBinContent(22), nEvent_4l_w_totalbkgMC.GetBinError(22),
        nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(22), nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinError(22),
        int(nEvent_4l_w_data.GetBinContent(22))))
   print outformat 
   #//& %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f  \\\\",nEvent_4l_w_ZZ.GetBinContent(22),nEvent_4l_w_DY.GetBinContent(22),nEvent_4l_w_WZ_WW_Wj.GetBinContent(22),nEvent_4l_w_TT.GetBinContent(22),nEvent_4l_w_TTV.GetBinContent(22),nEvent_4l_w_VVV.GetBinContent(22),nEvent_4l_w_totSM_H.GetBinContent(22),nEvent_4l_w_totalbkgMC.GetBinContent(22),nEvent_4l_w_ZpBaryonic_MZp500_MChi1.GetBinContent(22),nEvent_4l_w_data.GetBinContent(22))
   #//print outformat 

   print "\\hline \\hline \n" , "\\end{tabular} \n"  ,   "" 



   print "\\caption{Cut flow table the number of events passing the full selection for the $" , whichchannel , "$ final state, as obtained from simulation for background and signal and from real data with a luminosity of $35.9 \\fbinv$. The signal sample correspond to the Z' baryonic model with $m_{Z'}=500$ GeV and $m_{\\chi}=1$ GeV; only statistical errors are quoted.}" 

   print "\\label{tab:yields" , whichchannel, "} \n" ,   "\\end{center} \n" ,    "\\end{table*}" 

   #if ( "hM4l_9" in histlabel ) : self.outputyields.close()
        


   # In[21]:


   # ThE END

