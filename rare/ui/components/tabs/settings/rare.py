# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rare.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RareSettings(object):
    def setupUi(self, RareSettings):
        RareSettings.setObjectName("RareSettings")
        RareSettings.resize(526, 486)
        self.rare_layout = QtWidgets.QGridLayout(RareSettings)
        self.rare_layout.setObjectName("rare_layout")
        self.rpc_layout = QtWidgets.QVBoxLayout()
        self.rpc_layout.setObjectName("rpc_layout")
        self.rare_layout.addLayout(self.rpc_layout, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(RareSettings)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.desktop_link = QtWidgets.QPushButton(self.groupBox)
        self.desktop_link.setObjectName("desktop_link")
        self.verticalLayout.addWidget(self.desktop_link)
        self.startmenu_link = QtWidgets.QPushButton(self.groupBox)
        self.startmenu_link.setObjectName("startmenu_link")
        self.verticalLayout.addWidget(self.startmenu_link)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.rare_layout.addWidget(self.groupBox, 2, 1, 1, 1)
        self.settings_group = QtWidgets.QGroupBox(RareSettings)
        self.settings_group.setObjectName("settings_group")
        self.behavior_layout = QtWidgets.QGridLayout(self.settings_group)
        self.behavior_layout.setObjectName("behavior_layout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.behavior_layout.addItem(spacerItem1, 2, 1, 2, 1)
        self.save_size = QtWidgets.QCheckBox(self.settings_group)
        self.save_size.setObjectName("save_size")
        self.behavior_layout.addWidget(self.save_size, 5, 0, 1, 1)
        self.notification = QtWidgets.QCheckBox(self.settings_group)
        self.notification.setObjectName("notification")
        self.behavior_layout.addWidget(self.notification, 4, 0, 1, 1)
        self.auto_sync_cloud = QtWidgets.QCheckBox(self.settings_group)
        self.auto_sync_cloud.setObjectName("auto_sync_cloud")
        self.behavior_layout.addWidget(self.auto_sync_cloud, 3, 0, 1, 1)
        self.confirm_start = QtWidgets.QCheckBox(self.settings_group)
        self.confirm_start.setObjectName("confirm_start")
        self.behavior_layout.addWidget(self.confirm_start, 2, 0, 1, 1)
        self.auto_update = QtWidgets.QCheckBox(self.settings_group)
        self.auto_update.setObjectName("auto_update")
        self.behavior_layout.addWidget(self.auto_update, 1, 0, 1, 1)
        self.sys_tray = QtWidgets.QCheckBox(self.settings_group)
        self.sys_tray.setObjectName("sys_tray")
        self.behavior_layout.addWidget(self.sys_tray, 0, 0, 1, 1)
        self.rare_layout.addWidget(self.settings_group, 2, 0, 1, 1)
        self.log_dir_group = QtWidgets.QGroupBox(RareSettings)
        self.log_dir_group.setObjectName("log_dir_group")
        self.log_dir_layout = QtWidgets.QVBoxLayout(self.log_dir_group)
        self.log_dir_layout.setObjectName("log_dir_layout")
        self.log_dir_open_button = QtWidgets.QPushButton(self.log_dir_group)
        self.log_dir_open_button.setObjectName("log_dir_open_button")
        self.log_dir_layout.addWidget(self.log_dir_open_button)
        self.log_dir_clean_button = QtWidgets.QPushButton(self.log_dir_group)
        self.log_dir_clean_button.setObjectName("log_dir_clean_button")
        self.log_dir_layout.addWidget(self.log_dir_clean_button)
        self.log_dir_size_label = QtWidgets.QLabel(self.log_dir_group)
        self.log_dir_size_label.setText("")
        self.log_dir_size_label.setWordWrap(True)
        self.log_dir_size_label.setObjectName("log_dir_size_label")
        self.log_dir_layout.addWidget(self.log_dir_size_label)
        self.rare_layout.addWidget(self.log_dir_group, 0, 1, 1, 1, QtCore.Qt.AlignTop)
        self.interface_group = QtWidgets.QGroupBox(RareSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interface_group.sizePolicy().hasHeightForWidth())
        self.interface_group.setSizePolicy(sizePolicy)
        self.interface_group.setObjectName("interface_group")
        self.interface_layout = QtWidgets.QGridLayout(self.interface_group)
        self.interface_layout.setObjectName("interface_layout")
        self.color_select = QtWidgets.QComboBox(self.interface_group)
        self.color_select.setObjectName("color_select")
        self.color_select.addItem("")
        self.interface_layout.addWidget(self.color_select, 1, 1, 1, 1)
        self.style_label = QtWidgets.QLabel(self.interface_group)
        self.style_label.setObjectName("style_label")
        self.interface_layout.addWidget(self.style_label, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.style_select = QtWidgets.QComboBox(self.interface_group)
        self.style_select.setObjectName("style_select")
        self.style_select.addItem("")
        self.interface_layout.addWidget(self.style_select, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.interface_layout.addItem(spacerItem2, 1, 2, 1, 1)
        self.interface_info = QtWidgets.QLabel(self.interface_group)
        font = QtGui.QFont()
        font.setItalic(True)
        self.interface_info.setFont(font)
        self.interface_info.setWordWrap(True)
        self.interface_info.setObjectName("interface_info")
        self.interface_layout.addWidget(self.interface_info, 3, 0, 1, 3)
        self.lang_label = QtWidgets.QLabel(self.interface_group)
        self.lang_label.setObjectName("lang_label")
        self.interface_layout.addWidget(self.lang_label, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.lang_select = QtWidgets.QComboBox(self.interface_group)
        self.lang_select.setObjectName("lang_select")
        self.interface_layout.addWidget(self.lang_select, 0, 1, 1, 1)
        self.color_label = QtWidgets.QLabel(self.interface_group)
        self.color_label.setObjectName("color_label")
        self.interface_layout.addWidget(self.color_label, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.rare_layout.addWidget(self.interface_group, 1, 0, 1, 1, QtCore.Qt.AlignTop)
        self.img_dir_group = QtWidgets.QGroupBox(RareSettings)
        self.img_dir_group.setObjectName("img_dir_group")
        self.img_dir_layout = QtWidgets.QVBoxLayout(self.img_dir_group)
        self.img_dir_layout.setObjectName("img_dir_layout")
        self.rare_layout.addWidget(self.img_dir_group, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.rare_layout.addItem(spacerItem3, 3, 0, 1, 1)

        self.retranslateUi(RareSettings)
        QtCore.QMetaObject.connectSlotsByName(RareSettings)

    def retranslateUi(self, RareSettings):
        _translate = QtCore.QCoreApplication.translate
        RareSettings.setWindowTitle(_translate("RareSettings", "RareSettings"))
        self.groupBox.setTitle(_translate("RareSettings", "Shortcuts"))
        self.desktop_link.setText(_translate("RareSettings", "Create Desktop link"))
        self.startmenu_link.setText(_translate("RareSettings", "Create start menu link"))
        self.settings_group.setTitle(_translate("RareSettings", "Behavior"))
        self.save_size.setText(_translate("RareSettings", "Restore window size on application startup"))
        self.notification.setText(_translate("RareSettings", "Show notification on download completion"))
        self.auto_sync_cloud.setText(_translate("RareSettings", "Automatically sync with cloud"))
        self.confirm_start.setText(_translate("RareSettings", "Confirm game launch"))
        self.auto_update.setText(_translate("RareSettings", "Update games on application startup"))
        self.sys_tray.setText(_translate("RareSettings", "Exit to System tray"))
        self.log_dir_group.setTitle(_translate("RareSettings", "Logs"))
        self.log_dir_open_button.setText(_translate("RareSettings", "Open Log directory"))
        self.log_dir_clean_button.setText(_translate("RareSettings", "Clean Log directory"))
        self.interface_group.setTitle(_translate("RareSettings", "Interface"))
        self.color_select.setItemText(0, _translate("RareSettings", "None"))
        self.style_label.setText(_translate("RareSettings", "Style Sheet"))
        self.style_select.setItemText(0, _translate("RareSettings", "None"))
        self.interface_info.setText(_translate("RareSettings", "Restart Rare to apply."))
        self.lang_label.setText(_translate("RareSettings", "Language"))
        self.color_label.setText(_translate("RareSettings", "Color Scheme"))
        self.img_dir_group.setTitle(_translate("RareSettings", "Image Cache Directory"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RareSettings = QtWidgets.QWidget()
    ui = Ui_RareSettings()
    ui.setupUi(RareSettings)
    RareSettings.show()
    sys.exit(app.exec_())
