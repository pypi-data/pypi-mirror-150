# Import Modules
from ttscna import ttscna
import pandas as pd
from os.path import exists

# Generate some data
ttscna.ttscna('Example_Data/2021_10_28_0019.atf', 285.0, 80.0)

# Read the data you generated
results = pd.read_csv('Example_Data/2021_10_28_0019_results.csv', index_col = 0)

# Was the .csv made?
def test_csv_exists():
    assert exists('Example_Data/2021_10_28_0019_results.csv') == True

# Was the .png made?
def test_png_exists():
    assert exists('Example_Data/2021_10_28_0019_results.png') == True

# Is the Unitary Conductance what we'd expect?
def test_uconn():
    assert results['Unitary Conductance (fS)'][0] > 200.0 and results['Unitary Conductance (fS)'][0] < 250.0

# Is the Mean Dwell Time what we'd expect?
def test_dwell():
    assert results['Dwell Time (ms)'][0] > 10.0 and results['Dwell Time (ms)'][0] < 20.0

# Is the Mean Bulk Current what we'd expect?
def test_subcurr():
    assert results['Mean Bulk Current (pA)'][0] > -100.0 and results['Mean Bulk Current (pA)'][0] < -50.0
