from datetime import datetime, timedelta
import pymysql
import os.path
import pass_word

import numpy as np
import pandas as pd

def LoadCycles(ccypair,tenor):
    
    myconn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
    mycursor = myconn.cursor()
    mysql_order = r"select cycle_id, cycle_start, cycle_end from %s_%s_cycles order by cycle_id" % (ccypair,tenor)

    mycursor.execute(mysql_order)
    myconn.commit()
    results = mycursor.fetchall()
    myconn.close()    
    return results

def LoadTxtFile(filename):

    #filename = "../reports/eurusd_1w_500/report_7_2009-05-13_2009-05-20.txt"
    #columns_str = "date time spot chg step slpg ht delta unhedged de_pnl de_total op_chg po_pnl po_total o_delta o_gamma o_theta o_xgm op_prc"
    columns_str = "reb_date,reb_time,reb_spot,reb_spot_chg_pips,reb_step_pips,reb_slippage_pips,reb_no_orders_hit,reb_delta_hedge,reb_unhedged_delta,reb_delta_pnl,reb_total_delta_pnl,reb_option_price_change,reb_portfolio_pnl,reb_total_portfolio_pnl,reb_delta,reb_gamma,reb_theta,reb_xgamma,option_price"
    columns = columns_str.split(",")

    #read_csv("vol_fwdpts.txt",parse_dates=True,skiprows=1,infer_datetime_format=True,sep=",",names=cols,index_col="Date", na_values="N/A")
    report_df = pd.read_csv(filename,parse_dates=True,skiprows=1,infer_datetime_format=True,names=columns,delim_whitespace=True)

    return report_df

insert_into_cols = "(reb_cycle_id,reb_date,reb_time,reb_spot,reb_spot_chg_pips,reb_step_pips,reb_slippage_pips,reb_no_orders_hit,reb_delta_hedge,reb_unhedged_delta,reb_delta_pnl,reb_total_delta_pnl,reb_option_price_change,reb_portfolio_pnl,reb_total_portfolio_pnl,reb_delta,reb_gamma,reb_theta,reb_xgamma,option_price,threshold)"

ccypairs = ["eurusd"]
tenors = ["1m"]
thresholds = [500]

for ccypair in ccypairs:
    for tenor in tenors:
        cycles_results = LoadCycles(ccypair,tenor)
        for threshold in thresholds:
            for (cycle_id, cycle_start,cycle_end) in cycles_results:
                txt_filename = "../reports/%s_%s_%s/report_%s_%s_%s.txt" % (ccypair,tenor,threshold,cycle_id,str(cycle_start),str(cycle_end))
                if not os.path.exists(txt_filename):
                    print("no ", txt_filename)
                else:
                    txt_df = LoadTxtFile(txt_filename)
                    
                    str_array = []
                    for i in txt_df.index:
                        sql_query = "INSERT INTO reb_%s_%s %s VALUES (%s,\"%s\",\"%s\",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % (ccypair,tenor, insert_into_cols, cycle_id, 
                         txt_df.ix[i,"reb_date"], txt_df.ix[i,"reb_time"], txt_df.ix[i,"reb_spot"], txt_df.ix[i,"reb_spot_chg_pips"], 
                         txt_df.ix[i,"reb_step_pips"],txt_df.ix[i,"reb_slippage_pips"],txt_df.ix[i,"reb_no_orders_hit"], 
                         txt_df.ix[i,"reb_delta_hedge"],txt_df.ix[i,"reb_unhedged_delta"],txt_df.ix[i,"reb_delta_pnl"], 
                         txt_df.ix[i,"reb_total_delta_pnl"],txt_df.ix[i,"reb_option_price_change"], 
                         txt_df.ix[i,"reb_portfolio_pnl"],txt_df.ix[i,"reb_total_portfolio_pnl"], 
                         txt_df.ix[i,"reb_delta"],txt_df.ix[i,"reb_gamma"],txt_df.ix[i,"reb_theta"],txt_df.ix[i,"reb_xgamma"], 
                         txt_df.ix[i,"option_price"],threshold)

                        str_array.append(sql_query)
                    
                    myconn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
                    mycursor = myconn.cursor()

                    for str1 in str_array:
                        mycursor.execute(str1)
                    
                    myconn.commit()
                    myconn.close()    

                        


# #load cycles

# def ConvertCycleDateIntoDateTime(cycle_date):
#     local_date = datetime.strptime(cycle_date,"%Y-%m-%d")
#     local_date = datetime(local_date.year, local_date.month, local_date.day, 10, 0, 0)
#     return local_date

# r_str = r"reb_date reb_time reb_spot reb_spot_chg reb_no_trd reb_delta_hedge reb_unhdg_delta reb_delta_pnl reb_tot_delta_pnl reb_straddle_price reb_price_chg reb_port_pnl reb_tot_port_pnl "
# r_str += r"reb_delta_imp reb_gamma_imp reb_theta_imp reb_xgamma_imp reb_new_gamma reb_new_theta reb_step reb_t_interval reb_t_notional"
# r_str += r" threshold"
# r_str = r"reb_cycle_id "+r_str

# variables_names = r_str.replace(" ",",")

# _ccypairs=["eurusd"]
# #_optiontenors = ["1m"]
# #_thresholds = [100,500,1000,2500,5000,7500,10000]

# _optiontenors = ["1w"]
# _thresholds = [100,500,1000,2500,5000,7500,10000]


# myconn = pymysql.connect(host='127.0.0.1', user='root', passwd=pass_word.var1, db=pass_word.var2)
# mycursor = myconn.cursor()

# for _ccypair in _ccypairs:
#    for _optiontenor in _optiontenors:
#       for _threshold in _thresholds:

#          results = LoadCycles(_ccypair,_optiontenor)

#          for result in results:

#             (my_cycle_id, my_cycle_start, my_cycle_end, my_minrowid, my_maxrowid) = result

#             startdate = ConvertCycleDateIntoDateTime(str(my_cycle_start))
#             enddate = ConvertCycleDateIntoDateTime(str(my_cycle_end))

#             reportfile = aux_functions.GetPath(_ccypair) + r'reports.%s.%s/report_%s_0_%s-%s.txt' % (_optiontenor, _threshold, my_cycle_id, startdate.strftime("%Y-%m-%d"),enddate.strftime("%Y-%m-%d"))

#             if not os.path.exists(reportfile):
#                 print("!!! no ", reportfile)
#             else:
#                with open(reportfile,'r') as instrf:
#                   file_lines = instrf.readlines()
#                   instrf.closed
                 
#                file_lines.pop(0)

#                prev_t_notional = 0

#                for line in file_lines:
#                   if line=="\n":
#                      break
#                   else:
#                      line=line.replace("\n","")
#                      array_to_insert = []
#                      array_to_insert.append(my_cycle_id)

#                      reb_date = line[:10].strip()
#                      reb_time = line[11:19].strip()
#                      reb_spot = line[20:26].strip()
#                      reb_spot_chg = line[28:35].strip()
#                      reb_no_trd = line[36:42].strip()
#                      reb_delta_hedge = line[50:60].strip().replace(",","")
#                      reb_unhdg_delta = line[62:72].strip().replace(",","")
#                      reb_delta_pnl = line[74:82].strip().replace(",","")
#                      reb_tot_delta_pnl = line[84:96].strip().replace(",","")
#                      reb_straddle_price = line[98:111].strip().replace(",","")
#                      reb_price_chg = line[113:121].strip().replace(",","")
#                      reb_port_pnl = line[123:130].strip().replace(",","")
#                      reb_tot_port_pnl = line[132:143].strip().replace(",","")
#                      reb_delta_imp = line[145:153].strip().replace(",","")
#                      reb_gamma_imp = line[155:163].strip().replace(",","")
#                      reb_theta_imp = line[165:173].strip().replace(",","")
#                      reb_xgamma_imp = line[175:184].strip().replace(",","")

#                      reb_new_gamma = line[186:194].strip().replace(",","")
#                      reb_new_theta = line[196:204].strip().replace(",","")
#                      reb_step=line[206:209].strip()
#                      reb_t_interval=line[211:220].strip()
#                      reb_t_notional=abs(float(reb_delta_hedge)-prev_t_notional)
#                      prev_t_notional = float(reb_delta_hedge)

#                      array_to_insert.append("\""+str(reb_date)+"\"")
#                      array_to_insert.append("\""+str(reb_time)+"\"")
#                      array_to_insert.append(reb_spot)
#                      array_to_insert.append(reb_spot_chg)
#                      array_to_insert.append(reb_no_trd)
#                      array_to_insert.append(reb_delta_hedge)
#                      array_to_insert.append(reb_unhdg_delta)
#                      array_to_insert.append(reb_delta_pnl)
#                      array_to_insert.append(reb_tot_delta_pnl)
#                      array_to_insert.append(reb_straddle_price)
#                      array_to_insert.append(reb_price_chg)
#                      array_to_insert.append(reb_port_pnl)
#                      array_to_insert.append(reb_tot_port_pnl)
#                      array_to_insert.append(reb_delta_imp)
#                      array_to_insert.append(reb_gamma_imp)
#                      array_to_insert.append(reb_theta_imp)
#                      array_to_insert.append(reb_xgamma_imp)

#                      array_to_insert.append(reb_new_gamma)
#                      array_to_insert.append(reb_new_theta)
#                      array_to_insert.append(reb_step)
#                      array_to_insert.append(reb_t_interval)
#                      array_to_insert.append(reb_t_notional)
#                      array_to_insert.append(_threshold)

#                      #print(reb_date,reb_time,reb_spot,reb_spot_chg,reb_no_trd,reb_delta_hedge,reb_unhdg_delta,reb_delta_pnl,reb_tot_delta_pnl,reb_straddle_price,reb_price_chg)
#                      #print(reb_port_pnl,reb_tot_port_pnl,reb_delta_imp,reb_gamma_imp,reb_theta_imp,reb_xgamma_imp)
#                      #print(reb_new_gamma,reb_new_theta,reb_step,reb_t_interval)

#                      for i in range(0,len(array_to_insert)):
#                         array_to_insert[i]=str(array_to_insert[i])

#                      str_to_insert = ",".join(array_to_insert)

#                      mysql_order = "insert into reb_%s_%s (%s) values (%s)" % (_ccypair,_optiontenor,variables_names,str_to_insert)
#                      mycursor.execute(mysql_order)            

#             myconn.commit()

# myconn.close()

