import xarray as xr
from AstronomyDatasetReader import AstronomyDatasetReader
from pathlib import Path

if __name__ == "__main__":
    astro_data_reader = AstronomyDatasetReader(Path('../demo_data/'))
    ds = astro_data_reader.get_dataset()

    # Show the merged and cleaned up xarray Dataset
    print(ds)
    print()

    # Show how close we got to the desired lat/lon
    devon_lon, devon_lat = -97.5182337, 35.4670861 # Devon Tower
    desired_x, desired_y = astro_data_reader.proj.transformer.transform(devon_lon, devon_lat)
    print(f"x={desired_x:.1f}, y={desired_y:.1f}")
    nearest_point = ds.sel(x=desired_x, y=desired_y, method="nearest")
    print(f"selected_lat={nearest_point.latitude.values:.5f}, desired_lat={devon_lat:.5f}")
    print(f"selected_lon={nearest_point.longitude.values:.5f} (AKA {(nearest_point.longitude.values+180) % 360 - 180:.5f}), "
          f"desired_lon={devon_lon:.5f}")
    print()

    # Show the forecast
    print("OKC seeing forecast:")
    print(nearest_point["Seeing"].values)
    print("OKC transparency forecast:")
    print(nearest_point["Transparency"].values)