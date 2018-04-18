# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt4 import QtCore, QtGui

import os
import subprocess
import time

class msh_visualisation_thread(QtCore.QThread):
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

		blockMeshDict_file = pp_dir_th + '/' + 'constant' + '/' + 'polyMesh'
		if os.path.exists(blockMeshDict_file) == True:
			msh_viual_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + '/' + 'mesh_visual_script', 'w')
			msh_viual_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + 'paraFoam' + '\n' + 'exit')
			msh_viual_bash_file.close()

			msh_viual_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + '/' + 'mesh_visual_out.log', "w")
			msh_viual_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th + '_' + msh_t + "/" + "mesh_visual_script"], cwd = pp_dir_th, shell=True, stdout=msh_viual_out_file, stderr=msh_viual_out_file)
			msh_viual_out_file.close()
			
			print("но")
			
			self.emit(QtCore.SIGNAL("started(PyQt_PyObject, QString, QString)"), par, int_lng, msh_t)

			while msh_viual_run_subprocess.poll() is None:
				time.sleep(0.5)
			
			return_code = msh_viual_run_subprocess.returncode
			
			self.emit(QtCore.SIGNAL("finished(int, QString, QString, PyQt_PyObject, QString, QString)"), return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t)
				
		else:
			if int_lng == 'Russian':
				msg = "Выполните генерацию расчетной сетки"
			elif int_lng == 'English':
				msg = "Run mesh generation"
			par.listWidget.clear()
			par.item = QtGui.QListWidgetItem(msg, par.listWidget)
			color = QtGui.QColor("red")
			par.item.setTextColor(color)
			par.listWidget.addItem(par.item)