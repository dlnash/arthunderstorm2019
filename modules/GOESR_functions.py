"""
Filename:    GOESR_functions.py
Author:      Deanna Nash, dlnash@ucsb.edu
Description: Functions to deal with GOES-R Satellite data

"""
import numpy as np
import boto3

def goes_lat_lon_reproj(dataset):
    """A function that reprojects GOES-R x and y satellite radian angles into WGS-84 latitude and longitude. 
    This code is adapted from Joshua Hrisko's Algorithm:
    https://makersportal.com/blog/2018/11/25/goes-r-satellite-latitude-and-longitude-grid-projection-algorithm. 
    
    Parameters
    ----------
    dataset : 
        An xarray dataset object from the GOES-R satellite.
        
    Returns
    -------
    lats
        Array of latitudes in WGS-84 projection
    lons
        Array of longitudes in WGS-84 projection
    """
        
    DS = dataset
    ## GOES projection info and retrieving relavant constants
    r_eq = DS.goes_imager_projection.semi_major_axis
    r_pol = DS.goes_imager_projection.semi_minor_axis
    lon_origin = DS.goes_imager_projection.longitude_of_projection_origin
    h_sat = DS.goes_imager_projection.perspective_point_height
    H = r_eq + h_sat


    ## Data info
    lat_rad_1d = DS.x
    lon_rad_1d = DS.y
    # create meshgrid filled with radian angles
    lat_rad,lon_rad = np.meshgrid(lat_rad_1d,lon_rad_1d)
    
    # lat/lon calc routine from satellite radian angle vectors

    lambda_0 = (lon_origin*np.pi)/180.0

    a_var = np.power(np.sin(lat_rad),2.0) + (np.power(np.cos(lat_rad),2.0)*(np.power(np.cos(lon_rad),
    2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(lon_rad),2.0))))
    b_var = -2.0*H*np.cos(lat_rad)*np.cos(lon_rad)
    c_var = (H**2.0)-(r_eq**2.0)

    r_s = (-1.0*b_var - np.sqrt((b_var**2)-(4.0*a_var*c_var)))/(2.0*a_var)

    s_x = r_s*np.cos(lat_rad)*np.cos(lon_rad)
    s_y = - r_s*np.sin(lat_rad)
    s_z = r_s*np.cos(lat_rad)*np.sin(lon_rad)

    lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
    lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)
    
    return lat, lon


def get_s3_keys(bucket, prefix = ''):
    """
    Generate the keys in an S3 bucket.
    
    This code is from Hamed Alemohammad:
    https://github.com/HamedAlemo/visualize-goes16

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix):
                yield key

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break