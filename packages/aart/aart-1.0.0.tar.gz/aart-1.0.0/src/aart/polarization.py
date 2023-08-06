from aart import *

def polarization(spins, i_angles, bvapp=0, D_obs=10000, path='./Results/'):
    """
    :param spins: an iterable object containing the spins of the BH
    :param i_angles: an iterable object containing the inclination angles of the BH relative to the observer, in degrees
    :param bvapp: takes on values 0 or 1. If equal to 1, the Beloborodov approximation will also be computed
    :param D_obs: observer's distance in units of M
    :param path: path for saving the output. This should be consistent across the usage of all functions in this package
    """
    for spin_case in spins:
        for i_case in i_angles:
            
            isco=rms(spin_case)            
            thetao=i_case*np.pi/180
            #Disk's inclination  
            #Current version is just implemented for equatorial models   
            i_disk=90    
            thetad=i_disk*np.pi/180

            fnbands=path+"LensingBands_a_%s_i_%s.h5"%(spin_case,i_case)

            print("Reading file: ",fnbands)

            h5f = h5py.File(fnbands,'r')

            supergrid0=h5f['grid0'][:]
            mask0=h5f['mask0'][:]
            N0=int(h5f["N0"][0])

            h5f.close()

            if bvapp!=1:

                fnbands=path+"Rays_a_%s_i_%s.h5"%(spin_case,i_case)

                print("Reading file: ",fnbands)

                h5f = h5py.File(fnbands,'r')

                rs0=h5f['rs0'][:]
                sign0=h5f['sign0'][:]
                h5f.close()

                polarizationk.kappa(supergrid0,mask0,N0,rs0,sign0,spin_case,thetao, thetad, isco, path, i_case)

            else:

                fnrays=path+"Rays_bv_a_%s_i_%s.h5"%(spin_case,i_case)

                print("Reading file: ",fnrays)
                h5f = h5py.File(fnrays,'r')
                rs0_bv=h5f['rs0_bv'][:]
                sign0_bv=h5f['sign0_bv'][:]
                h5f.close()

                polarizationk.kappa_bv(supergrid0,mask0,N0,rs0_bv,sign0_bv,spin_case,thetao, thetad, isco, path, i_case)