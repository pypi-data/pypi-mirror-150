import argparse
import SimpleITK as sitk
import os
import tempfile


import p3dpkg.p3d_SITK_common_lib
from p3dpkg.p3d_SITK_common_lib import *
from p3dpkg.p3d_SITK_common_lib_16bit.py import *


import p3dpkg.p3d_SITK_read_raw
from p3dpkg.p3d_SITK_read_raw import *

import p3dpkg.p3dFiltPy
from p3dpkg.p3dFiltPy import py_p3dReadRaw8,py_p3dWriteRaw8

import p3dpkg.p3dFiltPy_16bit
from p3dpkg.p3dFiltPy_16bit import py_p3dReadRaw16,py_p3dWriteRaw16


"""

import p3d_SITK_common_lib
from p3d_SITK_common_lib import *

import p3d_SITK_read_raw
from p3d_SITK_read_raw import *

import p3dFiltPy
from p3dFiltPy import py_p3dReadRaw8,py_p3dWriteRaw8,py_p3dReadRaw16,py_p3dWriteRaw16
"""

########################################## Filters ##########################################


def py_p3d_SITK_Median_16(img, dimx,dimy,dimz, kWidth = 1):
    #img = p3d_to_sitk_file_format(img, dimx,dimy,dimz)
    median_filter = sitk.MedianImageFilter()
    median_filter.SetRadius(kWidth)
    outImg = median_filter.Execute(img)   
    #outImg = sitk_to_p3d_file_format (outImg, dimx,dimy,dimz)
    return outImg



###### sitk_WatershedSegmentation_16
def py_p3d_WatershedSegmentation_16(input_raw_file, output_raw_file, dimx, dimy, dimz = 0, level = 0, markWatershedLine = False, connected = False): 
	"""
 
  The sitk::CurvatureFlowImageFilter performs edge-preserving smoothing applying a variant of the curvature flow algorithm where  diffusion is turned on or off depending on the scale of the noise.
 
 The minimum-maximum variant of the curvature flow filter results in sharper edges than the application with the simple  curvature flow with similar parametrization.
 
  Syntax:
  ------
  Result = py_p3d_MinMaxCurvatureFlowImageFilter ( input_image, dimx, dimy[ , dimz ] [, iterations = value ] [, width = value] )
  
  Return Value:
  ------------
  Returns a filtered image with the same dimensions and type of input imaged.                 
  
  Arguments:
  ---------
  input_raw_file: The full file name (path, name without extension) of the input 16-bit raw image
  
  output_raw_file: The full file name (path, name without extension) of the output raw image
 
  dimx,dimy,dimz: three variables representing the dimensions of image to read. 
 
  iterations: A decimal value greater than 0 (default: 3.0) representing the standard deviation of the domain gaussian.
 
  width: A decimal value greater than 0 (default: 3.0) representing the standard deviation of the domain gaussian.
 
	""" 
	#input_image =  p3d_to_sitk_file_format_16(input_image, dimx,dimy,dimz)
	in_file = input_raw_file+ '.raw'
	Img = Read_Raw16(in_file, [dimx,dimy,dimz])
	Filter = sitk.MorphologicalWatershedImageFilter() 
	Filter.SetFullyConnected(connected)
	Filter.SetLevel(level)
	Filter.SetMarkWatershedLine(markWatershedLine)
        
	Img = Filter.Execute(Img)
	#outImg = apply_rescaler(outImg, dimx,dimy,dimz)
	#Img = sitk_to_p3d_file_format_16(Img, dimx,dimy,dimz)
	out_file = output_raw_file + '.mhd'
	sitk.WriteImage(Img,out_file)
	os.remove(out_file)
	return Img


#FUNCTION        P3DCONFIDENCEREGIONGROWING				1       1   KEYWORD#S