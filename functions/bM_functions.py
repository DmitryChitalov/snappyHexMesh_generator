# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt4 import QtCore, QtGui
import pickle
import os
import shutil

class bM_functions_class():		
	
	###..............................Функция вывода результатов потока t1..........................### 
	
	def on_bm_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/mesh_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты генерации сетки') 
		elif int_lng == 'English':
			par.outf_lbl.setText('Mesh generation results') 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg = "Расчетная сетка успешно сгенерирована"
			elif int_lng == 'English':
				msg = "Mesh was successfully generated"
			color = QtGui.QColor("green")

		else:
			if int_lng == 'Russian':
				msg = "Расчетная сетка сгенерирована c ошибками"
			elif int_lng == 'English':
				msg = "Mesh was generated with errors"
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)
		
	def on_bm_visual_run(par, int_lng):
		
		if int_lng == 'Russian':
			msg = "Визуализация сетки запущена"
		elif int_lng == 'English':
			msg = "Visualisation of the mesh is started"
		color = QtGui.QColor("blue")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)
		
	def on_bm_visual_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/mesh_viual_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты визуализации сетки') 
		elif int_lng == 'English':
			par.outf_lbl.setText('Mesh vizualization results') 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg = "Визуализация сетки завершена"
			elif int_lng == 'English':
				msg = "Mesh visualisation complete"
			color = QtGui.QColor("green")

		else:
			if int_lng == 'Russian':
				msg = "При отображении расчетной сетки возникли проблемы"
			elif int_lng == 'English':
				msg = "Mesh visualisation complete with errors"
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QtGui.QListWidgetItem(msg, par.listWidget)
		par.item.setTextColor(color)
		par.listWidget.addItem(par.item)			