#include <stdlib.h>
#include <iostream>

#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

#include "dt.h"
#include "portfolio.h"
#include "log_entry.h"
#include "aux_classes.h"

#include "portfolio.hpp"
#include "log_entry.hpp"
#include "aux_classes.hpp"

#include <algorithm>
#include <climits>

#include "params.h"

#include <sys/stat.h>

using namespace std;

int main(int argc, char **argv){

  if(argc<2){
    cout<<"usage: program_name conf_file1 conf_file2 ...\n";
    return 0;
  }

  struct stat st;
  if(stat("reports",&st)!=0){
    system("mkdir reports");
  }

  c_params **my_params = new c_params*[argc-1];

  for(int k=0;k<argc-1;k++){
    cout<<"reading conf file "+to_string(k+1)+" of "+to_string(argc-1)+"... ";
    my_params[k] = new c_params(argv[k+1]);
    cout<<"done\n";

    cout<<"preparing directory "+my_params[k]->folder_name+"... ";


    if(stat(my_params[k]->folder_name.c_str(),&st)!=0){
      system(("mkdir "+my_params[k]->folder_name).c_str());
    }
    cout<<"done\n";

    cout<<"connecting to database... ";
    sql::Driver *driver;
    sql::Connection *con;
    sql::Statement *stmt;
    sql::ResultSet *res;

    driver = get_driver_instance();
    con = driver->connect(my_params[k]->host, my_params[k]->user_name, my_params[k]->password);
    con->setSchema(my_params[k]->database_name);
    cout<<"done\n";

    string sql_query_cycles = my_params[k]->generate_sql_string();

    cout<<"loading cycles... ";
    stmt = con->createStatement();
    res = stmt->executeQuery(sql_query_cycles);

    int num_cycles = 0;
    int max_num_cycles = 2000;
    c_cycle **my_cycles = new c_cycle*[max_num_cycles];

    while (res->next()) {

      string cycle_id = res->getString(1);
      string cycle_start = res->getString(2);
      string cycle_end = res->getString(3);
      string start_quote = res->getString(4);
      string strike = res->getString(5);
      string forward = res->getString(5);
      string vol = res->getString(6);
      string minrowid = res->getString(7);
      string maxrowid = res->getString(8);

      my_cycles[num_cycles] = new c_cycle(cycle_id,cycle_start,"10:00:00.000",cycle_end,"10:00:00.000",start_quote,strike,forward,vol,minrowid,maxrowid,sell,XXXUSD,my_params[k]->manual_rebalancing_delta_fraction);
      num_cycles++;
    }

    //cout<<"loading cycles... ";
    cout<<"done\n";

    delete res;
    delete stmt;
    delete con;  
    res = NULL;
    stmt = NULL;
    con = NULL;

    int super_cycle_num = my_params[k]->num_cycles;

    for(int j=0; j<(int)(ceil(num_cycles/((double)super_cycle_num))); j++){
      cout<<"\tsuper cycle "+to_string(j+1)+" of "+to_string(int(ceil(num_cycles/((double)super_cycle_num))))+"\n";
      
      unsigned int num_quotes = 0;
      unsigned int max_num_quotes = 1000000; 
      c_quote **loaded_quotes = new c_quote*[max_num_quotes];

      unsigned int minrowid = UINT_MAX;
      unsigned int maxrowid = 0;

      for (int j1=super_cycle_num*j;j1<min(super_cycle_num*(j+1),num_cycles);j1++){
         
	if(minrowid>my_cycles[j1]->get_minrowid()){
	  minrowid = my_cycles[j1]->get_minrowid();
	}
	if(maxrowid<my_cycles[j1]->get_maxrowid()){
	  maxrowid = my_cycles[j1]->get_maxrowid();
	}
      }

      string sql_request = "";

      if(super_cycle_num>1){
	sql_request = sql_getquotesfromrowidrange(minrowid,maxrowid);
      }
      else{ //super_cycle_num==1
	sql_request = my_cycles[j]->sql_getcyclequotes();
      }

      cout<<"\tconnecting to database... ";
      con = driver->connect(my_params[k]->host, my_params[k]->user_name, my_params[k]->password);
      con->setSchema(my_params[k]->database_name);
      cout<<"done\n";

      cout<<"\tloading quotes... ";
      stmt = con->createStatement();
      res = stmt->executeQuery(sql_request);

      while (res->next()){
	string s1 = res->getString("quotedate");
	string s2 = res->getString("quotetime");
	string s3 = res->getString("quotems");
	double d4 = res->getDouble("quotebid");
	double d5 = res->getDouble("bidvolume");
	double d6 = res->getDouble("quoteoffer");
	double d7 = res->getDouble("offervolume");

	if(num_quotes+1==max_num_quotes){
	  c_quote **temparray = new c_quote*[max_num_quotes];

	  for(int i=0;i<num_quotes;i++){
	    temparray[i] = loaded_quotes[i];
	  }
	  delete[] loaded_quotes;
	  loaded_quotes=NULL;

	  max_num_quotes = 2*max_num_quotes;
	  loaded_quotes = new c_quote*[max_num_quotes];

	  for(int i=0;i<num_quotes;i++){
	    loaded_quotes[i] = temparray[i];
	  }
	  delete[] temparray;
	  temparray = NULL;
	}

	loaded_quotes[num_quotes]=new c_quote(s1,s2,s3,d4,d5,d6,d7);
	num_quotes++;
      }
      cout<<"done\n";

      delete res; delete stmt; delete con;  
      res = NULL; stmt = NULL; con = NULL;

      for (int i=0; i<num_quotes;i++){
	for (int j1=super_cycle_num*j;j1<min(super_cycle_num*(j+1),num_cycles);j1++){
	  my_cycles[j1]->add_quote(loaded_quotes[i]);
	}
      }

      for (int j1=super_cycle_num*j;j1<min(super_cycle_num*(j+1),num_cycles);j1++){
	cout<<"\t\tcycle_id: "<<my_cycles[j1]->cycle_id<<"\n";
	cout<<"\t\tnum quotes: "<<my_cycles[j1]->num_quotes<<"\n";
	
	//load straddle
	my_cycles[j1]->load_straddle(my_params[k]->linear_delta_width, my_params[k]->min_ytm);
	my_cycles[j1]->my_portf->SetThreshold(my_params[k]->threshold);

	//first rebalancing
	// cout<<"first rebalancing\n";
	double fill_rate = my_cycles[j1]->my_portf->RebalanceDeltaAtMarket(*(my_cycles[j1]->cycle_quotes[0]));
	my_cycles[j1]->set_first_quote(fill_rate);

	for(int q = 1; q<my_cycles[j1]->num_quotes;q++){

	  if(my_cycles[j1]->IfSkipQuote(q)){
	    continue;
	  }

	  bool condA = my_cycles[j1]->IfFridayRebalancing(*(my_cycles[j1]->cycle_quotes[q]));
	  bool condB = my_cycles[j1]->IfSundayRebalancing(*(my_cycles[j1]->cycle_quotes[q]));
	  bool condC = my_cycles[j1]->IfMinYTMRebalancing(*(my_cycles[j1]->cycle_quotes[q]));

	  //last rebalancing:
	  if(q==my_cycles[j1]->num_quotes-1){
	    //cout<<"last rebalancing\n";
	    fill_rate = my_cycles[j1]->my_portf->RebalanceDeltaAtMarket(*(my_cycles[j1]->cycle_quotes[q]),true);
	    my_cycles[j1]->set_last_quote(fill_rate);
	    my_cycles[j1]->my_portf->SetFinalPrice(fill_rate);
	  }
	  else if(condB){
	    //cout<<"Sunday rebalancing\n";
	    my_cycles[j1]->CalculateSundaySteps(*(my_cycles[j1]->cycle_quotes[q]));
	  }
	  else if(condA||condC){
	    //cout<<"condA or condC rebalancing\n";
	    my_cycles[j1]->my_portf->RebalanceDeltaAtMarket(*(my_cycles[j1]->cycle_quotes[q]));
	  }
	  else{
	    bool rebalancing_result = my_cycles[j1]->my_portf->RebalanceDeltaAtOrder(*(my_cycles[j1]->cycle_quotes[q]));

	    //manual rebalancing at market
	    if((!rebalancing_result)&&(my_cycles[j1]->IfAdjustOrders(q))){
	      // cout<<"manual rebalancing\n";
	      my_cycles[j1]->my_portf->RebalanceDeltaAtMarket(*(my_cycles[j1]->cycle_quotes[q]));
	    }
	  }
	}

	cout<<"\t\tnum rebalancings : "<<my_cycles[j1]->my_portf->GetNumLogEntries()<<"\n";

	cout<<"\t\tsaving results to "<<my_cycles[j1]->get_filename(my_params[k]->folder_name)<<" ";
	my_cycles[j1]->my_portf->WriteToFile(my_cycles[j1]->get_filename(my_params[k]->folder_name));
	cout<<"done\n";

	cout<<"\t\tappending summary file... ";
	my_cycles[j1]->WriteToFile(my_params[k]->folder_name+"/00.summary.txt");
	cout<<" done\n";
      }

      for (int j1=super_cycle_num*j;j1<min(super_cycle_num*(j+1),num_cycles);j1++){
	  my_cycles[j1]->delete_quotes_array();
      }

      for (int i=0; i<num_quotes; i++){
	delete loaded_quotes[i];
	loaded_quotes[i]=NULL;
      }
      delete [] loaded_quotes;
      loaded_quotes=NULL;
    }
    delete[] my_cycles;
    my_cycles = NULL;
  }

  for(int k=0;k<argc-1;k++){
    delete my_params[k];
    my_params[k]=NULL;
  }
  delete[] my_params;
  my_params=NULL;
}

