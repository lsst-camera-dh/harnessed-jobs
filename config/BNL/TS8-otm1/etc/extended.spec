# Specification file for extended header. Taken from LCA 13501 from June 8th 2016
#
NAXIS       Integer ${NAXIS}            number of axis
NAXIS1      Integer ${NAXIS1}           size of the n'th axis
NAXIS2      Integer ${NAXIS2}           size of the n'th axis
HEADVER     Integer 1                           Version number of header
CHANNEL     Integer ${CHANNEL}
EXTNAME     String  ${EXTNAME}
CCDSUM      String  ${CCDSUM}
AVERAGE     Float   ${AVERAGE}
AVGBIAS     Float   ${AVGBIAS}
AVWOBIAS    Float   ${AVWOBIAS}
STDVBIAS    Float   ${STDVBIAS}
STDEV       Float   ${STDEV}
# Mosaic coodinate keywords
DATASEC     String  ${DATASEC}
DETSEC      String  ${DETSEC}
DETSIZE     String  ${DETSIZE}
DTV1        Integer ${DTV1}           detector transformation vector
DTV2        Integer ${DTV2}           detector transformation vector
DTM1_1      Float   ${DTM1_1}         detector transformation matrix
DTM2_2      Float   ${DTM2_2}         detector transformation matrix
DTM1_2      Float   0.0               detector transformation matrix
DTM2_1      Float   0.0               detector transformation matrix
# WCS keywords
WCSNAMEA    String  "AMPLIFIER"       Name of coordinate system                                                 
CTYPE1A     String  "Seg_X"           In the camera coordinate system                                         
CTYPE2A     String  "Seg_Y"           In the camera coordinate system                                         
PC1_1A      Float   0.0                                                  
PC1_2A      Float   ${PC1_2A}                                                  
PC2_1A      Float   ${PC2_1A}                                               
PC2_2A      Float   0.0                                                    
CDELT1A     Float   1.0
CDELT2A     Float   1.0
CRPIX1A     Float   0.0                                               
CRPIX2A     Float   0.0
CRVAL1A     Float   ${CRVAL1A}
CRVAL2A     Float   ${CRVAL2A}
WCSNAMEC    String  "CCD"             Name of coordinate system                                                 
CTYPE1C     String  "CCD_X"           In the camera coordinate system                                         
CTYPE2C     String  "CCD_Y"           In the camera coordinate system                                         
PC1_1C      Float   0.0                                                  
PC1_2C      Float   ${PC1_2C}                                                  
PC2_1C      Float   ${PC2_1C}                                               
PC2_2C      Float   0.0                                                    
CDELT1C     Float   1.0
CDELT2C     Float   1.0
CRPIX1C     Float   0.0                                               
CRPIX2C     Float   0.0
CRVAL1C     Float   ${CRVAL1C}
CRVAL2C     Float   ${CRVAL2C}
WCSNAMER    String  "RAFT"            Name of coordinate system                                                 
CTYPE1R     String  "RAFT_X"          In the camera coordinate system                                         
CTYPE2R     String  "RAFT_Y"          In the camera coordinate system                                         
PC1_1R      Float   0.0                                                  
PC1_2R      Float   ${PC1_2R}                                                  
PC2_1R      Float   ${PC2_1R}                                               
PC2_2R      Float   0.0                                                    
CDELT1R     Float   1.0
CDELT2R     Float   1.0
CRPIX1R     Float   0.0                                               
CRPIX2R     Float   0.0
CRVAL1R     Float   ${CRVAL1R}
CRVAL2R     Float   ${CRVAL2R}
WCSNAMEF    String  "FOCAL_PLANE"     Name of coordinate system                                                 
CTYPE1F     String  "FP_X"            In the camera coordinate system                                         
CTYPE2F     String  "FP_Y"            In the camera coordinate system   
PC1_1F      Float   0.0                                                  
PC1_2F      Float   ${PC1_2F}                                                  
PC2_1F      Float   ${PC2_1F}                                               
PC2_2F      Float   0.0                                                    
CDELT1F     Float   1.0
CDELT2F     Float   1.0
CRPIX1F     Float   0.0                                               
CRPIX2F     Float   0.0
CRVAL1F     Float   ${CRVAL1F}
CRVAL2F     Float   ${CRVAL2F}
WCSNAMEB    String  "CCD_SERPAR"      Name of coordinate system                                                 
CTYPE1B     String  "CCD_S"           In the serial-parallel coordinate system                                         
CTYPE2B     String  "CCD_P"           In the serial-parallel coordinate system                                         
PC1_1B      Float   ${PC1_1B}                                                  
PC1_2B      Float   0.0                                                  
PC2_1B      Float   0.0                                               
PC2_2B      Float   ${PC2_2B}                                                    
CDELT1B     Float   1.0
CDELT2B     Float   1.0
CRPIX1B     Float   0.0                                               
CRPIX2B     Float   0.0
CRVAL1B     Float   ${CRVAL1B}
CRVAL2B     Float   ${CRVAL2B}
WCSNAMEQ    String  "RAFT_SERPAR"     Name of coordinate system                                                 
CTYPE1Q     String  "RAFT_S"          In the serial-parallel coordinate system                                         
CTYPE2Q     String  "RAFT_P"          In the serial-parallel coordinate system                                         
PC1_1Q      Float   ${PC1_1Q}                                                  
PC1_2Q      Float   0.0                                                  
PC2_1Q      Float   0.0                                               
PC2_2Q      Float   ${PC2_2Q}                                                    
CDELT1Q     Float   1.0
CDELT2Q     Float   1.0
CRPIX1Q     Float   0.0                                               
CRPIX2Q     Float   0.0
CRVAL1Q     Float   ${CRVAL1Q}
CRVAL2Q     Float   ${CRVAL2Q}
