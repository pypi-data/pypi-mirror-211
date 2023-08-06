import xrmreader
import pyconrad.autoinit
from edu.stanford.rsl.conrad.data.numeric import NumericGrid
import numpy as np
from pathlib import Path

pyconrad.start_gui()

# projection_data = r'../data/mouse_ankle.txrm'
projection_data = Path(r'/media/mareike/HDD/Data/ERC/ExVivoDatasetXRM/ERC68_6485-2/ERC68_6485-2_Ankle_1400nm_0-14s_200Fr_1401Project.txrm')
reco_data = Path('some_file.txm')
metadata = xrmreader.read_metadata(reco_data)
image_data = xrmreader.read_txrm(reco_data)

# load raw data
raw_projections = xrmreader.read_txrm(projection_data)
NumericGrid.from_numpy(raw_projections).show('No noise')
# preprocess data in individual steps
projections = xrmreader.divide_by_reference(raw_projections, metadata['reference'])
projections = xrmreader.revert_shifts(projections, metadata['x-shifts'], metadata['y-shifts'])
projections = xrmreader.downsample(projections, spatial_factor=2, angular_factor=1)
projections = xrmreader.negative_logarithm(projections)
projections = xrmreader.truncation_correction(projections)

# load and preprocess data in one step (this does the same thing as the individual steps above, but needs less memory)
preprocessed_projections = xrmreader.read_and_preprocess_txrm(projection_data, downsample_factor=4, angular_factor=2)
NumericGrid.from_numpy(preprocessed_projections).show('No noise')

