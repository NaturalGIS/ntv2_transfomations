# -*- coding: utf-8 -*-

"""
***************************************************************************
    transformations.py
    ---------------------
    Date                 : April 2019
    Copyright            : (C) 2019 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'April 2019'
__copyright__ = '(C) 2019, Alexander Bruy'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

pluginPath = os.path.dirname(__file__)
if (" " in pluginPath):
    #Default plugin locations: http://planet.qgis.org/planet/user/3/tag/qgis3/
    #BUG on Mac OS X: the nadgrids pointing to the default plugin folder which contains spaces and therefore the ogr command fails!
    #WORKAROUND: create symlink in userdirectory without spaces
    #WORKAROUND ALTERNATIVE: use the PROJ_LIB environment variable to point to the plugin directory and reference the grids by relative paths
    symlink = os.path.join(os.path.expanduser("~"),".qgis3_ntv2_transformation_plugin")
    try:
        os.symlink(pluginPath,symlink)
        pluginPath = symlink
        pass
    except FileExistsError:
        pluginPath = symlink
        pass
    except FileNotFoundError:
        print("Cannot create Symbolic link to map your plugin directory.")
        raise

NO_TRANSFORMATION = 'No transformation found for given parameters combination.'


def at_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == 'AT_GIS_GRID':
        if epsg == 4312:
            return True, '+proj=longlat +ellps=bessel +nadgrids={} +wktext +no_defs'.format(gridFile)
        elif epsg == 31254:
            return True, '+proj=tmerc +lat_0=0 +lon_0=10.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 31255:
            return True, '+proj=tmerc +lat_0=0 +lon_0=13.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 31256:
            return True, '+proj=tmerc +lat_0=0 +lon_0=16.33333333333333 +k=1 +x_0=0 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 31257:
            return True ,'+proj=tmerc +lat_0=0 +lon_0=10.33333333333333 +k=1 +x_0=150000 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 31258:
            return True, '+proj=tmerc +lat_0=0 +lon_0=13.33333333333333 +k=1 +x_0=450000 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 31259:
            return True, '+proj=tmerc +lat_0=0 +lon_0=16.33333333333333 +k=1 +x_0=750000 +y_0=-5000000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def cat_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == '100800401':
        if epsg == 23031:
            return True, '+proj=utm +zone=31 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def de_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == 'BETA2007':
        if epsg == 31467:
            return True, '+proj=tmerc +lat_0=0 +lon_0=9 +k=1 +x_0=3500000 +y_0=0 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
    if grid == 'BY_KANU':
        if epsg == 5678:
            return True, '+proj=tmerc +lat_0=0 +lon_0=12 +k=1 +x_0=4500000 +y_0=0 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def es_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == 'PENR2009':
        if epsg == 23029:
            return True, '+proj=utm +zone=29 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 23030:
            return True, '+proj=utm +zone=30 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 23031:
            return True, '+proj=utm +zone=31 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def uk_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == 'OSTN02_NTv2':
        if epsg == 27700:
            return True, '+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def hr_transformation(epsg, grid):
    gridFile = os.path.join(pluginPath, 'grids', '{}.gsb'.format(grid))
    if grid == 'HRNTv2':
        if epsg == 5:
            return True, '+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=15 +k=0.9999 +x_0=5500000 +y_0=0 +ellps=bessel +nadgrids={} +wktext +units=m'.format(gridFile)
        if epsg == 6:
            return True, '+proj=tmerc +pm=greenwich +lat_0=0 +lon_0=18 +k=0.9999 +x_0=6500000 +y_0=0 +ellps=bessel +nadgrids={} +wktext +units=m'.format(gridFile)

    return False, NO_TRANSFORMATION


def it_transformation(epsg, grid):
    if grid == 'RER_ETRS89':
        if epsg == 3003:
            gridFile = os.path.join(pluginPath, 'grids', 'RER_AD400_MM_ETRS89_V1A.gsb')
            return True, '+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 23032:
            gridFile = os.path.join(pluginPath, 'grids', 'RER_ED50_ETRS89_GPS7_K2.GSB')
            return True, '+proj=utm +zone=32 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def nl_transformation(epsg, grid):
    if grid == 'naptrans2008':
        if epsg == 28992:
            gridFile = os.path.join(pluginPath, 'grids', 'rdtrans2008.gsb')
            geoidFile = os.path.join(pluginPath, 'grids', 'naptrans2008.gtx')
            return True, '+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +nadgrids={} +geoidgrids={} +wktext +units=m +no_defs'.format(gridFile, geoidFile)
    elif grid == 'rdtrans2008':
        gridFile = os.path.join(pluginPath, 'grids', 'rdtrans2008.gsb')
        if epsg == 28992:
            return True, '+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)

    return False, NO_TRANSFORMATION


def pt_transformation(epsg, grid):
    if grid == 'pt_e89':
        if epsg == 20791:
            gridFile = os.path.join(pluginPath, 'grids', 'ptLX_e89.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=0 +y_0=0 +ellps=intl +nadgrids={} +wktext +pm=lisbon +units=m +no_defs'.format(gridFile)
        elif epsg == 20790:
            gridFile = os.path.join(pluginPath, 'grids', 'ptLX_e89.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids={} +wktext +pm=lisbon +units=m +no_defs'.format(gridFile)
        elif epsg == 27493:
            gridFile = os.path.join(pluginPath, 'grids', 'pt73_e89.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=180.598 +y_0=-86.99 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 102160:
            gridFile = os.path.join(pluginPath, 'grids', 'pt73_e89.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=200180.598 +y_0=299913.01 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 23029:
            gridFile = os.path.join(pluginPath, 'grids', 'ptED_e89.gsb')
            return True, '+proj=utm +zone=29 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
    elif grid == 'PT_ETRS89_geo':
        if epsg == 20791:
            gridFile = os.path.join(pluginPath, 'grids', 'DLX_ETRS89_geo.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=0 +y_0=0 +ellps=intl +nadgrids={} +wktext +pm=lisbon +units=m +no_defs'.format(gridFile)
        elif epsg == 20790:
            gridFile = os.path.join(pluginPath, 'grids', 'DLX_ETRS89_geo.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=1 +k=1 +x_0=200000 +y_0=300000 +ellps=intl +nadgrids={} +wktext +pm=lisbon +units=m +no_defs'.format(gridFile)
        elif epsg == 27493:
            gridFile = os.path.join(pluginPath, 'grids', 'D73_ETRS89_geo.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=180.598 +y_0=-86.99 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 102160:
            gridFile = os.path.join(pluginPath, 'grids', 'D73_ETRS89_geo.gsb')
            return True, '+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=200180.598 +y_0=299913.01 +ellps=intl +nadgrids={} +wktext +units=m +no_defs'.format(gridFile)
        elif epsg == 23029:
            return False, 'Transformation to "ED50 UTM 29N [EPSG:23029]" only possible with grid from José Alberto Gonçalves'

    return False, NO_TRANSFORMATION


def au_transformation_agd(src, zone):
    if src == 202:
        gridFile = os.path.join(pluginPath, 'grids', 'A66_National_13_09_01.gsb')
        return True, '+proj=utm +zone={} +south +ellps=aust_SA +towgs84=-117.808,-51.536,137.784,0.303,0.446,0.234,-0.29 +units=m +no_defs +nadgrids={} +wktext'.format(zone, gridFile)
    elif src == 4202:
        gridFile = os.path.join(pluginPath, 'grids', 'A66_National_13_09_01.gsb')
        return True, '+proj=longlat +ellps=aust_SA +towgs84=-117.808,-51.536,137.784,0.303,0.446,0.234,-0.29 +no_defs +nadgrids={} +wktext'.format(gridFile)
    elif src == 203:
        gridFile = os.path.join(pluginPath, 'grids', 'National_84_02_07_01.gsb')
        return True, '+proj=utm +zone={} +south +ellps=aust_SA +towgs84=-134,-48,149,0,0,0,0 +units=m +no_defs +nadgrids={} +wktext'.format(zone, gridFile)
    elif src == 4203:
        gridFile = os.path.join(pluginPath, 'grids', 'National_84_02_07_01.gsb')
        return True, '+proj=longlat +ellps=aust_SA +towgs84=-134,-48,149,0,0,0,0 +no_defs +nadgrids={} +wktext'.format(gridFile)
    elif src == 283:
        return True, '+proj=utm +zone={} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +wktext'.format(zone)
    elif src == 4283:
        return True, '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +wktext'

    return False, NO_TRANSFORMATION


def au_transformation_gda(src, dst, zone):
    src_proj = ''
    src_epsg = ''
    dst_proj = ''
    dst_epsg = ''

    if src == '283':
        gridFile = os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal.gsb')
        src_proj = '+proj=utm +zone={} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +nadgrids={} +wktext'.format(zone, gridFile)
        src_epsg = 'EPSG:283{}'.format(zone)
    elif src == '4283':
        gridFile = os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal.gsb')
        src_proj = '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +nadgrids={} +wktext'.format(gridFile)
        src_epsg = 'EPSG:4283'
    elif src == '283cd':
        gridFile = os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal_and_distortion.gsb')
        src_proj = '+proj=utm +zone={} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +nadgrids={} +wktext'.format(zone, gridFile)
        src_epsg = 'EPSG:283{}'.format(zone)
    elif src == '4283cd':
        gridFile = os.path.join(pluginPath, 'grids', 'GDA94_GDA2020_conformal_and_distortion.gsb')
        src_proj = '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +nadgrids={} +wktext'.format(gridFile)
        src_epsg = 'EPSG:4283'

    if dst == 78:
        dst_proj = '+proj=utm +zone={} +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +wktext'.format(zone)
        dst_epsg = 'EPSG:78{}'.format(zone)
    elif dst == 7844:
        dst_proj = '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs +wktext'
        dst_epsg = 'EPSG:7844'

    return (src_proj, src_epsg), (dst_proj, dst_epsg)
