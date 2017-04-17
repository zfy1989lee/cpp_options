from datetime import datetime, timedelta
import calendar
import pymysql
import pass_word

_ECB_holidays_2009 = (datetime(2009,1,1),datetime(2009,4,10),datetime(2009,4,13),datetime(2009,5,1),datetime(2009,12,25))
_ECB_holidays_2010 = (datetime(2010,1,1),datetime(2010,4,2),datetime(2010,4,5))
_ECB_holidays_2011 = (datetime(2011,4,22),datetime(2011,4,25),datetime(2011,12,26))
_ECB_holidays_2012 = (datetime(2012,4,6),datetime(2012,4,9),datetime(2012,5,1),datetime(2012,12,25),datetime(2012,12,26))
_ECB_holidays_2013 = (datetime(2013,1,1),datetime(2013,3,29),datetime(2013,4,1),datetime(2013,5,1),datetime(2013,12,25),datetime(2013,12,26))
_ECB_holidays_2014 = (datetime(2014,1,1),datetime(2014,4,18),datetime(2014,4,21),datetime(2014,5,1),datetime(2014,12,25),datetime(2014,12,26))
_ECB_holidays_2015 = (datetime(2015,1,1),datetime(2015,4,3),datetime(2015,4,6),datetime(2015,5,1),datetime(2015,12,25))
_ECB_holidays_2016 = (datetime(2016,1,1),datetime(2016,3,25),datetime(2016,3,25),datetime(2016,3,28),datetime(2016,12,26))
_ECB_holidays_2017 = (datetime(2017,1,1),datetime(2017,4,14),datetime(2017,4,17),datetime(2017,5,1),datetime(2017,12,25),datetime(2017,12,26))


_US_holidays_2009 = (datetime(2009,1,1),datetime(2009,1,19),datetime(2009,2,16),datetime(2009,4,10),datetime(2009,5,25),datetime(2009,7,3),datetime(2009,9,7),datetime(2009,10,12),datetime(2009,11,11),datetime(2009,11,26),datetime(2009,12,25))
_US_holidays_2010 = (datetime(2010,1,1),datetime(2010,1,19),datetime(2010,2,15),datetime(2010,4,2),datetime(2010,5,31),datetime(2010,7,5),datetime(2010,9,6),datetime(2010,10,11),datetime(2010,11,11),datetime(2010,11,25),datetime(2010,12,24))
_US_holidays_2011 = (datetime(2011,1,17),datetime(2011,2,21),datetime(2011,4,22),datetime(2011,5,30),datetime(2011,7,4),datetime(2011,9,5),datetime(2011,10,10),datetime(2011,11,11),datetime(2011,11,24),datetime(2011,12,26))
_US_holidays_2012 = (datetime(2012,1,1),datetime(2012,1,16),datetime(2012,2,20),datetime(2012,4,6),datetime(2012,5,28),datetime(2012,7,4),datetime(2012,9,3),datetime(2012,10,8),datetime(2012,11,12),datetime(2012,11,22),datetime(2012,12,25))
_US_holidays_2013 = (datetime(2013,1,1),datetime(2013,1,21),datetime(2013,2,18),datetime(2013,5,27),datetime(2013,7,4),datetime(2013,9,2),datetime(2013,10,14),datetime(2013,11,11),datetime(2013,11,28),datetime(2013,12,25))
_US_holidays_2014 = (datetime(2014,1,1),datetime(2014,1,20),datetime(2014,2,17),datetime(2014,4,18),datetime(2014,5,26),datetime(2014,7,4),datetime(2014,9,1),datetime(2014,10,13),datetime(2014,11,11),datetime(2014,11,27),datetime(2014,12,25))
_US_holidays_2015 = (datetime(2015,1,1),datetime(2015,1,19),datetime(2015,2,16),datetime(2015,4,3),datetime(2015,5,25),datetime(2015,7,3),datetime(2015,9,8),datetime(2015,10,12),datetime(2015,11,11),datetime(2015,11,26),datetime(2015,12,25))

_US_holidays_2016 = (datetime(2016,1,1),datetime(2016,1,18),datetime(2016,2,15),datetime(2016,5,30),datetime(2016,7,4),datetime(2016,9,5),datetime(2016,10,10),datetime(2016,11,11),datetime(2016,11,24),datetime(2016,12,26))
_US_holidays_2017 = (datetime(2017,1,2),datetime(2017,1,16),datetime(2017,2,20),datetime(2017,5,29),datetime(2017,7,4),datetime(2017,9,4),datetime(2017,10,9),datetime(2017,11,10),datetime(2017,11,23),datetime(2017,12,25))


_JPY_texts_2010 = ("2010-01-01", "2010-01-11", "2010-02-11", "2010-03-21", "2010-04-29", "2010-05-03", "2010-05-04", "2010-05-05", "2010-07-19", "2010-09-20", "2010-09-23", "2010-10-11", "2010-11-03", "2010-11-23", "2010-12-23")
_JPY_texts_2011 = ("2011-01-03", "2011-01-10", "2011-02-11", "2011-03-21", "2011-04-29", "2011-05-03", "2011-05-04", "2011-05-05", "2011-07-18", "2011-09-19", "2011-09-23", "2011-10-10", "2011-11-03", "2011-11-23", "2011-12-23")
_JPY_texts_2012 = ("2012-01-01", "2012-01-09", "2012-02-11", "2012-03-20", "2012-04-30", "2012-05-03", "2012-05-04", "2012-05-05", "2012-07-16", "2012-09-17", "2012-09-24", "2012-10-08", "2012-11-03", "2012-11-23", "2012-12-24")
_JPY_texts_2013 = ("2013-01-01", "2013-01-14", "2013-02-11", "2013-03-20", "2013-04-29", "2013-05-03", "2013-05-04", "2013-05-06", "2013-07-15", "2013-09-16", "2013-09-23", "2013-10-14", "2013-11-04", "2013-11-23", "2013-12-23")
_JPY_texts_2014 = ("2014-01-01", "2014-01-13", "2014-02-11", "2014-03-21", "2014-04-29", "2014-05-03", "2014-05-05", "2014-05-06", "2014-07-21", "2014-09-15", "2014-09-23", "2014-10-13", "2014-11-03", "2014-11-24", "2014-12-23")
_JPY_texts_2015 = ("2015-01-01", "2015-01-12", "2015-02-11", "2015-03-21", "2015-04-29", "2015-05-03", "2015-05-04", "2015-05-05", "2015-05-06", "2015-07-20", "2015-09-21", "2015-09-22", "2015-09-23", "2015-10-12", "2015-11-03", "2015-11-23", "2015-12-23")

_JPY_texts = _JPY_texts_2010+_JPY_texts_2011+_JPY_texts_2012+_JPY_texts_2013+_JPY_texts_2014+_JPY_texts_2015
_JPY_hols = []

for _text in _JPY_texts:
   _JPY_hols.append(datetime.strptime(_text,"%Y-%m-%d"))

_JPY_hols = tuple(_JPY_hols)


def IsHoliday(date):
   bIsHoliday=False
   for _day in _holidays:
      if date==_day:
         bIsHoliday=True
         break
   return bIsHoliday

def CondOperator(condition,a,b):
   if(condition==True):
      return a
   else:
      return b

def GetEndDate(startdate,tenor):

   num_of_months = 1

   if(tenor=="3m"):
      num_of_months=3

   my_year = CondOperator(startdate.month<=12-num_of_months,startdate.year,startdate.year+1)
   my_month = CondOperator(startdate.month<=12-num_of_months,startdate.month+num_of_months,num_of_months-(12-startdate.month))
   lastday = calendar.monthrange(my_year, my_month)[1]

   if(startdate.day<=lastday):
      enddate = datetime(CondOperator(startdate.month<=12-num_of_months,startdate.year,startdate.year+1), CondOperator(startdate.month<=12-num_of_months,startdate.month+num_of_months,num_of_months-(12-startdate.month)),startdate.day)
   else:
      enddate = datetime(CondOperator(startdate.month<=12-num_of_months,startdate.year,startdate.year+1), CondOperator(startdate.month<=12-num_of_months,startdate.month+num_of_months,num_of_months-(12-startdate.month)),lastday)

   return enddate

def GetEndDate1W(startdate):

   lastday = calendar.monthrange(startdate.year, startdate.month)[1]

   if(startdate.day+7<=lastday):
      enddate = datetime(startdate.year,startdate.month,startdate.day+7)
   elif(startdate.month<12):
      enddate = datetime(startdate.year,startdate.month+1,7-(lastday-startdate.day))
   else:
      enddate = datetime(startdate.year+1,1,7-(lastday-startdate.day))

   return enddate


def GetNumberOfDays(start,end):
    return (int(end.strftime("%j")) - int(start.strftime("%j")) + (int(end.year)-int(start.year))*365)

_tenors = ["1w", "1m", "3m"]
_ccypair = "eurusd"

if _ccypair=="jpyusd":
   _holidays = _JPY_hols + _US_holidays_2009 + _US_holidays_2010 + _US_holidays_2011 + _US_holidays_2012 + _US_holidays_2013 + _US_holidays_2014 + _US_holidays_2015 + _US_holidays_2016 + _US_holidays_2017
elif _ccypair=="eurusd":
   _holidays = _ECB_holidays_2009 + _ECB_holidays_2010 + _ECB_holidays_2011 + _ECB_holidays_2012 + _ECB_holidays_2013 + _ECB_holidays_2014 + _ECB_holidays_2015 + _ECB_holidays_2016 + _ECB_holidays_2017 + _US_holidays_2009 + _US_holidays_2010 + _US_holidays_2011 + _US_holidays_2012 + _US_holidays_2013 + _US_holidays_2014 + _US_holidays_2015 + _US_holidays_2016 + _US_holidays_2017

conn = pymysql.connect(host='127.0.0.1', user='valery', passwd=pass_word.var1, db=pass_word.var2)
cur = conn.cursor()

for _tenor in _tenors:

   cur.execute("SELECT max(cycle_start) from %s_%s_cycles" % (_ccypair,_tenor))
   results=cur.fetchone()
   startdate=datetime(2010,1,1)

   print(results[0])

   if (results[0]!=None):
      startdate = datetime.strptime(str(results[0]),"%Y-%m-%d")
      startdate = startdate+timedelta(1)

   cur.execute("SELECT max(quotedate) from %s_new1" % (_ccypair))
   results=cur.fetchone()
   enddate = datetime.strptime(str(results[0]),"%Y-%m-%d")


   cur.execute("SELECT max(cycle_id) from %s_%s_cycles" % (_ccypair,_tenor))
   results=cur.fetchone()
   cycle_id = 1
   
   if (results[0]!=None):
      cycle_id = int(str(results[0]))+1

   tempstart = startdate
   tempdate = startdate

   if(_tenor == "1w"):
      tempend = GetEndDate1W(tempstart)
   else:
      tempend = GetEndDate(tempstart,_tenor)
      
   while((tempend.weekday()>4) or (IsHoliday(tempend))):
      tempend = tempend+timedelta(1)

   while tempend<=enddate:
      if((tempstart.weekday()<=4) and (not IsHoliday(tempstart))):
         print (cycle_id," ",tempstart," ",tempend," ",GetNumberOfDays(tempstart,tempend))
         
         query = "INSERT INTO %s_%s_cycles (cycle_id,cycle_start,cycle_end,cycle_days) VALUES (" % (_ccypair, _tenor)
         query = query+str(cycle_id)+",\'"+str(tempstart.strftime("%Y-%m-%d"))+"\',\'"+str(tempend.strftime("%Y-%m-%d"))+"\',"+str(GetNumberOfDays(tempstart,tempend))+")"
         
         print(query)
         cycle_id=cycle_id+1
         cur.execute(query)

      tempstart = tempstart+timedelta(1)
      
      if(_tenor == "1w"):
         tempend = GetEndDate1W(tempstart)
      else:
         tempend = GetEndDate(tempstart,_tenor)
      
      while((tempend.weekday()>4) or (IsHoliday(tempend))):
         tempend = tempend+timedelta(1)
      
conn.commit()
conn.close()


