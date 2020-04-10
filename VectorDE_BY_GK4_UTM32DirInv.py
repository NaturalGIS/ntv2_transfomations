# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorDE_BY_GK4_UTM32DirInv.py
    ---------------------
    Date                 : April 2020
    Copyright            : (C) 2019 by Giovanni Manghi
    Email                : giovanni dot manghi at naturalgis dot pt
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy, Giovanni Manghi'
__date__ = 'April 2020'
__copyright__ = '(C) 2019, Giovanni Manghi'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from urllib.request import urlretrieve

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsProcessingException,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterVectorDestination
                      )

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from ntv2_transformations.transformations import de_transformation

pluginPath = os.path.dirname(__file__)


class VectorDE_BY_GK4_UTM32DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'debyvectortransform'

    def displayName(self):
        return '[DE-BY] Direct and inverse Vector Transformation'

    def group(self):
        return '[DE] Germany'

    def groupId(self):
        return 'germany'

    def tags(self):
        return 'vector,grid,ntv2,direct,inverse,germany,bavaria'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse vector transformations using Germany NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'de.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old GK4 Data -> UTM32 [EPSG:25832]',
                           'Inverse: UTM32 [EPSG:25832] -> Old GK4 Data'
                          ]

        self.datums = (('Gauss-Krüger zone 4 [EPSG:5678 or EPSG:31468]', 5678),
                      )

        self.grids = (('BY-KanU (CC-BY-ND; High accuracy for Bavaria)', 'BY_KANU'),
                     )

        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              'Input vector'))
        self.addParameter(QgsProcessingParameterEnum(self.TRANSF,
                                                     'Transformation',
                                                     options=self.directions,
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.CRS,
                                                     'Old Datum',
                                                     options=[i[0] for i in self.datums],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterEnum(self.GRID,
                                                     'NTv2 Grid',
                                                     options=[i[0] for i in self.grids],
                                                     defaultValue=0))
        self.addParameter(QgsProcessingParameterVectorDestination(self.OUTPUT,
                                                                  'Output'))

    def getConsoleCommands(self, parameters, context, feedback, executing=True):
        ogrLayer, layerName = self.getOgrCompatibleSource(self.INPUT, parameters, context, feedback, executing)
        outFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        self.setOutputValue(self.OUTPUT, outFile)

        output, outputFormat = GdalUtils.ogrConnectionStringAndFormat(outFile, context)
        if outputFormat in ('SQLite', 'GPKG') and os.path.isfile(output):
            raise QgsProcessingException('Output file "{}" already exists.'.format(output))

        direction = self.parameterAsEnum(parameters, self.TRANSF, context)
        epsg = self.datums[self.parameterAsEnum(parameters, self.CRS, context)][1]
        grid = self.grids[self.parameterAsEnum(parameters, self.GRID, context)][1]

        found, text = de_transformation(epsg, grid)
        if not found:
           raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            # Example
            # ogr2ogr -s_srs 
            # text ="+proj=tmerc +lat_0=0 +lon_0=12 +k=1 +x_0=4500000 +y_0=0 +ellps=bessel +nadgrids=PLATZHALTER\NTV2\ntv2_bayern.gsb +wktext +units=m +no_defs"
            # -t_srs EPSG:25832 -f "ESRI Shapefile" -lco ENCODING=UTF-8  "PLATZHALTER\OUTPUT\Testpunkte_Echtumstellung_UTM32.shp" "PLATZHALTER\INPUT\Testpunkte_Echtumstellung.shp"
            arguments.append('-s_srs')
            #text = '+proj=tmerc +lat_0=0 +lon_0=12 +k=1 +x_0=4500000 +y_0=0 +ellps=bessel +nadgrids=/Users/Valentin/Documents/PROGRAMMING/python/projects/Block_5_NTV2_Transformation/VEKTOR/NTV2/BY_KANU_LOCAL.gsb +wktext +units=m +no_defs'
            #TODO: Bug (at least for Mac OS): The default plugin directory contains a space character ( ) in it's path, which doesn't get properly escaped -> ogr can't find the path for the grid file and fails!
            #TODO: Proposed fix: Escape the space letter properly
            # Default Plugin Path under Mac: /Users/<Username>/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins
            
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:25832')

            arguments.append('-f {}'.format(outputFormat))
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')

            arguments.append(output)
            arguments.append(ogrLayer)
            arguments.append(layerName)
        else:
            # Inverse transformation
            arguments.append('-s_srs')
            arguments.append('EPSG:25832')
            arguments.append('-t_srs')
            arguments.append(text)
            arguments.append('-f')
            arguments.append('Geojson')
            arguments.append('/vsistdout/')
            arguments.append(ogrLayer)
            arguments.append(layerName)
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')
            arguments.append('|')
            arguments.append('ogr2ogr')
            arguments.append('-f {}'.format(outputFormat))
            arguments.append('-a_srs')
            arguments.append('EPSG:5678')
            arguments.append(output)
            arguments.append('/vsistdin/')

        gridFile = os.path.join(pluginPath, 'grids', 'BY_KANU.gsb')
        if not os.path.isfile(gridFile):
            #TODO: Add Message/Popup to inform the user to download the .gsb file from the official government website and place it under the plugins>grids directory.
            # User has to do following steps: 1) Download .gsb.zip file 2) unzip the file 3) rename it to `BY_KANU.gsb`
            #TODO (Best way, altough a lot of effort): 1) Display popup which informs the user about the big file size > OK / Exit > OnClick OK: Download file with progress bar... 3) save downloaded file and unzip it in the plugins folder 4) proceed with transforming the geodata
            # urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/de/BETA2007.gsb', gridFile)
            # iface.messageBar().pushMessage("Error", "I'm sorry Dave, I'm afraid I can't do that", level=Qgis.Critical)
            print("Error: you have to download the file first...")
        return ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
