
# coding: utf-8

# In[1]:


import os
import sys
import ROOT
from PlotStack4l import PlotStack4l
from math import sqrt 

#et_ipython().magic(u'jsroot on')
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


f4mu = ROOT.TFile.Open("plots/htotalfinal_hM4l_7_4mu.root")
f4e = ROOT.TFile.Open("plots/htotalfinal_hM4l_7_4e.root")
f2e2mu = ROOT.TFile.Open("plots/htotalfinal_hM4l_7_2e2mu.root")


# In[3]:


f4mu_qqZZ = f4mu.Get("nEvent_4l_w_qqZZ")
f4e_qqZZ = f4e.Get("nEvent_4l_w_qqZZ")
f2e2mu_qqZZ = f2e2mu.Get("nEvent_4l_w_qqZZ")

f4mu_ggZZ = f4mu.Get("nEvent_4l_w_ggZZ")
f4e_ggZZ = f4e.Get("nEvent_4l_w_ggZZ")
f2e2mu_ggZZ = f2e2mu.Get("nEvent_4l_w_ggZZ")

f4mu_ZZ = f4mu.Get("nEvent_4l_w_ZZ")
f4e_ZZ = f4e.Get("nEvent_4l_w_ZZ")
f2e2mu_ZZ = f2e2mu.Get("nEvent_4l_w_ZZ")

f4mu_totSM_H   = f4mu.Get("nEvent_4l_w_totSM_H")
f4e_totSM_H    = f4e.Get("nEvent_4l_w_totSM_H")
f2e2mu_totSM_H = f2e2mu.Get("nEvent_4l_w_totSM_H")

#// bkg no Higgs
#// f4mu_totalbkg_noSM_H   = f4mu.Get("nEvent_4l_w_totbkg_noSM_H")
#// f4e_totalbkg_noSM_H    = f4e.Get("nEvent_4l_w_totbkg_noSM_H")
#// f2e2mu_totalbkg_noSM_H = f2e2mu.Get("nEvent_4l_w_totbkg_noSM_H")



#// Total bkg
f4mu_totalbkg   = f4mu.Get("nEvent_4l_w_totalbkgMC")
f4e_totalbkg    = f4e.Get("nEvent_4l_w_totalbkgMC")
f2e2mu_totalbkg = f2e2mu.Get("nEvent_4l_w_totalbkgMC")

#// Data
f4mu_totaldata   = f4mu.Get("nEvent_4l_w_data")
f4e_totaldata    = f4e.Get("nEvent_4l_w_data")
f2e2mu_totaldata = f2e2mu.Get("nEvent_4l_w_data")


# In[7]:


latexOUTFile = "plots/SMHiggsTableWithErrors.tex" # cutflow_%s_%s.tex" % (whichchannel, self.whichenergy))
latexOUTFD = open(latexOUTFile, "w")
latexOUTFD.write("\documentclass[a4paper,12pt]{article}\n")
latexOUTFD.write("\usepackage{geometry}\n")
latexOUTFD.write("\usepackage{pdflscape}\n")
latexOUTFD.write("\input epsf\n")
latexOUTFD.write("\pagestyle{plain}\n")
latexOUTFD.write("\\begin{document}\n")
latexOUTFD.write("\\bibliographystyle{plain}\n")
latexOUTFD.write("\\begin{landscape}\n")
latexOUTFD.write("\\begin{table}[htbH]\n") 
latexOUTFD.write("\\begin{center}\n") 
latexOUTFD.write("\\resizebox{\\textwidth}{!}{% \n") 
latexOUTFD.write("\\begin{tabular}{l|c|c|c|c}\n" )
latexOUTFD.write("\\hline \\hline\n" )
latexOUTFD.write("{\\textbf{Channel}} & {\\textbf{$4e$}} & {\\textbf{$4\\mu$}} & {\\textbf{$2e2\\mu$}} & {\\textbf{$4l$}} \\\\ \n") 
latexOUTFD.write("\\hline\n")

outformat = ( "$q \\bar{q}\\rightarrow ZZ$ & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\ \n" % ( f4e_qqZZ.GetBinContent(15), f4e_qqZZ.GetBinError(15), f4mu_qqZZ.GetBinContent(15), f4mu_qqZZ.GetBinError(15), f2e2mu_qqZZ.GetBinContent(15), f2e2mu_qqZZ.GetBinError(15), f4e_qqZZ.GetBinContent(15)+f4mu_qqZZ.GetBinContent(15)+f2e2mu_qqZZ.GetBinContent(15), sqrt(f4e_qqZZ.GetBinError(15)*f4e_qqZZ.GetBinError(15) + f4mu_qqZZ.GetBinError(15)*f4mu_qqZZ.GetBinError(15) + f2e2mu_qqZZ.GetBinError(15)*f2e2mu_qqZZ.GetBinError(15) )  ) )
latexOUTFD.write( outformat )
 
outformat = ( "$gg\\rightarrow ZZ$ & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\ \n" % ( f4e_ggZZ.GetBinContent(15), f4e_ggZZ.GetBinError(15), f4mu_ggZZ.GetBinContent(15), f4mu_ggZZ.GetBinError(15), f2e2mu_ggZZ.GetBinContent(15), f2e2mu_ggZZ.GetBinError(15), f4e_ggZZ.GetBinContent(15)+f4mu_ggZZ.GetBinContent(15)+f2e2mu_ggZZ.GetBinContent(15), sqrt(f4e_ggZZ.GetBinError(15)*f4e_ggZZ.GetBinError(15) + f4mu_ggZZ.GetBinError(15)*f4mu_ggZZ.GetBinError(15) + f2e2mu_ggZZ.GetBinError(15)*f2e2mu_ggZZ.GetBinError(15) )  ) )
latexOUTFD.write( outformat )

ZX_4e=27.2;    ZX_4e_err=ZX_4e*0.43
ZX_4mu=31.0;   ZX_4mu_err=ZX_4mu*0.36
ZX_2e2mu=62.0; ZX_2e2mu_err=ZX_2e2mu*0.40
sumbkg_4e    = f4e_ZZ.GetBinContent(15)+ZX_4e;  sumbkg_4e_err=sqrt(f4e_ZZ.GetBinError(15)*f4e_ZZ.GetBinError(15)+ZX_4e_err*ZX_4e_err)
sumbkg_4mu   = f4mu_ZZ.GetBinContent(15)+ZX_4mu; sumbkg_4mu_err=sqrt(f4mu_ZZ.GetBinError(15)*f4mu_ZZ.GetBinError(15)+ZX_4mu_err*ZX_4mu_err)
sumbkg_2e2mu = f2e2mu_ZZ.GetBinContent(15)+ZX_2e2mu; sumbkg_2e2mu_err=sqrt(f2e2mu_ZZ.GetBinError(15)*f2e2mu_ZZ.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err)
sumbkg_4l    = sumbkg_4e+sumbkg_4mu+sumbkg_2e2mu
sumbkg_4l_err=sqrt((f4e_ZZ.GetBinError(15)*f4e_ZZ.GetBinError(15)+ZX_4e_err*ZX_4e_err)+(f4mu_ZZ.GetBinError(15)*f4mu_ZZ.GetBinError(15)+ZX_4mu_err*ZX_4mu_err)+(f2e2mu_ZZ.GetBinError(15)*f2e2mu_ZZ.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err))

outformat = ( "$Z+X$ & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f \\\\ \n" % ( ZX_4e, ZX_4e_err, ZX_4mu, ZX_4mu_err, ZX_2e2mu, ZX_2e2mu_err, ZX_4e+ZX_4mu+ZX_2e2mu, sqrt( ZX_4e_err*ZX_4e_err+ZX_4mu_err*ZX_4mu_err+ZX_2e2mu_err*ZX_2e2mu_err) ) )
latexOUTFD.write( outformat )

#// sprintf(outformat,"Sum of bkgs & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\",
#// 	 f4e_totalbkg_noSM_H.GetBinContent(15)+ZX_4e, sqrt(f4e_totalbkg_noSM_H.GetBinError(15)*f4e_totalbkg_noSM_H.GetBinError(15)+ZX_4e_err*ZX_4e_err),
#// 	 f4mu_totalbkg_noSM_H.GetBinContent(15)+ZX_4mu, sqrt(f4mu_totalbkg_noSM_H.GetBinError(15)*f4mu_totalbkg_noSM_H.GetBinError(15)+ZX_4mu_err*ZX_4mu_err),
#// 	 f2e2mu_totalbkg_noSM_H.GetBinContent(15)+ZX_2e2mu, sqrt(f2e2mu_totalbkg_noSM_H.GetBinError(15)*f2e2mu_totalbkg_noSM_H.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err),
#// 	 f4e_totalbkg_noSM_H.GetBinContent(15)+ZX_4e+f4mu_totalbkg_noSM_H.GetBinContent(15)+ZX_4mu+f2e2mu_totalbkg_noSM_H.GetBinContent(15)+ZX_2e2mu,
#// 	 sqrt(
#// 	      (f4e_totalbkg_noSM_H.GetBinError(15)*f4e_totalbkg_noSM_H.GetBinError(15)+ZX_4e_err*ZX_4e_err) +
#// 	      (f4mu_totalbkg_noSM_H.GetBinError(15)*f4mu_totalbkg_noSM_H.GetBinError(15)+ZX_4mu_err*ZX_4mu_err) +
#// 	      (f2e2mu_totalbkg_noSM_H.GetBinError(15)*f2e2mu_totalbkg_noSM_H.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err)
#// 	      ) 
#// 	 )
#// print outformat 

outformat = ( "Sum of bkgs & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\ \n" % ( sumbkg_4e, sqrt(f4e_ZZ.GetBinError(15)*f4e_ZZ.GetBinError(15)+ZX_4e_err*ZX_4e_err), sumbkg_4mu, sqrt(f4mu_ZZ.GetBinError(15)*f4mu_ZZ.GetBinError(15)+ZX_4mu_err*ZX_4mu_err), sumbkg_2e2mu, sqrt(f2e2mu_ZZ.GetBinError(15)*f2e2mu_ZZ.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err), sumbkg_4l, sqrt((f4e_ZZ.GetBinError(15)*f4e_ZZ.GetBinError(15)+ZX_4e_err*ZX_4e_err)+ (f4mu_ZZ.GetBinError(15)*f4mu_ZZ.GetBinError(15)+ZX_4mu_err*ZX_4mu_err)+ (f2e2mu_ZZ.GetBinError(15)*f2e2mu_ZZ.GetBinError(15)+ZX_2e2mu_err*ZX_2e2mu_err)  ) ) )
latexOUTFD.write( outformat )

outformat = ( "SM Higgs ($m_{H}=125$ GeV)) & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\ \n" % ( f4e_totSM_H.GetBinContent(15), f4e_totSM_H.GetBinError(15), f4mu_totSM_H.GetBinContent(15), f4mu_totSM_H.GetBinError(15), f2e2mu_totSM_H.GetBinContent(15), f2e2mu_totSM_H.GetBinError(15), f4e_totSM_H.GetBinContent(15)+f4mu_totSM_H.GetBinContent(15)+f2e2mu_totSM_H.GetBinContent(15), sqrt(f4e_totSM_H.GetBinError(15)*f4e_totSM_H.GetBinError(15) + f4mu_totSM_H.GetBinError(15)*f4mu_totSM_H.GetBinError(15) + f2e2mu_totSM_H.GetBinError(15)*f2e2mu_totSM_H.GetBinError(15) ) ) )
latexOUTFD.write( outformat )

H_sumbkg_4e    = sumbkg_4e+f4e_totSM_H.GetBinContent(15)
H_sumbkg_4mu   = sumbkg_4mu+f4mu_totSM_H.GetBinContent(15)
H_sumbkg_2e2mu = sumbkg_2e2mu+f2e2mu_totSM_H.GetBinContent(15)
H_sumbkg_4l    = H_sumbkg_4e+H_sumbkg_4mu+H_sumbkg_2e2mu

latexOUTFD.write("\\hline \n" )
outformat = ( "Total expected & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f \\\\ \n" % ( H_sumbkg_4e, sqrt(f4e_totSM_H.GetBinError(15)*f4e_totSM_H.GetBinError(15)          +  sumbkg_4e_err*sumbkg_4e_err), H_sumbkg_4mu, sqrt(f4mu_totSM_H.GetBinError(15)*f4mu_totSM_H.GetBinError(15)       +  sumbkg_4mu_err*sumbkg_4mu_err), H_sumbkg_2e2mu, sqrt(f2e2mu_totSM_H.GetBinError(15)*f2e2mu_totSM_H.GetBinError(15) +  sumbkg_2e2mu_err*sumbkg_2e2mu_err), H_sumbkg_4l,  sqrt(      (f4e_totSM_H.GetBinError(15)*f4e_totSM_H.GetBinError(15)          +  sumbkg_4e_err*sumbkg_4e_err)   +      (f4mu_totSM_H.GetBinError(15)*f4mu_totSM_H.GetBinError(15)       +  sumbkg_4mu_err*sumbkg_4mu_err)  +      (f2e2mu_totSM_H.GetBinError(15)*f2e2mu_totSM_H.GetBinError(15) +  sumbkg_2e2mu_err*sumbkg_2e2mu_err) ) ) )
latexOUTFD.write( outformat )

latexOUTFD.write("\\hline\n" )
outformat = ( "Observed & %d & %d & %d & %d \\\\ \n" % (  int(f4e_totaldata.GetBinContent(15)), int(f4mu_totaldata.GetBinContent(15)), int(f2e2mu_totaldata.GetBinContent(15)), int(f4e_totaldata.GetBinContent(15)+f4mu_totaldata.GetBinContent(15)+f2e2mu_totaldata.GetBinContent(15)) ) )
latexOUTFD.write( outformat )
 
latexOUTFD.write( "\\hline \\hline \n") 
latexOUTFD.write( "\\end{tabular}\n") 
latexOUTFD.write( "}\n") 
latexOUTFD.write( "\\caption{Number of estimated background and signal events and number of observed candidates, after the SM Higgs selection, in the mass range $m_{4l}>$ 70 GeV. SM Higgs signal and ZZ background are estimated from Monte Carlo simulation, while Z+X is estimated from data; only statistical errors are quoted.}\n") 

latexOUTFD.write( "\\label{tab:SMHiggs_yields}\n")
latexOUTFD.write( "\\end{center}\n") 
latexOUTFD.write( "\\end{table}\n") 
latexOUTFD.write("\end{landscape}\n")
latexOUTFD.write("\end{document}\n")
latexOUTFD.close()

sys.exit(0)
# In[ ]:


#root_file="root://cms-xrd-global.cern.ch//store/user/nvanegas/BckgndW+Jets/tag_1_delphes_events01.root"
root_file = "root://cmseos.fnal.gov//store/group/lpchzz4leptons/histos4mu_25ns/output_DoubleMuon_Run2016B-23Sep2016-v3_miniaod_1.root"
ff = ROOT.TFile.Open(root_file)
ff.ls()


# In[2]:


thestack = PlotStack4l()
thestack.plotstack4l()

