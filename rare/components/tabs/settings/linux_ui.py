# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/components/tabs/settings/linux.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LinuxSettings(object):
    def setupUi(self, LinuxSettings):
        LinuxSettings.setObjectName("LinuxSettings")
        LinuxSettings.resize(569, 454)
        self.linux_layout = QtWidgets.QGridLayout(LinuxSettings)
        self.linux_layout.setObjectName("linux_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.linux_layout.addItem(spacerItem, 3, 0, 1, 1)
        self.wine_groupbox = QtWidgets.QGroupBox(LinuxSettings)
        self.wine_groupbox.setObjectName("wine_groupbox")
        self.wine_layout = QtWidgets.QGridLayout(self.wine_groupbox)
        self.wine_layout.setObjectName("wine_layout")
        self.exec_label = QtWidgets.QLabel(self.wine_groupbox)
        self.exec_label.setObjectName("exec_label")
        self.wine_layout.addWidget(self.exec_label, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.prefix_label = QtWidgets.QLabel(self.wine_groupbox)
        self.prefix_label.setObjectName("prefix_label")
        self.wine_layout.addWidget(self.prefix_label, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.prefix_frame = QtWidgets.QFrame(self.wine_groupbox)
        self.prefix_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.prefix_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.prefix_frame.setObjectName("prefix_frame")
        self.prefix_layout = QtWidgets.QVBoxLayout(self.prefix_frame)
        self.prefix_layout.setObjectName("prefix_layout")
        self.wine_layout.addWidget(self.prefix_frame, 0, 1, 1, 1)
        self.exec_frame = QtWidgets.QFrame(self.wine_groupbox)
        self.exec_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.exec_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.exec_frame.setObjectName("exec_frame")
        self.exec_layout = QtWidgets.QVBoxLayout(self.exec_frame)
        self.exec_layout.setObjectName("exec_layout")
        self.wine_layout.addWidget(self.exec_frame, 1, 1, 1, 1)
        self.linux_layout.addWidget(self.wine_groupbox, 0, 0, 1, 1)
        self.dxvk_layout = QtWidgets.QVBoxLayout()
        self.dxvk_layout.setObjectName("dxvk_layout")
        self.linux_layout.addLayout(self.dxvk_layout, 1, 0, 1, 1)

        self.retranslateUi(LinuxSettings)
        QtCore.QMetaObject.connectSlotsByName(LinuxSettings)

    def retranslateUi(self, LinuxSettings):
        _translate = QtCore.QCoreApplication.translate
        LinuxSettings.setWindowTitle(_translate("LinuxSettings", "LinuxSettings"))
        self.wine_groupbox.setTitle(_translate("LinuxSettings", "Wine Settings"))
        self.exec_label.setText(_translate("LinuxSettings", "Wine executable:"))
        self.prefix_label.setText(_translate("LinuxSettings", "Wine prefix:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LinuxSettings = QtWidgets.QWidget()
    ui = Ui_LinuxSettings()
    ui.setupUi(LinuxSettings)
    LinuxSettings.show()
    sys.exit(app.exec_())
