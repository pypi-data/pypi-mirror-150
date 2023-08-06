# nsstools
This python tools has two methods that applies on nss_two_body_orbit Gaia solutions
- covmat: for all kind of nss_solution_type, converts the correlation matrix+uncertainties to the covariance matrix of the solution
- campbell: for a NSS solution that is either astrometric Orbital* or AstroSpectroSB1, converts the Thiele-Innes orbital elements to the Campbell elements and propagates the uncertainties.
            Ref: Halbwachs et al., 2022, Gaia Data Release 3. Astrometric binary star processing, Astronomy and Astrophysics, Appendix A
input: dataframe 
output: dataframe

## Installation

### with pip
pip3 install --user nsstools

### with setup
python3 setup.py install

## Usage

```python3
import pandas as pd
from nsstools import NssSource

nss = pd.read_csv("tests/nss_sample.csv.gz")
source_index = 0 # position of the source in the csv file

source = NssSource(nss, indice=source_index)
print(source.covmat())
print(source.campbell())

```

## Authors and acknowledgment
Jean-Louis Halbwachs
Carine Babusiaux
Nicolas Leclerc
