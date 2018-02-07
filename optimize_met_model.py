
# coding: utf-8

# In[1]:


import os
import sys
import ROOT
#from PlotStack4l import PlotStack4l
import numpy as np
import math
import argparse
import matplotlib.pyplot as plt

#get_ipython().magic(u'jsroot on')
# voms-proxy-init generated user proxy file to access the xrootd servers
#os.environ['X509_USER_PROXY'] = '/home/bockjoo/.cmsuser.proxy'
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


# Convert root ntuple format to arrays
def get_data(t):
  weight = []
  pfmet  = []
  mass4l = []
  mT     = []
  dphi   = []
  Dkin   = []
  D      = []
  Ngood  = []
  for evt in t:
    weight.append(evt.f_weight)
    pfmet .append(evt.f_pfmet)
    mass4l.append(evt.f_mass4l)
    mT    .append(evt.f_mT)
    dphi  .append(evt.f_dphi)
    Dkin  .append(evt.f_D_bkg_kin)
    #D     .append(Dmass4l(evt.f_mass4l, evt.f_D_bkg_kin, 0, 199))
    Ngood .append(evt.f_Ngood)
  return (weight, pfmet, mass4l, mT, dphi, Dkin, D, Ngood)


# In[5]:


# Calculate the Punzi significance for a signal model, fill hists
def get_punzi(signal, flist, cut_pfmet):
  
  # Initialize arrays
  counter_B = np.zeros((len(cut_pfmet)))
  counter_S = np.zeros((len(cut_pfmet)))
  eff_S     = np.zeros((len(cut_pfmet)))
  punzi     = np.zeros((len(cut_pfmet)))

  # load bnn
  #record = open('Dmass4l.cpp').read()
  #gROOT.ProcessLine(record)

  # loop through files in filelist, incrementing counters and filling arrays
  for ff in flist:
    
    print ff
    # Get Data
    #f = TFile(f)
    f = ROOT.TFile.Open(ff)
    t = f.Get("HZZ4LeptonsAnalysisReduced")
    weight, pfmet, mass4l, m4lt, dphi, Dkin, D, Ngood = get_data(t)
    
    # Loop through arrays
    for n in range(0, len(weight)):

      # Signal region selection
      if Ngood[n] != 4: continue
      #if pfmet[n] < 140: continue
      if np.abs(mass4l[n] - 125) > 10: continue
      #if m4lt[n] < 280: continue
      #if dphi[n] < 2.8: continue
      #if D[n] > 0.2: continue
    
      # Increment counters
      for i in range(0, len(cut_pfmet)):     
         #if np.abs(mass4l[n] - 125) < cut_pfmet[i] and 'Run2016' not in f.GetName() and 'MZp' not in f.GetName(): 
         #    counter_B[i] += weight[n]
         #if np.abs(mass4l[n] - 125) < cut_pfmet[i] and signal in f.GetName():
         #    counter_S[i] += weight[n]
         if pfmet[n] > cut_pfmet[i] and 'Run2016' not in f.GetName() and 'MZp' not in f.GetName(): 
             counter_B[i] += weight[n]
         if pfmet[n] > cut_pfmet[i] and signal in f.GetName():
             counter_S[i] += weight[n]
  print counter_B
  print counter_S  
  # Calculate efficiency and Punzi signficance from counter arrays
  for i in range(0, len(cut_pfmet)):
    eff_S[i] = counter_S[i]/counter_S[0]
    punzi[i] = (counter_S[i]/counter_S[0]) / (5/2 + np.sqrt(counter_B[i]))
 
  print eff_S
  print punzi
 
  return (punzi, eff_S)


# In[14]:


if __name__ == "__main__":
  #print "It is main"
  # Parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--channel', required=True, help='Decay channel: 4mu, 4e, or 2e2mu')
  parser.add_argument('--site', required=False, help='Site: Choose from one of Bari, Florida or FNAL')
  parser.add_argument('--monoh_model', required=False, help='Mono Higgs Model: Choose from one of Zp2HDM or ZpBaryonic')
  args = parser.parse_args()
  #args_channel = "2e2mu"
  #args_channel = "4e"
  args_channel = args.channel
  print "Channel : ",args_channel
  
  args_site = "Bari"
  args_monoh_model = "Zp2HDM"
  if args.site is not None: args_site = args.site 
  if args.monoh_model is not None : args_monoh_model = args.monoh_model
  # Read in file list
  inputfilename='filelist_' + args_channel + '_2016_Spring16_AN_' + args_site + '_noZX.txt'
  print "Site : ",args_site 
  print "Mono Higgs Model : ", args_monoh_model
  print "Filelist : ",inputfilename
  

  #flist = map(lambda x: x.split()[-1], open('filelist_' + args.channel + '_2016_Spring16_AN_Bari_noZX.txt').readlines())
  flist = map(lambda x: x.split()[-1], open('filelist_' + args_channel + '_2016_Spring16_AN_Florida_noZX.txt').readlines())
  #flist = map(lambda x: x.split()[-1], open( inputfilename )
  #for f in flist: print f
  #sys.exit(0)

  # Define range and step size for met cut
  cut_pfmet = np.arange(1, 500, 25)
  #cut_pfmet = np.arange(1, 8, 0.25)
  print "PFMET Cut Range : ",cut_pfmet
  #for ff in flist:
  #  f = ROOT.TFile.Open(ff)
  #  t = f.Get("HZZ4LeptonsAnalysisReduced")
  #  t.Print()
  #  break
  # for i in $(grep ZpBaryonic filelist_2e2mu_2016_Spring16_AN_Florida_noZX.txt | grep MChi-1_ | sed 's|_MChi-1| _MChi-1|g' | sed 's|_MZp-| |g' | awk '{print $2}' | sort -n) ; do  echo ZpBaryonic_MZp-${i}_MChi-1 ; done
  #ZpBaryonic_MZp-10_MChi-1
  #ZpBaryonic_MZp-20_MChi-1
  #ZpBaryonic_MZp-50_MChi-1
  #ZpBaryonic_MZp-100_MChi-1
  #ZpBaryonic_MZp-200_MChi-1
  #ZpBaryonic_MZp-300_MChi-1
  #ZpBaryonic_MZp-500_MChi-1
  #ZpBaryonic_MZp-1000_MChi-1
  #ZpBaryonic_MZp-2000_MChi-1
  #ZpBaryonic_MZp-10000_MChi-1
  #
  # for i in $(grep ZpBaryonic filelist_2e2mu_2016_Spring16_AN_Florida_noZX.txt | grep MChi-1_ | sed 's|_MChi-1| _MChi-1|g' | sed 's|_MZp-| |g' | awk '{print $2}' | sort -n) ; do  echo " "" "print $i ; echo " "" "punzi${i},  eff_S${i}  = "get_punzi('ZpBaryonic_MZp-${i}_MChi-1', flist, cut_pfmet)" ; done
  # Return signal efficiency and punzi significance for different signals
  if 'Zp2HDM' in args_monoh_model :
      print 600
      punzi600,  eff_S600  = get_punzi('2HDM_MZp-600_MA0-300', flist, cut_pfmet)
      print 800
      punzi800,  eff_S800  = get_punzi('2HDM_MZp-800_MA0-300', flist, cut_pfmet)
      print 1000
      punzi1000, eff_S1000 = get_punzi('2HDM_MZp-1000_MA0-300', flist, cut_pfmet)
      print 1200
      punzi1200, eff_S1200 = get_punzi('2HDM_MZp-1200_MA0-300', flist, cut_pfmet)
      print 1400
      punzi1400, eff_S1400 = get_punzi('2HDM_MZp-1400_MA0-300', flist, cut_pfmet)
      print 1700
      punzi1700, eff_S1700 = get_punzi('2HDM_MZp-1700_MA0-300', flist, cut_pfmet)
      print 2000
      punzi2000, eff_S2000 = get_punzi('2HDM_MZp-2000_MA0-300', flist, cut_pfmet)
      print 2500
      punzi2500, eff_S2500 = get_punzi('2HDM_MZp-2500_MA0-300', flist, cut_pfmet)

      # Print optimal significance and MET cuts
      print 'MZP [GeV]      | 600  | 800  | 1000 | 1200 | 1400 | 1700 | 2000 | 2500'
      print 'Max punzi      | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f' % (max(punzi600), max(punzi800), max(punzi1000), max(punzi1200), max(punzi1400), max(punzi1700), max(punzi2000), max(punzi2500))
      print 'MET cut [GeV]  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f' % (cut_pfmet[np.argmax(punzi600)], cut_pfmet[np.argmax(punzi800)], cut_pfmet[np.argmax(punzi1000)], cut_pfmet[np.argmax(punzi1200)], cut_pfmet[np.argmax(punzi1400)], cut_pfmet[np.argmax(punzi1700)], cut_pfmet[np.argmax(punzi2000)], cut_pfmet[np.argmax(punzi2500)])
  elif 'ZpBaryonic' in args_monoh_model :
      print 10
      punzi10,  eff_S10  = get_punzi('ZpBaryonic_MZp-10_MChi-1', flist, cut_pfmet)
      print 20
      punzi20,  eff_S20  = get_punzi('ZpBaryonic_MZp-20_MChi-1', flist, cut_pfmet)
      print 50
      punzi50, eff_S50 = get_punzi('ZpBaryonic_MZp-50_MChi-1', flist, cut_pfmet)
      print 100
      punzi100, eff_S100 = get_punzi('ZpBaryonic_MZp-100_MChi-1', flist, cut_pfmet)
      print 200
      punzi200, eff_S200 = get_punzi('ZpBaryonic_MZp-200_MChi-1', flist, cut_pfmet)
      print 300
      punzi300, eff_S300 = get_punzi('ZpBaryonic_MZp-300_MChi-1', flist, cut_pfmet)
      print 500
      punzi500, eff_S500 = get_punzi('ZpBaryonic_MZp-500_MChi-1', flist, cut_pfmet)
      print 1000
      punzi1000, eff_S1000 = get_punzi('ZpBaryonic_MZp-1000_MChi-1', flist, cut_pfmet)
      print 2000
      punzi2000, eff_S2000 = get_punzi('ZpBaryonic_MZp-2000_MChi-1', flist, cut_pfmet)
      print 10000
      punzi10000, eff_S10000 = get_punzi('ZpBaryonic_MZp-10000_MChi-1', flist, cut_pfmet)


      # In[24]:
      #line1="  print 'MZP [GeV]      "
      #line2="  print 'Max punzi      "
      #line3="  print 'MET cut [GeV]  "
      #for i in $(grep ZpBaryonic filelist_2e2mu_2016_Spring16_AN_Florida_noZX.txt | grep MChi-1_ | sed 's|_MChi-1| _MChi-1|g' | sed 's|_MZp-| |g' | awk '{print $2}' | sort -n) ; do
      # line1="${line1}| $i " ; line2="${line2}| %.2f" ; line3="${line3}| %3.2f"
      #done
      #line1="${line1}'"
      #line2="${line2}' % ("
      #line3="${line3}' % ("
      #for i in $(grep ZpBaryonic filelist_2e2mu_2016_Spring16_AN_Florida_noZX.txt | grep MChi-1_ | sed 's|_MChi-1| _MChi-1|g' | sed 's|_MZp-| |g' | awk '{print $2}' | sort -n) ; do
      #  line2="${line2}max(punzi${i})," ; line3="${line3}cut_pfmet[np.argmax(punzi${i})],"
      #done
      #line2=" "" "$(echo $line2 | sed 's#),$#))#') 
      #line3=" "" "$(echo $line3 | sed 's#\],$#\]),#') 
      # Print optimal significance and MET cuts
      print 'MZP [GeV] | 10 | 20 | 50 | 100 | 200 | 300 | 500 | 1000 | 2000 | 10000 '
      #print 'MZP [GeV]      | 600  | 800  | 1000 | 1200 | 1400 | 1700 | 2000 | 2500'
      #print 'Max punzi      | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f' % (max(punzi600), max(punzi800), max(punzi1000), max(punzi1200), max(punzi1400), max(punzi1700), max(punzi2000), max(punzi2500))
      print 'Max punzi | %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f' % (max(punzi10),max(punzi20),max(punzi50),max(punzi100),max(punzi200),max(punzi300),max(punzi500),max(punzi1000),max(punzi2000),max(punzi10000))
      #print 'MET cut [GeV]  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f  | %3.2f' % (cut_pfmet[np.argmax(punzi600)], cut_pfmet[np.argmax(punzi800)], cut_pfmet[np.argmax(punzi1000)], cut_pfmet[np.argmax(punzi1200)], cut_pfmet[np.argmax(punzi1400)], cut_pfmet[np.argmax(punzi1700)], cut_pfmet[np.argmax(punzi2000)], cut_pfmet[np.argmax(punzi2500)])
      print 'MET cut [GeV] | %3.2f| %3.2f| %3.2f| %3.2f| %3.2f| %3.2f| %3.2f| %3.2f| %3.2f| %3.2f' % (cut_pfmet[np.argmax(punzi10)],cut_pfmet[np.argmax(punzi20)],cut_pfmet[np.argmax(punzi50)],cut_pfmet[np.argmax(punzi100)],cut_pfmet[np.argmax(punzi200)],cut_pfmet[np.argmax(punzi300)],cut_pfmet[np.argmax(punzi500)],cut_pfmet[np.argmax(punzi1000)],cut_pfmet[np.argmax(punzi2000)],cut_pfmet[np.argmax(punzi10000)])

  # In[26]:
  # Format plots
  plt.figure(1)
  #for i in $(grep ZpBaryonic filelist_2e2mu_2016_Spring16_AN_Florida_noZX.txt | grep MChi-1_ | sed 's|_MChi-1| _MChi-1|g' | sed 's|_MZp-| |g' | awk '{print $2}' | sort -n) ; do   echo " "" ""plt.plot(cut_pfmet, punzi${i},  linewidth=2.0, label=r'$m_{Z\prime} = ${i} \rm{\ GeV}$')" ; done  
  if 'Zp2HDM' in args_monoh_model :
      plt.plot(cut_pfmet, punzi600,  linewidth=2.0, label=r'$m_{Z\prime} = 600 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi800,  linewidth=2.0, label=r'$m_{Z\prime} = 800 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi1000, linewidth=2.0, label=r'$m_{Z\prime} = 1000 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi1200, linewidth=2.0, label=r'$m_{Z\prime} = 1200 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi1400, linewidth=2.0, label=r'$m_{Z\prime} = 1400 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi1700, linewidth=2.0, label=r'$m_{Z\prime} = 1700 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi2000, linewidth=2.0, label=r'$m_{Z\prime} = 2000 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi2500, linewidth=2.0, label=r'$m_{Z\prime} = 2500 \rm{\ GeV}$')
  elif 'ZpBaryonic' in args_monoh_model :
      plt.plot(cut_pfmet, punzi10,  linewidth=2.0, label=r'{Z\prime} = 10 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi20,  linewidth=2.0, label=r'{Z\prime} = 20 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi50,  linewidth=2.0, label=r'{Z\prime} = 50 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi100,  linewidth=2.0, label=r'{Z\prime} = 100 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi200,  linewidth=2.0, label=r'{Z\prime} = 200 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi300,  linewidth=2.0, label=r'{Z\prime} = 300 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi500,  linewidth=2.0, label=r'{Z\prime} = 500 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi1000,  linewidth=2.0, label=r'{Z\prime} = 1000 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi2000,  linewidth=2.0, label=r'{Z\prime} = 2000 \rm{\ GeV}$')
      plt.plot(cut_pfmet, punzi10000,  linewidth=2.0, label=r'{Z\prime} = 10000 \rm{\ GeV}$')

  #plt.axis([0, 500, 0, 0.5])
  plt.ylabel(args_channel + ' Punzi\'s Significance (N=5)', fontsize=16)
  plt.xlabel('PFMET cut [GeV]', horizontalalignment='right', x=1.0, fontsize=16)
  #plt.xlabel(r'$M_{llll} \rm{\ cut\ [GeV]}$', horizontalalignment='right', x=1.0, fontsize=16)
  plt.grid(True)
  plt.legend(loc='best', frameon=False, prop={'size':12})
  figout = args_channel + '_punzi_met_'+args_monoh_model+'.png'
  plt.savefig( figout )
  print "Figure ", figout, " is saved"  
  #plt.savefig(args.channel + '_punzi_m4l.png')
 
  #plt.figure(2)
  #plt.plot(cut_pfmet, eff_S600,  linewidth=2.0, label=r'$m_{Z\prime} = 600 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S800,  linewidth=2.0, label=r'$m_{Z\prime} = 800 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S1000, linewidth=2.0, label=r'$m_{Z\prime} = 1000 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S1200, linewidth=2.0, label=r'$m_{Z\prime} = 1200 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S1400, linewidth=2.0, label=r'$m_{Z\prime} = 1400 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S1700, linewidth=2.0, label=r'$m_{Z\prime} = 1700 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S2000, linewidth=2.0, label=r'$m_{Z\prime} = 2000 \rm{GeV}$')
  #plt.plot(cut_pfmet, eff_S2500, linewidth=2.0, label=r'$m_{Z\prime} = 2500 \rm{GeV}$')
  #plt.axis([0, 500, 0, 1.1])
  #plt.ylabel(args.channel + ' Signal Efficiency', horizontalalignment='right', y=1.0, fontsize=18)
  #plt.xlabel('MET cut [GeV]', horizontalalignment='right', x=1.0, fontsize=18)
  #plt.grid(True)
  #plt.legend(loc='best', frameon=False, prop={'size':14})
  #plt.savefig(args.channel + '_eff_met.png')

  plt.show()
  # The End