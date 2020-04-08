# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:51:36 2019

==========
Name: FileWiz (fw)
==========
Consideration: The imagewiz module is designed to work with established image processing python modules.
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

    def __init__(self,
                 ref_df,
                 orig_folder):
        # ref_df should be a reference dataframe
        self.df = ref_df
        self.ori = orig_folder

        # updated using classgrab()
        self.class_map = None
        self.class_list = None
        self.pki_index = None

        # Updated once foldermove is run
        self.dest_folder = None
        self.file_ori = None
        self.file_move = None

    class FileWiz:
        """Class dealing with the process of arranging files
        into directories for Tensorflow training"""

        def __init__(self,
                     ref_df,
                     orig_folder):
            # ref_df should be a reference dataframe
            self.df = ref_df
            self.ori = orig_folder

            # updated using classgrab()
            self.class_map = None
            self.class_list = None
            self.pki_index = None

            # Updated once foldermove is run
            self.dest_folder = None
            self.file_ori = None
            self.file_move = None

        def classgrab(self,
                      pki_index_col,
                      tar_class='class',
                      verbose=False):
            """Grabs each unique class in a list and attaches each pki to a class (via a dictionary)"""

            class_list = list(self.df[tar_class].unique())

            class_map = dict()
            for i in class_list:
                df_slice = self.df[self.df[tar_class] == i]
                class_map[i] = df_slice[pki_index_col].tolist()

            if verbose == True:
                print("Classes: " + str(len(class_list)))
                print("Classes are as follows: " + class_list)

            self.class_map = class_map
            self.class_list = class_list
            self.pki_index = pki_index_col

            return self.class_list

        def foldermove(self,
                       dest_folder,
                       train_folder_name="train",
                       val_folder_name="validation",
                       tra_t_split=0.2,
                       extension_type=".png",
                       activate=False):
            """Takes files from one folder,
            determines their classes using a pandas dataframe with a 'class' column
            and a pki index, splits them into training and validation sets,
            and places them into folders by training/validation and class.
            """
            # creating training and validation
            train, val = train_test_split(self.df, test_size=tra_t_split)

            # Making directories as needed
            if not os.path.exists(os.path.join(dest_folder, train_folder_name)):
                os.makedirs(os.path.join(dest_folder, train_folder_name))
            if not os.path.exists(os.path.join(dest_folder, val_folder_name)):
                os.makedirs(os.path.join(dest_folder, val_folder_name))

            # Switch for unique classes
            for i in self.class_list:
                if not os.path.exists(os.path.join(dest_folder, train_folder_name, str(i))):
                    os.makedirs(os.path.join(dest_folder, train_folder_name, str(i)))
                if not os.path.exists(os.path.join(dest_folder, val_folder_name, str(i))):
                    os.makedirs(os.path.join(dest_folder, val_folder_name, str(i)))

            # Creating and storing destination locations for our files
            filename_list_train = []
            for i in self.class_list:
                for x in self.class_map[i]:
                    if x in list(train[self.pki_index]):
                        filename_list_train.append(os.path.join(dest_folder,
                                                                train_folder_name,
                                                                str(i),
                                                                str(x) + extension_type))
                    else:
                        filename_list_train.append(os.path.join(dest_folder,
                                                                val_folder_name,
                                                                str(i),
                                                                str(x) + extension_type))

            # Organizing the original file names for our files
            filename_list_orig = []
            for f in self.class_list:
                for y in self.class_map[f]:
                    filename_list_orig.append(os.path.join(self.ori,
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

            self.file_ori = filename_list_orig
            self.file_move = filename_list_train

    def dicomelse(self,
                  dest_folder,
                  dic_extension="dcm",
                  grey=True,
                  coef_max=255.0):
        """Converts DICOM file arrays to PNG images
        and places them into a target folder.
        By default, it interprets them as greyscale"""

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        list_files_temp = os.listdir(self.ori)
        # Narrow the list to only include files with our desired extension
        list_files = list()
        for i in list_files_temp:
            if i[-3:] == dic_extension:
                list_files.append(i)

        for filename in tqdm.tqdm(list_files):
            ds = pydicom.dcmread(os.path.join(self.ori + filename))
            shape = ds.pixel_array.shape
            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)
            image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * coef_max
            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)
            p_filename = filename[:-3] + "png"

        with open(os.path.join(dest_folder + p_filename), 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=grey)
            w.write(png_file, image_2d_scaled)

        return os.listdir(dest_folder)