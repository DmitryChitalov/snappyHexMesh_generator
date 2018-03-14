# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt4 import QtCore, QtGui

import os
import subprocess
import time

class msh_generation_thread(QtCore.QThread):
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th
		global pp_dir_th
		global par
		global int_lng

		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		
	def run(self):

		blockMeshDict_file = prj_path_val_th + '/' + 'blockMeshDict'
		if os.path.exists(blockMeshDict_file) == True:
			msh_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '/' + 'mesh_script', 'w')
			msh_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + 'blockMesh' + '\n' + 'exit')
			msh_bash_file.close()

			msh_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '/' + 'mesh_out.log', "w")
			msh_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th + "/" + "mesh_script"], cwd = pp_dir_th, shell=True, stdout=msh_out_file, stderr=msh_out_file)
			msh_out_file.close()

			while msh_run_subprocess.poll() is None:
				time.sleep(0.5)
			
			return_code = msh_run_subprocess.returncode
			self.emit(QtCore.SIGNAL("finished(int, QString, QString, PyQt_PyObject, QString)"), return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng)	

		else:
			if int_lng == 'Russian':
				msg = "Выполните сохранение расчетной сетки - файл blockMeshDict"
			elif int_lng == 'English':
				msg = "Save the mesh - 'blockMeshDict' file"
			par.listWidget.clear()
			par.item = QtGui.QListWidgetItem(msg, par.listWidget)
			color = QtGui.QColor("red")
			par.item.setTextColor(color)
			par.listWidget.addItem(par.item)