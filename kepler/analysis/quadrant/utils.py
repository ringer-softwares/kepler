

from root_utils.axis import *
from root_utils.functions import *
from root_utils.utils import SumHists
from root_utils import tobject_collector
from ROOT import kBlack,kRed,kGreen,kGray,kMagenta,kBlue
import ROOT
from copy import copy

#
# Plot quadrant 
#
def plot_quadrant( hists, xlabel, legends, drawopt='hist', divide='B', 
                   these_colors = [kBlack,kRed+1, kBlue+2,kGray+1] , 
                   runLabel = None,
                   canvas_name='canvas',
                   etbins=None,
                   etabins=None,
                   etidx=None,
                   etaidx=None):



  canvas  = RatioCanvas(canvas_name, canvas_name, 500, 500)
  pad_top = canvas.GetPrimitive('pad_top')
  pad_bot = canvas.GetPrimitive('pad_bot')
  pad_top.SetLogy()

  ref_hist = SumHists( hists )
  collect=[]
  divs=[]

  these_transcolors = [ ROOT.TColor.GetColorTransparent(color, .5) for color in these_colors ]

  divs = []
  for idx, hist in enumerate(hists):
    
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.55)
    hist.SetLineColor(these_colors[idx])
    hist.SetMarkerColor(these_colors[idx])
    hist.SetFillColor(these_transcolors[idx])
    AddHistogram( pad_top, hist, 'histE2 L same', False, None, None)
    div = hist.Clone(); div.Divide(div,ref_hist,1.,1.,'b'); div.Scale(100.); collect.append(div)
    div.SetMarkerSize(0.5)
    div.SetMarkerColor(these_colors[idx])
    # TODO: Check why error bar still here. Force error bar equal zero
    for ibin in range(div.GetNbinsX()):  div.SetBinError(ibin,0.0)
    divs.append( div )
    # add left axis
    if idx == 1 or idx == 2: AddHistogram( pad_bot, div , 'p', False, None, None)
    #if idx == 2: AddHistogram( pad_bot, div , 'p', False, None, None)
    def AddTopLabels(canvas,legends, legOpt = 'p', etlist = None, etalist = None, etidx = None, etaidx = None, legTextSize=10, 
                     runLabel = '', extraText1 = None, legendY1=.66, legendY2=.97, maxLegLength = 19):
        text_lines = [GetAtlasInternalText(), GetSqrtsText(13) ]
        if runLabel: text_lines.append( runLabel )
        DrawText(can,text_lines,.40,.68,.70,.93,totalentries=4)
        MakeLegend( canvas,.67,legendY1,.93,legendY2,textsize=legTextSize, names=legends, option = legOpt, squarebox=False,     
                    totalentries=0, maxlength=maxLegLength )
        extraText = []; _etlist = copy(etlist); _etalist = copy(etalist)
        if _etlist and etidx is not None:
            # add infinity in case of last et value too large
            if _etlist[-1]>9999:  _etlist[-1]='#infty'
            binEt = (str(_etlist[etidx]) + ' < E_{T} [GeV] < ' + str(_etlist[etidx+1]) if etidx+1 < len(_etlist) else
                     'E_{T} > ' + str(_etlist[etidx]) + ' GeV')
            extraText.append(binEt)
        if _etalist and etaidx is not None:
            binEta = (str(_etalist[etaidx]) + ' < #eta < ' + str(_etalist[etaidx+1]) if etaidx+1 < len(_etalist) else
                      str(_etalist[etaidx]) + ' < #eta < 2.47')
            extraText.append(binEta)
        DrawText(canvas,extraText,.14,.68,.35,.93,totalentries=4)

  AddTopLabels(canvas, legends, runLabel=runLabel, legOpt='p',legTextSize=12, 
               etlist=etbins,etalist=etabins,etidx=etidx,etaidx=etaidx)
  SetAxisLabels(canvas,xlabel,'Count','Disagreement [%]')
  #SetAxisLabels(canvas,xlabel,'Count','(Red or Blue)/Total [%]')
  FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5, YTitleSize=16)
  #FormatCanvasAxes(canvas, XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
  AutoFixAxes(pad_top,ignoreErrors=False)
  AutoFixAxes(pad_bot,ignoreErrors=False)
  FixYaxisRanges(pad_bot, ignoreErrors=True, yminc=-eps )
  #AddRightAxisObj(pad_bot, [divs[1]], drawopt="p,same", equate=[0., max([d.GetBinContent(h.GetMaximumBin()) for d,h in zip([divs[1]], [hists[1]])])]
  #               , drawAxis=True, axisColor=(ROOT.kRed+1), ignorezeros=False, ignoreErrors=True, label = "Ringer Rejected [%]")
  return canvas







  def make_report()