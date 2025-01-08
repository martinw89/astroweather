## astroweather
Repo to process Environment and Climate Change Canada (ECCC) data for astronomy forecasts and serve RESTfully.

See https://eccc-msc.github.io/open-data/msc-data/nwp_rdps/readme_astro-rdps-datamart-alpha_en/ for more information about the ECCC data

### app
To run the app:
1. create a venv
    - `python3 -m venv .venv`
2. Activate venv
    - `source .venv/bin/activate`
3. Install requirements 
    - `pip3 install -r requirements.txt`
    - Note: on MacOS, eccodes binaries may need to be installed separately. See https://pypi.org/project/eccodes/
4. Run app
    - `cd astroweather; litestar run`
