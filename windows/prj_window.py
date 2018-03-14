# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------#

from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path

from windows.bMD_window import bmd_window_class

# ---------------------------Главная форма проекта-------------------------------#
		
class prj_form_class(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
		self.setWindowModality(QtCore.Qt.WindowModal)

		global par
		par = parent
		
		global int_lng
		int_lng = par.interface_lng_val		

# ------------------------------------Первый блок формы--------------------------------------#

		self.chc_label = QtGui.QLabel()
		self.chc_lbl_hbox = QtGui.QHBoxLayout()
		self.chc_lbl_hbox.addWidget(self.chc_label)
		self.nf_radio = QtGui.QRadioButton()
		self.nf_radio.toggled.connect(self.on_nf_clicked)
		self.cf_radio = QtGui.QRadioButton()
		self.cf_radio.toggled.connect(self.on_cf_clicked)
		self.icon = self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon)
		self.chc_button = QtGui.QPushButton()
		self.chc_button.setFixedSize(30, 30)
		self.chc_button.setIcon(self.icon)
		self.chc_button.setEnabled(False)
		self.chc_button.clicked.connect(self.on_chc_clicked)
		self.chc_grid = QtGui.QGridLayout()
		self.chc_grid.addWidget(self.nf_radio, 0, 0)
		self.chc_grid.addWidget(self.cf_radio, 0, 1)
		self.chc_grid.addWidget(self.chc_button, 0, 2)
		self.chc_frame = QtGui.QFrame()
		self.chc_frame.setFrameShape(QtGui.QFrame.Panel)
		self.chc_frame.setFrameShadow(QtGui.QFrame.Sunken)
		self.chc_frame.setLayout(self.chc_grid)
		self.chc_hbox = QtGui.QHBoxLayout() 
		self.chc_hbox.addWidget(self.chc_frame)
        
# -------------------------------------Второй блок формы------------------------------------#

		self.mesh_label = QtGui.QLabel()
		self.mesh_name = QtGui.QLineEdit()
		self.mesh_name.setFixedSize(214, 25)
		regexp = QtCore.QRegExp('[А-яА-Яa-zA-Z0-9\_]+')
		validator = QtGui.QRegExpValidator(regexp)
		self.mesh_name.setValidator(validator)
		
		self.prj_path_label = QtGui.QLabel()
		self.prj_path_name = QtGui.QLineEdit()
		self.prj_path_name.setEnabled(False)
		self.prj_path_name.setFixedSize(214, 25)
		self.prj_button = QtGui.QPushButton("...")
		self.prj_button.clicked.connect(self.on_prj_choose)
		self.prj_button.setFixedSize(25, 25)
				
		self.prj_grid = QtGui.QGridLayout()
		self.prj_grid.addWidget(self.mesh_label, 0, 0, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.mesh_name, 0, 1, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.prj_path_label, 1, 0, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.prj_path_name, 1, 1, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.prj_button, 1, 2)
		self.prj_frame = QtGui.QFrame()
		self.prj_frame.setEnabled(False)
		self.prj_frame.setStyleSheet("border-color: darkgray;")
		self.prj_frame.setFrameShape(QtGui.QFrame.Panel)
		self.prj_frame.setFrameShadow(QtGui.QFrame.Sunken)
		self.prj_frame.setLayout(self.prj_grid) 
		
		self.prj_grid_vbox = QtGui.QVBoxLayout() 
		self.prj_grid_vbox.addWidget(self.prj_frame)

		# ---------------------Кнопки сохранения и отмены и их блок-------------------------#

		self.save_button = QtGui.QPushButton()
		self.save_button.setFixedSize(80, 25)
		self.save_button.clicked.connect(self.on_save_clicked)
		self.save_button.setEnabled(False)
		self.cancel_button = QtGui.QPushButton()
		self.cancel_button.setFixedSize(80, 25)
		self.cancel_button.clicked.connect(self.on_cancel_clicked)
		self.buttons_hbox = QtGui.QHBoxLayout()
		self.buttons_hbox.addWidget(self.save_button)
		self.buttons_hbox.addWidget(self.cancel_button)

		# -------------------------Фрейм формы---------------------------#

		self.form_grid = QtGui.QGridLayout()
		self.form_grid.addLayout(self.chc_lbl_hbox, 0, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.chc_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.prj_grid_vbox, 2, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.buttons_hbox, 3, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_frame = QtGui.QFrame()
		self.form_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
		self.form_frame.setLayout(self.form_grid)
		self.form_vbox = QtGui.QVBoxLayout() 
		self.form_vbox.addWidget(self.form_frame)

		# --------------------Размещение на форме всех компонентов---------#

		self.form = QtGui.QFormLayout()
		self.form.addRow(self.form_vbox)
		self.setLayout(self.form)
		
		# --------------------Определяем параметры интерфейса окна---------#
		
		if int_lng == 'Russian':
			self.chc_label.setText("Создайте новую сетку или откройте существующую")
			self.nf_radio.setText("Создать новую")
			self.cf_radio.setText("Открыть существующую")
			self.mesh_label.setText("Название сетки:")
			self.prj_path_label.setText("Путь:")
			self.save_button.setText("Сохранить")
			self.cancel_button.setText("Отмена")
		elif int_lng == 'English':
			self.chc_label.setText("Create a new mesh or open an existing mesh")
			self.nf_radio.setText("Create new mesh")
			self.cf_radio.setText("Open existing mesh")
			self.mesh_label.setText("Mesh name:")
			self.prj_path_label.setText("Path:")
			self.save_button.setText("Save")
			self.cancel_button.setText("Cancel")
		
	# ------------------------Функции связанные с формой-----------------------------#

	# .....Функция, запускаемая при нажатии радио-кнопки "создать новый проект"......#
	def on_nf_clicked(self):
		self.prj_path_label.setEnabled(True)
		self.prj_frame.setEnabled(True)
		self.prj_frame.setStyleSheet("border-color: dimgray;")
		self.chc_button.setEnabled(False)

	# .....Функция, запускаемая при нажатии радио-кнопки "открыть имеющийся проект"......#

	def on_cf_clicked(self):
		self.prj_path_label.setEnabled(False)
		self.prj_frame.setEnabled(False)
		self.prj_frame.setStyleSheet("border-color: darkgray;")
		self.chc_button.setEnabled(True)
		self.prj_path_name.setText('')
			
	# .....Функция, запускаемая при нажатии кнопки выбора директории сохранения нового проекта"......#

	def on_prj_choose(self):
		global prj_path
		prj_path = QtGui.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
		prj_dir, prj_sys = os.path.split(prj_path)
		
		pckls_path = prj_path + '/' + self.mesh_name.text() + '/'
		
		if prj_sys == 'system':
			if os.path.exists(pckls_path) == True:
				shutil.rmtree(pckls_path)
			self.prj_path_name.setText(prj_path)
			self.save_button.setEnabled(True)
		else:
			if int_lng == 'Russian':
				dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Внимание!", "Конечная директория должна называться system", buttons = QtGui.QMessageBox.Ok)
			elif int_lng == 'English':
				dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Attention!", "The destination directory should be called system", buttons = QtGui.QMessageBox.Ok)
			result = dialog.exec_()
			
	# .....Функция, запускаемая при нажатии кнопки "выбрать имеющийся проект"......#
		
	def on_chc_clicked(self):
		global prj_path
		global pickles_dir
		global prj_dir

		prj_dir = QtGui.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
		prj_path, pickles_dir = os.path.split(prj_dir)

		initial_path = prj_dir + '/' + 'initial.pkl'
		if os.path.exists(initial_path) == True:
			self.prj_path_name.setText(prj_dir)
			self.save_button.setEnabled(True)
			self.mesh_name.setText(pickles_dir)
			self.prj_frame.setEnabled(True)
			self.prj_path_name.setEnabled(False)
		else:
			if int_lng == 'Russian':
				dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Внимание!", "Это не директория сетки или в ней отсутствуют все необходимые файлы", buttons = QtGui.QMessageBox.Ok)
			elif int_lng == 'English':
				dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Attention!", "This is not a grid directory, or all necessary files are missing in it", buttons = QtGui.QMessageBox.Ok)
			result = dialog.exec_()			
		
	# ....................Функция, запускаемая при нажатии кнопки "сохранить"....................#

	def on_save_clicked(self):
		global mesh_name_txt
		mesh_name_txt = self.mesh_name.text()
		
		prj_lbl = QtGui.QLabel()
		if int_lng == 'Russian':
			prj_lbl.setText('Путь до файла расчетной сетки:')
		elif int_lng == 'English':
			prj_lbl.setText('Path to mesh file:')
			
		prj_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
		prj_path_lbl = QtGui.QLineEdit()
		prj_path_lbl.setStyleSheet("background-color: white;" "font-size: 10pt;" "color: green;")
		prj_path_lbl.setFixedSize(500, 25)
		prj_path_lbl.setText(prj_path + '/' + mesh_name_txt)
		prj_path_lbl.setEnabled(False)
		par.tdw_grid.addWidget(prj_lbl, 0, 0, alignment=QtCore.Qt.AlignCenter)
		par.tdw_grid.addWidget(prj_path_lbl, 0, 1, alignment=QtCore.Qt.AlignCenter) 		
		
		par.serv_mes.setWidget(par.listWidget)
		if int_lng == 'Russian':
			par.serv_mes.setWindowTitle("Служебные сообщения")
		elif int_lng == 'English':
			par.serv_mes.setWindowTitle("Service messages")
		
		ldw_label = QtGui.QLabel()
		if int_lng == 'Russian':
			ldw_label.setText("Форма генерации расчетной сетки")
		elif int_lng == 'English':
			ldw_label.setText("Form of mesh generation")
			
		ldw_label.setAlignment(QtCore.Qt.AlignCenter)
		ldw_label.setStyleSheet("border-style: none;" "font-size: 10pt;")
		par.ldw_grid.addWidget(ldw_label, 0, 0)
		par.ldw.setTitleBarWidget(par.ldw_frame)
		bmd_form = bmd_window_class(self, par)
		par.ldw.setWidget(bmd_form)
		
		if self.cf_radio.isChecked() == True:
			if int_lng == 'Russian':
				msg = 'Загружены параметры сетки ' + self.mesh_name.text() + '. Установите ее в качестве текущей, выполнив создание файла blockMeshDict и генерацию сетки'
			elif int_lng == 'English':
				msg = 'Mesh parameters are loaded ' + self.mesh_name.text() + '. Set it as current by creating a blockMeshDict file and mesh generation'
			par.listWidget.clear()
			par.item = QtGui.QListWidgetItem(msg, par.listWidget)
			color = QtGui.QColor("blue")
			par.item.setTextColor(color)
			par.listWidget.addItem(par.item)	
		
		self.close()
		
		par.msh_run.setEnabled(True)
		par.msh_visual_run.setEnabled(True)
		par.on_prj_path_get(prj_path, mesh_name_txt)
		
		if self.mesh_name.text() != pickles_dir:
			os.rename(prj_dir, prj_path + '/' + self.mesh_name.text())
		
	def prj_path_return(self):
		return(prj_path, mesh_name_txt)
	
	def int_lng_path_return(self):
		return(int_lng)

# .....................Функция, запускаемая при нажатии кнопки "отмена"......................#
        
	def on_cancel_clicked(self):
		self.close()
