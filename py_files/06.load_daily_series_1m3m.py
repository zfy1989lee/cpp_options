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
tenors = ["3m"]
thresholds = [100,500,1000,2500,5000]

divider = 20

dates = []
years = []
yearly_sharpe_df = []

for i in range(2010,2018):
    dates.append(datetime(i,1,1).date())
    years.append(i)

reportdir = "../daily_returns";
if not os.path.exists(reportdir):
    os.makedirs(reportdir)

for ccypair in ccypairs:
    for tenor in tenors:

        if(tenor=="1m"):
            divider = 20
        elif(tenor=="3m"):
            divider = 60

        weekdays = range(0,divider)
        weekdaysL = []
        for w in weekdays:
            weekdaysL.append(str(w)+"s")

        column_names = []
        column_tnames = []

        for threshold in thresholds:
            for weekdayL in weekdaysL:
                column_names.append(weekdayL+str(threshold))
                column_tnames.append("t"+weekdayL+str(threshold))

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

                mysql_order02 = r"select reb_date, reb_portfolio_pnl from reb_%s_%s where threshold=%s and reb_cycle_id %s order by reb_date" % (ccypair,tenor,threshold,"%"+str(divider)+"="+str(weekday))

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
