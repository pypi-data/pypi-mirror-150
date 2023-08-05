
import p3dpkg.p3d_SITK_read_raw
from p3dpkg.p3d_SITK_read_raw import *

import p3dpkg.p3dFiltPy
from p3dpkg.p3dFiltPy import py_p3dReadRaw8,py_p3dWriteRaw8,py_p3dReadRaw16,py_p3dWriteRaw16
"""

import p3d_SITK_read_raw
from p3d_SITK_read_raw import *

import p3dFiltPy
from p3dFiltPy import py_p3dReadRaw8,py_p3dWriteRaw8,py_p3dReadRaw16,py_p3dWriteRaw16
"""

###### common 16 bit
def sitk_to_p3d_file_format_16 (sitk_image, dimx,dimy,dimz):
    sitk.WriteImage(sitk_image , "tempMeta.mhd")
    im_P3D_format_out = py_p3dReadRaw16( 'tempMeta.raw', dimx,dimy,dimz)
    os.remove('tempMeta.raw')
    return im_P3D_format_out

def p3d_to_sitk_file_format_16(p3d_image, dimx,dimy,dimz):
    im_SITK_format_out = py_p3dWriteRaw16( p3d_image, 'tempOutMeta.raw',dimx,dimy,dimz)
    im_SITK_format_out = Read_Raw16("tempOutMeta.raw", [dimx,dimy,dimz])
    os.remove('tempOutMeta.raw')
    return im_SITK_format_out
  

