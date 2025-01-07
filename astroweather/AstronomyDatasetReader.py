import xarray as xr
from MapProjection import MapProjection

class AstronomyDatasetReader:
    """
    Represents a reader for ECCC astronomy grib2 files

    Attributes:
        data_path: pathlib.Path
            Directory where ECCC data files are contained
        seei_files: list(pathlib.Path)
            list of Paths of the *_SEEI_* portion of the ECCC data files
        trsp_files: list(pathlib.Path)
            list of Paths of the *_TRSP_* portion of the ECCC data files
        proj: MapProjection
            MapProjection of this data set
    """

    def __init__(self, data_path):
        """
        Create an AstronomyDatasetReader object

        :param data_path: pathlib.Path
            Directroy where ECCC data files are contained
        """

        self.data_path = data_path
        self.seei_files = list(self.data_path.glob("*_SEEI_*.grib2"))
        self.trsp_files = list(self.data_path.glob("*_TRSP_*.grib2"))
        self.proj = MapProjection(self.seei_files[0])

    def get_dataset(self):
        """
        Open and process ECCC grib2 files in self.data_path
        to create a combined dataset of seeing and transparency forecast

        :return: xarray.Dataset
            Merged dataset where empty seeing values are filled in with nearest neighbor
        """

        seei_ds = xr.open_mfdataset(paths=self.seei_files,
                                    engine='cfgrib',
                                    preprocess=lambda ds: ds.rename_vars({"unknown": "Seeing"}),
                                    combine="nested",
                                    concat_dim="step",
                                    compat="broadcast_equals")
        trsp_ds = xr.open_mfdataset(paths=self.trsp_files,
                                    engine='cfgrib',
                                    preprocess=lambda ds: ds.rename_vars({"unknown": "Transparency"}),
                                    combine="nested",
                                    concat_dim="step",
                                    compat="broadcast_equals")

        ds = trsp_ds.merge(seei_ds)
        ds = self._fill_in_seeing(ds)
        ds = self.proj.add_projection(ds)
        return ds

    def _fill_in_seeing(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Fill in empty seeing values (because the ECCC forecast only produces seeing data once every three steps)

        Steps 0, 1, and 2 have seeing values filled in with step 3's data
        Steps 4 and 5 have 6's data, steps 7 and 8 have 9's data, etc.

        :param ds: dataset in which to fill in empty seeing values
        :return: dataset with filled in seeing values
        """
        for i in range(len(ds["step"])):
            if i < 3:
                ds["Seeing"][i] = ds["Seeing"][3]
            elif i % 3 != 0:
                ds["Seeing"][i] = ds["Seeing"][i + 3 - (i % 3)]
        return ds