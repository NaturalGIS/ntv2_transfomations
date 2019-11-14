# -*- coding: utf-8 -*-

"""
***************************************************************************
    DETransformProvider.py
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

from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from processing.tools import system

from ntv2_transformations.VectorDE_GK3ETRS8932NDirInv import VectorDE_GK3ETRS8932NDirInv
from ntv2_transformations.RasterDE_GK3ETRS8932NDirInv import RasterDE_GK3ETRS8932NDirInv
from ntv2_transformations.VectorPT_ETR89PTTM06DirInv import VectorPT_ETR89PTTM06DirInv
from ntv2_transformations.RasterPT_ETR89PTTM06DirInv import RasterPT_ETR89PTTM06DirInv
from ntv2_transformations.VectorES_ED50ERTS89DirInv import VectorES_ED50ERTS89DirInv
from ntv2_transformations.RasterES_ED50ERTS89DirInv import RasterES_ED50ERTS89DirInv
from ntv2_transformations.VectorIT_RER_ETRS89DirInv import VectorIT_RER_ETRS89DirInv
from ntv2_transformations.RasterIT_RER_ETRS89DirInv import RasterIT_RER_ETRS89DirInv
from ntv2_transformations.VectorIT_ITALY_ETRS89DirInv import VectorIT_ITALY_ETRS89DirInv
from ntv2_transformations.VectorCH_LV95ETRS89DirInv import VectorCH_LV95ETRS89DirInv
from ntv2_transformations.RasterCH_LV95ETRS89DirInv import RasterCH_LV95ETRS89DirInv
from ntv2_transformations.VectorUK_OSGB36ETRS89DirInv import VectorUK_OSGB36ETRS89DirInv
from ntv2_transformations.RasterUK_OSGB36ETRS89DirInv import RasterUK_OSGB36ETRS89DirInv
from ntv2_transformations.VectorKR_HDKSHTRS96DirInv import VectorKR_HDKSHTRS96DirInv
from ntv2_transformations.RasterKR_HDKSHTRS96DirInv import RasterKR_HDKSHTRS96DirInv
from ntv2_transformations.VectorCAT_ED50ETRS89DirInv import VectorCAT_ED50ETRS89DirInv
from ntv2_transformations.RasterCAT_ED50ETRS89DirInv import RasterCAT_ED50ETRS89DirInv
from ntv2_transformations.VectorNL_RDNAPETRS89DirInv import VectorNL_RDNAPETRS89DirInv
from ntv2_transformations.RasterNL_RDNAPETRS89DirInv import RasterNL_RDNAPETRS89DirInv
from ntv2_transformations.VectorAT_MGIETRS89DirInv import VectorAT_MGIETRS89DirInv
from ntv2_transformations.RasterAT_MGIETRS89DirInv import RasterAT_MGIETRS89DirInv
from ntv2_transformations.RasterAU_AGD66_84_GDA94DirInv import RasterAU_AGD66_84_GDA94DirInv
from ntv2_transformations.VectorAU_AGD66_84_GDA94DirInv import VectorAU_AGD66_84_GDA94DirInv
from ntv2_transformations.RasterAU_GDA94_2020DirInv import RasterAU_GDA94_2020DirInv
from ntv2_transformations.VectorAU_GDA94_2020DirInv import VectorAU_GDA94_2020DirInv


NTV2_ACTIVATE = 'NTV2_ACTIVATE'


class DETransformProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()
        self.algs = []

    def id(self):
        return 'ntv2_transformations'

    def name(self):
        return 'NTV2 Datum Transformations'

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), 'icons', 'naturalgis_32.png'))


    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(),
                                    NTV2_ACTIVATE,
                                    'Activate',
                                    False))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        ProcessingConfig.removeSetting(NTV2_ACTIVATE)

    def isActive(self):
        return ProcessingConfig.getSetting(NTV2_ACTIVATE)

    def setActive(self, active):
        ProcessingConfig.setSettingValue(NTV2_ACTIVATE, active)

    def getAlgs(self):
        algs = [VectorPT_ETR89PTTM06DirInv(),
                RasterPT_ETR89PTTM06DirInv(),
                VectorDE_GK3ETRS8932NDirInv(),
                RasterDE_GK3ETRS8932NDirInv(),
                VectorES_ED50ERTS89DirInv(),
                RasterES_ED50ERTS89DirInv(),
                VectorIT_RER_ETRS89DirInv(),
                RasterIT_RER_ETRS89DirInv(),
                VectorIT_ITALY_ETRS89DirInv(),
                VectorCH_LV95ETRS89DirInv(),
                RasterCH_LV95ETRS89DirInv(),
                VectorUK_OSGB36ETRS89DirInv(),
                RasterUK_OSGB36ETRS89DirInv(),
                VectorKR_HDKSHTRS96DirInv(),
                RasterKR_HDKSHTRS96DirInv(),
                VectorCAT_ED50ETRS89DirInv(),
                RasterCAT_ED50ETRS89DirInv(),
                VectorNL_RDNAPETRS89DirInv(),
                RasterNL_RDNAPETRS89DirInv(),
                VectorAT_MGIETRS89DirInv(),
                RasterAT_MGIETRS89DirInv(),
                RasterAU_AGD66_84_GDA94DirInv(),
                VectorAU_AGD66_84_GDA94DirInv(),
                RasterAU_GDA94_2020DirInv(),
                VectorAU_GDA94_2020DirInv(),
               ]
        return algs

    def loadAlgorithms(self):
        self.algs = self.getAlgs()
        for a in self.algs:
            self.addAlgorithm(a)
