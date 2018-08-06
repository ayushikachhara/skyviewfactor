library("data.table")
library("foreign")
library("NISTunits")

setwd("H:/AQUARIUS/Hypothetical/Wellington/WLG_NORTH/skylineangles")

path = "H:/AQUARIUS/Hypothetical/Wellington/WLG_NORTH/skylineangles/"

fileName <- list.files(path = paste0(path,"/"), ".dbf")
fileName <- fileName[seq_along(fileName) %% 2 > 0]
f1 <- read.dbf(paste0(path,"/",fileName[1]))
files <- data.frame()
final_output <- data.table()

for (i in 1:length(fileName)){
  files <- read.dbf(paste0(path,"/",fileName[i]))
  files <- files[order(files$HORIZ_ANG),]
  files$ElevationAngle <- 90- (files$ZENITH_ANG)
  files$Elev_angle_radians <- NISTdegTOradian(files$ElevationAngle)
  files$ElevAngleCheck <- acos(files$DIST_2D/files$DIST_3D)
  
  files$AzimuthSlice <-  c(NA, abs(diff(files$HORIZ_ANG, 1)))
  
  files$WallView <-(files$AzimuthSlice/360)* ((sin(files$Elev_angle_radians))*(sin(files$Elev_angle_radians)))
  
  Skyviewfactor <- 1.000 - sum(files$WallView, na.rm = T)
  
  Wallview_sumtable <- as.data.table(cbind(fileName[i], sum(files$WallView, na.rm = T), Skyviewfactor))
  FID <- unlist(strsplit(fileName[i], "Skyline"))[2]
  FID <- unlist(strsplit(FID, ".dbf"))
  FID <- unlist(strsplit(FID, "_"))[2]
  Wallview_sumtable$FID <- unlist(strsplit(FID, ".dbf"))
  
  final_output<- rbind(final_output,Wallview_sumtable)
}

names(final_output) <- c("Skyline_name","wallview","skyview","FID")
final_output$skyview <- as.numeric(final_output$skyview)
final_output$FID <- as.numeric(final_output$FID)

write.csv(final_output, "H:/AQUARIUS/Hypothetical/Wellington//SVF_WellingtonNorth.csv")





### tests

f1 <- fileName[13]
f2 <- fileName[21]
f1 <-read.dbf(f1)
f2 <- read.dbf(f2)
