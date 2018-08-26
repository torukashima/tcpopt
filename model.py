import math
import datetime as dt
import pandas as pd

class FareTable():
    def __init__(self):
        # plan names
        plans = ['short', 'hour6', 'hour12', 'hour24', 'early', 'late', 'double']

        # fare amount
        a = {'base':[0, 4020, 6690, 8230, 2060, 2060, 2580], 
             'extra':[206, 206, 206, 206, 206, 206, 206],
             'distance':[0, 0, 16, 16, 16, 16, 16]}
        amount = pd.DataFrame(data=a, index=plans)

        # fare condition
        c = {'type':['length', 'length', 'length', 'length', 'time', 'time', 'time'],
             'length':[0, 6, 12, 24, 6, 9, 15],
             'start':['', '', '', '', 18, 0, 18],
             'by':['', '', '', '', 24, 9, 24],
             'max':[72, 6, 6, 6, 6, 6, 6]}
        condition = pd.DataFrame(data=c, index=plans)
        self.__whole = pd.concat([amount, condition], axis=1)
    
    @property
    def whole(self):
        return self.__whole
        
class FareCalculator():
    def __init__(self, start, end, distance):
        self.s = start
        self.e = end
        self.d = distance
        self.__f = FareTable()
    
    @property
    def fare_table(self):
        return self.__f.whole

    def __calc_extra(self, plan):
        fare = self.__f.whole
        if fare.at[plan, 'type'] == 'length':
            extra = self.e - self.s - dt.timedelta(
                hours=int(fare.at[plan, 'length']))
        elif fare.at[plan, 'type'] == 'time':
            plan_start = dt.datetime(year=self.s.year, 
                                     month=self.s.month, 
                                     day=self.s.day, 
                                     hour=fare.at[plan, 'start'])
            plan_end = plan_start + dt.timedelta(
                hours=int(fare.at[plan, 'length']))
            extra = self.e - plan_end
        else:
            extra = math.inf
        return max(0, math.ceil((extra.total_seconds()/3600)*4))

    def calc_fare(self, plan):
        fare = self.__f.whole
        if (fare.at[plan, 'type'] == 'time') and (
                self.s.hour < fare.at[plan, 'start'] or
                self.s.hour >= fare.at[plan, 'by']):
            return math.inf
        else:
            extra_qnum = self.__calc_extra(plan)
        if extra_qnum > fare.at[plan, 'max']*4:
            return math.inf
        else:
            return (fare.at[plan, 'base'] + 
                    fare.at[plan, 'extra'] * extra_qnum + 
                    fare.at[plan, 'distance'] * self.d)