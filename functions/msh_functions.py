# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt4 import QtCore, QtGui
import pickle
import os
import shutil

class msh_functions_class():		
	
	###..............................Функция вывода результатов потока t1..........................### 
	
	def on_msh_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + "/mesh_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты генерации сетки типа ' + msh_t) 
		elif int_lng == 'English':
			par.outf_lbl.setText('Generation results of mesh of type ' + msh_t) 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg = "Расчетная сетка типа " + msh_t + " успешно сгенерирована"
			elif int_lng == 'English':
				msg = "Mesh of type " + msh_t + " was successfully generated"
			color = QtGui.QColor("green")

		else:
			if int_lng == 'Russian':
				msg = "Расчетная сетка типа " + msh_t + " сгенерирована c ошибками"
			elif int_lng == 'English':
				msg = "Mesh of type " + msh_t + " was generated with errors"
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)
		
	def on_msh_visual_run(par, int_lng, msh_t):
		print(msh_t)
		if int_lng == 'Russian':
			msg = "Визуализация сетки типа " + msh_t + " запущена"
		elif int_lng == 'English':
			msg = "Visualisation of the mesh of type " + msh_t + " is started"
		color = QtGui.QColor("blue")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)
		
	def on_msh_visual_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + "/mesh_visual_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты визуализации сетки типа ' + msh_t) 
		elif int_lng == 'English':
			par.outf_lbl.setText('Vizualization results of mesh of type ' + msh_t) 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg = "Визуализация сетки " + msh_t + " завершена"
			elif int_lng == 'English':
				msg = "Mesh visualisation of type " + msh_t + " complete"
			color = QtGui.QColor("green")

		else:
			if int_lng == 'Russian':
				msg = "При отображении расчетной сетки " + msh_t + " возникли проблемы"
			elif int_lng == 'English':
				msg = "Mesh visualisation of type " + msh_t + " complete with errors"
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)			