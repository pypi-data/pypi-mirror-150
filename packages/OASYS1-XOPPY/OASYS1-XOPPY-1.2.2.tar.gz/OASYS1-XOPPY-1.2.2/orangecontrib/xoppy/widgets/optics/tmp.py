
#
# script to make the calculations (created by XOPPY:crosssec)
#
from xoppylib.scattering_functions.xoppy_calc_crosssec import xoppy_calc_crosssec
import xraylib
from dabax.dabax_xraylib import DabaxXraylib

out_dict =  xoppy_calc_crosssec(
    descriptor   = "Si",
    density      = 2.33,
    MAT_FLAG     = 0,
    CALCULATE    = 1,
    GRID         = 0,
    GRIDSTART    = 100.0,
    GRIDEND      = 10000.0,
    GRIDN        = 200,
    UNIT         = 0,
    DUMP_TO_FILE = 0,
    FILE_NAME    = "CrossSec.dat",
    material_constants_library = DabaxXraylib(file_CrossSec="CrossSec_EPDL97.dat"),
    )

#
# example plot
#
from srxraylib.plot.gol import plot

plot(out_dict["data"][0,:],out_dict["data"][-1,:],
    xtitle=out_dict["labels"][0],ytitle=out_dict["labels"][1],title="xcrosssec",
    xlog=True,ylog=True,show=True)

#
# end script
#
