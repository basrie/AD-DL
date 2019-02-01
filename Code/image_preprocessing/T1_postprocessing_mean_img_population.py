# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 14:17:41 2017

@author: Junhao WEN
"""

__author__ = "Junhao Wen"
__copyright__ = "Copyright 2018 The Aramis Lab Team"
__credits__ = ["Junhao Wen"]
__license__ = "See LICENSE.txt file"
__version__ = "0.1.0"
__maintainer__ = "Junhao Wen"
__email__ = "junhao.wen89@gmail.com"
__status__ = "Development"

def get_mean_image_population(caps_directory, tsv):
    """
    THis is a function to grab all the cropped files
    :param caps_directory:
    :param tsv:
    :return:
    """
    import pandas as pd
    import os
    import nibabel as nib
    import numpy as np

    if not os.path.exists(os.path.join(caps_directory, 'group')):
        os.makedirs(os.path.join(caps_directory, 'group'))

    df = pd.read_csv(tsv, sep='\t')
    if ('session_id' != list(df.columns.values)[1]) and (
                'participant_id' != list(df.columns.values)[0]):
        raise Exception('the data file is not in the correct format.')
    participant_id = list(df['participant_id'])
    session_id = list(df['session_id'])

    for i in range(len(participant_id)):
        image = os.path.join(caps_directory, 'subjects', participant_id[i], session_id[i], 't1', 'preprocessing_dl', participant_id[i] + '_' + session_id[i] + '_space-MNI_res-1x1x1.nii.gz')
        image_data = nib.load(image)
        image_array = image_data.get_data()
        if i == 0:
            image_shape0, image_shape1, image_shape2 = image_array.shape[0], image_array.shape[1], image_array.shape[2]
            ## empty array
            final_array = np.empty((image_shape0, image_shape1, image_shape2, len(participant_id)))
            header = nib.load(image).header
            affine = image_data.affine
        np.append(final_array, image_array)

    ## take the mean of image
    final_mean_array = np.mean(final_array, axis=3)

    ## save the mean image as nifti
    mean_image = nib.Nifti1Image(final_mean_array, affine, header)
    nib.save(mean_image, os.path.join(caps_directory, 'group', 'mean_population.nii.gz'))


