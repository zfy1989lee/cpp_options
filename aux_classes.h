#ifndef _AUX_CLASSES_H
#define _AUX_CLASSES_H

#include <string>
#include "dt.h"
#include "portfolio.h"
#include "log_entry.h"

enum checkhit {bottomhit=-1,nohit=0,tophit=1};

class order{
 public:
  double fxrate;
  double deltac1amt;
  order(double r,double d){this->fxrate=r; this->deltac1amt=d;};
  order(const order & mycopy){this->fxrate = mycopy.fxrate; this->deltac1amt=mycopy.deltac1amt;}
};

class c_quote{
 public:
  //volume is adjusted by 1e6 multiple
  c_quote(std::string, std::string, std::string, std::string, std::string);
  c_quote(std::string datetimems, double, double, double, double);
  c_quote(const c_quote &);
  ~c_quote();
  void printquote();
  dt * quote_dt = NULL;
  double bid = 0.0;
  double bidsize = 0.0;
  double offer = 0.0;
  double offersize = 0.0;
};

class c_cycle{
 public:
  c_cycle(std::string, std::string,std::string, std::string, std::string, std::string, std::string, std::string, std::string, std::string, std::string, option_direction, option_ccypair, double);
  ~c_cycle();

  void WriteToFile(std::string);

  bool IfAdjustOrders(unsigned int);
  bool IfSkipQuote(unsigned int) const;
  void add_quote(std::string, std::string,std::string, std::string, std::string, std::string, std::string);
  void add_quote(std::string, std::string,std::string, double, double,double,double);
  void delete_all_quotes();

  void load_straddle(double,double);

  void set_first_quote(double x){this->first_quote=x;}
  void set_last_quote(double x){this->last_quote=x;}

  std::string sql_getcyclequotes();
  std::string sql_getquotesfromrowidrange(unsigned int, unsigned int);
  std::string get_filename(std::string);

  unsigned int get_minrowid(){return this->minrowid;}
  unsigned int get_maxrowid(){return this->maxrowid;}

  void CalculateSundaySteps(const c_quote &);

  bool IfFridayRebalancing(const dt &);
  bool IfFridayRebalancing(const c_quote &);

  bool IfSundayRebalancing(const dt &);
  bool IfSundayRebalancing(const c_quote &);

  bool IfMinYTMRebalancing(const c_quote &);

  unsigned int cycle_id;
  std::string cycle_start;
  dt * cycle_start_dt;
  std::string cycle_end;
  dt * cycle_end_dt;

  dt * last_friday;
  dt * last_sunday;

  unsigned int minrowid=0;
  unsigned int maxrowid=0;

  double first_quote=0;
  double last_quote=0;

  double starting_spot;
  double vol;
  double forward;
  double strike;
  option_direction odir;
  option_ccypair ocp;

  double manual_rebalancing_delta_fraction = 0.2;
  
  bool closetoexpiry = false;

  c_quote ** cycle_quotes = NULL;
  unsigned int num_quotes = 0;
  unsigned int max_num_quotes = 1000000;  

  Portfolio * my_portf = NULL;
};


#endif
