# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 13:17:05 2016

@author: kachharaa
"""


## the script works only on one shape file at a time. A pre-step of split the shapefile by 'FID' is required. I usually do it in qgis  because of license unavailability to use 'split' tool in ARCGIS (or arcpy).


import sys
sys.path.append('')
sys.path.append(u'c:\\program files (x86)\\arcgis\\desktop10.3\\arcpy') 
sys.path.append('C:\\Python27\\ArcGISx6410.3\\Lib\\site-packages\\arcpy')
sys.path.append('C:\\Windows\\system32\\python27.zip')
sys.path.append('C:\\Users\\kachharaa\\AppData\\Local\\Continuum\\Anaconda2\\Lib') 
sys.path.append('C:\\Users\\kachharaa\\AppData\\Local\\Continuum\\Anaconda2\\DLLs')
sys.path.append('C:\\Anaconda2\\Lib')
sys.path.append('C:\\Anaconda2\\DLLs')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\bin')
sys.path.append('C:\\Anaconda2') 
sys.path.append('C:\\Anaconda2\\lib\\site-packages') 
sys.path.append('C:\\Anaconda2\\lib\\site-packages\\Sphinx-1.4.1-py2.7.egg')
sys.path.append('C:\\Anaconda2\\lib\\site-packages\\win32')
sys.path.append('C:\\Anaconda2\\lib\\site-packages\\win32\\lib') 
sys.path.append('C:\\Anaconda2\\lib\\site-packages\\Pythonwin')
sys.path.append('C:\\Anaconda2\\lib\\site-packages\\setuptools-23.0.0-py2.7.egg')


# Import arcpy module
import arcpy, glob, os


## Checking out all the required extensions
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("Network")
arcpy.CheckOutExtension("GeoStats")
arcpy.env.overwriteOutput = True


##############################################################################################################################
## read ONLY the shapefile

arcpy.env.workspace = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\Port\portsplit_subset2"
files = glob.glob("H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\Port\portsplit_subset2\*.shp") 


#running the skyline function on each point file separately.

#AKL_CBD_Raster = r'H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCK_RASTER.gdb\AKL_BLDG_raster'

i = 0
# set local variables
inRaster = r'H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCK_RASTER.gdb\AKL_BLDG_raster'


analysisType = "OBSERVERS"
nonVisibleValue = "ZERO"


for file in files:
    name = file                
    parts = name.split('_')      
    newname = parts[8]
    final = newname.split('.')
    FID = final[0]
    
    outvis = arcpy.sa.Visibility(in_raster = inRaster, in_observer_features = file, 
                                 analysis_type = "OBSERVERS", observer_elevation = "Elevation")
                            
    #output_location1 = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\Port\Visibility_rasters.gdb\Visibility_raster_subset2_" + FID
    output_location2 = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\Port\Visibility_rasters_subset2.gdb\Visibility_raster_" + FID
    #outvis.save(output_location1)
    outvis.save(output_location2)
    ## creating a unique name extension for each skyline shape output file based on its feature ID.    
    
    i = i+1
    print FID+ "FID"
    
   
print "done"


##Summation of all the rasters


dataPath = 'H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\Port\Visibility_rasters_subset2.gdb'
outPath = 'H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCK_RASTER.gdb'

# change the environment setting to be overwritten
arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('Spatial')      # package needed for the arcpy.raster() tool

arcpy.env.scratchWorkspace = outPath
arcpy.env.workspace = dataPath
#create a list of rasters in the workspace
rasters = arcpy.ListRasters('','')

i = 0
#loop through rasters in list
for raster in rasters:
    print "processing raster: %s" %os.path.join(dataPath,raster)

   
    out1 = raster   # to avoid overwriting the raster file

    #sum rasters together
    if i == 0:
        out2 = arcpy.Raster(out1)
        i += 1
    else:
        out2 = out2 + out1
        i += 1

#save final output
out2.save(os.path.join(outPath,'SumOfSubset2_visibilityrasters'))