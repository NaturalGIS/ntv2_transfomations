# -*- coding: utf-8 -*-

"""
***************************************************************************
    RasterDE_BY_GK4_UTM32DirInv.py
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

__author__ = 'Alexander Bruy, Giovanni Manghi, Valentin Marquart'
__date__ = 'April 2020'
__copyright__ = '(C) 2019, Giovanni Manghi'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsRasterFileWriter,
                       QgsProcessingException,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination,
                       QgsMessageLog,
                       Qgis
                      )

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from ntv2_transformations.transformations import de_transformation

pluginPath = os.path.dirname(__file__)


class RasterDE_BY_GK4_UTM32DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'debyrastertransform'

    def displayName(self):
        return '[DE-BY] Direct and inverse Raster Transformation'

    def group(self):
        return '[DE] Germany'

    def groupId(self):
        return 'germany'

    def tags(self):
        return 'raster,grid,ntv2,direct,inverse,germany,bavaria'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse raster transformations using Germany NTv2 grids.'

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

        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT,
                                                            'Input raster'))
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
        self.addParameter(QgsProcessingParameterRasterDestination(self.OUTPUT,
                                                                  'Output'))

    def getConsoleCommands(self, parameters, context, feedback, executing=True):
        inLayer = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        if inLayer is None:
            raise QgsProcessingException(self.invalidRasterError(parameters, self.INPUT))

        outFile = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        self.setOutputValue(self.OUTPUT, outFile)

        direction = self.parameterAsEnum(parameters, self.TRANSF, context)
        epsg = self.datums[self.parameterAsEnum(parameters, self.CRS, context)][1]
        grid = self.grids[self.parameterAsEnum(parameters, self.GRID, context)][1]

        gridFile = os.path.join(pluginPath, 'grids', 'BY_KANU.gsb')
        if not os.path.isfile(gridFile):
            error_message = 'ERROR GRID FILE NOT FOUND / USER ACTION REQUIRED:\nThe grid file BY_KANU.gsb is to big to be downloaded in the background (3.03 GB), but therefore has a high transformation accuracy of +- 1cm.\n\nFollowing steps are required:\n1. Download the grid from "http://geodaten.bayern.de/oadownload/bvv_internet/kanu/ntv2_bayern.zip"\n2. Unzip the file and rename it to "BY_KANU.gsb"\n3. Move the file to following location: "{}"'.format(gridFile)
            QgsMessageLog.logMessage(error_message, level=Qgis.Critical)
            raise QgsProcessingException(error_message)

        found, text = de_transformation(epsg, grid)
        if not found:
            raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-s_srs')
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:25832')
        else:
            # Inverse transformation
            arguments = ['-s_srs']
            arguments.append('EPSG:25832')
            arguments.append('-t_srs')
            arguments.append(text)

        arguments.append('-multi')
        arguments.append('-of')
        arguments.append(QgsRasterFileWriter.driverForExtension(os.path.splitext(outFile)[1]))
        arguments.append(inLayer.source())
        arguments.append(outFile)

        return ['gdalwarp', GdalUtils.escapeAndJoin(arguments)]
