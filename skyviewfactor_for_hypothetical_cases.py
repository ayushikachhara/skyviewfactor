# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 09:07:15 2016

@author: kachharaa
"""


## importing libraries necessary to import arcpy

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
import arcpy, glob


## Checking out all the required extensions
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("Network")
arcpy.CheckOutExtension("GeoStats")
arcpy.env.overwriteOutput = True

############################-------------------------------------------------------------------------------#######################################

# model 1: Point elevation
AKL_CBD_Raster = r'H:\AQUARIUS\Hypothetical\Hypothetical_simple\working_hypothetical.gdb\AKL_BLDG_raster'
Elev_sitemaster = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCKLAND_NORTH.shp"
Elev_sitemaster2 = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCKLAND_NORTH_rasteradded.shp"
Elev_site3Dmaster = "H:\AQUARIUS\Hypothetical\AUCKLAND_NORTH\AUCKLAND_NORTH_3D.shp"

# Process: Extract Values to Points
arcpy.gp.ExtractValuesToPoints_sa(Elev_sitemaster, AKL_CBD_Raster, Elev_sitemaster2, "INTERPOLATE", "VALUE_ONLY")
# Process: Add Field
#arcpy.AddField_management(Elev_sitemaster2, "Elevation", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(Elev_sitemaster2, "ElevationFINAL", "[RASTERVALU]+2", "VB", "")

# Process: Feature To 3D By Attribute
arcpy.FeatureTo3DByAttribute_3d(Elev_sitemaster2, Elev_site3Dmaster, "ElevationFINAL", "")


# Split vector layer on FID - for quick analysis I split the entire file. It also helps me understand immediately if anything is going wrong with the execution.
## arcpy.Split_analysis()
########## ------------------------------------------------------------------------------- ##############

# model 2: building elevation

# Input and output variable definition
Bldg_footprint = "H:\AQUARIUS\Hypothetical\Hypothetical_simple\BLDG_c25b16.shp"
Bldg3D ="H:\AQUARIUS\Hypothetical\Hypothetical_simple\BLDG_c25b16_3D.shp"

# Process: Add Field
arcpy.AddField_management(Bldg_footprint, "Z", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(Bldg_footprint, "Z", "16", "VB", "")

# Process: Feature To 3D By Attribute
arcpy.FeatureTo3DByAttribute_3d(Bldg_footprint, Bldg3D, "Z","")

#############################-------------------------------------------------------------------------------#################################################




# model 3: Skyline iterator
# Local variables used in the skyline function:

#arcpy.env.workspace = r'H:\AQUARIUS\Hypothetical\Hypothetical_simple\working_hypothetical.gdb\'

#ALL_rasters = arcpy.Raster()  ##raster
inSurface = r'H:\AQUARIUS\Hypothetical\Hypothetical_simple\working_hypothetical.gdb\AKL_BLDG_raster'

#obstructionFCs = "H:\AQUARIUS\Hypothetical\Hypothetical_simple\BLDG_c25b16_pointfile_3D.shp"
surfRad = "1000 meters"
surfElev = "0 meters"
LOD = "FULL_DETAIL"
fromAzim = 0
toAzim = 360
incAzim = 2
maxHorizRad = 1000
segSky = "NO_SEGMENT_SKYLINE"
scale = 100
scaleAcc = "VERTICAL_ANGLE"
scaleMethod = "SKYLINE_MAXIMUM"


## importing all the .shp files using glob module

##NOTE: I have split my "centreline points" shapefile based on feature ID for easy for-loop running of the function over each feature point. 
##It thus produces more than one output for each feature (100 in this case) which I merge later for further analysis
arcpy.env.workspace = 'H:\AQUARIUS\Hypothetical\Artificial_centrelinepoints'
files = glob.glob("H:\AQUARIUS\Hypothetical\Artificial_centrelinepoints\*.shp")      ## read ONLY the shapefiles
#Output_Folder = "H:\AQUARIUS\Hypothetical\Hypothetical_simple\skylineangles_rasterbased"
i = 0
#running the skyline function on each point file separately.

for file in files:

    ## creating a unique name extension for each skyline shape output file based on its feature ID.    
    name = file                
    parts = name.split('_')      
    newname = parts[7]
    final = newname.split('.')
    FID = final[0]
    
    
    ## definiing the output layer location and name based on their feature ID.
    output_layer = "H:\AQUARIUS\Hypothetical\skylineshapes_vicpark\Skyline_" + FID + ".shp"
    output_angle = "H:\AQUARIUS\Hypothetical\skylineangles_vicpark\Skyline_" + FID + ".dbf"
    
    arcpy.Skyline_3d(file, output_layer, inSurface, azimuth_increment_value_or_field= incAzim)
    
    arcpy.SkylineGraph_3d(file, output_layer, "0", "ADDITIONAL_FIELDS", output_angle)
    i = i+1
   
print "done"

