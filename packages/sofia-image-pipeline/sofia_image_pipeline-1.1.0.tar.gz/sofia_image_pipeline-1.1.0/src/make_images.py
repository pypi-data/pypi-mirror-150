import os

from astropy.nddata import Cutout2D
from astropy import constants as const
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy import units as u
import astropy.wcs
from astropy.wcs import WCS
from matplotlib import colors
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
import numpy as np
from reproject import reproject_interp
from urllib.error import HTTPError

from src.modules.functions import get_info
from src.modules.functions import chan2freq, chan2vel, sbr2nhi
from src.modules.functions import create_pv
from src.modules.functions import plot_labels
from src.modules.get_ancillary import *
from src.modules.get_hst_cosmos import get_hst_cosmos

HI_restfreq = 1420405751.77 * u.Hz
optical_HI = u.doppler_optical(HI_restfreq)


###################################################################

# Overlay HI contours on user image

def make_overlay_usr(source, src_basename, cube_params, patch, opt, base_contour, swapx, perc, suffix='png'):
    """Overlay HI contours on top of a user provided image

    :param source: source object
    :type source: Astropy data object?
    :param src_basename: basename for the source for data files
    :type src_basename: str
    :param cube_params: parameters of the data cube
    :type cube_params: dict
    :param patch: observing patch parameters
    :type patch: dict
    :param opt: optical data
    :type opt: dict
    :param base_contour: base contour
    :type base_contour: float
    :param swapx: invert the x-axis if cdelt is negative
    :type swapx: bool
    :param perc: percentage range of data for plotting user image
    :type perc: list, float
    :param suffix: file type, defaults to 'png'
    :type suffix: str, optional
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_mom0_{}.{}'.format(source['id'], 'usr', suffix)

    if not os.path.isfile(outfile):
        try:
            print("\tMaking {} overlaid with HI contours.".format('usr'))
            hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        except FileNotFoundError:
            print("\tNo mom0 fits file. Perhaps you ran SoFiA without generating moments?")
            return
        
        nhi, nhi_label, nhi_labels = sbr2nhi(base_contour, hdulist_hi[0].header['bunit'], cube_params['bmaj'].value,
                                             cube_params['bmin'].value)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=opt.wcs)
        plot_labels(source, ax1)
        ax1.imshow(opt.data, origin='lower', cmap='viridis', vmin=np.percentile(opt.data, perc[0]),
                   vmax=np.percentile(opt.data, perc[1]))
        ax1.contour(hdulist_hi[0].data, cmap='Oranges', linewidths=1, levels=base_contour * 2 ** np.arange(10),
                    transform=ax1.get_transform(WCS(hdulist_hi[0].header)))
        ax1.text(0.5, 0.05, nhi_labels, ha='center', va='center', transform=ax1.transAxes,
                 color='white', fontsize=18)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, edgecolor='white', linewidth=1))
        if swapx:
            ax1.set_xlim(ax1.get_xlim()[::-1])
        fig.savefig(outfile, bbox_inches='tight')
        hdulist_hi.close()
    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Overlay HI contours on another image

def make_overlay(source, src_basename, cube_params, patch, opt, base_contour, suffix='png', survey='DSS2 Blue'):
    """Overlay HI contours on top of an optical image

    :param source: source object
    :type source: Astropy data object?
    :param src_basename: basename for the source for data files
    :type src_basename: str
    :param cube_params: parameters of the data cube
    :type cube_params: dict
    :param patch: observing patch parameters
    :type patch: dict
    :param opt: optical data
    :type opt: dict
    :param base_contour: base contour
    :type base_contour: float
    :param suffix: file type, defaults to 'png'
    :type suffix: str, optional
    :param survey: survey from which to use data, defaults to 'DSS2 Blue'
    :type survey: str, optional
    """
    survey_nospace = survey.replace(" ", "").lower()
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_mom0_{}.{}'.format(source['id'], survey_nospace, suffix)

    if not os.path.isfile(outfile):
        try:
            print("\tMaking {} overlaid with HI contours.".format(survey))
            hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        except FileNotFoundError:
            print("\tNo mom0 fits file. Perhaps you ran SoFiA without generating moments?")
            return

        nhi, nhi_label, nhi_labels = sbr2nhi(base_contour, hdulist_hi[0].header['bunit'], cube_params['bmaj'].value,
                                             cube_params['bmin'].value)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(opt[0].header))
        plot_labels(source, ax1)
        if survey == 'hst':
            # ax1.imshow(opt[0].data, origin='lower', cmap='twilight', norm=LogNorm(vmax=5))
            # ax1.imshow(opt[0].data, origin='lower', cmap='Greys', norm=LogNorm(vmin=-0.003, vmax=30))
            ax1.imshow(opt[0].data, origin='lower', cmap='Greys',
                       norm=PowerNorm(gamma=0.25, vmin=np.percentile(opt[0].data, 20),
                                      vmax=np.percentile(opt[0].data, 99.5)))
        else:
            ax1.imshow(opt[0].data, cmap='viridis', vmin=np.percentile(opt[0].data, 10),
                       vmax=np.percentile(opt[0].data, 99.8), origin='lower')
        # Plot positive contours
        ax1.contour(hdulist_hi[0].data, cmap='Oranges', linewidths=1, levels=base_contour * 2 ** np.arange(10),
                    transform=ax1.get_transform(WCS(hdulist_hi[0].header)))
        # Plot negative contours
        ax1.contour(hdulist_hi[0].data, cmap='BuPu_r', linewidths=1.2, linestyles='dashed',
                    levels=-1 * base_contour * 2 ** np.arange(10, 0, -1),
                    transform=ax1.get_transform(WCS(hdulist_hi[0].header)))
        ax1.text(0.5, 0.05, nhi_labels, ha='center', va='center', transform=ax1.transAxes, color='white', fontsize=18)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, edgecolor='white', linewidth=1))

        fig.savefig(outfile, bbox_inches='tight')

        hdulist_hi.close()

    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Make HI grey scale image
def make_mom0(source, src_basename, cube_params, patch, opt_head, base_contour, suffix='png'):
    """Overlay HI contours on the HI gray scale image.

    :param source: source object
    :type source: Astropy table
    :param src_basename: directory name
    :type src_basename: str
    :param cube_params: The characteristics of the beam and coordinate system of the image.
    :type cube_params: dict
    :param patch: size of the beam ellipse for plotting
    :type patch: dict
    :param opt_head: Header for the color image
    :type opt_head: FITS header
    :param base_contour: lowest HI contour
    :type base_contour: float
    :param suffix: image file type
    :type suffix: str
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_mom0.{}'.format(source['id'], suffix)

    if not os.path.isfile(outfile):
        try:
            print("\tMaking HI grey scale map.")
            hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        except FileNotFoundError:
            print("\tNo mom0 fits file. Perhaps you ran SoFiA without generating moments?")
            return

        hi_reprojected, footprint = reproject_interp(hdulist_hi, opt_head)

        nhi, nhi_label, nhi_labels = sbr2nhi(base_contour, hdulist_hi[0].header['bunit'], cube_params['bmaj'].value,
                                             cube_params['bmin'].value)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(opt_head))
        plot_labels(source, ax1, x_color='white')
        im = ax1.imshow(hi_reprojected, cmap='gray_r', origin='lower')
        ax1.set(facecolor="white")  # Doesn't work with the color im
        # Plot positive contours
        ax1.contour(hi_reprojected, cmap='Oranges_r', linewidths=1.2, levels=base_contour * 2 ** np.arange(10))
        # Plot negative contours
        ax1.contour(hi_reprojected, cmap='YlOrBr_r', linewidths=1.2, linestyles='dashed',
                    levels=-1 * base_contour * 2 ** np.arange(10, 0, -1))
        ax1.text(0.5, 0.05, nhi_labels, ha='center', va='center', transform=ax1.transAxes, fontsize=18)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, facecolor='darkorange', edgecolor='black', linewidth=1))
        cb_ax = fig.add_axes([0.91, 0.11, 0.02, 0.76])
        cbar = fig.colorbar(im, cax=cb_ax)
        cbar.set_label("HI Intensity [{}]".format(hdulist_hi[0].header['bunit']), fontsize=18)

        fig.savefig(outfile, bbox_inches='tight')

        hdulist_hi.close()

    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Make HI significance image
def make_snr(source, src_basename, cube_params, patch, opt_head, base_contour, suffix='png'):
    """Plot the pixel-by-pixel signal-to-noise ratio for the total intensity map of the source.

    :param source: source object
    :type source: Astropy table
    :param src_basename: directory name
    :type src_basename: str
    :param cube_params: The characteristics of the beam and coordinate system of the image.
    :type cube_params: dict
    :param patch: size of the beam ellipse for plotting
    :type patch: dict
    :param opt_head: Header for the color image
    :type opt_head: FITS header
    :param base_contour: lowest HI contour
    :type base_contour: float
    :param suffix: image file type
    :type suffix: str
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_snr.{}'.format(source['id'], suffix)

    if not os.path.isfile(outfile):
        try:
            print("\tMaking pixel SNR map.")
            hdulist_snr = fits.open(src_basename + '_{}_snr.fits'.format(str(source['id'])))
        except FileNotFoundError:
            print("\tNo SNR fits file. Perhaps you ran SoFiA without generating moments?")
            return

        hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        snr_reprojected, footprint = reproject_interp(hdulist_snr, opt_head)
        hi_reprojected, footprint = reproject_interp(hdulist_hi, opt_head)

        nhi, nhi_label, nhi_labels = sbr2nhi(base_contour, hdulist_hi[0].header['bunit'], cube_params['bmaj'].value,
                                             cube_params['bmin'].value)
        wa_cmap = colors.ListedColormap(['w', 'royalblue', 'limegreen', 'yellow', 'orange', 'r'])
        boundaries = [0, 1, 2, 3, 4, 5, 6]
        norm = colors.BoundaryNorm(boundaries, wa_cmap.N, clip=True)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(opt_head))
        plot_labels(source, ax1)
        ax1.set(facecolor="white")  # Doesn't work with the color im
        im = ax1.imshow(snr_reprojected, cmap=wa_cmap, origin='lower', norm=norm)
        ax1.contour(hi_reprojected, linewidths=2, levels=[base_contour, ], colors=['k', ])
        ax1.text(0.5, 0.05, nhi_label, ha='center', va='center', transform=ax1.transAxes, fontsize=18)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, facecolor='gold', edgecolor='indigo', linewidth=1))
        cb_ax = fig.add_axes([0.91, 0.11, 0.02, 0.76])
        cbar = fig.colorbar(im, cax=cb_ax)
        cbar.set_label("Pixel SNR", fontsize=18)
        fig.savefig(outfile, bbox_inches='tight')
        hdulist_hi.close()

    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Make velocity map for object
def make_mom1(source, src_basename, cube_params, patch, opt_head, HIlowest, opt_view=6*u.arcmin, suffix='png', sofia=2):
    """

    :param source: source object
    :type source: Astropy table
    :param src_basename: directory name
    :type src_basename: str
    :param cube_params: The characteristics of the beam and coordinate system of the image.
    :type cube_params: dict
    :param patch: size of the beam ellipse for plotting
    :type patch: dict
    :param opt_head: Header for the color image
    :type opt_head: FITS header
    :param HIlowest: lowest HI contour
    :type HIlowest: float
    :param opt_view: requested size of the image for regriding
    :type opt_view: quantity
    :param suffix: image file type
    :type suffix: str
    :param sofia: major sofia version number
    :type sofia: int
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_mom1.{}'.format(source['id'], suffix)

    if not os.path.isfile(outfile):

        try:
            print("\tMaking velocity map.")
            mom1 = fits.open(src_basename + '_{}_mom1.fits'.format(source['id']))
        except FileNotFoundError:
            print("\tNo mom1 fits file. Perhaps you ran SoFiA without generating moments?")
            return

        # Do some preparatory work depending on the units of the spectral axis on the input cube.
        convention = 'Optical'
        if 'freq' in source.colnames:
            # Convert moment map from Hz into units of km/s
            mom1[0].data = (mom1[0].data * u.Hz).to(u.km / u.s, equivalencies=optical_HI).value
            # Calculate spectral quantities for plotting
            v_sys = (source['freq'] * u.Hz).to(u.km/u.s, equivalencies=optical_HI).value
            # Currently SoFiA-2 puts out frequency w20/w50 in Hz units (good)
            w50 = (const.c * source['w50'] * u.Hz / (source['freq'] * u.Hz)).to(u.km/u.s,
                                                                                equivalencies=optical_HI).value
            w20 = (const.c * source['w20'] * u.Hz / (source['freq'] * u.Hz)).to(u.km/u.s,
                                                                                equivalencies=optical_HI).value
            if sofia == 2:
                freqmin = chan2freq(source['z_min'], src_basename + '_{}_cube.fits'.format(source['id']))
                freqmax = chan2freq(source['z_max'], src_basename + '_{}_cube.fits'.format(source['id']))
            elif sofia == 1:
                freqmin = chan2freq(source['z_min'], src_basename + '_{}.fits'.format(source['id']))
                freqmax = chan2freq(source['z_max'], src_basename + '_{}.fits'.format(source['id']))
            velmax = freqmin.to(u.km / u.s, equivalencies=optical_HI).value
            velmin = freqmax.to(u.km / u.s, equivalencies=optical_HI).value
        else:
            # Convert moment map from m/s into units of km/s.
            mom1[0].data = (mom1[0].data * u.m / u.s).to(u.km / u.s).value
            # Calculate spectral quantities for plotting
            v_sys = (source['v_col'] * u.m / u.s).to(u.km / u.s).value
            # SoFiA-2 puts out velocity w20/w50 in pixel units. https://github.com/SoFiA-Admin/SoFiA-2/issues/63
            w50 = (source['w50'] * u.m / u.s).to(u.km / u.s).value
            w20 = (source['w20'] * u.m / u.s).to(u.km / u.s).value
            velmin = chan2vel(source['z_min'], src_basename +
                              '_{}_cube.fits'.format(source['id'])).to(u.km / u.s).value
            velmax = chan2vel(source['z_max'], src_basename +
                              '_{}_cube.fits'.format(source['id'])).to(u.km / u.s).value
            if cube_params['spec_axis'] == 'VRAD':
                convention = 'Radio'

        mom1_reprojected, footprint = reproject_interp(mom1, opt_head)

        # Only plot values above the lowest calculated HI value:
        hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        hi_reprojected, footprint = reproject_interp(hdulist_hi, opt_head)

        mom1_reprojected[hi_reprojected < HIlowest] = np.nan

        hi_pos = SkyCoord(source['pos_x'], source['pos_y'], unit='deg')
        kinpa = source['kin_pa'] * u.deg

        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(opt_head))
        plot_labels(source, ax1)
        im = ax1.imshow(mom1_reprojected, cmap='RdBu_r', origin='lower')
        vel_maxhalf = np.max([np.abs(velmax-v_sys), np.abs(v_sys-velmin)])
        for vunit in [5, 10, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150]:
            n_contours = vel_maxhalf // vunit
            if n_contours <= 4:
                break
        levels = [v_sys-3*vunit, v_sys-2*vunit, v_sys-1*vunit, v_sys, v_sys+1*vunit, v_sys+2*vunit, v_sys+3*vunit]
        clevels = ['white', 'lightgray', 'dimgrey', 'black', 'dimgrey', 'lightgray', 'white']
        cf = ax1.contour(mom1_reprojected, colors=clevels, levels=levels, linewidths=0.6)
        v_sys_label = "$v_{{sys}}$ = {}  $W_{{50}}$ = {}  $W_{{20}}$ = {} km/s".format(int(v_sys), int(w50), int(w20))
        # Plot kin_pa from HI center of galaxy
        ax1.annotate("", xy=((hi_pos.ra + 0.45 * opt_view[0] * np.sin(kinpa) / np.cos(hi_pos.dec)).deg,
                             (hi_pos.dec + 0.45 * opt_view[0] * np.cos(kinpa)).deg), xycoords=ax1.get_transform('icrs'),
                     xytext=((hi_pos.ra - 0.45 * opt_view[0] * np.sin(kinpa) / np.cos(hi_pos.dec)).deg,
                             (hi_pos.dec - 0.45 * opt_view[0] * np.cos(kinpa)).deg), textcoords=ax1.get_transform('icrs'),
                     arrowprops=dict(arrowstyle="->,head_length=0.8,head_width=0.4", connectionstyle="arc3",
                                     linestyle='--'))
        ax1.text(0.5, 0.05, v_sys_label, ha='center', va='center', transform=ax1.transAxes, color='black', fontsize=18)
        ax1.text(0.95, 0.5, "$\Delta v_{{contours}}$ = {} km/s".format(int(vunit)), ha='center', va='center',
                 transform=ax1.transAxes, color='black', fontsize=18, rotation=90)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, edgecolor='darkred', linewidth=1))
        cb_ax = fig.add_axes([0.91, 0.11, 0.02, 0.76])
        cbar = fig.colorbar(im, cax=cb_ax)
        cbar.add_lines(cf)
        cbar.set_label("{} {} Velocity [km/s]".format(cube_params['spec_sys'].capitalize(), convention), fontsize=18)

        fig.savefig(outfile, bbox_inches='tight')

        mom1.close()

    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Overlay HI contours on false color optical image
def make_color_im(source, src_basename, cube_params, patch, color_im, opt_head, base_contour, suffix='png',
                  survey='panstarrs'):
    """Overlay HI contours on a false color image.

    :param source: source object
    :type source: Astropy table
    :param src_basename: directory name
    :type src_basename: str
    :param cube_params: The characteristics of the beam and coordinate system of the image.
    :type cube_params: dict
    :param patch: size of the beam ellipse for plotting
    :type patch: dict
    :param color_im: color image
    :type color_im: NDarray?
    :param opt_head: Header for the color image
    :type opt_head: FITS header
    :param base_contour: lowest HI contour
    :type base_contour: float
    :param suffix: image file type
    :type suffix: str
    :param survey: survey name to retrieve color image
    :type survey: str
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_mom0_{}.{}'.format(source['id'], survey, suffix)

    if survey == 'panstarrs': survey = 'PanSTARRS'
    elif survey == 'decals': survey = 'DECaLS'

    if not os.path.isfile(outfile):
        print("\tMaking {} image overlaid with HI contours.".format(survey))
        hdulist_hi = fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id'])))
        hi_reprojected, footprint = reproject_interp(hdulist_hi, opt_head)

        nhi, nhi_label, nhi_labels = sbr2nhi(base_contour, hdulist_hi[0].header['bunit'], cube_params['bmaj'].value,
                                             cube_params['bmin'].value)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(opt_head))
        # ax1.set_facecolor("darkgray")   # Doesn't work with the color im
        ax1.imshow(color_im, origin='lower')
        plot_labels(source, ax1, x_color='white')
        ax1.contour(hi_reprojected, cmap='Oranges', linewidths=1, levels=base_contour * 2 ** np.arange(10))
        ax1.text(0.5, 0.05, nhi_labels, ha='center', va='center', transform=ax1.transAxes,
                 color='white', fontsize=18)
        ax1.add_patch(Ellipse((0.92, 0.9), height=patch['height'], width=patch['width'], angle=cube_params['bpa'],
                              transform=ax1.transAxes, edgecolor='lightgray', linewidth=1))
        fig.savefig(outfile, bbox_inches='tight')
    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


# Make pv plot for object
def make_pv(source, src_basename, cube_params, opt_view=6*u.arcmin, suffix='png'):
    """Plot the position-velocity slice for the source.

    :param source: source object
    :type source: Astropy table
    :param src_basename: directory name
    :type src_basename: str
    :param cube_params: The characteristics of the beam and coordinate system of the image.
    :type cube_params: dict
    :param opt_view: requested size of the image for regriding
    :type opt_view: quantity
    :param suffix: image file type
    :type suffix: str
    :return:
    """
    outfile = src_basename.replace('cubelets', 'figures') + '_{}_pv.{}'.format(source['id'], suffix)

    if not os.path.isfile(outfile):
        try:
            print("\tMaking pv slice.")
            pv = fits.open(src_basename + '_{}_pv.fits'.format(str(source['id'])))
        except FileNotFoundError:
            print("\tNo pv fits file. Perhaps you ran source finding with an old version of SoFiA-2?")
            return

        # For plotting mask, reproject needs to know unit explicitly, whereas WCS assumes it is degs
        pv[0].header['CUNIT1'] = 'deg'

        wcs_pv = WCS(pv[0].header, fix=True, translate_units='shd')
        ang1, freq1 = wcs_pv.wcs_pix2world(0, 0, 0)
        ang2, freq2 = wcs_pv.wcs_pix2world(pv[0].header['NAXIS1'] - 1, pv[0].header['NAXIS2'] - 1, 0)
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111, projection=WCS(pv[0].header, fix=True, translate_units='shd'))
        pvd = pv[0].data
        pvd_rms = 1.4826 * np.nanmedian(np.abs(pvd[pvd < 0]))  # Estimate rms as MAD of negative pix assuming median = 0

        # Append second color map for above the 3 sigma noise:
        # https://matplotlib.org/3.5.0/tutorials/colors/colormapnorms.html#twoslopenorm-different-mapping-on-either-side-of-a-center
        colors_noise = plt.cm.gray(np.linspace(0, 1, 256))
        colors_galaxy = plt.cm.afmhot(np.linspace(1, 0.4, 256))
        all_colors = np.vstack((colors_noise, colors_galaxy))
        pvd_map = colors.LinearSegmentedColormap.from_list('pvd_map', all_colors)
        divnorm = colors.TwoSlopeNorm(vmin=-3*pvd_rms, vcenter=+3*pvd_rms, vmax=15*pvd_rms)
        # ax1.imshow(pvd, cmap='gray', aspect='auto', vmin=-3*pvd_rms, vmax=+3*pvd_rms)
        ax1.imshow(pvd, cmap=pvd_map, aspect='auto', norm=divnorm)

        # if np.all (np.isnan (pv[0].data)): continue
        # Plot positive contours
        ax1.contour(pvd, colors=['k', ], levels=3**np.arange(1, 10)*pvd_rms)
        # Plot negative contours
        ax1.contour(pvd, colors=['w', ], levels=-1 * 3**np.arange(10, 0, -1) * pvd_rms, linestyles=['dashed', ])

        ax1.autoscale(False)
        if os.path.isfile(src_basename + '_{}_mask.fits'.format(str(source['id']))):
            print("\tReading in mask cubelet.")
            mask_pv = create_pv(source, src_basename + '_{}_mask.fits'.format(str(source['id'])), opt_view=opt_view[0])
            if mask_pv:
                # Extract_pv has a header bug, reset the reference pixel:
                mask_pv.header['CRPIX1'] = mask_pv.header['NAXIS1'] / 2 + 1
                ax1.contour(mask_pv.data, colors='red', levels=[0.01], transform=ax1.get_transform(WCS(mask_pv.header)))
        else:
            print("\tNo mask cubelet.  Will continue without plotting mask boundaries on pv plot.")
        ax1.plot([0.0, 0.0], [freq1, freq2], c='orange', linestyle='--', linewidth=0.75,
                 transform=ax1.get_transform('world'))
        ax1.set_title(source['name'], fontsize=16)
        ax1.tick_params(axis='both', which='major', labelsize=18)
        ax1.set_xlabel('Angular Offset [deg]', fontsize=16)
        ax1.text(0.5, 0.05, 'Kinematic PA = {:5.1f} deg'.format(source['kin_pa']), ha='center', va='center',
                 transform=ax1.transAxes, color='orange', fontsize=18)
        ax1.coords[1].set_ticks_position('l')

        convention = 'Optical'
        if 'freq' in source.colnames:
            freq_sys = source['freq']
            ax1.plot([ang1, ang2], [freq_sys, freq_sys], c='orange', linestyle='--',
                     linewidth=0.75, transform=ax1.get_transform('world'))
            ax1.set_ylabel('Frequency [MHz]', fontsize=16)
            ax1.coords[1].set_format_unit(u.MHz)
            # freq_yticks = ax1.get_yticks()  # freq auto yticks from matplotlib
            ax2 = ax1.twinx()
            vel1 = const.c.to(u.km / u.s).value * (HI_restfreq.value / freq1 - 1)
            vel2 = const.c.to(u.km / u.s).value * (HI_restfreq.value / freq2 - 1)
            ax2.set_ylim(vel1, vel2)
            ax2.set_ylabel('{} {} velocity [km/s]'.format(cube_params['spec_sys'].capitalize(), convention))
        else:
            if cube_params['spec_axis'] == 'VRAD':
                convention = 'Radio'
            vel_sys = source['v_col']
            ax1.plot([ang1, ang2], [vel_sys, vel_sys], c='orange', linestyle='--',
                     linewidth=0.75, transform=ax1.get_transform('world'))
            ax1.coords[1].set_format_unit(u.km / u.s)
            ax1.set_ylabel('{} {} velocity [km/s]'.format(cube_params['spec_sys'].capitalize(), convention,
                                                          fontsize=18))

        if pv[0].header['cdelt2'] < 0:
            ax1.set_ylim(ax1.get_ylim()[::-1])
            ax1.set_xlim(ax1.get_xlim()[::-1])
        fig.savefig(outfile, bbox_inches='tight')
        pv.close()

    else:
        print('\t{} already exists. Will not overwrite.'.format(outfile))

    return


def main(source, src_basename, opt_view=6*u.arcmin, suffix='png', sofia=2, beam=None, chan_width=None, surveys=None,
         snr_range=[2, 3], user_image=None, user_range=[10., 99.]):

    print("\tStart making spatial images.")

    # Get beam information from the source cubelet
    if sofia == 2:
        try:
            cube_params = get_info(src_basename + '_{}_cube.fits'.format(source['id']), beam)
        except FileNotFoundError:
            # Exits, but need to see if one can proceed without this...say with only mom0.fits as min requirement?
            print("\tWARNING: No cubelet to match source {}."
                  " Try retrieving coordinate info from moment 0 map.".format(source['id']))
            try:
                cube_params = get_info(src_basename + '_{}_mom0.fits'.format(source['id']), beam)
            except FileNotFoundError:
                print("\tERROR: No cubelet or mom0 to match source {}.\n".format(source['id']))
                exit()
    elif sofia == 1:
        cube_params = get_info(src_basename + '_{}.fits'.format(source['id']), beam)

    opt_head = None

    # Calculate base contour from the SNR map and requested SNR range
    try:
        with fits.open(src_basename + '_{}_snr.fits'.format(str(source['id']))) as hdulist_snr, \
                fits.open(src_basename + '_{}_mom0.fits'.format(str(source['id']))) as hdulist_hi:
            HIlowest = np.median(hdulist_hi[0].data[(hdulist_snr[0].data > snr_range[0]) *
                                                    (hdulist_snr[0].data < snr_range[1])])
        print("\tThe first HI contour defined at SNR = {0} has level = {1:.3e} (mom0 data units).".format(snr_range,
                                                                                                          HIlowest))
    # If no SNR map use the channel width of the original data (provided by user if necessary) for lowest HI contour.
    except FileNotFoundError:
        if os.path.isfile(src_basename + '_{}_mom0.fits'.format(str(source['id']))):
            print("\tNo SNR fits file found. Will determine lowest contour based on rms in catalog,"
                  " min(user provided SNR), and user provided channel width.")
            # Probably never uses the first instance of if statement (this would be weird to save in mom0 map)
            if cube_params['chan_width']:
                HIlowest = source['rms'] * np.nanmin(snr_range) * cube_params['chan_width']
            # Assumes user gives chan_width in correct units of original data but SIP knows units from mom0 header!
            elif chan_width:
                HIlowest = source['rms'] * np.nanmin(snr_range) * chan_width
            else:
                print("\tWARNING: No user provided channel width. Check figures! Either provide channel width,"
                      " or rms in mom0 map units.")
                HIlowest = source['rms'] * np.nanmin(snr_range)
            print("\tThe first HI contour defined at SNR = {0} has level = {1:.3e} (mom0 data units)."
                  " ".format(np.nanmin(snr_range), HIlowest))
        else:
            print("\tERROR: No mom0 to match source {}.\n".format(source['id']))
            return

    # Get the position of the source to retrieve a survey image
    # Temporarily replace source coords w/ ICRS ra,dec or Gal l,b for plotting in the rest (won't change catalog file).
    if 'ra' in source.colnames:
        hi_pos = SkyCoord(ra=source['ra'], dec=source['dec'], unit='deg', equinox=cube_params['equinox'],
                          frame=cube_params['frame'])
        hi_pos_common = hi_pos.transform_to('icrs')
        source['pos_x'] = hi_pos_common.ra.deg
        source['pos_y'] = hi_pos_common.dec.deg
    if 'l' in source.colnames:
        hi_pos_gal = SkyCoord(l=source['l'], b=source['b'], unit='deg', frame=cube_params['frame'])
        hi_pos_common = hi_pos_gal
        source['pos_x'] = [hi_pos_common.l.deg]
        source['pos_y'] = [hi_pos_common.b.deg]

    # Calculate the size of the survey image for the moment maps
    Xc = source['x']
    Yc = source['y']
    Xmin = source['x_min']
    Ymin = source['y_min']
    Xmax = source['x_max']
    Ymax = source['y_max']
    Xsize = np.array([((Xmax - Xc) * cube_params['cellsize']).to(u.arcmin).value,
                      ((Xc - Xmin) * cube_params['cellsize']).to(u.arcmin).value])
    Ysize = np.array([((Ymax - Yc) * cube_params['cellsize']).to(u.arcmin).value,
                      ((Yc - Ymin) * cube_params['cellsize']).to(u.arcmin).value])
    if np.any(Xsize > opt_view.value / 2) | np.any(Ysize > opt_view.value / 2):
        opt_view = np.max([Xsize, Ysize]) * 2 * 1.05
        print("\tImage size bigger than default. Now {:.2f} arcmin".format(opt_view))
        opt_view = np.array([opt_view,]) * u.arcmin

    # Calculate the size of the beam (plotted as a fraction of the image size)
    patch_height = (cube_params['bmaj'] / opt_view).decompose()
    patch_width = (cube_params['bmin'] / opt_view).decompose()
    patch = {'width': patch_width, 'height': patch_height}

    # Extract cutout from user image
    # !!! Actually we do not need to read the entire image every single time. We want to read it just once.
    # I leave this for later.
    if user_image:
        print("\tExtracting cutout from image {0:s}".format(user_image))
        with fits.open(user_image) as usrim:
            usrim_d = usrim[0].data
            usrim_h = usrim[0].header
            if ('cdelt1' in usrim_h) and ('cdelt2' in usrim_h):
                usrim_pix_x, usrim_pix_y = usrim_h['cdelt1'], np.abs(usrim_h['cdelt2'])
            elif ('cd1_1' in usrim_h) and ('cd2_2' in usrim_h):
                usrim_pix_x, usrim_pix_y = usrim_h['cd1_1'], np.abs(usrim_h['cd2_2'])
            else:
                print("\tCould not determine pixel size of user image. Aborting.")
                exit()
            if usrim_pix_x > 0:
                swapx = True
            else:
                swapx = False
            usrim_pix_x = np.abs(usrim_pix_x)
            usrim_wcs = WCS(usrim_h)
        print('\tImage loaded. Extracting {0}-wide 2D cutout centred at RA = {1}, Dec = {2}.'.format(opt_view, hi_pos.ra, hi_pos.dec))
        try:
            usrim_cut = Cutout2D(usrim_d, hi_pos, [opt_view.to(u.deg).value/usrim_pix_y, opt_view.to(u.deg).value/usrim_pix_x], wcs=usrim_wcs)
            make_overlay_usr(source, src_basename, cube_params, patch, usrim_cut, HIlowest, swapx, user_range, suffix='png')
            opt_head = usrim_cut.wcs.to_header()
            # wcs.to_header() seems to have a bug where it doesn't include the axis information.
            opt_head['NAXIS'] = 2
            opt_head['NAXIS1'] = usrim_cut.wcs.array_shape[0]
            opt_head['NAXIS2'] = usrim_cut.wcs.array_shape[1]
        except:
            print('\tWARNING: 2D cutout extraction failed. Source outside user image? Will try again with the next source.')
    else:
        print("\tNo user image given. Proceeding with the download of any requested archive images.")

    # For CHILES: plot HI contours on HST image if desired.
    if ('hst' in surveys) | ('HST' in surveys):
        hst_opt_view = 40 * u.arcsec
        if np.any(Xsize > hst_opt_view.to(u.arcmin).value / 2) | np.any(Ysize > hst_opt_view.to(u.arcmin).value / 2):
            hst_opt_view = (np.max([Xsize, Ysize]) * 2 * 1.05 * u.arcmin).to(u.arcsec)
        hst_opt = get_hst_cosmos(source, opt_view=hst_opt_view)
        if hst_opt:
            patch_height = (cube_params['bmaj'] / hst_opt_view).decompose()
            patch_width = (cube_params['bmin'] / hst_opt_view).decompose()
            patch_hst = {'width': patch_width, 'height': patch_height}
            make_overlay(source, src_basename, cube_params, patch_hst, hst_opt, HIlowest, suffix=suffix,
                         survey='hst')
        if surveys[0] == 'hst':
            opt_head = hst_opt[0].header
            opt_view = hst_opt_view
            patch = patch_hst
        surveys.remove('hst')

    # Create a false color optical panstarrs overlay, if requested, or if dss2 fails for some reason:
    if ('panstarrs' in surveys) and (hi_pos_common.frame.name != 'galactic'):
        pstar_im, pstar_head = get_panstarrs(hi_pos_common, opt_view=opt_view)
        if pstar_im:
            make_color_im(source, src_basename, cube_params, patch, pstar_im, pstar_head, HIlowest,
                          suffix=suffix, survey='panstarrs')
        if surveys[0] == 'panstarrs':
            opt_head = pstar_head
        surveys.remove('panstarrs')
    elif ('panstarrs' in surveys) and (hi_pos_common.frame.name == 'galactic'):
        print("\t'panstarrs' image retrieval not supported for catalog in Galactic coordinates.")
        surveys.remove('panstarrs')

    # If requested plot HI contours on DECaLS imaging
    if ('decals' in surveys) and (hi_pos_common.frame.name != 'galactic'):
        decals_im, decals_head = get_decals(hi_pos_common, opt_view=opt_view)
        make_color_im(source, src_basename, cube_params, patch, decals_im, decals_head, HIlowest, suffix=suffix,
                      survey='decals')
        if surveys[0] == 'decals':
            opt_head = decals_head
        surveys.remove('decals')
    elif ('decals' in surveys) and (hi_pos_common.frame.name == 'galactic'):
        print("\t'decals' image retrieval not supported for catalog in Galactic coordinates.")
        surveys.remove('decals')

    # If requested, plot the HI contours on any number of survey images available through SkyView.
    if len(surveys) > 0:
        for survey in surveys:
            try:
                overlay_image = get_skyview(hi_pos_common, opt_view=opt_view, survey=survey)
                make_overlay(source, src_basename, cube_params, patch, overlay_image, HIlowest, suffix=suffix,
                             survey=survey)
                if surveys[0] == survey:
                    opt_head = overlay_image[0].header
            except ValueError:
                print("\tERROR: \"{}\" may not among the survey hosted at skyview or survey names recognized by "
                      "astroquery. \n\t\tSee SkyView.list_surveys or SkyView.survey_dict from astroquery for valid "
                      "surveys.".format(survey))
            except HTTPError:
                print("\tERROR: http error 404 returned from SkyView query for {} survey image. Trying with"
                      " cache=False.".format(survey))
                try:
                    overlay_image = get_skyview(hi_pos_common, opt_view=opt_view, survey=survey, cache=False)
                    make_overlay(source, src_basename, cube_params, patch, overlay_image, HIlowest, suffix=suffix,
                                 survey=survey)
                    if surveys[0] == survey:
                        opt_head = overlay_image[0].header
                except:
                    print("\t\tSecond attempt failed. Either survey doesn't cover this area, or server failed.  Try again later?")
            except:
                print("\tERROR: general error attempting return image from SkyView query for {} survey. Trying with"
                      " cache=False.".format(survey))
                try:
                    overlay_image = get_skyview(hi_pos_common, opt_view=opt_view, survey=survey, cache=False)
                    make_overlay(source, src_basename, cube_params, patch, overlay_image, HIlowest, suffix=suffix,
                                 survey=survey)
                    if surveys[0] == survey:
                        opt_head = overlay_image[0].header
                except:
                    print("\t\tSecond attempt failed. Try again later?")

    # Make the rest of the images if there is a survey image to regrid to.
    if opt_head:
        make_mom0(source, src_basename, cube_params, patch, opt_head, HIlowest, suffix=suffix)
        make_snr(source, src_basename, cube_params, patch, opt_head, HIlowest, suffix=suffix)
        make_mom1(source, src_basename, cube_params, patch, opt_head, HIlowest, opt_view=opt_view, suffix=suffix,
                  sofia=2)

    # Make pv if it was created (only in SoFiA-1); not dependent on having a survey image to regrid to.
    make_pv(source, src_basename, cube_params, opt_view=opt_view, suffix=suffix)

    plt.close('all')

    print("\tDone making spatial images of the spectral line source {}: {}.".format(source['id'], source['name']))

    return True


if __name__ == '__main__':

    main(source, src_basename, opt_view=6*u.arcmin, suffix='png', snr_range=[2, 3], user_image=None)
