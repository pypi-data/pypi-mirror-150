from paradoxdjango.contrib.gis.gdal.error import GDALException
from paradoxdjango.contrib.gis.ptr import CPointerBase


class GDALBase(CPointerBase):
    null_ptr_exception_class = GDALException
