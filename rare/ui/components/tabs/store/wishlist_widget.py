# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rare/ui/components/tabs/store/wishlist_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WishlistWidget(object):
    def setupUi(self, WishlistWidget):
        WishlistWidget.setObjectName("WishlistWidget")
        WishlistWidget.resize(523, 172)
        WishlistWidget.setWindowTitle("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(WishlistWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(WishlistWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setText("TextLabel")
        self.title_label.setWordWrap(True)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_2.addWidget(self.title_label)
        self.developer = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.developer.setFont(font)
        self.developer.setText("TextLabel")
        self.developer.setObjectName("developer")
        self.verticalLayout_2.addWidget(self.developer)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.discount_price = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discount_price.sizePolicy().hasHeightForWidth())
        self.discount_price.setSizePolicy(sizePolicy)
        self.discount_price.setText("TextLabel")
        self.discount_price.setObjectName("discount_price")
        self.horizontalLayout_2.addWidget(self.discount_price)
        self.price = QtWidgets.QLabel(self.widget)
        self.price.setText("TextLabel")
        self.price.setObjectName("price")
        self.horizontalLayout_2.addWidget(self.price)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget)
        self.delete_button = QtWidgets.QPushButton(WishlistWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy)
        self.delete_button.setText("")
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)

        self.retranslateUi(WishlistWidget)
        QtCore.QMetaObject.connectSlotsByName(WishlistWidget)

    def retranslateUi(self, WishlistWidget):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WishlistWidget = QtWidgets.QWidget()
    ui = Ui_WishlistWidget()
    ui.setupUi(WishlistWidget)
    WishlistWidget.show()
    sys.exit(app.exec_())
