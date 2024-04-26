# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:33:00 2024

@author: anapa
"""

import geopandas as gpd
import rasterio
from rasterio.mask import mask
import xarray as xr
import numpy as np

# Caminho para o arquivo NetCDF
nc_file = r'C:\Users\anapa\OneDrive - UNIVALI\Doutorado\Deposicao_Cla\BRAIN_BASECONC_AALJ_2019_01_01_01_to_2019_12_31_00.nc'

# Caminho para o shapefile contendo o polígono de recorte
shapefile_path = r'C:\Users\anapa\OneDrive - UNIVALI\Doutorado\Deposicao_Cla\buffer_costa\200_milhas\Mascara_200_milhas_nauticas.shp'

# Carregar o shapefile usando geopandas
polygon_gdf = gpd.read_file(shapefile_path)

# Abrir o arquivo NetCDF usando xarray
dataset = xr.open_dataset(nc_file)

# Obter os dados de coordenadas do arquivo NetCDF
lon = dataset.variables['LON'][:]
lat = dataset.variables['LAT'][:]

# Obter a transformação do conjunto de dados NetCDF
transform = rasterio.transform.from_origin(lon.min(), lat.max(), lon[1] - lon[0], lat[0] - lat[1])

# Criar uma máscara booleana com base no polígono
mask = rasterio.features.geometry_mask(
    [polygon_gdf.geometry.values[0]],
    out_shape=(len(lat), len(lon)),
    transform=transform,
    invert=True
)

# Aplicar a máscara ao conjunto de dados NetCDF
masked_data = {}
for var_name, var_data in dataset.variables.items():
    if 'time' in var_data.dims:
        masked_data[var_name] = (('time', 'lat', 'lon'), np.where(mask, var_data[:], np.nan))
    else:
        masked_data[var_name] = (('lat', 'lon'), np.where(mask, var_data[:], np.nan))

masked_dataset = xr.Dataset(masked_data, coords=dataset.coords)

# Salvar o novo arquivo NetCDF recortado
masked_dataset.to_netcdf(r'C:\Users\anapa\OneDrive - UNIVALI\Doutorado\Deposicao_Cla\/arquivo_recortado.nc')