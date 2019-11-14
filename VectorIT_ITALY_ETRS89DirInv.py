# -*- coding: utf-8 -*-

"""
***************************************************************************
    VectorIT_ITALY_ETRS89DirInv.py
    ---------------------
    Date                 : August 2019
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
__date__ = 'August 2019'
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

from ntv2_transformations.transformations import it_transformation

pluginPath = os.path.dirname(__file__)


class VectorIT_ITALY_ETRS89DirInv(GdalAlgorithm):

    INPUT = 'INPUT'
    TRANSF = 'TRANSF'
    CRS = 'CRS'
    GRID = 'GRID'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'itvectortransform'

    def displayName(self):
        return '[IT] (Italy) Vector - Direct and inverse Transformation'

    def group(self):
        return '[IT] Italy'

    def groupId(self):
        return 'italy'

    def tags(self):
        return 'vector,grid,ntv2,direct,inverse,italy'.split(',')

    def shortHelpString(self):
        return 'Direct and inverse vector transformations using Globogis NTv2 grids.'

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'it.png'))

    def initAlgorithm(self, config=None):
        self.directions = ['Direct: Old Data -> ETRS89 [EPSG:4258]',
                           'Inverse: ETRS89 [EPSG:4258] -> Old Data'
                          ]

        self.datums = (('Monte Mario - GBO Italy 1 [EPSG:3003]', 3003),
                       ('Monte Mario - GBO Italy 2 [EPSG:3004]', 3004),
                       ('UTM - ED50 32N [EPSG:23033]', 23032),
                       ('UTM - ED50 33N [EPSG:23033]', 23033),
                      )

        self.grids = (('Grigliati NTv2 Globogis per la trasformazione di coordinate in Italia', 'ITALY_ETRS89'),
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

        found, text = it_transformation(epsg, grid)
        if not found:
           raise QgsProcessingException(text)

        arguments = []

        if direction == 0:
            # Direct transformation
            arguments.append('-s_srs')
            arguments.append(text)
            arguments.append('-t_srs')
            arguments.append('EPSG:4258')

            arguments.append('-f {}'.format(outputFormat))
            arguments.append('-lco')
            arguments.append('ENCODING=UTF-8')

            arguments.append(output)
            arguments.append(ogrLayer)
            arguments.append(layerName)
        else:
            # Inverse transformation
            arguments.append('-s_srs')
            arguments.append('EPSG:4258')
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
            arguments.append('EPSG:{}'.format(epsg))
            arguments.append(output)
            arguments.append('/vsistdin/')

        if not os.path.isfile(os.path.join(pluginPath, 'grids', 'NadRoma40.gsb')):
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/it_globo/NadRoma40.gsb', os.path.join(pluginPath, 'grids', 'NadRoma40.gsb'))
            urlretrieve('http://www.naturalgis.pt/downloads/ntv2grids/it_globo/NadED50.gsb', os.path.join(pluginPath, 'grids', 'NadED50.gsb'))

        return ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]
