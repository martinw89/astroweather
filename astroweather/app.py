import xarray as xr
from AstronomyDatasetReader import AstronomyDatasetReader
from pathlib import Path
from litestar import Litestar, get

astro_data_reader = AstronomyDatasetReader(Path('../demo_data/'))
ds = astro_data_reader.get_dataset()
# Sacrifice a little memory to speed up indexing time 256%
ds = ds.load()

@get("/", include_in_schema=False)
async def index() -> str:
    return "See /schema/swagger for API information"

@get("/api/forecast/")
async def get_forecast(lat: float, lon: float) -> dict["str", list[int]]:
    nearest_point = _select_forecast(lat, lon)
    return {"Seeing": [int(x) for x in nearest_point.Seeing.values], 
            "Transparency": [int(x) for x in nearest_point.Transparency.values]}

def _select_forecast(lat: float, lon: float) -> xr.DataArray:
    desired_x, desired_y = astro_data_reader.proj.transformer.transform(lon, lat)
    nearest_point = ds.sel(x=desired_x, y=desired_y, method="nearest")
    return nearest_point

app = Litestar([index, get_forecast])
