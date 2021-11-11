

# External
from ROOT import TH1F, TH2F, TProfile, TProfile2D, TCanvas
import numpy as np
import array



def GetHistogramFromMany( basepath, paths, keys ,  prefix='Loading...'):
  
    from Gaugi import progressbar, expand_folders
    from copy import deepcopy     
    # internal open function
    def Open( path ):
        from ROOT import TFile
        f = TFile(path, 'read')
        if len(f.GetListOfKeys())>0:
            run_numbers = [ key.GetName() for key in  f.GetListOfKeys() ]
            return f, run_numbers
        else:
            return f, None
    # internal close function
    def Close( f ):
        f.Close()
        del f
    # internal retrive histogram
    def GetHistogram( f, run_number, path ,logger=None):
        try:            
            hist = f.Get(run_number+'/'+path)
            hist.GetEntries()
            return hist
            
        except:
            return None
    # internal integration
    def SumHists(histList):
        totalHist = None
        for hist in histList:
            if hist is None:
                continue
            if totalHist is None:
                totalHist=deepcopy(hist.Clone())
            else:
                totalHist.Add( hist )
        return totalHist

    files = expand_folders(basepath)
    hists = {}
    for f in progressbar(files, 'Loading'):
        try:
            _f, _run_numbers = Open(f)
        except:
            continue
        if _run_numbers is None:
            continue
        for idx, _path in enumerate(paths):
            for _run_number in _run_numbers:
                hist = GetHistogram(_f, _run_number, _path)
                if (hist is not None):
                    if not keys[idx] in hists.keys():
                        hists[keys[idx]]=[deepcopy(hist.Clone())]
                    else:
                        hists[keys[idx]].append(deepcopy(hist.Clone()))
        Close(_f)

    for key in hists.keys():
        hists[key]=SumHists(hists[key])
    #from pprint import pprint
    #pprint(hists)
    return hists



def GetXAxisWorkAround( hist, nbins, xmin, xmax ):
  from ROOT import TH1F
  h=TH1F(hist.GetName()+'_resize', hist.GetTitle(), nbins,xmin,xmax)
  for bin in range(h.GetNbinsX()):
    x = h.GetBinCenter(bin+1)
    m_bin = hist.FindBin(x)
    y = hist.GetBinContent(m_bin)
    error = hist.GetBinError(m_bin)
    h.SetBinContent(bin+1,y)
    h.SetBinError(bin+1,error)
  return h


def GetProfile( passed, tot, resize=None):
    """
      Resize optin must be a list with [nbins, xmin, xmax]
    """
    if resize:
        tot=GetXAxisWorkAround(tot,resize[0],resize[1],resize[2])
        passed=GetXAxisWorkAround(passed,resize[0],resize[1],resize[2])
    passed.Sumw2(); tot.Sumw2()
    h = passed.Clone()
    h.Divide( passed, tot,1.,1.,'B' )
    return h
 

def GetHistogramRootPaths( triggerList, removeInnefBefore=False, is_emulation=False):
  plot_names = ['et','eta','mu']
  level_names = ['L1Calo','L2Calo','L2','EFCalo','HLT']
  levels_input = ['L1Calo','L1Calo','L1Calo','L2','EFCalo']
  from Gaugi import progressbar
  paths=[]; keys=[]

  def check_etthr_higher_than(trigger , etthr):
      et = int(trigger.replace('HLT_','').split('_')[0][1::])
      return True if et >= etthr else False

  entries=len(triggerList)
  step = int(entries/100) if int(entries/100) > 0 else 1
  for trigItem in progressbar(triggerList, 'Making paths...'):
    ### Retrieve all paths
    for idx ,level in enumerate(level_names):
      for histname in plot_names:
        if 'et' == histname and check_etthr_higher_than(trigItem,100):  histname='highet'
        if is_emulation:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Emulation/{LEVEL}/{HIST}'
        else:
          histpath = 'HLT/Egamma/Expert/{TRIGGER}/Efficiency/{LEVEL}/{HIST}'
        paths.append(histpath.format(TRIGGER=trigItem,HIST='match_'+histname,LEVEL=level))
        if removeInnefBefore:
          paths.append(histpath.format(TRIGGER=trigItem,HIST= ('match_'+histname if idx!=0 else histname),LEVEL=levels_input[idx]))
        else:
          paths.append(histpath.format(TRIGGER=trigItem,HIST=histname,LEVEL='L1Calo'))
        if 'highet' == histname:  histname='et'
        keys.append(trigItem+'_'+level+'_match_'+histname)
        keys.append(trigItem+'_'+level+'_'+histname)
  # Loop over triggers
  return paths, keys


