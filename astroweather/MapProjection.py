import xarray as xr
import numpy as np
from pyproj import CRS, Transformer
import rasterio

class MapProjection:
    """
    A class that represents a CRS and that can add projection info into datasets using that CRS

    Attributes
    ----------
    wkt: str
        WKT1 string
    transformer: pyproj.Transformer
        Transformer from lat/lon (geodetic CRS) to this CRS
        Transformer.always_xy is set to True

    """
    def __init__(self, grib_path):
        """
        Create a new MapProjection with CRS obtained from grib2 file
        :param grib_path: path to a grib 2 file
        """
        # gdal library does not support context manager AKA try-with-resource
        with rasterio.open(grib_path) as f:
            self.wkt = f.crs.wkt

        crs = CRS.from_wkt(self.wkt)
        self.transformer = Transformer.from_crs(crs.geodetic_crs, crs, always_xy=True)
        self.vect_transform = np.vectorize(pyfunc=lambda x, y: self.transformer.transform(xx=x, yy=y),
                                            doc="""Vectorized `self.transformer.transform`""")


    def add_projection(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Modify the x and y coordinates of a dataset to include projection information from this CRS

        :param ds: xarray.dataset to add projection into
        :return: new xarray.dataset where x and y coordinates have projection added
        """
        grid_y = ds.isel(x=0)
        grid_x = ds.isel(y=0)

        _, proj_y = self.vect_transform(grid_y.longitude, grid_y.latitude)
        proj_x, _ = self.vect_transform(grid_x.longitude, grid_x.latitude)

        ds["x"] = proj_x
        ds["y"] = proj_y
        return ds