import xarray as xr
from AstronomyDatasetReader import AstronomyDatasetReader
from pathlib import Path
from litestar import Litestar, get

astro_data_reader = AstronomyDatasetReader(Path('../demo_data/'))
ds = astro_data_reader.get_dataset()

@get("/", include_in_schema=False)
async def index() -> str:
    return "See /schema/swagger for API information"

@get("/api/forecast/")
async def get_forecast(lat: float, lon: float) -> dict["str", list[int]]:
    desired_x, desired_y = astro_data_reader.proj.transformer.transform(lon, lat)
    nearest_point = ds.sel(x=desired_x, y=desired_y, method="nearest")
    return {"Seeing": [int(x) for x in nearest_point.Seeing.values], 
            "Transparency": [int(x) for x in nearest_point.Transparency.values]}

app = Litestar([index, get_forecast])
