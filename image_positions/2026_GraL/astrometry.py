""" #> IMPORTS =======================
================================== """

import numpy as np

global rad_per_deg
rad_per_deg = np.pi / 180

""" #> FUNCTIONS =====================
================================== """

def RADEC_to_ARCSEC(RA,Dec,zpra,zpdec):
    # Takes you from RA,Dec in observed degrees to arcsec with respect to given zero point zpra,zpdec

    # First convert RA,Dec to real RA,Dec in deg
    RA = (RA-zpra)*np.cos(Dec*rad_per_deg)
    Dec = Dec - zpdec

    # Next convert to arcsec
    x_arc,y_arc = RA*3600,Dec*3600

    return x_arc,y_arc

def ARCSEC_to_RADEC(xarc,yarc,zpra,zpdec):
    # Takes you from arcsec to RA,Dec with respect to given zero point zpra,zpdec

    Dec = (yarc/3600)+zpdec
    RA = ((xarc/3600)/np.cos(Dec*rad_per_deg))+zpra
    # RA = (xarc/3600)+zpra

    return RA,Dec


""" #> MAIN FUNCTION =================
================================== """

#> main function
if __name__ == '__main__':
    
    #> name
    import os
    print('> '+os.path.basename(__file__))
    
    array = [[169.0981667,	-6.9607222],
            [169.0980417,	-6.9606111],
            [169.0980417,	-6.96075],
            [169.098125,	-6.9606111],
            [169.0980833,	-6.9606667]]
    array = np.array(array)

    print(RADEC_to_ARCSEC(array[:,0], array[:,1],
                          array[-1,0], array[-1,1]))
    inFile = ''
    
    # end
# thank