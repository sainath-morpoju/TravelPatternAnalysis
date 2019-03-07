import pandas as pd
import xlrd
from geopy.distance import great_circle
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from decimal import *


class DistanceCalculator():
    def __init__(self, homeLocation = None, path = "C:/Users/saina/Documents/sample/test/data/sensorDataSelf.xlsx", distance_margin = 0.10 ):
        # read the file
        self.dataframe = pd.read_excel(path,header = 0).filter(items =['locLat','locLon','collectedTimeStamp'])
    #    self.dataframe = self.dataframe[self.dataframe['locLat'] != "None"]
        #print(dataframe.sample())
        self.dist_margin = distance_margin
        self.mean = homeLocation
        self.startPt = homeLocation
        self.distanceMap = {}
        self.totalDayDistanceMap = {}
        self._daySelector_()

    def _haversinedistance_(self,item):
        dval = great_circle([self.startPt[0],self.startPt[1]],[item[0],item[1]])
        startPt = item
        if dval.miles < self.dist_margin and great_circle([self.startPt[0],self.startPt[1]],[self.mean[0],self.mean[1]]).miles < self.dist_margin:
            return None
        return dval.miles

    def _daySelector_(self):
        days = self.dataframe["collectedTimeStamp"].map(lambda t: t.date()).unique()
        # print(days)

        for day in days:
            self.distanceMap[day] = []
            filtered_df = self.dataframe.loc[self.dataframe["collectedTimeStamp"].map(lambda t: t.date()) == day]
            for indx,record in filtered_df.iterrows():
                dayDistVal = self._haversinedistance_(record)
                if dayDistVal is not None :
                    self.distanceMap[day].append(dayDistVal)
            self.startPt = self.mean

        print("the distance map per day is: ")
        # print(self.distanceMap)
        for key,value in self.distanceMap.items():
            print (str(key),':',list(value))

        print('distance map end')
        self._totalDistanceCal_()

    def _totalDistanceCal_(self):
        # totalDayDistanceMap = {}
        for day in self.distanceMap.keys():
            # if len(dc.distanceMap.get(day)) != 0:
            self.totalDayDistanceMap[day] = np.sum(self.distanceMap.get(day))

        print("the total distance map per day is:")

        for key,value in self.totalDayDistanceMap.items():
            print (str(key),':',value)

        print('total distance map end')
        print('mean travelled distance per day is: ')
        print(np.mean(list(self.totalDayDistanceMap.values())))
        # print(str(totalDayDistanceMap.keys()))
        # print(totalDayDistanceMap.values())
        # print(totalDayDistanceMap)
        # print(str(totalDayDistanceMap.keys()))
        self._plot_()



    def _plot_(self):
        y_values = list(self.totalDayDistanceMap.values())
        x_values = list(self.totalDayDistanceMap.keys())

        # fig, ax = plt.subplots()

        plt.barh(range(len(x_values)), y_values)
        plt.yticks(range(len(x_values)), x_values)
        # plt.xticks(range(len(y_values)), y_values)
        plt.ylabel('Days')
        plt.title('Travel Pattern')
        plt.xlabel('Total Distance in Miles')

        for i, v in enumerate(y_values):
            plt.text(v, i, " "+str(Decimal(v).quantize(Decimal((0, (1,), -2)), rounding=ROUND_DOWN)), color='blue', va='center')
        #     Decimal(v).quantize(Decimal((0, (1,), -2)), rounding=ROUND_DOWN)
        plt.show()

if __name__ == "__main__":
    DistanceCalculator(homeLocation=[29.6899146011189,-82.3379786107599])



