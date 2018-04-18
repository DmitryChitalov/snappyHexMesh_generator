# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt4 import QtCore, QtGui

import os
import subprocess
import time

class msh_generation_thread(QtCore.QThread):
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th
		global pp_dir_th
		global par
		global int_lng
		global msh_t
		

		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		msh_t = msh_type
		
	def run(self):
		MeshDict_file = prj_path_val_th + '/' + msh_t + "Dict"
		if os.path.exists(MeshDict_file) == True:
			if msh_t == 'blockMesh':
				
				msh_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + '/' + 'mesh_script', 'w')
				msh_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + msh_t + '\n' + 'exit')
				msh_bash_file.close()
			elif msh_t == 'snappyHexMesh':
				msh_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + '/' + 'mesh_script', 'w')
				msh_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + 'blockMesh' + '\n' + 'surfaceFeatureExtract' + '\n' + msh_t + '\n' + 'exit')
				msh_bash_file.close()

			msh_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + '/' + 'mesh_out.log', "w")
			msh_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + "/" + "mesh_script"], cwd = pp_dir_th, shell=True, stdout=msh_out_file, stderr=msh_out_file)
			msh_out_file.close()
			
			if int_lng == 'Russian':
				msg = "Выполняется генерация расчетной сетки типа " + msh_t
			elif int_lng == 'English':
				msg = "Making the generation of mesh of type " + msh_t
			par.listWidget.clear()
			par.item = QtGui.QListWidgetItem(msg, par.listWidget)
			color = QtGui.QColor("blue")
			par.item.setTextColor(color)
			par.listWidget.addItem(par.item)

			while msh_run_subprocess.poll() is None:
				time.sleep(0.5)
			
			return_code = msh_run_subprocess.returncode
			self.emit(QtCore.SIGNAL("finished(int, QString, QString, PyQt_PyObject, QString, QString)"), return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t)	

		else:
			if int_lng == 'Russian':
				msg = "Выполните сохранение расчетной сетки - файл " + msh_t
			elif int_lng == 'English':
				msg = "Save the mesh - " + msh_t + "file"
			par.listWidget.clear()
			par.item = QtGui.QListWidgetItem(msg, par.listWidget)
			color = QtGui.QColor("red")
			par.item.setTextColor(color)
			par.listWidget.addItem(par.item)