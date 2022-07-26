
__all__ = ["Electron_v2"]

#
# electron struct
#
def Electron_v2():

  code = """
  namespace edm{
  
  struct Electron_v2{

   // Declaration of leaf types
   float         avgmu;
   float         el_e;
   float         el_pt;
   float         el_eta;
   float         el_phi;
   float         el_Reta;
   float         el_Rphi;
   float         el_e237;
   float         el_e277;
   float         el_Rhad;
   float         el_Rhad1;
   float         el_weta1;
   float         el_weta2;
   float         el_f1;
   float         el_f3;
   float         el_f1core;
   float         el_fracs1;
   float         el_f3core;
   float         el_Eratio;
   float         el_deltaE;
   float         el_ethad;
   float         el_wtots1;
   float         el_ethad1;
   float         el_deltaEta0;
   float         el_deltaEta1;
   float         el_deta2;
   float         el_deltaEta3;
   float         el_deltaPhi0;
   float         el_deltaPhi1;
   float         el_dphi2;
   float         el_deltaPhi3;
   float         el_deltaPhiRescaled2;
   float         el_ptcone20;
   float         el_ptcone30;
   float         el_ptcone40;
   float         el_ptvarcone20;
   float         el_ptvarcone30;
   float         el_ptvarcone40;
   float         el_nGoodVtx;
   float         el_nPileupPrimaryVtx;
   bool          el_hasCalo;
   float         el_calo_eta;
   float         el_calo_phi;
   float         el_calo_et;
   float         el_calo_etaBE2;
   float         el_calo_e;
   bool          el_hasTrack;
   float         el_trk_d0;
   float         el_trk_z0;
   float         el_trk_eta;
   float         el_trk_phi;
   float         el_trk_pt;
   float         el_trk_qOverP;
   float         el_trk_charge;
   float         el_trk_sigd0;
   float         el_trk_eProbabilityHT;
   vector<int>     *el_trk_summaryValues;
   float         el_trk_deltaPOverP;
   float         el_trk_transformed_eProbabilityHT;
   float         el_trk_d0Significance;
   bool          el_lhtight;
   bool          el_lhmedium;
   bool          el_lhloose;
   bool          el_lhvloose;
   bool          el_dnntight;
   bool          el_dnnmedium;
   bool          el_dnnloose;
   float         trig_L1_el_eta;
   float         trig_L1_el_phi;
   float         trig_L1_el_emClus;
   float         trig_L1_el_roi_et;
   float         trig_L1_el_emIso;
   float         trig_L1_el_hadCore;
   float         trig_L1_el_tauClus;
   float         trig_L2_calo_et;
   float         trig_L2_calo_eta;
   float         trig_L2_calo_phi;
   float         trig_L2_calo_e237;
   float         trig_L2_calo_e277;
   float         trig_L2_calo_fracs1;
   float         trig_L2_calo_weta2;
   float         trig_L2_calo_ehad1;
   float         trig_L2_calo_emaxs1;
   float         trig_L2_calo_e2tsts1;
   float         trig_L2_calo_wstot;
   vector<float>   *trig_L2_calo_energySample;
   vector<float>   *trig_L2_calo_rings;
   vector<int>     *trig_L2_el_hasTrack;
   vector<float>   *trig_L2_el_charge;
   vector<float>   *trig_L2_el_pt;
   vector<float>   *trig_L2_el_eta;
   vector<float>   *trig_L2_el_phi;
   vector<float>   *trig_L2_el_etOverPt;
   vector<float>   *trig_L2_el_trkClusDeta;
   vector<float>   *trig_L2_el_trkClusDphi;
   vector<float>   *trig_L2_el_trk_d0;
   vector<int>     *trig_EF_el_hasCalo;
   vector<float>   *trig_EF_calo_et;
   vector<float>   *trig_EF_calo_e;
   vector<float>   *trig_EF_calo_eta;
   vector<float>   *trig_EF_calo_etaBE2;
   vector<float>   *trig_EF_calo_phi;
   bool            trig_EF_el_hasHLT;
   vector<float>   *trig_EF_el_e;
   vector<float>   *trig_EF_el_et;
   vector<float>   *trig_EF_el_pt;
   vector<float>   *trig_EF_el_eta;
   vector<float>   *trig_EF_el_phi;
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
   vector<float>   *trig_EF_el_ptvarcone20;
   vector<int>     *trig_EF_el_hasTrack;
   vector<float>   *trig_EF_el_trk_pt;
   vector<float>   *trig_EF_el_trk_eta;
   vector<float>   *trig_EF_el_trk_phi;
   vector<float>   *trig_EF_el_trk_d0;
   vector<float>   *trig_EF_el_trk_qOverP;
   vector<float>   *trig_EF_el_trk_charge;
   vector<float>   *trig_EF_el_trk_eProbabilityHT;
   vector<float>   *trig_EF_el_trk_transformed_eProbabilityHT;
   vector<float>   *trig_EF_el_trk_DeltaPOverP;
   vector<float>   *trig_EF_el_trk_sigd0;
   vector<float>   *trig_EF_el_trk_d0significance;
   vector<int>     *trig_EF_el_trk_summaryValues;
   vector<int>     *trig_EF_el_dnntight;
   vector<int>     *trig_EF_el_dnnmedium;
   vector<int>     *trig_EF_el_dnnloose;
   vector<int>     *trig_EF_el_lhtight;
   vector<int>     *trig_EF_el_lhmedium;
   vector<int>     *trig_EF_el_lhloose;
   vector<int>     *trig_EF_el_lhvloose;
   bool          mc_hasMC;
   float         mc_eta;
   float         mc_phi;
   float         mc_pt;
   bool          mc_isTruthElectronAny;
   bool          mc_isTruthElectronFromZ;
   bool          mc_isTruthElectronFromJpsiPrompt;
   int           mc_origin;
   int           mc_type;
   int           mc_firstEgMotherTruthType;
   int           mc_firstEgMotherTruthOrigin;
   float         tag_el_e;
   float         tag_el_pt;
   float         tag_el_eta;
   float         tag_el_phi;
   float         tap_lifetime;
   float         tap_mass;
   float         tap_dR;

  };
  }
  """
  
  import ROOT
  ROOT.gInterpreter.ProcessLine(code)

  from ROOT import edm
  return edm.Electron_v2()

