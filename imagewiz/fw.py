# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:51:36 2019

==========
Name: FileWiz (fw)
==========
Consideration: The imagewiz module is deisgned to work with established image processing python modules.
==========
Description: This module is meant to be used to streamline the practical workflow of image preprocessing. 
             This script deals with file movement, environment setup, and with reformatting unruly data.
==========
Invokation: import imagewiz.fw as fw
=========


@author: Evan Gibson
"""

#%% Libraries

import pandas as pd
import os 
import shutil
from sklearn.model_selection import train_test_split
import tqdm
import numpy as np
import png
import pydicom


#%% Definitions

class FileWiz:
    """Class dealing with the process of arranging files
    into directories for Tensorflow training"""
    def __init__(self, ref_df, pki_index_col, orig_folder):
        # ref_df should be a reference dataframe
        self.df = df
        self.pki = pki_index_col
        self.ori

    def classGrab(df,
                  pki_index_col,
                  tar_class = 'class',
                  verbose = False):
        """Grabs the each unique class in a list"""
    
        class_list = list(df[tar_class].unique())
        
        diag_map = dict()
        for i in class_list:
            df_slice = df[df[tar_class] == i]
            diag_map[i] = df_slice[pki_index_col].tolist()
        
        if verbose == True:
            print("Classes: " + len(class_list))
            print("Classes are as follows: " + class_list)
        
        return diag_map, class_list
    
    def folderKing(df,
                   orig_folder,
                   dest_folder,
                   pki_index_col,
                   tar_class_temp = 'class',
                   train_folder_name = "train",
                   val_folder_name = "val",
                   tra_t_split = 0.2, 
                   extension_type = ".png",
                   repo_folder = str(os.getcwd()),
                   activate = False):
        """Takes files from one folder,
        determines their classes using a pandas dataframe with a 'class' column
        and a pki index, splits them into training and validation sets,
        and places them into folders by training/validation and class.
        """
        #creating training and validation
        train, val = train_test_split(df, test_size=tra_t_split)
        
        #Making directories as needed
        if not os.path.exists(os.path.join(dest_folder, train_folder_name)):
            os.makedirs(os.path.join(dest_folder, train_folder_name))
        if not os.path.exists(os.path.join(dest_folder, val_folder_name)):
            os.makedirs(os.path.join(dest_folder, val_folder_name)) 
            
        # Switch for unique classes    
        for i in fileWiz.classGrab(df, pki_index_col, tar_class = tar_class_temp)[1]:
            if not os.path.exists(os.path.join(dest_folder, train_folder_name, str(i))):
                os.makedirs(os.path.join(dest_folder, train_folder_name, str(i)))
            if not os.path.exists(os.path.join(dest_folder, val_folder_name, str(i))):
                os.makedirs(os.path.join(dest_folder, val_folder_name, str(i)))
                
        # Creating and storing destination locations for our files
        filename_list_train = []
        for i in fileWiz.classGrab(train, pki_index_col, tar_class = tar_class_temp)[1]:
            for x in fileWiz.classGrab(train, pki_index_col, tar_class = tar_class_temp)[0][i]:
                filename_list_train.append(os.path.join(dest_folder,
                                                        train_folder_name,
                                                        str(i),
                                                        str(x) + extension_type))
    
        for i in fileWiz.classGrab(val, pki_index_col, tar_class = tar_class_temp)[1]:
            for x in fileWiz.classGrab(val, pki_index_col, tar_class = tar_class_temp)[0][i]:
                filename_list_train.append(os.path.join(dest_folder,
                                                        val_folder_name,
                                                        str(i),
                                                        str(x) + extension_type))
        
        # Organizing the original file names for our files
        filename_list_orig = []
        for f in fileWiz.classGrab(train, pki_index_col, tar_class = tar_class_temp)[1]:
            for y in fileWiz.classGrab(train, pki_index_col, tar_class = tar_class_temp)[0][f]:
                filename_list_orig.append(os.path.join(orig_folder,
                                                        str(y) + extension_type))      
            for y in fileWiz.classGrab(val, pki_index_col, tar_class = tar_class_temp)[0][f]:
                filename_list_orig.append(os.path.join(orig_folder,
                                                        str(y) + extension_type))  
                
        # Performs the prescribed movement
        if activate == True:
            
            if len(filename_list_orig) == len(filename_list_train):
                for d in tqdm.tqdm(range(0, len(filename_list_orig))):
                    try:
                        if os.path.exists(filename_list_orig[d]):
                            shutil.move(filename_list_orig[d], filename_list_train[d])
                    except:
                        pass
            
        return filename_list_train, filename_list_orig   

class weirdWrang:
    """Built for dealing with images that behave strangely
    or need to be reformatted before modeling"""
    
    def dicomToPNG(dicom_folder,
                   output_folder,
                   dic_extension = "dcm",
                   grey = True,
                   coef_max = 255.0):
        """Converts DICOM file arrays to PNG images
        and places them into a target folder. 
        By default, it interprets them as greyscale"""
        
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
            
        list_files_temp = os.listdir(dicom_folder)
        # Narrow the list to only include files with our desired extension
        list_files = list()
        for i in list_files_temp:
            if i[-3:] == dic_extension:
                list_files.append(i)
        
        for filename in list_files:
            ds = pydicom.dcmread(os.path.join(dicom_folder + filename))
            shape = ds.pixel_array.shape
            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * coef_max
            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)
            p_filename = filename[:-3] + "png"
    
        with open(os.path.join(output_folder + p_filename), 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=grey)
            w.write(png_file, image_2d_scaled)
            
        return os.listdir(output_folder)
            