"""
Temporal interpolation input forcings to the current output timestep.
"""
import sys
from core import errMod
import numpy as np

def no_interpolation(input_forcings,ConfigOptions,MpiConfig):
    """
    Function for simply setting the final regridded fields to the
    input forcings that are from the next input forcing frequency.
    :param input_forcings:
    :param ConfigOptions:
    :param MpiConfig:
    :return:
    """
    input_forcings.final_forcings[:,:,:] = input_forcings.regridded_forcings2[:,:,:]

def nearest_neighbor(input_forcings,ConfigOptions,MpiConfig):
    """
    Function for setting the current output regridded forcings to the nearest
    input forecast step.
    :param input_forcings:
    :param ConfigOptions:
    :param MpiConfig:
    :return:
    """
    # Calculate the difference between the current output timestep,
    # and the previous input forecast output step.
    dtFromPrevious = ConfigOptions.current_output_step - input_forcings.fcst_date1

    # Calculate the difference between the current output timesetp,
    # and the next forecast output step.
    dtFromNext = ConfigOptions.current_output_step - input_forcings.fcst_date2

    if abs(dtFromNext.total_seconds()) <= abs(dtFromPrevious.total_seconds()):
        # Default to the regridded states from the next forecast output step.
        input_forcings.final_forcings[:,:,:] = input_forcings.regridded_forcings2[:,:,:]
    else:
        # Default to the regridded states from the previous forecast output
        # step.
        input_forcings.final_forcings[:,:,:] = input_forcings.regridded_forcings1[:,:,:]

def weighted_average(input_forcings,ConfigOptions,MpiConfig):
    """
    Function for setting the current output regridded fields as a weighted
    average between the previous output step and the next output step.
    :param input_forcings:
    :param ConfigOptions:
    :param MpiConfig:
    :return:
    """
    # Calculate the difference between the current output timestep,
    # and the previous input forecast output step. Use this to calculate a fraction
    # of the previous forcing output to use in the final output for this step.
    dtFromPrevious = ConfigOptions.current_output_step - input_forcings.fcst_date1
    weight1 = 1-(dtFromPrevious.total_seconds()/(input_forcings.outFreq*60.0))

    # Calculate the difference between the current output timesetp,
    # and the next forecast output step. Use this to calculate a fraction of
    # the next forcing output to use in the final output for this step.
    dtFromNext = ConfigOptions.current_output_step - input_forcings.fcst_date2
    weight2 = 1-(dtFromNext.total_seconds()/(input_forcings.outFreq*60.0))

    input_forcings.final_forcings[:,:,:] = input_forcings.regridded_forcings1[:,:,:]*weight1 + \
        input_forcings.regridded_forcings2[:,:,:]*weight2
