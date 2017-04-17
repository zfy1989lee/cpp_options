import pymysql
import pass_word
import pandas as pd
import numpy as np

cols = ["Date","EURv1w","EURf1w","EURv1m","EURf1m","EURv3m","EURf3m"]
volfwdpts_df = pd.read_csv("vol_fwdpts.txt",parse_dates=True,skiprows=1,infer_datetime_format=True,sep=",",names=cols,index_col="Date", na_values="N/A")

ccypair = "eurusd"
tenor = "3m"

midtobid = 0
fwdptsmult = 0

if(tenor=="1w"):
   midtobid = 0.40
elif((tenor=="1m")or(tenor=="3m")):
   midtobid = 0.15

if(ccypair=="eurusd"):
   fwdptsmult=10000
elif(ccypair=="usdjpy"):
   fwdptsmult=100

#1w b/o	0.55 // 0.80
#1m b/o	0.20 // 0.30
#3m b/o	0.20 // 0.30

conn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
cur = conn.cursor()

cur.execute("SELECT cycle_id, cycle_start from %s_%s_cycles where (vol_bid IS NULL or fwd_pts is NULL) order by cycle_id;" % (ccypair, tenor))
results=cur.fetchall()

for result in results:
   (cycle_id, cycle_start) = result
   if(str(cycle_start) in volfwdpts_df.index):
      if((not np.isnan(volfwdpts_df.ix[cycle_start,"EURv"+tenor])) and (not np.isnan(volfwdpts_df.ix[cycle_start,"EURf"+tenor]))):
         volbid = volfwdpts_df.ix[cycle_start,"EURv"+tenor]-midtobid
         fwdpts = volfwdpts_df.ix[cycle_start,"EURf"+tenor]/fwdptsmult
         print(cycle_id," vol = ",volbid, "fwdpts = ",fwdpts)
         query = r"UPDATE %s_%s_cycles set vol_bid=%s, fwd_pts=%s where cycle_id=%s;" % (ccypair,tenor,volbid,fwdpts,cycle_id)
         print(query)
         cur.execute(query)

conn.commit()

cur.execute("SELECT a.cycle_id, a.cycle_start, a.fwd_pts, b.m_minrowid from %s_%s_cycles as a, eurusd_date_mapping as b where a.cycle_start=b.m_date and a.starting_spot IS NULL and (not a.fwd_pts is null) order by a.cycle_id;" % (ccypair, tenor))
results=cur.fetchall()

for result in results:
   (cycle_id, cycle_start, fwd_pts, minrowid) = result
   sql_query = "SELECT quotebid, quoteoffer from %s_new1 where quotedate='%s' and quotetime>='10:00:00' and rowid>=%s order by rowid limit 1;" % (ccypair,str(cycle_start),minrowid)
   cur.execute(sql_query)
   results2 = cur.fetchone();
   spot = round((results2[0]+results2[1])*0.5,6)
   strike = round(spot+float(fwd_pts),6)

   sql_query = "UPDATE %s_%s_cycles set starting_spot=%s, strike=%s where cycle_id=%s;" % (ccypair,tenor,spot,strike,cycle_id)
   print(sql_query)
   cur.execute(sql_query)

conn.commit()

conn.close()
