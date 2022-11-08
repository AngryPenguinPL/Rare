from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPalette
from PyQt5.QtWidgets import QProxyStyle, QTabBar, QStyle


class RareStyle(QProxyStyle):
    pass

    def sizeFromContents(self, types, option, size, widget):
        size = super(RareStyle, self).sizeFromContents(types, option, size, widget)
        if types == self.CT_TabBarTab:
            if option.shape == QTabBar.RoundedEast or option.shape == QTabBar.RoundedWest:
                size.transpose()
        return size

    def drawControl(self, element, option, painter, widget):
        if element == self.CE_TabBarTabLabel:
            if option.shape == QTabBar.RoundedEast or option.shape == QTabBar.RoundedWest:
                painter.drawText(option.rect, Qt.AlignCenter, option.text)
                return
        super(RareStyle, self).drawControl(element, option, painter, widget)
