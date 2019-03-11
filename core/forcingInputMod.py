"""
This module will guide the forcing engine in defining
parameters in all input forcing products. These parameters
include things such as file types, grid definitions (including
initializing ESMF grids and regrid objects), etc
"""
from core import dateMod
from core import regridMod
import numpy as np
from core import timeInterpMod
import os
from core import errMod

class input_forcings:
    """
    This is an abstract class that will define all the parameters
    of a single input forcing product.
    """
    def __init__(self):
        """
        Initializing all attributes and objects to None.
        """
        self.keyValue = None
        self.inDir = None
        self.userFcstHorizon = None
        self.userCycleOffset = None
        self.productName = None
        self.fileType = None
        self.nx_global = None
        self.ny_global = None
        self.nx_local = None
        self.ny_local = None
        self.x_lower_bound = None
        self.x_upper_bound = None
        self.y_lower_bound = None
        self.y_upper_bound = None
        self.cycleFreq = None
        self.outFreq = None
        self.regridOpt = None
        self.timeInterpOpt = None
        self.t2dDownscaleOpt = None
        self.swDowscaleOpt = None
        self.precipDownscaleOpt = None
        self.q2dDownscaleOpt = None
        self.psfcDownscaleOpt = None
        self.t2dBiasCorrectOpt = None
        self.swBiasCorrectOpt = None
        self.precipBiasCorrectOpt = None
        self.q2dBiasCorrectOpt = None
        self.windBiasCorrectOpt = None
        self.psfcBiasCorrectOpt = None
        self.lwBiasCorrectOpt = None
        self.esmf_lats = None
        self.esmf_lons = None
        self.esmf_grid_in = None
        self.regridComplete = False
        self.regridObj = None
        self.esmf_field_in = None
        self.esmf_field_out = None
        self.regridded_forcings1 = None
        self.regridded_forcings2 = None
        self.final_forcings = None
        self.ndv = None
        self.file_in1 = None
        self.file_in2 = None
        self.fcst_hour1 = None
        self.fcst_hour2 = None
        self.fcst_date1 = None
        self.fcst_date2 = None
        self.height = None
        self.netcdf_var_names = None
        self.input_map_output = None
        self.grib_levels = None
        self.grib_vars = None
        self.tmpFile = None
        self.tmpFileHeight = None
        self.psfcTmp = None
        self.t2dTmp = None

    def define_product(self):
        """
        Function to define the product name based on the mapping
        forcing key value.
        :return:
        """
        product_names = {
            1: "NLDAS2_GRIB1",
            2: "NARR_GRIB1",
            3: "GFS_Production_GRIB2",
            4: "NAM_Conus_Nest_GRIB2",
            5: "HRRR_Conus_GRIB2",
            6: "RAP_Conus_GRIB2",
            7: "CFSv2_GRIB2",
            8: "WRF_ARW_Hawaii_GRIB2",
            9: "GFS_Production_025d_GRIB2",
            10: "Custom_NetCDF"
        }
        self.productName = product_names[self.keyValue]

        product_types = {
            1: "GRIB1",
            2: "GRIB1",
            3: "GRIB2",
            4: "GRIB2",
            5: "GRIB2",
            6: "GRIB2",
            7: "GRIB2",
            8: "GRIB2",
            9: "GRIB2",
            10: "NetCDF"
        }
        self.fileType = product_types[self.keyValue]

        cycle_freq_minutes = {
            1: 60,
            2: 180,
            3: 360,
            4: 360,
            5: 60,
            6: 60,
            7: 360,
            8: 1440,
            9: 360,
            10: 60
        }
        self.cycleFreq = cycle_freq_minutes[self.keyValue]

        grib_vars_in = {
            1: None,
            2: None,
            3: ['TMP','SPFH','UGRD','VGRD','PRATE','DSWRF',
                'DLWRF','PRES'],
            4: None,
            5: ['TMP','SPFH','UGRD','VGRD','PRATE','DSWRF',
                'DLWRF','PRES'],
            6: None,
            7: None,
            8: None,
            9: ['TMP','SPFH','UGRD','VGRD','PRATE','DSWRF',
                'DLWRF','PRES'],
            10: None
        }
        self.grib_vars = grib_vars_in[self.keyValue]

        grib_levels_in = {
            1: None,
            2: None,
            3: ['2 m above ground','2 m above ground',
                '10 m above ground','10 m above ground',
                'surface','surface','surface','surface'],
            4: None,
            5: ['2 m above ground','2 m above ground',
                '10 m above ground','10 m above ground',
                'surface','surface','surface','surface'],
            6: None,
            7: None,
            8: None,
            9:['2 m above ground','2 m above ground',
                '10 m above ground','10 m above ground',
                'surface','surface','surface','surface'],
            10: None
        }
        self.grib_levels = grib_levels_in[self.keyValue]

        netcdf_variables = {
            1: None,
            2: None,
            3: ['TMP_2maboveground','SPFH_2maboveground',
                'UGRD_10maboveground','VGRD_10maboveground',
                'PRATE_surface','DSWRF_surface','DLWRF_surface',
                'PRES_surface'],
            4: None,
            5: ['TMP_2maboveground','SPFH_2maboveground',
                'UGRD_10maboveground','VGRD_10maboveground',
                'PRATE_surface','DSWRF_surface','DLWRF_surface',
                'PRES_surface'],
            6: None,
            7: None,
            8: None,
            9: ['TMP_2maboveground','SPFH_2maboveground',
                'UGRD_10maboveground','VGRD_10maboveground',
                'PRATE_surface','DSWRF_surface','DLWRF_surface',
                'PRES_surface'],
            10: None
        }
        self.netcdf_var_names = netcdf_variables[self.keyValue]

        input_matp_to_outputs = {
            1: None,
            2: None,
            3: [4,5,0,1,3,7,2,6],
            4: None,
            5: [4,5,0,1,3,7,2,6],
            6: None,
            7: None,
            8: None,
            9: [4,5,0,1,3,7,2,6],
            10: None
        }
        self.input_map_output = input_matp_to_outputs[self.keyValue]

    def calc_neighbor_files(self,ConfigOptions,dCurrent,MpiConfig):
        """
        Function that will calculate the last/next expected
        input forcing file based on the current time step that
        is being processed.
        :param ConfigOptions:
        :param dCurrent:
        :return:
        """
        # First calculate the current input cycle date this
        # WRF-Hydro output timestep corresponds to.
        find_neighbor_files = {
            3: dateMod.find_gfs_neighbors,
            5: dateMod.find_conus_hrrr_neighbors,
            9: dateMod.find_gfs_neighbors
        }

        find_neighbor_files[self.keyValue](self, ConfigOptions, dCurrent,MpiConfig)
        #try:
        #    find_neighbor_files[self.keyValue](self,ConfigOptions,dCurrent,MpiConfig)
        #except TypeError:
        #    ConfigOptions.errMsg = "Unable to execute find_neighbor_files for " \
        #                           "input forcing: " + self.productName
        #    raise
        #except:
        #    raise

    def regrid_inputs(self,ConfigOptions,wrfHyroGeoMeta,MpiConfig):
        """
        Polymorphic function that will regrid input forcings to the
        final output grids for this particular timestep. For
        timesteps that require interpolation, two sets of input
        forcing grids will be regridded IF we have come across new
        files and the process flag has been reset.
        :param ConfigOptions:
        :return:
        """
        # Establish a mapping dictionary that will point the
        # code to the functions to that will regrid the data.
        regrid_inputs = {
            3: regridMod.regrid_gfs,
            5: regridMod.regrid_conus_hrrr,
            9: regridMod.regrid_gfs
        }
        regrid_inputs[self.keyValue](self,ConfigOptions,wrfHyroGeoMeta,MpiConfig)
        #try:
        #    regrid_inputs[self.keyValue](self,ConfigOptions,MpiConfig)
        #except:
        #    ConfigOptions.errMsg = "Unable to execute regrid_inputs for " + \
        #        "input forcing: " + self.productName
        #    raise

    def temporal_interpolate_inputs(self,ConfigOptions,MpiConfig):
        """
        Polymorphic function that will run temporal interpolation of
        the input forcing grids that have been regridded. This is
        especially important for forcings that have large output
        frequencies. This is also important for frequent WRF-Hydro
        input timesteps.
        :param ConfigOptions:
        :param MpiConfig:
        :return:
        """
        temporal_interpolate_inputs = {
            0: timeInterpMod.no_interpolation,
            1: timeInterpMod.nearest_neighbor,
            2: timeInterpMod.weighted_average
        }
        temporal_interpolate_inputs[self.timeInterpOpt](self,ConfigOptions,MpiConfig)
        #temporal_interpolate_inputs[self.keyValue](self,ConfigOptions,MpiConfig)
        #try:
        #    temporal_interpolate_inputs[self.timeInterpOpt](self,ConfigOptions,MpiConfig)
        #except:
        #    ConfigOptions.errMsg = "Unable to execute temporal_interpolate_inputs " + \
        #        " for input forcing: " + self.productName
        #    raise

def initDict(ConfigOptions,GeoMetaWrfHydro):
    """
    Initial function to create an input forcing dictionary, which
    will contain an abstract class for each input forcing product.
    This gets called one time by the parent calling program.
    :param ConfigOptions:
    :return: InputDict - A dictionary defining our inputs.
    """
    # Initialize an empty dictionary
    InputDict = {}

    # Loop through and initialize the empty class for each product.
    for force_tmp in range(0,ConfigOptions.number_inputs):
        force_key = ConfigOptions.input_forcings[force_tmp]
        InputDict[force_key] = input_forcings()
        InputDict[force_key].keyValue = force_key
        InputDict[force_key].regridOpt = ConfigOptions.regrid_opt[force_tmp]
        InputDict[force_key].timeInterpOpt = ConfigOptions.forceTemoralInterp[force_tmp]

        InputDict[force_key].q2dDownscaleOpt = ConfigOptions.q2dDownscaleOpt[force_tmp]
        InputDict[force_key].t2dDownscaleOpt = ConfigOptions.t2dDownscaleOpt[force_tmp]
        InputDict[force_key].precipDownscaleOpt = ConfigOptions.precipDownscaleOpt[force_tmp]
        InputDict[force_key].swDowscaleOpt = ConfigOptions.swDownscaleOpt[force_tmp]
        InputDict[force_key].psfcDownscaleOpt = ConfigOptions.psfcDownscaleOpt[force_tmp]
        # Check to make sure the necessary input files for downscaling are present.
        if InputDict[force_key].t2dDownscaleOpt == 2:
            # We are using a pre-calculated lapse rate on the WRF-Hydro grid.
            pathCheck = ConfigOptions.downscaleParamDir = "/T2M_Lapse_Rate_" + \
                InputDict[force_key].productName + ".nc"
            if not os.path.isfile(pathCheck):
                ConfigOptions.errMsg = "Expected temperature lapse rate grid: " + \
                    pathCheck + " not found."
                errMod.err_out_screen(ConfigOptions.errMsg)

        InputDict[force_key].t2dBiasCorrectOpt = ConfigOptions.t2BiasCorrectOpt[force_tmp]
        InputDict[force_key].q2dBiasCorrectOpt = ConfigOptions.q2BiasCorrectOpt[force_tmp]
        InputDict[force_key].precipBiasCorrectOpt = ConfigOptions.precipBiasCorrectOpt[force_tmp]
        InputDict[force_key].swBiasCorrectOpt = ConfigOptions.swBiasCorrectOpt[force_tmp]
        InputDict[force_key].lwBiasCorrectOpt = ConfigOptions.lwBiasCorrectOpt[force_tmp]
        InputDict[force_key].windBiasCorrectOpt = ConfigOptions.windBiasCorrect[force_tmp]
        InputDict[force_key].psfcBiasCorrectOpt = ConfigOptions.psfcBiasCorrectOpt[force_tmp]

        InputDict[force_key].inDir = ConfigOptions.input_force_dirs[force_tmp]
        InputDict[force_key].define_product()
        InputDict[force_key].userFcstHorizon = ConfigOptions.fcst_input_horizons[force_tmp]
        InputDict[force_key].userCycleOffset = ConfigOptions.fcst_input_offsets[force_tmp]

        # Initialize the local final grid of values. This is represntative
        # of the local grid for this forcing, for a specific output timesetp.
        # This grid will be updated from one output timestep to another, and
        # also through downscaling and bias correction.
        InputDict[force_key].final_forcings = np.empty([8,GeoMetaWrfHydro.ny_local,
                                                        GeoMetaWrfHydro.nx_local],
                                                       np.float64)
        InputDict[force_key].height = np.empty([GeoMetaWrfHydro.ny_local,
                                                GeoMetaWrfHydro.nx_local],np.float32)

    return InputDict