import os
import glob
import subprocess
import datetime
import pyfits
import lsst.eotest.sensor as sensorTest

class VendorFitsTranslator(object):
    """
    Translate vendor data to conform to LCA-10140.  Current
    implementations only perform minimal header changes to allow
    eotest to run.

    Valid test types, image types, and filename format are

    test_types: fe55 dark flat lambda trap sflat_nnn spot
    image_types: bias dark fe55 flat spot ppump
    filenames: <lsst_num>_<test_type>_<image_type>_<seqno>_<time_stamp>.fits
    """
    def __init__(self, lsst_num, rootdir, outputBaseDir):
        self.lsst_num = lsst_num
        self.rootdir = rootdir
        self.outputBaseDir = outputBaseDir
        self._infiles = lambda x : sorted(glob.glob(os.path.join(rootdir, x)))
        self.outfiles = []
    def _writeFile(self, hdulist, local_vars, verbose=True):
        outfile = "%(lsst_num)s_%(test_type)s_%(image_type)s_%(seqno)s_%(time_stamp)s.fits" % local_vars
        outdir = os.path.join(self.outputBaseDir, local_vars['test_type'],
                              local_vars['time_stamp'])
        try:
            os.makedirs(outdir)
        except OSError:
            pass
        outfile = os.path.join(outdir, outfile)
        if verbose:
            print "writing", outfile
        hdulist.writeto(outfile, clobber=True, checksum=True)
        self.outfiles.append(os.path.relpath(outfile))
    def _setAmpGeom(self, hdulist):
        detxsize = 8*hdulist[1].header['NAXIS1']
        detysize = 2*hdulist[1].header['NAXIS2']
        ampGeom = sensorTest.AmplifierGeometry(detxsize=detxsize,
                                               detysize=detysize)
        hdulist[0].header['DETSIZE'] = ampGeom.DETSIZE
        for hdu in range(1, 17):
            amp = hdulist[hdu].header['AMPNO']
            hdulist[hdu].header['DETSIZE'] = ampGeom[amp]['DETSIZE']
            hdulist[hdu].header['DATASEC'] = ampGeom[amp]['DATASEC']
            hdulist[hdu].header['DETSEC'] = ampGeom[amp]['DETSEC']
    def _processFiles(self, test_type, image_type, pattern, 
                      time_stamp=None, verbose=True):
        infiles = self._infiles(pattern)
        if time_stamp is None:
            time_stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        for iframe, infile in enumerate(infiles):
            if verbose:
                print "processing", os.path.basename(infile)
            seqno = '%03i' % iframe
            self.translate(infile, test_type, image_type, seqno,
                           time_stamp=time_stamp, verbose=verbose)
        return time_stamp

        
class ItlFitsTranslator(VendorFitsTranslator):
    """
    FITS Translator for ITL data.
    """
    def __init__(self, lsst_num, rootdir, outputBaseDir='.'):
        raise NotImplementedError("ITL translator not implemented yet")

class e2vFitsTranslator(VendorFitsTranslator):
    """
    FITS Translator for e2v data based on their TRR package.
    """
    def __init__(self, lsst_num, rootdir, outputBaseDir='.'):
        super(e2vFitsTranslator, self).__init__(lsst_num, rootdir,
                                                outputBaseDir)
    def translate(self, infile, test_type, image_type, seqno, time_stamp=None,
                  verbose=True):
        try:
            hdulist = pyfits.open(infile)
        except IOError, eobj:
            print eobj
            print "skipping"
            return
        lsst_num = self.lsst_num
        exptime = hdulist[0].header['EXPOSURE']
        hdulist[0].header['LSST_NUM'] = lsst_num
        hdulist[0].header['CCD_MANU'] = 'E2V'
        hdulist[0].header['CCD_SERN'] = hdulist[0].header['DEV_ID']
        hdulist[0].header['EXPTIME'] = exptime
        hdulist[0].header['MONOWL'] = hdulist[0].header['WAVELEN']
        hdulist[0].header['MONDIODE'] = hdulist[0].header['LIGHTPOW']
        hdulist[0].header['CCDTEMP'] = hdulist[0].header['TEMP_MEA']
        hdulist[0].header['TESTTYPE'] = test_type.upper()
        hdulist[0].header['IMGTYPE'] = image_type.upper()
        self._setAmpGeom(hdulist)
        self._writeFile(hdulist, locals(), verbose=verbose)
    def fe55(self, pattern='Images/*_xray_xray_*.fits', time_stamp=None,
             verbose=True):
        return self._processFiles('fe55', 'fe55', pattern, 
                                  time_stamp=time_stamp, verbose=verbose)
    def bias(self, pattern='Images/*_noims_nois_*.fits', time_stamp=None,
             verbose=True):
        return self._processFiles('fe55', 'bias', pattern,
                                  time_stamp=time_stamp, verbose=verbose)
    def dark(self, pattern='Images/*_dark_dark_*.fits', time_stamp=None,
             verbose=True):
        return self._processFiles('dark', 'dark', pattern,
                                  time_stamp=time_stamp, verbose=verbose)
    def trap(self, pattern='Images/*_trapspp_cycl*.fits', time_stamp=None,
             verbose=True):
        return self._processFiles('trap', 'ppump', pattern,
                                  time_stamp=time_stamp, verbose=verbose)
    def sflat_500(self, pattern='Images/*_sflatl_illu_*.fits', time_stamp=None,
                  verbose=True):
        return self._processFiles('sflat_500', 'flat', pattern,
                                  time_stamp=time_stamp, verbose=verbose)
    def spot(self, pattern='Images/*_xtalk_illu_*.fits', time_stamp=None,
             verbose=True):
        return self._processFiles('spot', 'spot', pattern,
                                  time_stamp=time_stamp, verbose=verbose)
    def flat(self, pattern='Images/*_ifwm_illu_*.fits', time_stamp=None,
             verbose=True):
        if time_stamp is None:
            time_stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        exptime = lambda x : pyfits.open(x)[0].header['EXPOSURE']
        infiles = self._infiles(pattern)
        for infile in infiles:
            if verbose:
                print "processing", os.path.basename(infile)
            seqno = '%03i_flat1' % exptime(infile)
            self.translate(infile, 'flat', 'flat', seqno, time_stamp=time_stamp,
                           verbose=verbose)
        return time_stamp
    def lambda_scan(self, pattern='Images/*_flat_*_illu_*.fits', time_stamp=None,
               verbose=True):
        if time_stamp is None:
            time_stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        wl = lambda x : pyfits.open(x)[0].header['WAVELEN']
        infiles = self._infiles(pattern)
        for infile in infiles:
            if verbose:
                print "processing", os.path.basename(infile)
            seqno = "%04i" % wl(infile)
            self.translate(infile, 'lambda', 'flat', seqno,
                           time_stamp=time_stamp, verbose=verbose)
        return time_stamp
#    def dark_defects_data(self, pattern='superflat high/PRDefs/*.fits',
#                          time_stamp=None, verbose=True):
#        return self._processFiles('sflat_500', 'dark_flat', pattern,
#                                  time_stamp=time_stamp, verbose=verbose)
    def run_all(self):
        time_stamp = self.fe55()
        self.bias(time_stamp=time_stamp)
        self.dark()
        self.trap()
        time_stamp = self.sflat_500()
        self.spot()
        self.flat()
        self.lambda_scan()
#        self.dark_defects_data(time_stamp=time_stamp)
