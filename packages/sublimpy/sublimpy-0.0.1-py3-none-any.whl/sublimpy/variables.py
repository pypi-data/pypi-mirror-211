"""
Convenience functions for calculating additional variables from SoS measurements. 
"""
import xarray as xr
import numpy as np
import metpy
from metpy.units import units

from sublimpy.gradients import LogPolynomial, LogPolynomialWithRoughness, Ri

# Constants used in calculations.
STEVEN_BOLTZMAN = 5.67e-08 #W/m^2/degK^4
SNOW_EMMISIVITY = 0.98 
VON_KARMAN = 0.4

# A list of the default variables that one might use when analyzing SoS datasets.
# These are the variables required to run other functions in variables.py.
DEFAULT_VARIABLES = [
    # Sonic Anemometer Data for 4 towers
    'tc_1m_uw',     'spd_1m_uw',     'dir_1m_uw',     'u_1m_uw',   'v_1m_uw',   'w_1m_uw',   'u_u__1m_uw',    'v_v__1m_uw',    'w_w__1m_uw',    
        'u_w__1m_uw',    'v_w__1m_uw',  'u_tc__1m_uw',  'v_tc__1m_uw',   'u_h2o__1m_uw',  'v_h2o__1m_uw',   'w_tc__1m_uw',   'w_h2o__1m_uw',
    'tc_3m_uw',     'spd_3m_uw',     'dir_3m_uw',     'u_3m_uw',   'v_3m_uw',   'w_3m_uw',   'u_u__3m_uw',    'v_v__3m_uw',    'w_w__3m_uw',    
        'u_w__3m_uw',    'v_w__3m_uw',  'u_tc__3m_uw',  'v_tc__3m_uw',   'u_h2o__3m_uw',  'v_h2o__3m_uw',   'w_tc__3m_uw',   'w_h2o__3m_uw',
    'tc_10m_uw',    'spd_10m_uw',    'dir_10m_uw',    'u_10m_uw',  'v_10m_uw',  'w_10m_uw',  'u_u__10m_uw',   'v_v__10m_uw',   'w_w__10m_uw',   
        'u_w__10m_uw',   'v_w__10m_uw', 'u_tc__10m_uw', 'v_tc__10m_uw',  'u_h2o__10m_uw', 'v_h2o__10m_uw',  'w_tc__10m_uw',  'w_h2o__10m_uw',

    'tc_1m_ue',     'spd_1m_ue',     'dir_1m_ue',     'u_1m_ue',   'v_1m_ue',   'w_1m_ue',   'u_u__1m_ue',    'v_v__1m_ue',    'w_w__1m_ue',    
        'u_w__1m_ue',    'v_w__1m_ue',  'u_tc__1m_ue',  'v_tc__1m_ue',   'u_h2o__1m_ue',  'v_h2o__1m_ue',   'w_tc__1m_ue',   'w_h2o__1m_ue',
    'tc_3m_ue',     'spd_3m_ue',     'dir_3m_ue',     'u_3m_ue',   'v_3m_ue',   'w_3m_ue',   'u_u__3m_ue',    'v_v__3m_ue',    'w_w__3m_ue',    
        'u_w__3m_ue',    'v_w__3m_ue',  'u_tc__3m_ue',  'v_tc__3m_ue',   'u_h2o__3m_ue',  'v_h2o__3m_ue',   'w_tc__3m_ue',   'w_h2o__3m_ue',
    'tc_10m_ue',    'spd_10m_ue',    'dir_10m_ue',    'u_10m_ue',  'v_10m_ue',  'w_10m_ue',  'u_u__10m_ue',   'v_v__10m_ue',   'w_w__10m_ue',   
        'u_w__10m_ue',   'v_w__10m_ue', 'u_tc__10m_ue', 'v_tc__10m_ue',  'u_h2o__10m_ue', 'v_h2o__10m_ue',  'w_tc__10m_ue',  'w_h2o__10m_ue',

    'tc_1m_d',      'spd_1m_d',     'dir_1m_d',     'u_1m_d',   'v_1m_d',   'w_1m_d',   'u_u__1m_d',    'v_v__1m_d',    'w_w__1m_d',    
        'u_w__1m_d',    'v_w__1m_d',  'u_tc__1m_d',  'v_tc__1m_d',   'u_h2o__1m_d',  'v_h2o__1m_d',   'w_tc__1m_d',   'w_h2o__1m_d',
    'tc_3m_d',      'spd_3m_d',     'dir_3m_d',     'u_3m_d',   'v_3m_d',   'w_3m_d',   'u_u__3m_d',    'v_v__3m_d',    'w_w__3m_d',    
        'u_w__3m_d',    'v_w__3m_d',  'u_tc__3m_d',  'v_tc__3m_d',   'u_h2o__3m_d',  'v_h2o__3m_d',   'w_tc__3m_d',   'w_h2o__3m_d',
    'tc_10m_d',     'spd_10m_d',    'dir_10m_d',    'u_10m_d',  'v_10m_d',  'w_10m_d',  'u_u__10m_d',   'v_v__10m_d',   'w_w__10m_d',   
        'u_w__10m_d',   'v_w__10m_d', 'u_tc__10m_d', 'v_tc__10m_d',  'u_h2o__10m_d', 'v_h2o__10m_d',  'w_tc__10m_d',  'w_h2o__10m_d',

    'tc_2m_c',  'spd_2m_c',     'dir_2m_c',     'u_2m_c',   'v_2m_c',   'w_2m_c',   'u_u__2m_c',    'v_v__2m_c',    'w_w__2m_c',    
        'u_w__2m_c',    'v_w__2m_c',  'u_tc__2m_c',  'v_tc__2m_c',   'u_h2o__2m_c',  'v_h2o__2m_c',   'w_tc__2m_c',   'w_h2o__2m_c',
    'tc_3m_c',  'spd_3m_c',     'dir_3m_c',     'u_3m_c',   'v_3m_c',   'w_3m_c',   'u_u__3m_c',    'v_v__3m_c',    'w_w__3m_c',    
        'u_w__3m_c',    'v_w__3m_c',  'u_tc__3m_c',  'v_tc__3m_c',   'u_h2o__3m_c',  'v_h2o__3m_c',   'w_tc__3m_c',   'w_h2o__3m_c',
    'tc_5m_c',  'spd_5m_c',     'dir_5m_c',     'u_5m_c',   'v_5m_c',   'w_5m_c',   'u_u__5m_c',    'v_v__5m_c',    'w_w__5m_c',    
        'u_w__5m_c',    'v_w__5m_c',  'u_tc__5m_c',  'v_tc__5m_c',   'u_h2o__5m_c',  'v_h2o__5m_c',   'w_tc__5m_c',   'w_h2o__5m_c',
    'tc_10m_c', 'spd_10m_c',    'dir_10m_c',    'u_10m_c',  'v_10m_c',  'w_10m_c',  'u_u__10m_c',   'v_v__10m_c',   'w_w__10m_c',   
        'u_w__10m_c',   'v_w__10m_c', 'u_tc__10m_c', 'v_tc__10m_c',  'u_h2o__10m_c', 'v_h2o__10m_c',  'w_tc__10m_c',  'w_h2o__10m_c',
    'tc_15m_c', 'spd_15m_c',    'dir_15m_c',    'u_15m_c',  'v_15m_c',  'w_15m_c',  'u_u__15m_c',   'v_v__15m_c',   'w_w__15m_c',   
        'u_w__15m_c',   'v_w__15m_c', 'u_tc__15m_c', 'v_tc__15m_c',  'u_h2o__15m_c', 'v_h2o__15m_c',  'w_tc__15m_c',  'w_h2o__15m_c',
    'tc_20m_c', 'spd_20m_c',    'dir_20m_c',    'u_20m_c',  'v_20m_c',  'w_20m_c',  'u_u__20m_c',   'v_v__20m_c',   'w_w__20m_c',   
        'u_w__20m_c',   'v_w__20m_c', 'u_tc__20m_c', 'v_tc__20m_c',  'u_h2o__20m_c', 'v_h2o__20m_c',  'w_tc__20m_c',  'w_h2o__20m_c',

    
    # Temperature & Relative Humidity Array 
    'T_2m_c', 'T_3m_c', 'T_4m_c', 'T_5m_c', 'T_6m_c', 'T_7m_c', 'T_8m_c', 'T_9m_c', 'T_10m_c',
    'T_11m_c', 'T_12m_c', 'T_13m_c', 'T_14m_c', 'T_15m_c', 'T_16m_c', 'T_17m_c', 'T_18m_c', 'T_19m_c', 'T_20m_c',

    'RH_2m_c', 'RH_3m_c', 'RH_4m_c', 'RH_5m_c', 'RH_6m_c', 'RH_7m_c', 'RH_8m_c', 'RH_9m_c', 'RH_10m_c',
    'RH_11m_c','RH_12m_c','RH_13m_c','RH_14m_c','RH_15m_c','RH_16m_c','RH_17m_c','RH_18m_c','RH_19m_c','RH_20m_c',

    # Pressure Sensors
    'P_20m_c',
    'P_10m_c', 'P_10m_d', 'P_10m_uw', 'P_10m_ue',

    # Blowing snow/FlowCapt Sensors
    'SF_avg_1m_ue', 'SF_avg_2m_ue',

    # Apogee sensors
    "Vtherm_c", "Vtherm_d", "Vtherm_ue", "Vtherm_uw", 
    "Vpile_c", "Vpile_d", "Vpile_ue", "Vpile_uw",
    "IDir_c", "IDir_d", "IDir_ue", "IDir_uw",

    # Snow-level temperature arrays (towers D and UW)
    'Tsnow_0_4m_d', 'Tsnow_0_5m_d', 'Tsnow_0_6m_d', 'Tsnow_0_7m_d', 'Tsnow_0_8m_d', 'Tsnow_0_9m_d', 'Tsnow_1_0m_d', 'Tsnow_1_1m_d', 'Tsnow_1_2m_d', 'Tsnow_1_3m_d', 'Tsnow_1_4m_d', 'Tsnow_1_5m_d',
    'Tsnow_0_4m_uw', 'Tsnow_0_5m_uw', 'Tsnow_0_6m_uw', 'Tsnow_0_7m_uw', 'Tsnow_0_8m_uw', 'Tsnow_0_9m_uw', 'Tsnow_1_0m_uw', 'Tsnow_1_1m_uw', 'Tsnow_1_2m_uw', 'Tsnow_1_3m_uw', 'Tsnow_1_4m_uw', 'Tsnow_1_5m_uw',
    
    # Downward Facing Longwave Radiometer (tower D) - for measuring snow surface temperature
    'Rpile_out_9m_d',
    'Tcase_out_9m_d',
    
    # Upward facing shortwave radiometer (tower D) - for measuring incoming solar radiation!
    'Rsw_in_9m_d',
]

def apogee2temp(ds,tower):
    """Calculate surface temperature from apogee data.

    Args:
        ds (xr.Dataset): SoS dataset with apogee columns. Must have variables 
                IDir_{tower}
                Vtherm_{tower}
                Vpile_{tower}
            where tower can be 'c', 'd', 'ue', 'uw'
        tower (str): 'c', 'd', 'ue', or 'uw'

    Returns:
        xr.DataArray: DataArray of the calculated temperature measured by the
                apogee.
    """
    # hard-coded sensor-specific calibrations
    Vref = 2.5
    ID = ds[f"IDir_{tower}"]
    sns = [136, 137, 138, 139, 140]
    im = [ sns.index(x) if x in sns else None for x in ID ][0]
    # unclear if we want these, or scaled up versions
    mC0 = [57508.575,56653.007,58756.588,58605.7861, 58756.588][im] * 1e5
    mC1 = [289.12189,280.03380,287.12487,285.00285, 287.12487][im] * 1e5
    mC2 = [2.16807,2.11478,2.11822,2.08932, 2.11822][im] * 1e5
    bC0 = [-168.3687,-319.9362,-214.5312,-329.6453, -214.5312][im]* 1e5
    bC1 = [-0.22672,-1.23812,-0.59308,-1.24657, -0.59308][im]* 1e5
    bC2 = [0.08927,0.08612,0.10936,0.09234, 0.10936][im]* 1e5
    # read data
    Vtherm = ds[f"Vtherm_{tower}"]
    Vpile = ds[f"Vpile_{tower}"]*1000
    # calculation of detector temperature from Steinhart-Hart
    Rt = 24900.0/((Vref/Vtherm) - 1)
    Ac = 1.129241e-3
    Bc = 2.341077e-4
    Cc = 8.775468e-8
    TDk = 1/(Ac + Bc*np.log(Rt) + Cc*(np.log(Rt)**3))
    TDc = TDk - 273.15
    # finally, calculation of "target" temperature including thermopile measurement
    m = mC2*TDc**2 + mC1*TDc + mC0
    b = bC2*TDc**2 + bC1*TDc + bC0
    TTc = (TDk**4 + m*Vpile + b)**0.25 - 273.15
    # sufs = suffixes(TTc,leadch='') # get suffixes
    # dimnames(TTc)[[2]] = paste0("Tsfc.Ap.",sufs)
    TTc = TTc * units('celsius')
    return TTc

def add_surface_temps(ds):
    """Add surface temperatures calculated from the apogees on 4 towers and from the 
    radiometer on tower d.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    # Radiometer temperatures
    ds['Tsurf_rad_d'] = (
        (
            ds['Rpile_out_9m_d'] + STEVEN_BOLTZMAN * (ds['Tcase_out_9m_d']+273.15)**4
        ) / (SNOW_EMMISIVITY*STEVEN_BOLTZMAN)
    )**(1/4) - 273.15

    # Apogee temperatures
    ds['Tsurf_c'] = (['time'],  apogee2temp(ds, 'c').values)
    ds['Tsurf_d'] = (['time'],  apogee2temp(ds, 'd').values)
    ds['Tsurf_ue'] = (['time'],  apogee2temp(ds, 'ue').values)
    ds['Tsurf_uw'] = (['time'],  apogee2temp(ds, 'uw').values)
    
    return ds

def add_potential_virtual_temperatures(ds):
    """Add potential temperature, virtual temperature, potential virtual temperature, 
    air density, and mixing ratio variables for all heights on the C tower.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    # iterate over heights on C tower.
    for i in range(2,21):
        absolute_temperature = ds[f'T_{i}m_c'] * units.celsius
        relative_humidity = ds[f'RH_{i}m_c']
        absolute_pressure = ds['P_10m_c'] * units.millibar
        height_relative_to_10m_pressure_sensor = i*units.m - (10*units.m)

        height_adj_pressure = metpy.calc.add_height_to_pressure(
            absolute_pressure, 
            height_relative_to_10m_pressure_sensor
        )
        potential_temperature = metpy.calc.potential_temperature(    
                height_adj_pressure,
                absolute_temperature
        ).pint.to(units.celsius)
        mixing_ratio = xr.DataArray(relative_humidity/100) * metpy.calc.saturation_mixing_ratio(
            height_adj_pressure,
            absolute_temperature
        )
        air_density = metpy.calc.density(height_adj_pressure, absolute_temperature, mixing_ratio)
        virtual_potential_temperature = metpy.calc.virtual_temperature(
            potential_temperature,
            mixing_ratio,
        )

        virtual_temperature = metpy.calc.virtual_temperature(
            absolute_temperature,
            mixing_ratio,
        )
    
        ds[f'Tpot_{i}m_c'] = (['time'], potential_temperature.pint.magnitude)
        ds[f'Tpot_{i}m_c'] = ds[f'Tpot_{i}m_c'].assign_attrs(units = str(potential_temperature.pint.units))

        ds[f'Tvirtual_{i}m_c'] = (['time'], virtual_temperature.pint.magnitude)
        ds[f'Tvirtual_{i}m_c'] = ds[f'Tvirtual_{i}m_c'].assign_attrs(units = str(virtual_temperature.pint.units))

        ds[f'Tpotvirtual_{i}m_c'] = (['time'], virtual_potential_temperature.pint.magnitude)
        ds[f'Tpotvirtual_{i}m_c'] = ds[f'Tpotvirtual_{i}m_c'].assign_attrs(units = str(virtual_potential_temperature.pint.units))

        ds[f'airdensity_{i}m_c'] = (['time'], air_density.pint.magnitude)
        ds[f'airdensity_{i}m_c'] = ds[f'airdensity_{i}m_c'].assign_attrs(units = str(air_density.pint.units))

        ds[f'mixingratio_{i}m_c'] = (['time'], mixing_ratio.pint.magnitude)
        ds[f'mixingratio_{i}m_c'] = ds[f'mixingratio_{i}m_c'].assign_attrs(units = str(mixing_ratio.pint.units))
    
    return ds

def add_surface_potential_virtual_temperatures(ds):
    """Add potential temperature, virtual temperature, potential virtual temperature, 
    air density, and mixing ratio variables for surface temperature measurements on the C tower.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    height_relative_to_10m_pressure_sensor = - (10*units.m)
    absolute_temperature = ds['Tsurf_rad_d']*units.celsius
    absolute_pressure = ds['P_10m_c'] * units.millibar

    relative_humidity = 100

    height_adj_pressure = metpy.calc.add_height_to_pressure(
        absolute_pressure, 
        height_relative_to_10m_pressure_sensor
    )

    potential_temperature = metpy.calc.potential_temperature(    
        height_adj_pressure,
        absolute_temperature
    ).pint.to(units.celsius)

    mixing_ratio = xr.DataArray(relative_humidity/100) * metpy.calc.saturation_mixing_ratio(
            height_adj_pressure,
            absolute_temperature
        )
    air_density = metpy.calc.density(height_adj_pressure, absolute_temperature, mixing_ratio)

    virtual_potential_temperature = metpy.calc.virtual_temperature(
        potential_temperature,
        mixing_ratio,
    )

    virtual_temperature = metpy.calc.virtual_temperature(
        absolute_temperature,
        mixing_ratio,
    )

    ds[f'Tsurfvirtual_rad_c'] = (['time'], virtual_temperature.pint.magnitude)
    ds[f'Tsurfvirtual_rad_c'] = ds[f'Tsurfvirtual_rad_c'].assign_attrs(units = str(virtual_temperature.pint.units))

    ds[f'Tsurfpotvirtual_rad_c'] = (['time'], virtual_potential_temperature.pint.magnitude)
    ds[f'Tsurfpotvirtual_rad_c'] = ds[f'Tsurfpotvirtual_rad_c'].assign_attrs(units = str(virtual_potential_temperature.pint.units))

    ds[f'Tsurfairdensity_rad_c'] = (['time'], air_density.pint.magnitude)
    ds[f'Tsurfairdensity_rad_c'] = ds[f'Tsurfairdensity_rad_c'].assign_attrs(units = str(air_density.pint.units))

    ds[f'Tsurfmixingratio_rad_c'] = (['time'], mixing_ratio.pint.magnitude)
    ds[f'Tsurfmixingratio_rad_c'] = ds[f'Tsurfmixingratio_rad_c'].assign_attrs(units = str(mixing_ratio.pint.units))

    ds[f'Tsurfpot_rad_c'] = (['time'], potential_temperature.pint.magnitude)
    ds[f'Tsurfpot_rad_c'] = ds[f'Tsurfpot_rad_c'].assign_attrs(units = str(potential_temperature.pint.units))
    
    return ds

def add_tke(ds):
    """Add TKE variables for all sonic anemometers.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    ds['tke_2m_c'] = 0.5*(ds['u_u__2m_c'] + ds['v_v__2m_c'] + ds['w_w__2m_c'])
    ds['tke_3m_c'] = 0.5*(ds['u_u__3m_c'] + ds['v_v__3m_c'] + ds['w_w__3m_c'])
    ds['tke_5m_c'] = 0.5*(ds['u_u__5m_c'] + ds['v_v__5m_c'] + ds['w_w__5m_c'])
    ds['tke_10m_c'] = 0.5*(ds['u_u__10m_c'] + ds['v_v__10m_c'] + ds['w_w__10m_c'])
    ds['tke_15m_c'] = 0.5*(ds['u_u__15m_c'] + ds['v_v__15m_c'] + ds['w_w__15m_c'])
    ds['tke_20m_c'] = 0.5*(ds['u_u__20m_c'] + ds['v_v__20m_c'] + ds['w_w__20m_c'])

    ds['tke_1m_uw'] = 0.5*(ds['u_u__1m_uw'] + ds['v_v__1m_uw'] + ds['w_w__1m_uw'])
    ds['tke_3m_uw'] = 0.5*(ds['u_u__3m_uw'] + ds['v_v__3m_uw'] + ds['w_w__3m_uw'])
    ds['tke_10m_uw'] = 0.5*(ds['u_u__10m_uw'] + ds['v_v__10m_uw'] + ds['w_w__10m_uw'])

    ds['tke_1m_ue'] = 0.5*(ds['u_u__1m_ue'] + ds['v_v__1m_ue'] + ds['w_w__1m_ue'])
    ds['tke_3m_ue'] = 0.5*(ds['u_u__3m_ue'] + ds['v_v__3m_ue'] + ds['w_w__3m_ue'])
    ds['tke_10m_ue'] = 0.5*(ds['u_u__10m_ue'] + ds['v_v__10m_ue'] + ds['w_w__10m_ue'])

    ds['tke_1m_d'] = 0.5*(ds['u_u__1m_d'] + ds['v_v__1m_d'] + ds['w_w__1m_d'])
    ds['tke_3m_d'] = 0.5*(ds['u_u__3m_d'] + ds['v_v__3m_d'] + ds['w_w__3m_d'])
    ds['tke_10m_d'] = 0.5*(ds['u_u__10m_d'] + ds['v_v__10m_d'] + ds['w_w__10m_d'])

    return ds

def add_gradients_and_ri(ds):
    """Add wind gradient, temperature gradient, gradient Richardson number (Ri), and bulk
    Richardson number (RiB) at all sonic anemometer heights on the c tower. Wind gradient is 
    calculated by fitting a log-polynomial function to wind u and v measurements from all sonics
    on tower. Temperature gradient is calculated by fitting a log-polygnomial function to air and 
    surface temperature measurements from the tower C temperature sensors and the radiometer on 
    tower D, where the surface temperature is assumed to apply at a roughness length. 

    gradient Richardson number is calculated using the common formula.

    Bulk richardson numner is calculated according to the citation provided in the documentation
    for `Ri.calculate_richardson_number_bulk`.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    ds['wind_gradient_2m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 2, 'c').values)
    ds['wind_gradient_3m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 3, 'c').values)
    ds['wind_gradient_5m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 5, 'c').values)
    ds['wind_gradient_10m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 10, 'c').values)
    ds['wind_gradient_15m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 15, 'c').values)
    ds['wind_gradient_20m_c'] = (['time'], LogPolynomial.calculate_wind_gradient_for_height(ds, 20, 'c').values)

    ds['temp_gradient_2m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 2
        ).values
    )
    ds['temp_gradient_3m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 3
        ).values
    )
    ds['temp_gradient_5m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 5
        ).values
    )
    ds['temp_gradient_10m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 10)
        .values
    )
    ds['temp_gradient_15m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 15
        ).values
    )
    ds['temp_gradient_20m_c'] = (['time'], 
        LogPolynomialWithRoughness.calculate_temperature_gradient_for_height(
            ds, 20
        ).values
    )

    ds['Ri_2m_c'] = (['time'], Ri.calculate_richardson_number(ds, 2, 'c'))
    ds['Ri_3m_c'] = (['time'], Ri.calculate_richardson_number(ds, 3, 'c'))
    ds['Ri_5m_c'] = (['time'], Ri.calculate_richardson_number(ds, 5, 'c'))
    ds['Ri_10m_c'] = (['time'], Ri.calculate_richardson_number(ds, 10, 'c'))
    ds['Ri_15m_c'] = (['time'], Ri.calculate_richardson_number(ds, 15, 'c'))
    ds['Ri_20m_c'] = (['time'], Ri.calculate_richardson_number(ds, 20, 'c'))

    ds['RiB_2m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 2, 'c'))
    ds['RiB_3m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 3, 'c'))
    ds['RiB_5m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 5, 'c'))
    ds['RiB_10m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 10, 'c'))
    ds['RiB_15m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 15, 'c'))
    ds['RiB_20m_c'] = (['time'], Ri.calculate_richardson_number_bulk(ds, 20, 'c'))
    
    return ds

def add_obukhov_length(ds):
    """Add Obukhov length at all sonic anemometer heights on the c tower.

    Args:
        ds (xr.Dataset): SoS dataset to add variables too

    Returns:
        xr.Dataset: Augmented SoS dataset.
    """
    # iterate over pressure measurements
    for i in [2,3,5,10,15,20]:

        shear_velocity = np.sqrt(np.sqrt(ds[f'u_w__{i}m_c']**2 + ds[f'v_w__{i}m_c']**2))

        L = - ( 
            (273.15 + ds[f'Tvirtual_{i}m_c']) * shear_velocity**3 
        ) / (
            metpy.constants.g.magnitude * VON_KARMAN * ds[f'w_tc__{i}m_c']
        )
        
        ds[f'u*_{i}m_c'] = shear_velocity
        ds[f'L_{i}m_c'] = L

    return ds