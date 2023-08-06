#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   nii_processor.py
@Author  :   Raighne.Weng
@Version :   0.7.3
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Nii Processor
'''

import tempfile
from typing import List
from pathlib import Path
from os import makedirs, path

import cv2
import numpy as np
import nibabel as nib
from datature import error
from datature.processor.base_processor import BaseProcessor


# pylint: disable=R0914,E1101
class NiiProcessor(BaseProcessor):
    """Nii processor class"""

    def valid(self, request_data):
        """Valid the input

        :param request_data: The request data, include file path.
        :return: None.
        """
        file_path = request_data.get("file")

        if not file_path:
            raise error.BadRequestError(
                "Required field, must include file path")

    def process(self, request_data) -> List[str]:
        """Start process file to asset video

        :param request_data: The request data, include file path.
        :return: str: The generate video path.
        """
        out_path = tempfile.mkdtemp()

        file_path = request_data.get("file")
        orientation = request_data.get("options").get("orientation")

        file_name = Path(file_path).stem

        video_output = path.join(out_path, file_name)

        if not path.exists(video_output):
            makedirs(video_output)

        scan = nib.load(file_path)

        # Read data and get scan's shape
        scan_array = scan.get_fdata()

        # if client provide the orientation
        if orientation and orientation in ["x", "y", "z"]:
            output_file_path = f"{video_output}/{file_name}-{orientation}.mp4"

            self.__write_video(scan_array, orientation, output_file_path)

            return [output_file_path]

        # if not then save all orientations
        output_file_paths = []
        for orientation in ["x", "y", "z"]:
            output_file_path = f"{video_output}/{file_name}-{orientation}.mp4"

            self.__write_video(scan_array, orientation, output_file_path)

            output_file_paths.append(output_file_path)

        return output_file_paths

    def __write_video(self, scan_array, orientation, saved_path):
        """Write video to file

        :param scan_array: The NIfTI scan array data.
        :param axis: The orientation of the pics.
        :param saved_path: The saved file path.
        """
        four_cc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(saved_path, four_cc, 30.0, (1024, 1024))

        axis = {'x': 0, 'y': 1, 'z': 2}[orientation]

        for i in range(scan_array.shape[axis]):
            # Get slice along the correct axis and resize
            slice_axis = scan_array.take(i, axis=axis)
            image = cv2.resize(slice_axis, (1024, 1024))

            # Convert to RGB and write to video file
            new_image = cv2.cvtColor(np.uint8(image), cv2.COLOR_GRAY2RGB)
            video_writer.write(new_image)
        video_writer.release()
