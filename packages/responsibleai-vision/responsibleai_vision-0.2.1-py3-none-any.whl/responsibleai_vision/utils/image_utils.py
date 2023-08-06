# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

"""Contains image handling utilities."""

import numpy as np
from responsibleai_vision.utils.image_reader import get_image_from_path
from responsibleai_vision.common.constants import ImageColumns

IMAGE = ImageColumns.IMAGE.value
IMAGE_URL = ImageColumns.IMAGE_URL.value


def convert_images(dataset, image_mode):
    """Converts the images to the format required by the model.

    If the images are base64 encoded, they are decoded and converted to
    numpy arrays. If the images are already numpy arrays, they are
    returned as is.

    :param dataset: The dataset to convert.
    :type dataset: numpy.ndarray
    :param image_mode: The mode to open the image in.
        See pillow documentation for all modes:
        https://pillow.readthedocs.io/en/stable/handbook/concepts.html
    :type image_mode: str
    :return: The converted dataset.
    :rtype: numpy.ndarray
    """
    if len(dataset) > 0 and isinstance(dataset[0], str):
        try:
            dataset = np.array([get_image_from_path(
                x, image_mode) for x in dataset])
        except ValueError:
            # if images of different sizes, try to convert one by one
            jagged = np.empty(len(dataset), dtype=object)
            for i, x in enumerate(dataset):
                jagged[i] = get_image_from_path(x, image_mode)
            dataset = jagged
    return dataset


def get_images(dataset, image_mode, transformations=None):
    """Get the images from the dataset.

    If transformations are provided as a callable, the images
    are transformed. If transformations are provided as a string,
    the images are retrieved from that column name in the test dataset.

    :param dataset: The dataset to get the images from.
    :type dataset: numpy.ndarray
    :param image_mode: The mode to open the image in.
        See pillow documentation for all modes:
        https://pillow.readthedocs.io/en/stable/handbook/concepts.html
    :type image_mode: str
    :param transformations: The transformations to apply to the images.
    :type transformations: torchvision.transforms
    :return: The images.
    :rtype: numpy.ndarray
    """
    column_names = dataset.columns
    is_transformations_str = isinstance(transformations, str)
    if is_transformations_str:
        images = dataset[transformations]
    else:
        if IMAGE in column_names:
            images = dataset[IMAGE]
        elif IMAGE_URL in column_names:
            images = dataset[IMAGE_URL]
        else:
            raise ValueError('No image column found in test data')

    images = np.array(images.tolist())
    converted_images = convert_images(images, image_mode)

    if not is_transformations_str and transformations is not None:
        converted_images = transformations(converted_images)

    return converted_images
