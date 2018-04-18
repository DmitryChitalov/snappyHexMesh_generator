#!/usr/bin/python3
# -*- coding: utf-8 -*-
###-------------------------------Импорт модулей----------------------------------###

from PyQt4 import QtCore, QtGui                                                 
import sys, os
import subprocess
import time

from windows.prj_window import prj_form_class
from windows.lng_window import lng_form_class

from threads.msh_generation import msh_generation_thread
from threads.msh_visualisation import msh_visualisation_thread
from functions.bM_functions import bM_functions_class

###-------------------------Главное окно программы-----------------------------###

class MainWindowClass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.interface_lng_val = 'Russian'
        self.setWindowTitle("Генератор расчетных сеток")
		
        ###----------------------Панель управления программой--------------------------###

        self.prj_open = QtGui.QAction(self)
        self.prj_open.setEnabled(True)
        prj_ico = self.style().standardIcon(QtGui.QStyle.SP_FileDialogNewFolder)
        self.prj_open.setIcon(prj_ico)

        self.msh_run = QtGui.QAction(self)
        self.msh_run.setEnabled(False)
        msh_ico = self.style().standardIcon(QtGui.QStyle.SP_ArrowRight)
        self.msh_run.setIcon(msh_ico)

        self.msh_visual_run = QtGui.QAction(self)
        self.msh_visual_run.setEnabled(False)
        msh_visual_run_ico = self.style().standardIcon(QtGui.QStyle.SP_MediaSeekForward)
        self.msh_visual_run.setIcon(msh_visual_run_ico)

        self.lng_chs = QtGui.QAction(self)
        self.lng_chs.setEnabled(True)
        lng_chs_ico = self.style().standardIcon(QtGui.QStyle.SP_FileDialogDetailedView)
        self.lng_chs.setIcon(lng_chs_ico)

        self.prj_open.setToolTip('Открыть проект')
        self.msh_run.setToolTip('Выполнить генерацию расчетной сетки')
        self.msh_visual_run.setToolTip('Выполнить визуализацию расчетной сетки')
        self.lng_chs.setToolTip('Выбрать язык интерфейса программы')

        self.tool_bar = QtGui.QToolBar()
        self.tool_bar.addAction(self.prj_open)
        self.tool_bar.addAction(self.msh_run)
        self.tool_bar.addAction(self.msh_visual_run)
        self.tool_bar.addAction(self.lng_chs)

        self.prj_open.triggered.connect(self.on_prj_open)
        self.msh_run.triggered.connect(self.on_bm_run)
        self.msh_visual_run.triggered.connect(self.on_visual_bm_run)
        self.lng_chs.triggered.connect(self.on_lng_chs)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)		
                
        ###----------------Верхний виджет с полным путем до файла сетки----------------###

        self.tdw = QtGui.QDockWidget()
        self.tdw.setFixedSize(1400, 65)
        self.tdw.setFeatures(self.tdw.NoDockWidgetFeatures)       
        self.tdw_grid = QtGui.QGridLayout()
        self.tdw_grid.setColumnStretch(2, 1)
        self.tdw_frame = QtGui.QFrame()
        self.tdw_frame.setStyleSheet("background-color: ghostwhite;" "border-width: 0.5px;" "border-style: solid;" "border-color: silver;")
        self.tdw_frame.setLayout(self.tdw_grid)
        self.tdw.setWidget(self.tdw_frame)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.tdw)
                
        ###-----------------Левый виджет с формой генерации сетки--------------------###

        self.ldw = QtGui.QDockWidget()
        self.ldw.setFixedSize(800, 780)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ldw)
        self.ldw.setFeatures(self.ldw.NoDockWidgetFeatures)
        self.ldw_grid = QtGui.QGridLayout()
        self.ldw_frame = QtGui.QFrame()
        self.ldw_frame.setFixedSize(800, 44)
        self.ldw_frame.setStyleSheet("background-color: honeydew;" "border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;")
        self.ldw_frame.setLayout(self.ldw_grid)	

        ###-----------Центральный виджет с виджетом содержимого файла сетки-----------###

        self.cdw = QtGui.QDockWidget()
        self.setCentralWidget(self.cdw)
        self.cdw.setFeatures(self.cdw.NoDockWidgetFeatures)

        self.cdw_grid = QtGui.QGridLayout()
        self.cdw_frame = QtGui.QFrame()
        self.cdw_frame.setFixedSize(590, 35)
        self.cdw_frame.setStyleSheet("border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;" "background-color: honeydew;")
        self.cdw_frame.setLayout(self.cdw_grid)

        self.outf_lbl = QtGui.QLabel()
        self.outf_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.outf_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
		
        self.cdw_grid.addWidget(self.outf_lbl, 0, 0)

        self.outf_edit = QtGui.QTextEdit()
        self.outf_scroll = QtGui.QScrollArea()
        self.outf_scroll.setWidgetResizable(True) 
        self.outf_scroll.setWidget(self.outf_edit)
        self.outf_scroll.setFixedSize(590, 700)

        ###------------------Нижний виджет со служебными сообщениями------------------###

        self.serv_mes = QtGui.QDockWidget()
        self.serv_mes.setFixedSize(1400, 160)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.serv_mes)
        self.serv_mes.setFeatures(self.serv_mes.NoDockWidgetFeatures)
        self.listWidget = QtGui.QListWidget()

    ###---------------------Функции, связанные с работой главного окна------------------------###

    ###........................Функция открытия окна выбора интерфейса программы...................###
        
    def on_lng_chs(self):
        lng_win = lng_form_class(self)
        if self.interface_lng_val == 'Russian':
            lng_win.setWindowTitle('Окно выбора языка интерфейса')
        elif self.interface_lng_val == 'English':
            lng_win.setWindowTitle('Interface language selection window')
        lng_win.show()

    ###.........................Функция получения языка интерфейса..........................###        

    def on_lng_get(self, interface_lng):
        global interface_lng_val

        self.interface_lng_val = interface_lng

        if self.interface_lng_val == 'Russian':
            self.setWindowTitle("Генератор расчетных сеток")
            self.prj_open.setToolTip('Открыть проект')
            self.msh_run.setToolTip('Выполнить генерацию расчетной сетки')
            self.msh_visual_run.setToolTip('Выполнить визуализацию расчетной сетки')
            self.lng_chs.setToolTip('Выбрать язык интерфейса программы')
        elif self.interface_lng_val == 'English':
            self.setWindowTitle("Mesh generator")
            self.prj_open.setToolTip('Open project')
            self.msh_run.setToolTip('Run mesh generation')
            self.msh_visual_run.setToolTip('Run mesh vizualization')
            self.lng_chs.setToolTip('Select the interface language for the program')          

    ###.......................Функция открытия окна выбора директории расчетной сетки.......................###

    def on_prj_open(self):
        prj_win = prj_form_class(self)
        if self.interface_lng_val == 'Russian':
            prj_win.setWindowTitle('Окно выбора директории расчетной сетки')
        elif self.interface_lng_val == 'English':
            prj_win.setWindowTitle('Mesh directory selection window')
        prj_win.show()

    ###.........................Функция получения пути до директории..........................###

    def on_prj_path_get(self, prj_path, mesh_name_txt):
        global prj_path_val
        global mesh_name_txt_val
        global pp_dir
        
        prj_path_val = prj_path
        mesh_name_txt_val = mesh_name_txt

        pp_dir, pp_sys = os.path.split(prj_path_val)

    ###.............................Функция получения типа сетки..............................###

    def on_mesh_type_get(self, pd_2):
        global msh_type
        msh_type = pd_2

    ###...........................Функция запуска генерации расчетной сетки........................###    

    def on_bm_run(self): 
        
        bm = msh_generation_thread(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type)
        self.connect(bm, QtCore.SIGNAL("finished(int, QString, QString, PyQt_PyObject, QString, QString)"), msh_functions_class.on_msh_finished)
        bm.start()

    ###...........................Функция запуска визуализации расчетной сетки.....................###         

    def on_visual_bm_run(self):

        bmv = msh_visualisation_thread(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type)
        self.connect(bmv, QtCore.SIGNAL("started(PyQt_PyObject, QString, QString)"), msh_functions_class.on_msh_visual_run)
        self.connect(bmv, QtCore.SIGNAL("finished(int, QString, QString, PyQt_PyObject, QString, QString)"), msh_functions_class.on_msh_visual_finished)
        bmv.start()

###---------------------------Формирование главного окна программы-------------------------###

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindowClass()
    window.setFixedSize(1400, 1000)
    window.setGeometry(200, 30, 0, 0)
    window.show()
    sys.exit(app.exec_())
       
