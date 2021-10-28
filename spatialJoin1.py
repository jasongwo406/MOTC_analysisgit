# import essential modules
import os 
import sys
import json
import numpy as np
import requests
import pandas as pd
from os import listdir, stat
from typing import List, Dict
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
import schedule
import arcpy
from arcpy.arcobjects.arcobjects import SpatialReference

#import arcpy
#from arcpy.arcobjects.arcobjects import SpatialReference
init(convert=True)

# import main functionality
from src.Parser import GeoJsonParser
from src.dbcontext import Dbcontext
from src.requester import Requester
from src.utils import UrlBundler, Key
if __name__ == "__main__":

    # initialize dbcontext
    myDBcontext = Dbcontext({"user": "postgres", 
                            "password": "r2tadmiadc", 
                            "host": "localhost", 
                            "port": "5432"}, "motcdev")

    #Read MOH Data                        
    MOH_columns = myDBcontext.fetchColumns("Mobile_Sensor_History")
    def RoadStatistics(startDate,endDate,startTime,endTime,Region,Statistic,myExtent):
        #Select Date and time range     
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  Selecting Data start!")
        data = myDBcontext.fetchMSHData(startDate,endDate)
        L = []
        for i in range(len(data)):
            k=[]
            for j in range(len(MOH_columns)+3):
                k.append(data[i][j])
            L.append(k)
        T = []
        for i in range(len(MOH_columns)):
            T.append(MOH_columns[i][0])
        T.append("PM_Mean")
        T.append("Lon")
        T.append("Lat")
        mohRD = pd.DataFrame(L,columns=T)
        #DO or not Do the Location Search
        
        if myExtent.strip("()")=="":
            pass
            print("No Spatial Select")
        else:
            myExtent = tuple(float(s) for s in myExtent.strip("()").split(","))
            xmin = myExtent[0]
            ymin = myExtent[1]
            xMax = myExtent[2]
            yMax = myExtent[3]
            print(xmin,ymin,xMax,yMax)
            mask = (((mohRD["Lon"]>=xmin)&(mohRD["Lon"]<=xMax))&((mohRD["Lat"]>=ymin)&(mohRD["Lat"]<=yMax)))
            mohRD = mohRD[mask]

        #print(mohRD.sort_values(by="Datetime",ascending=True).head(10))
        startDateTemp = pd.to_datetime(startDate).date()
        endDateTemp = pd.to_datetime(endDate).date()
        selectedData = pd.DataFrame()
        selectDays = [(startDateTemp+timedelta(days=x)).strftime("%Y-%m-%d") for x in range((endDateTemp-startDateTemp).days+1)]
        for i in selectDays:
            temp = mohRD[(mohRD["CreatedTime"]>=i+" {}".format(startTime))&(mohRD["CreatedTime"]<=i+" {}".format(endTime))]
            selectedData = pd.concat([selectedData,temp],axis=0)
        
        selectedData["CreatedTime"] = selectedData["CreatedTime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        selectedData["Datetime"] = selectedData["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        print(selectedData.dtypes)
        in_array = selectedData.to_records()
        arcpy.env.workspace="D:\\MOTC_analysis\\"
        arcpy.env.overwriteOutput =True
        points = "D:\\MOTC_analysis\\Mypoints"
        
        #arcpy.da.NumPyArrayToFeatureClass(in_array,points,["Lon","Lat"],SpatialReference(4326))
        #selectedData.to_csv("temp1.csv")
        #os.system('"C:/Program Files/ArcGIS/Pro/bin/Python/Scripts/propy" D:\MOTC_analysis\src\spatialJoinAnalyzenew.py {} {}'.format(Region,Statistic))
    try:
        RoadStatistics(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    except Exception as e:
        print(e)
    #sys.argv[1]  開始日期 "2021-09-06"
    #sys.argy[2]  結束日期 "2021-09-10"
    #sys.argv[3]  開始時間 "00:00"
    #sys,argv[4]  結束時間 "23:59"
    #sys.argv[5]  地區路網 "TCC_Road_Split"
    #sys.argv[6]  統計方式 "Mean"
    #sys.argv[7]  空間查詢範圍   ()
