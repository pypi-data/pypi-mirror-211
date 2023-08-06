from aart import *

def cvisamp(spins, i_angles, path='./Results/', radonangles=[0,90], radonfile=0, dx0=0.02, dx1=0.02, dx2=0.02, limits=30, psi=1.07473555940836, dBH=5.214795112e23, fudge=1.5, maxbaseline=500, Ncut=0):
    """
    Computes the visibility amplitude for specified baesline angles. Requires 'cintensity' and 'clb' from the 'radialintensity' and 'lensingbands' modules respectively to have been called for the corresponding spins and angles.
    :param spins: an iterable object containing BH spins
    :param i_angles: an iterable object containing BH inclination angles, relative to the observer, in degrees
    :param path: path for saving the output. This should be consistent across the usage of all functions in this package
    :param radonangles: iterable object containing the projection angles for the radon transformation
    :param radonfile: takes on values 0 or 1. If equal to 1, the radon cut profiles will be stored
    :param dx0: resolution for the n=0 image in units of M
    :param dx1: resolution for the n=1 image in units of M
    :param dx2: resolution for the n=2 image in units of M
    :param limits: limits for the image in units of M. It should coincide with the source profile used for computing and plotting observables
    :param psi: BH mass-to-distance ratio (default: 1/psi=6.2e9 Kg)
    :param dBH: distance to the BH in meters (default: M87)
    :param fudge: fudge factor (for n>0)
    :param maxbaseline: max baseline in G\lambda
    :param Ncut: Ncut==0 to use the same x-axis baselines for each case
    """
    for spin_case in spins:
        for i_case in i_angles:
            
            isco=rms(spin_case)            
            thetao=i_case*np.pi/180
           
            fnbands=path+"LensingBands_a_%s_i_%s.h5"%(spin_case,i_case)

            print("Reading file: ",fnbands)

            h5f = h5py.File(fnbands,'r')

            supergrid0=h5f['grid0'][:]
            N0=int(h5f["N0"][0])
            supergrid1=h5f['grid1'][:]
            N1=int(h5f["N1"][0])
            supergrid2=h5f['grid2'][:]
            N2=int(h5f["N2"][0])
            h5f.close()

            fint=path+"Intensity_a_%s_i_%s.h5"%(spin_case,i_case)

            print("Reading file: ",fint)

            h5f = h5py.File(fint,'r')

            bghts0=h5f['bghts0'][:]
            bghts1=h5f['bghts1'][:]
            bghts2=h5f['bghts2'][:]

            h5f.close()

            vamp.radon_cut(radonangles,bghts0,bghts1,bghts2,supergrid0,supergrid1,supergrid2, path, radonfile, dx0, dx1, dx2, limits, spin_case, i_case, psi, dBH, fudge, maxbaseline, Ncut)   
           