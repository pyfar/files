# %% Collect and save raw data from FABIAN HRTF measurements
import pyfar as pf  # v0.7.3
import numpy as np  # v2.3.0
import scipy as sp  # v1.15.3
import os

# path to internal database at Audio Communication Group, TU Berlin
# This is useless for everyone else, but I thought its nice as a reminder for
# how the test data was collected.
path = '3 Messung/7 HRTF data/1 Raw Data/2 HRTF data'

# source positions to include in the dataset
azimuths = np.array([0, 90, 180, 270, 0])
elevations = np.array([0, 0, 0, 0, 90])
source_positions = pf.Coordinates().from_spherical_elevation(
    azimuths / 180 * np.pi, elevations / 180 * np.pi, 1.7)

# positions of the left and right microphone at the blocked ear channel
# entrances
ear_positions = pf.Coordinates(0, np.atleast_2d([.0662, -.0662]).T, 0)

# Origin of coordinates
reference_position = pf.Coordinates(0, 0, 0)

for n, (az, el) in enumerate(zip(azimuths, elevations)):

    # load reference measurement (recorded sweep)
    data = sp.io.loadmat(
        os.path.join(path, 'reference', 'data', f'ElP{el}_Az{az}'),
        variable_names=['rec_sweep'])
    rec_ref = data['rec_sweep']

    # load measurement (recorded sweep, neutral head orientation)
    data = sp.io.loadmat(
        os.path.join(path, 'pm0', 'data', f'ElP{el}_Az{az}'),
        variable_names=['rec_sweep'])
    rec_meas = data['rec_sweep']

    if n == 0:
        reference = np.zeros((azimuths.size, 2, rec_meas.shape[0]))
        ear = np.zeros((azimuths.size, 2, rec_meas.shape[0]))

    reference[n] = rec_ref.T
    ear[n] = rec_meas.T

reference = pf.Signal(
    reference, sampling_rate=44100,
    comment=('sweep recorded with DPA 4060 microphones'
             'in the center of the loudspeaker array'))

ear = pf.Signal(
    ear, sampling_rate=44100,
    comment=('sweep recorded with DAP 4060 microphones'
             'at the blocked ear channel entrances '
             'of the FABIAN head and torso simulator'))

pf.io.write('hrtf_post_processing_and_normalization',
            reference_pressure=reference, ear_pressure=ear,
            source_positions=source_positions,
            ear_positions=ear_positions,
            reference_position=reference_position)
