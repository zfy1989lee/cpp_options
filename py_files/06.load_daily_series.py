from datetime import datetime, timedelta
import pymysql
import os.path
import pass_word
import pandas as pd
import numpy as np
from math import sqrt

#load cycles
def LoadCyclesThatStartOnGivenWeekday(ccypair, optiontenor, weekday):
    
    myconn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
    mycursor = myconn.cursor()
    mysql_order = r"select cycle_id, cycle_start, cycle_end from %s_%s_cycles where dayofweek(cycle_start)=%s order by cycle_id" %(ccypair,optiontenor,weekday)
    mycursor.execute(mysql_order)
    myconn.commit()
    results = mycursor.fetchall()
    myconn.close()    
    return results

ccypairs = ["eurusd"]
tenors = ["1w"]
thresholds = [100,500,1000]
weekdaysL = ["Mon", "Tue", "Wed", "Thu", "Fri"]
weekdays = range(2,2+len(weekdaysL))

column_names = []
column_tnames = []

dates = []
years = []
yearly_sharpe_df = []

for i in range(2010,2018):
    dates.append(datetime(i,1,1).date())
    years.append(i)

for threshold in thresholds:
    for weekdayL in weekdaysL:
        column_names.append(weekdayL+str(threshold))
        column_tnames.append("t"+weekdayL+str(threshold))

reportdir = "../daily_returns";
if not os.path.exists(reportdir):
    os.makedirs(reportdir)

for ccypair in ccypairs:
    for tenor in tenors:
        mysql_order01 = r"select distinct(reb_date) from reb_%s_%s order by reb_date" % (ccypair,tenor)
        myconn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
        mycursor = myconn.cursor()
        mycursor.execute(mysql_order01)
        myconn.commit()
        results = mycursor.fetchall()
        myconn.close()

        index_values = []
        for res in results:
            index_values.append(res[0])

        results_df = pd.DataFrame(0.0,columns=column_names+column_tnames,index=index_values)
        sharpe_df = pd.DataFrame(0.0,columns=thresholds,index=weekdaysL)
        for i in range(0,len(dates)-1):
            yearly_sharpe_df.append(pd.DataFrame(0.0,columns=thresholds,index=weekdaysL))
        
        del results

        for threshold in thresholds:
            for i in range(0,len(weekdays)):
                weekday = weekdays[i]
                weekdayL = weekdaysL[i]
                       
                print("analyzing: ",ccypair,tenor,threshold,weekday)

                mysql_order02 = r"select a.reb_date, a.reb_portfolio_pnl from reb_%s_%s a, %s_%s_cycles b where a.threshold=%s and a.reb_cycle_id = b.cycle_id and dayofweek(b.cycle_start)=%s order by a.reb_date" % (ccypair, tenor,ccypair,tenor,threshold,weekday)

                myconn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
                mycursor = myconn.cursor()
                mycursor.execute(mysql_order02)
                myconn.commit()
                results = mycursor.fetchall()
                myconn.close()
                print("total volume: ",len(results))

                for (my_date,my_pnl) in results:
                    results_df.ix[my_date,weekdayL+str(threshold)]+=my_pnl

        for col in column_names:
            results_df["t"+col]=results_df[col].cumsum()
            
        for threshold in thresholds:
            for weekdayL in weekdaysL:
                sharpe_df.ix[weekdayL,threshold]=sqrt(250)*results_df[weekdayL+str(threshold)].mean()/results_df[weekdayL+str(threshold)].std()
                for j in range(0,len(yearly_sharpe_df)):
                    yearly_sharpe_df[j].ix[weekdayL,threshold]=sqrt(250)*results_df.ix[dates[j]:dates[j+1],weekdayL+str(threshold)].mean()/results_df.ix[dates[j]:dates[j+1],weekdayL+str(threshold)].std()

        sharpe_df = sharpe_df.round(4)
        for j in range(0,len(yearly_sharpe_df)):
            yearly_sharpe_df[j] = yearly_sharpe_df[j].round(4)
        
        reportfile = reportdir+r"/daily_%s_%s.txt" % (ccypair,tenor)

        reportf = open(reportfile,'w')
        reportf.write(results_df.to_string())
        reportf.close()

        sharpefile = reportdir+r"/sharpe_%s_%s.txt" % (ccypair,tenor)
        reportf = open(sharpefile,'w')
        reportf.write(sharpe_df.to_string())

        for j in range(0,len(yearly_sharpe_df)):
            reportf.write("\n\n"+str(years[j])+" to "+str(years[j+1])+"\n")
            reportf.write(yearly_sharpe_df[j].to_string())

        reportf.close()
