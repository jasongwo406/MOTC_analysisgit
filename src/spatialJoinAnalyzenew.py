#import modules
import datetime
import sys
import os
import arcpy
from arcpy.arcobjects.arcobjects import SpatialReference

arcpy.env.workspace="D:\\MOTC_analysis"
arcpy.env.overwriteOutput =True

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  Arcpy imported \n")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  Analysis start!")

# Read CSV and XYTableToPoint
try:
     myfile = "\\temp1.csv"
     out_feature_class = "TableToPnt"
     x_coor = "Lon"
     y_coor = "Lat"
     arcpy.management.XYTableToPoint(myfile,"memory\\"+out_feature_class,x_coor,y_coor,coordinate_system =SpatialReference(4326))
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  Table to points done!")
except Exception as e:
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Failed to turn the mobile data to points!")
     print(e)
     sys.exit(1)
#Select roads by MOT pnts' location within 10 meters
try:
     Road_path = "D:\\MOTC_analysis\\Split_Roads\\" 
     Road_file = sys.argv[1]+".shp"
     Road = os.path.join(Road_path,Road_file)
     arcpy.MakeFeatureLayer_management(Road,'Road_Lyr')
     arcpy.MakeFeatureLayer_management("memory\\"+out_feature_class,"Pnt_Lyr")
     arcpy.management.SelectLayerByLocation("Road_Lyr", "INTERSECT", "Pnt_Lyr", "10 Meters", "NEW_SELECTION", "NOT_INVERT")
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"  Select Roads done!")
except Exception as e:
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Failed to Select Roads around the MOT data!")
     print(e)
     sys.exit(1)
#Spatial Join
try:
     PM25_RSJ = ("spatial_join_file")
     statisticMethod = sys.argv[2]
     #Calculate for PM2.5 Statistic
     arcpy.analysis.SpatialJoin("Road_Lyr", "Pnt_Lyr", PM25_RSJ, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'ROADNAME "ROADNAME" true true false 36 Text 0 0,First,#,Road_Lyr,ROADNAME,0,36;RDNAMESECT "RDNAMESECT" true true false 8 Text 0 0,First,#,Road_Lyr,RDNAMESECT,0,8;RDNAMELANE "RDNAMELANE" true true false 20 Text 0 0,First,#,Road_Lyr,RDNAMELANE,0,20;RDNAMENON "RDNAMENON" true true false 16 Text 0 0,First,#,Road_Lyr,RDNAMENON,0,16;Datetime "Datetime" true true false 8 Date 0 0,First,#,Pnt_Lyr,Datetime,-1,-1;Voc "Voc" true true false 19 Double 0 0,{},#,Pnt_Lyr,Voc,-1,-1;Flow "Flow" true true false 19 Double 0 0,{},#,Pnt_Lyr,Flow,-1,-1;Pm2_5_UART "Pm2_5_UART" true true false 19 Double 0 0,{},#,Pnt_Lyr,Pm2_5_UART,-1,-1;Pm2_5_I2C "Pm2_5_I2C" true true false 19 Double 0 0,{},#,Pnt_Lyr,Pm2_5_I2C,-1,-1;Temperatur "Temperatur" true true false 19 Double 0 0,{},#,Pnt_Lyr,Temperatur,-1,-1;Humidity "Humidity" true true false 19 Double 0 0,{},#,Pnt_Lyr,Humidity,-1,-1;Speed "Speed" true true false 19 Double 0 0,{},#,Pnt_Lyr,Speed,-1,-1;PM_Mean "PM_Mean" true true false 19 Double 0 0,{},#,Pnt_Lyr,PM_Mean,-1,-1'.format(staticmethod,staticmethod,staticmethod,staticmethod,staticmethod,staticmethod,staticmethod,staticmethod), "INTERSECT", "10 Meters", '')
     #Clear Selected features
     arcpy.SelectLayerByAttribute_management('Road_Lyr',"Clear_Selection")
     
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"+" Spatial Joined done!"))
except Exception as e:
     print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Failed to Spatial Join the MOT data to Roads!")
     print(e)
     sys.exit(1)
#FeaturesToJSON
try:
     dir = r"C:\inetpub\wwwroot\MOT\wwwroot\Contents"
     arcpy.conversion.FeaturesToJSON(PM25_RSJ+".shp",os.path.join(dir,(PM25_RSJ)),format_json=True,geoJSON=True,outputToWGS84=True)
     if os.path.exists(os.path.join(dir,(PM25_RSJ))+".json"):         
          os.remove(os.path.join(dir,(PM25_RSJ))+".json")
     os.rename(os.path.join(dir,(PM25_RSJ))+".geojson",os.path.join(dir,(PM25_RSJ))+".json")
     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'+"  FeaturesTogeoJson finished!"))
except Exception as e:
     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'+"  Failed to export to geojson!"))
     print(e)
     sys.exit(1)
     """
     with open(os.path.join(dir,(PM25_RSJ+".json")),'w'):
          pass
     """