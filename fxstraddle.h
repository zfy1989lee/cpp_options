#ifndef _FXSTRADDLE_H
#define _FXSTRADDLE_H

#include<iostream>
#include<math.h>
#include "dt.h"
#include "norm.h"
#include "fxoptions.h"
#include <cstdlib>

class FXStraddle{
 public:
  FXStraddle(double, double, double, double, double,         dt, dt, option_direction, option_ccypair, double, double);
  FXStraddle(double, double, double, double, double, double, dt, dt, option_direction, option_ccypair, double, double);
  FXStraddle(const FXStraddle &);
  ~FXStraddle();

  FXStraddle copy();

  double GetUSDPayout(double) const;
  double GetLinearDeltaWidth() const {return this->portf[0]->GetLinearDeltaWidth();}
  double GetUSDNotional() const {return this->portf[0]->GetUSDNotional();} 
  double GetC1Notional() const {return this->portf[0]->GetC1Notional();}
  double GetC2Notional() const {return this->portf[0]->GetC2Notional();}
  double GetStrike() const {return this->portf[0]->GetStrike();} 
  double GetSpot() const {return this->portf[0]->GetSpot();}
  double GetVol() const {return this->portf[0]->GetVol();}
  dt GetMaturityDate() const {return this->portf[0]->GetMaturityDate();}
  dt GetCurrentDate() const {return this->portf[0]->GetCurrentDate();}
  double GetForward() const {return this->portf[0]->GetForward();}
  double GetR_c2() const {return this->portf[0]->GetR_c2();}
  double GetR_c1() const {return this->portf[0]->GetR_c1();}
  double GetYTM() const {return this->portf[0]->GetYTM();}
  double GetMinYTM() const {return this->portf[0]->GetMinYTM();}
  option_ccypair GetOptionCcyPair() const {return this->portf[0]->GetOptionCcyPair();}
  option_direction GetOptionDir() const {return this->portf[0]->GetOptionDir();}

  double GetUSDPrice() const {return (this->portf[0]->GetUSDPrice()+this->portf[1]->GetUSDPrice());}
  double GetUSDVega(double ch) const {return (this->portf[0]->GetUSDVega(ch)+this->portf[1]->GetUSDVega(ch));}
  double GetUSDTheta(double ch) const {return (this->portf[0]->GetUSDTheta(ch)+this->portf[1]->GetUSDTheta(ch));}
  double GetUSDDelta(double step) const {return (this->portf[0]->GetUSDDelta(step)+this->portf[1]->GetUSDDelta(step));}
  double GetUSDGamma(double step) const {return (this->portf[0]->GetUSDGamma(step)+this->portf[1]->GetUSDGamma(step));}
  double GetUSDGammaForStepCalculation() const {return (this->portf[0]->GetUSDGammaForStepCalculation()+this->portf[1]->GetUSDGammaForStepCalculation());}
  double GetUSDSpeed(double step) const {return (this->portf[0]->GetUSDSpeed(step)+this->portf[1]->GetUSDSpeed(step));}
  double GetDeltaC1Amount() const {return (this->portf[0]->GetDeltaC1Amount()+this->portf[1]->GetDeltaC1Amount());}

  void PrintParams() const;
  
  void UpdateDT(const dt&);
  void UpdateSpot(double);
  void UpdateSpotDT(double, const dt&);
  void UpdateVol(double);
  void UpdateRisks(){this->portf[0]->UpdateRisks();this->portf[1]->UpdateRisks();}

 private:
  fxopt ** portf = NULL;
  unsigned int num_portf;

};

double FXStraddle::GetUSDPayout(double last_quote) const {
  double value1 = this->portf[0]->GetUSDPayout(last_quote);
  double value2 = this->portf[1]->GetUSDPayout(last_quote);
  return (value1+value2);
}

void FXStraddle::PrintParams() const{
  std::printf("K=%9.5f; F=%9.5f; V=%5.2f; YTM=%6.6f\n",this->GetStrike(), this->GetForward(), this->GetVol()*100, this->GetYTM());
  std::printf("s=%9.5f; p=%8.0f; d=%9.0f; C1not=%10.0f\n",this->GetSpot(),this->GetUSDPrice(), this->GetDeltaC1Amount(),this->GetC1Notional());
}

void FXStraddle::UpdateSpotDT(double x, const dt& newdt){
  this->portf[0]->UpdateSpotDT(x,newdt);
  this->portf[1]->UpdateSpotDT(x,newdt);
  //this->UpdateRisks();
}

void FXStraddle::UpdateDT(const dt& newdt){
  this->portf[0]->UpdateDT(newdt);
  this->portf[1]->UpdateDT(newdt);
  //this->UpdateRisks();
}

void FXStraddle::UpdateSpot(double x){
  this->portf[0]->UpdateSpot(x);
  this->portf[1]->UpdateSpot(x);
  //this->UpdateRisks();
}

void FXStraddle::UpdateVol(double x){
  this->portf[0]->UpdateVol(x);
  this->portf[1]->UpdateVol(x);
  //this->UpdateRisks();  
}

//(double K, double V, double S, double r_c2, double r_c1, double notional, dt mat, dt cur, option_direction mydir, option_ccypair mycp)
FXStraddle FXStraddle::copy(){
  return FXStraddle(this->GetStrike(),this->GetVol(),this->GetSpot(),this->GetR_c2(),this->GetR_c1(),this->GetUSDNotional(),this->GetMaturityDate(),this->GetCurrentDate(),this->GetOptionDir(),this->GetOptionCcyPair(),this->GetLinearDeltaWidth(),this->GetMinYTM());
}

FXStraddle::FXStraddle(const FXStraddle & straddletocopy){
  this->num_portf = 2;
  this->portf = new fxopt*[2];

  this->portf[0] = new fxopt(straddletocopy.GetStrike(),straddletocopy.GetVol(),straddletocopy.GetSpot(),straddletocopy.GetR_c2(),straddletocopy.GetR_c1(),straddletocopy.GetUSDNotional(),straddletocopy.GetMaturityDate(),straddletocopy.GetCurrentDate(),call,straddletocopy.GetOptionDir(),straddletocopy.GetOptionCcyPair(),straddletocopy.GetLinearDeltaWidth(),straddletocopy.GetMinYTM());

  this->portf[1] = new fxopt(straddletocopy.GetStrike(),straddletocopy.GetVol(),straddletocopy.GetSpot(),straddletocopy.GetR_c2(),straddletocopy.GetR_c1(),straddletocopy.GetUSDNotional(),straddletocopy.GetMaturityDate(),straddletocopy.GetCurrentDate(),put,straddletocopy.GetOptionDir(),straddletocopy.GetOptionCcyPair(),straddletocopy.GetLinearDeltaWidth(),straddletocopy.GetMinYTM());
}

FXStraddle::FXStraddle(double K, double V, double S, double F, double notional, dt mat, dt cur, option_direction mydir, option_ccypair mycp, double linear_delta_width, double min_ytm){
  this->num_portf = 2;
  this->portf = new fxopt*[2];
  //(double K, double V, double S, double F, double notional, dt mat, dt cur, option_type mytype, option_direction mydir, option_ccypair mycp,double,double)
  this->portf[0] = new fxopt(K,V,S,F,notional,mat,cur,call,mydir,mycp, linear_delta_width, min_ytm);
  this->portf[1] = new fxopt(K,V,S,F,notional,mat,cur, put,mydir,mycp, linear_delta_width, min_ytm);
}

//(double K, double V, double S, double r_c2, double r_c1, double notional, dt mat, dt cur, option_type mytype, option_direction mydir, option_ccypair mycp,double,double)
FXStraddle::FXStraddle(double K, double V, double S, double r_c2, double r_c1, double notional, dt mat, dt cur, option_direction mydir, option_ccypair mycp, double linear_delta_width, double min_ytm){

  this->num_portf = 2;
  this->portf = new fxopt*[2];

  this->portf[0] = new fxopt(K,V,S,r_c2,r_c1,notional,mat,cur,call,mydir,mycp, linear_delta_width, min_ytm);
  this->portf[1] = new fxopt(K,V,S,r_c2,r_c1,notional,mat,cur, put,mydir,mycp, linear_delta_width, min_ytm);
}

FXStraddle::~FXStraddle(){

  for(int i=0;i<this->num_portf;i++){
    delete this->portf[i];
    this->portf[i]=NULL;
  }
  delete[] this->portf;
  this->portf=NULL;
}

#endif
