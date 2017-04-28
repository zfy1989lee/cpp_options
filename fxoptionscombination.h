#ifndef _FXOPTIONSCOMBINATION_H
#define _FXOPTIONSCOMBINATION_H

#include<iostream>
#include<math.h>
#include "dt.h"
#include "norm.h"
#include "fxoptions.h"
#include <cstdlib>

class FXOptionsCombination{
 public:
  FXOptionsCombination(){};
  ~FXOptionsCombination(){};
  virtual void PrintParams() const = 0;

  //each of these functions returns a parameter that is the same for all options in a combination:
  double GetLinearDeltaWidth() const {return this->portf[0]->GetLinearDeltaWidth();}
  double GetC1Notional() const {return this->portf[0]->GetC1Notional();}
  double GetSpot() const {return this->portf[0]->GetSpot();}
  dt GetMaturityDate() const {return this->portf[0]->GetMaturityDate();}
  dt GetCurrentDate() const {return this->portf[0]->GetCurrentDate();}
  double GetForward() const {return this->portf[0]->GetForward();}
  double GetR_c2() const {return this->portf[0]->GetR_c2();}
  double GetR_c1() const {return this->portf[0]->GetR_c1();}
  double GetYTM() const {return this->portf[0]->GetYTM();}
  double GetMinYTM() const {return this->portf[0]->GetMinYTM();}
  option_ccypair GetOptionCcyPair() const {return this->portf[0]->GetOptionCcyPair();}
  option_direction GetOptionDir() const {return this->portf[0]->GetOptionDir();}

  //each of these functions returns a parameter that may vary for options in a combination:
  double GetUSDNotional(int i=0) const {return this->portf[i]->GetUSDNotional();} 
  double GetC2Notional(int i=0) const {return this->portf[i]->GetC2Notional();}
  double GetStrike(int i=0) const {return this->portf[i]->GetStrike();} 
  double GetVol(int i=0) const {return this->portf[i]->GetVol();}

  ////combination of risks/parameters
  double GetUSDPayout(double) const;
  double GetUSDPrice() const;
  double GetUSDVega(double ch) const;
  double GetUSDTheta(double ch) const; 
  double GetUSDDelta(double step) const;
  double GetUSDGamma(double step) const;
  double GetUSDGammaForStepCalculation() const;
  double GetDeltaC1Amount() const;

  void UpdateRisks();   
  void UpdateDT(const dt&);
  void UpdateSpot(double);
  void UpdateSpotDT(double, const dt&);
  //void UpdateVol(double); 

 protected:
  fxopt ** portf = NULL;
  unsigned int num_portf;
};

double FXOptionsCombination::GetUSDPayout(double last_quote) const {
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDPayout(last_quote);
  }
  return sum;
}

double FXOptionsCombination::GetUSDPrice() const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDPrice();
  }
  return sum;
}

double FXOptionsCombination::GetUSDVega(double ch) const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDVega(ch);
  }
  return sum;
}

double FXOptionsCombination::GetUSDTheta(double ch) const{ // {retur
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDTheta(ch);
  }
  return sum;
}

double FXOptionsCombination::GetUSDDelta(double step) const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDDelta(step);
  }
  return sum;
}

double FXOptionsCombination::GetUSDGamma(double step) const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDGamma(step);
  }
  return sum;
} 

double FXOptionsCombination::GetUSDGammaForStepCalculation() const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetUSDGammaForStepCalculation();
  }
  return sum;
}

double FXOptionsCombination::GetDeltaC1Amount() const{
  double sum=0;
  for(int i=0;i<this->num_portf;i++){
    sum+=this->portf[i]->GetDeltaC1Amount();
  }
  return sum;
}

void FXOptionsCombination::UpdateRisks() {
  for(int i=0;i<this->num_portf;i++){
    this->portf[i]->UpdateRisks();
  }
}

void FXOptionsCombination::UpdateSpotDT(double x, const dt& newdt){
  for(int i=0;i<this->num_portf;i++){
    this->portf[i]->UpdateSpotDT(x,newdt);
  }
}

void FXOptionsCombination::UpdateDT(const dt& newdt){
  for(int i=0;i<this->num_portf;i++){
    this->portf[i]->UpdateDT(newdt);
  }
}

void FXOptionsCombination::UpdateSpot(double x){
  for(int i=0;i<this->num_portf;i++){
    this->portf[i]->UpdateSpot(x);
  }
}

#endif
