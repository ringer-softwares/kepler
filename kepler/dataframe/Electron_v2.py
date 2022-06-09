
__all__ = ["Electron_v2"]

#
# electron struct
#
def Electron_v2():

  code = """
  namespace edm{
  
  struct Electron_v2{
  

   // Declaration of leaf types
   Float_t         avgmu;
   Float_t         el_et;
   Float_t         el_eta;
   Float_t         el_phi;
   Float_t         el_Reta;
   Float_t         el_Rphi;
   Float_t         el_e237;
   Float_t         el_e277;
   Float_t         el_Rhad;
   Float_t         el_Rhad1;
   Float_t         el_weta1;
   Float_t         el_weta2;
   Float_t         el_f1;
   Float_t         el_f3;
   Float_t         el_f1core;
   Float_t         el_fracs1;
   Float_t         el_f3core;
   Float_t         el_Eratio;
   Float_t         el_deltaE;
   Float_t         el_ethad;
   Float_t         el_wtots1;
   Float_t         el_ethad1;
   Float_t         el_calo_eta;
   Float_t         el_calo_phi;
   Float_t         el_calo_et;
   Float_t         el_calo_etaBE2;
   Float_t         el_calo_e;
   Bool_t          el_hasCalo;
   Float_t         el_trk_d0;
   Float_t         el_trk_z0;
   Float_t         el_trk_eta;
   Float_t         el_trk_phi;
   Float_t         el_trk_pt;
   Float_t         el_trk_qOverP;
   Float_t         el_trk_charge;
   Float_t         el_trk_sigd0;
   Float_t         el_trk_eProbabilityHT;
   Bool_t          el_hasTrack;
   Float_t         el_deltaEta0;
   Float_t         el_deltaEta1;
   Float_t         el_deta2;
   Float_t         el_deltaEta3;
   Float_t         el_deltaPhi0;
   Float_t         el_deltaPhi1;
   Float_t         el_dphi2;
   Float_t         el_deltaPhi3;
   Float_t         el_deltaPhiRescaled2;
   vector<float>   *el_ringsE;
   Float_t         el_trk_d0Significance;
   Float_t         el_ptcone20;
   Float_t         el_ptcone30;
   Float_t         el_ptcone40;
   Float_t         el_ptvarcone20;
   Float_t         el_ptvarcone30;
   Float_t         el_ptvarcone40;
   vector<char>    *el_trk_summaryValues;
   Float_t         el_trk_deltaPOverP;
   Float_t         el_trk_transformed_eProbabilityHT;
   Bool_t          el_tight;
   Bool_t          el_medium;
   Bool_t          el_loose;
   Bool_t          el_lhtight;
   Bool_t          el_lhmedium;
   Bool_t          el_lhloose;
   Bool_t          el_lhvloose;
   Bool_t          el_dnntight;
   Bool_t          el_dnnmedium;
   Bool_t          el_dnnloose;
   Float_t         el_nGoodVtx;
   Float_t         el_nPileupPrimaryVtx;
   Float_t         trig_L1_el_eta;
   Float_t         trig_L1_el_phi;
   Float_t         trig_L1_el_emClus;
   Float_t         trig_L1_el_roi_et;
   Float_t         trig_L1_el_emIso;
   Float_t         trig_L1_el_hadCore;
   Float_t         trig_L1_el_tauClus;
   Bool_t          trig_L1_isLegacy;
   Float_t         trig_L1eFex_el_eta;
   Float_t         trig_L1eFex_el_phi;
   Float_t         trig_L1eFex_el_roi_et;
   Float_t         trig_L1eFex_el_wstot;
   Float_t         trig_L1eFex_el_reta;
   Float_t         trig_L1eFex_el_rhad;
   Float_t         trig_L2_calo_et;
   Float_t         trig_L2_calo_eta;
   Float_t         trig_L2_calo_phi;
   Float_t         trig_L2_calo_e237;
   Float_t         trig_L2_calo_e277;
   Float_t         trig_L2_calo_fracs1;
   Float_t         trig_L2_calo_weta2;
   Float_t         trig_L2_calo_ehad1;
   Float_t         trig_L2_calo_emaxs1;
   Float_t         trig_L2_calo_e2tsts1;
   Float_t         trig_L2_calo_wstot;
   vector<float>   *trig_L2_calo_energySample;
   vector<float>   *trig_L2_calo_rings;
   vector<float>   *trig_L2_el_charge;
   vector<float>   *trig_L2_el_pt;
   vector<float>   *trig_L2_el_eta;
   vector<float>   *trig_L2_el_phi;
   vector<float>   *trig_L2_el_px;
   vector<float>   *trig_L2_el_py;
   vector<float>   *trig_L2_el_pz;
   vector<float>   *trig_L2_el_E;
   vector<float>   *trig_L2_el_etOverPt;
   vector<float>   *trig_L2_el_caloEta;
   vector<float>   *trig_L2_el_caloPhi;
   vector<float>   *trig_L2_el_nTRTHiThresholdHits;
   vector<float>   *trig_L2_el_nTRTHits;
   vector<float>   *trig_L2_el_trkClusDeta;
   vector<float>   *trig_L2_el_trkClusDphi;
   vector<float>   *trig_L2_el_trk_d0;
   vector<float>   *trig_L2_el_hasTrack;
   
   vector<float>   *trig_EF_calo_et;
   vector<float>   *trig_EF_calo_e;
   vector<float>   *trig_EF_calo_eta;
   vector<float>   *trig_EF_calo_etaBE2;
   vector<float>   *trig_EF_calo_phi;
   
   vector<float>   *trig_EF_el_hasCalo;
   vector<float>   *trig_EF_el_Eratio;
   vector<float>   *trig_EF_el_Reta;
   vector<float>   *trig_EF_el_Rhad;
   vector<float>   *trig_EF_el_Rhad1;
   vector<float>   *trig_EF_el_Rphi;
   vector<float>   *trig_EF_el_DeltaE;
   vector<float>   *trig_EF_el_ethad;
   vector<float>   *trig_EF_el_ethad1;
   vector<float>   *trig_EF_el_f1;
   vector<float>   *trig_EF_el_f1core;
   vector<float>   *trig_EF_el_f3;
   vector<float>   *trig_EF_el_f3core;
   vector<float>   *trig_EF_el_fracs1;
   vector<float>   *trig_EF_el_weta1;
   vector<float>   *trig_EF_el_weta2;
   vector<float>   *trig_EF_el_e237;
   vector<float>   *trig_EF_el_e277;
   vector<float>   *trig_EF_el_ehad1;
   vector<float>   *trig_EF_el_wtots1;
   vector<float>   *trig_EF_el_deltaEta1;
   vector<float>   *trig_EF_el_deltaPhiRescaled2;
   vector<float>   *trig_EF_el_deta2;
   vector<float>   *trig_EF_el_dphi2;
   vector<float>   *trig_EF_el_dphiresc;
   vector<float>   *trig_EF_el_e;
   vector<float>   *trig_EF_el_et;
   vector<float>   *trig_EF_el_etCone;
   vector<float>   *trig_EF_el_pt;
   vector<float>   *trig_EF_el_eta;
   vector<float>   *trig_EF_el_phi;
   vector<float>   *trig_EF_el_trk_pt;
   vector<float>   *trig_EF_el_trk_eta;
   vector<float>   *trig_EF_el_trk_phi;
   vector<float>   *trig_EF_el_trk_d0;
   vector<float>   *trig_EF_el_trk_z0;
   vector<float>   *trig_EF_el_trk_qOverP;
   vector<float>   *trig_EF_el_trk_charge;
   vector<float>   *trig_EF_el_trk_eProbabilityHT;
   vector<float>   *trig_EF_el_trk_transformed_eProbabilityHT;
   vector<float>   *trig_EF_el_trk_DeltaPOverP;
   vector<float>   *trig_EF_el_hasTrack;
   vector<float>   *trig_EF_el_trk_sigd0;
   vector<float>   *trig_EF_el_trk_d0significance;
   vector<char>    *trig_EF_el_trk_summaryValues;
   vector<int>     *trig_EF_el_dnntight;
   vector<int>     *trig_EF_el_dnnmedium;
   vector<int>     *trig_EF_el_dnnloose;
   vector<int>     *trig_EF_el_lhtight;
   vector<int>     *trig_EF_el_lhmedium;
   vector<int>     *trig_EF_el_lhloose;
   vector<int>     *trig_EF_el_lhvloose;
   Bool_t          mc_hasMC;
   Float_t         mc_eta;
   Float_t         mc_phi;
   Float_t         mc_pt;
   Bool_t          mc_isTop;
   Bool_t          mc_isQuark;
   Bool_t          mc_isParton;
   Bool_t          mc_isMeson;
   Bool_t          mc_isTau;
   Bool_t          mc_isMuon;
   Bool_t          mc_isPhoton;
   Bool_t          mc_isElectron;
   Bool_t          mc_isTruthElectronAny;
   Bool_t          mc_isTruthElectronFromZ;
   Bool_t          mc_isTruthElectronFromJpsi;
   Int_t           mc_origin;
   Int_t           mc_type;
  
  };
  }
  """
  
  import ROOT
  ROOT.gInterpreter.ProcessLine(code)

  from ROOT import edm
  return edm.Electron_v2()

