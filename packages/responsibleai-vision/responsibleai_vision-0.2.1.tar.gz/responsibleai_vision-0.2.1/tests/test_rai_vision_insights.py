# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

import numpy as np
import pytest
import sys

from responsibleai.feature_metadata import FeatureMetadata
from responsibleai_vision import RAIVisionInsights, ModelTask
from common_vision_utils import (
    create_pytorch_vision_model,
    gridify_fridge_multilabel_labels,
    load_multilabel_fridge_dataset,
    load_fridge_dataset, load_imagenet_dataset,
    load_fridge_object_detection_dataset,
    load_mnist_dataset,
    create_image_classification_pipeline,
    load_imagenet_labels, retrieve_or_train_fridge_model,
    retrieve_fridge_object_detection_model,
    FRIDGE_MULTILABEL_TARGETS,
    ImageTransforms,
    ImageTransformEnum,
    load_flowers_dataset,
    create_dummy_model)
from responsibleai_vision.common.constants import ImageColumns
from rai_vision_insights_validator import validate_rai_vision_insights


class TestRAIVisionInsights(object):

    def test_rai_insights_image_classification_imagenet(self):
        data = load_imagenet_dataset()
        pred = create_image_classification_pipeline()
        task_type = ModelTask.IMAGE_CLASSIFICATION
        class_names = load_imagenet_labels()
        run_rai_insights(pred, data[:3], ImageColumns.LABEL,
                         task_type, class_names, image_mode='RGB')

    def test_rai_insights_image_classification_fridge(self):
        data = load_fridge_dataset()
        try:
            model = retrieve_or_train_fridge_model(data)
        except Exception as e:
            print("Failed to retrieve or load Fastai model, force training")
            print("Inner exception message on retrieving model: {}".format(e))
            model = retrieve_or_train_fridge_model(data, force_train=True)
        task_type = ModelTask.IMAGE_CLASSIFICATION
        class_names = data[ImageColumns.LABEL.value].unique()
        run_rai_insights(model, data[:3], ImageColumns.LABEL,
                         task_type, class_names, test_error_analysis=True)

    def test_rai_insights_image_classification_mnist(self):
        train_data, test_data = load_mnist_dataset()
        model = create_pytorch_vision_model(train_data, test_data)
        task_type = ModelTask.IMAGE_CLASSIFICATION
        class_names = train_data[ImageColumns.LABEL.value].unique()
        run_rai_insights(
            model, test_data[:3], ImageColumns.LABEL,
            task_type, class_names)

    def test_rai_insights_multilabel_image_classification_fridge(self):
        data = load_multilabel_fridge_dataset()
        try:
            model = retrieve_or_train_fridge_model(data, multilabel=True)
        except Exception as e:
            print("Failed to retrieve or load Fastai model, force training")
            print("Inner exception message on retrieving model: {}".format(e))
            model = retrieve_or_train_fridge_model(
                data, force_train=True, multilabel=True)
        data = gridify_fridge_multilabel_labels(data)
        task_type = ModelTask.MULTILABEL_IMAGE_CLASSIFICATION
        run_rai_insights(model, data[:3], FRIDGE_MULTILABEL_TARGETS,
                         task_type, test_error_analysis=True)

    @pytest.mark.skip("This test seems to fail due to issues in the \
                      MacOS/Linux versions of the build/PR gate.")
    def test_rai_insights_object_detection_fridge(self):
        data = load_fridge_object_detection_dataset()
        model = retrieve_fridge_object_detection_model()
        task_type = ModelTask.OBJECT_DETECTION
        class_names = np.array(['can', 'carton',
                                'milk_bottle', 'water_bottle'])
        run_rai_insights(model, data[:3], ImageColumns.LABEL,
                         task_type, class_names)

    @pytest.mark.skip("This test fails in the build due to \
                      incompatibility between fastai and pytorch \
                      2.0.0. TODO: fix may be to ping pytorch <2.0.0 \
                      in the build until fastai updates.")
    def test_rai_insights_object_detection_fridge_label_format(self):
        data = load_fridge_object_detection_dataset()
        model = retrieve_fridge_object_detection_model()
        task_type = ModelTask.OBJECT_DETECTION
        class_names = np.array(['can', 'carton',
                                'milk_bottle', 'water_bottle'])

        rai_insights = RAIVisionInsights(model, data[:3],
                                         ImageColumns.LABEL,
                                         task_type=task_type,
                                         classes=class_names)
        y = [
            [
                [1, 100, 200, 300, 400, 0.95],
                [2, 100, 200, 300, 400, 0.95],
                [1, 100, 200, 300, 400, 0.95]
            ],
            [
                [1, 100, 200, 300, 400, 0.95],
                [2, 100, 200, 300, 400, 0.95],
            ]
        ]
        result = [
            [2, 1, 0, 0],
            [1, 1, 0, 0]
        ]
        assert rai_insights._format_od_labels(y, class_names) == result

    @pytest.mark.skipif(sys.platform == 'darwin',
                        reason='torch version downgrade on macos')
    @pytest.mark.parametrize("path, transform, size", [
        ("./data/odFridgeObjects/img_transforms_large",
         ImageTransformEnum.RESIZE,
         (1000, 1000)),
        ("./data/odFridgeObjects/img_transforms_gray",
         ImageTransformEnum.GRAYSCALE,
         None),
        ("./data/odFridgeObjects/img_transforms_opacity",
         ImageTransformEnum.OPACITY,
         None),
        ("./data/odFridgeObjects/img_transforms_blackout",
         ImageTransformEnum.BLACKOUT,
         None),
        ("./data/odFridgeObjects/img_transforms_png",
         ImageTransformEnum.PNG,
         None),
    ])
    def test_rai_insights_object_detection_fridge_image_transforms(self,
                                                                   path,
                                                                   transform,
                                                                   size):
        data = load_fridge_object_detection_dataset()[:10]
        data = ImageTransforms(data).apply_transformation(path,
                                                          transform,
                                                          size)
        model = retrieve_fridge_object_detection_model()
        task_type = ModelTask.OBJECT_DETECTION
        class_names = np.array(['can', 'carton',
                                'milk_bottle', 'water_bottle'])
        dropped_features = [i for i in range(0, 10)]
        run_rai_insights(model, data[:3], ImageColumns.LABEL,
                         task_type, class_names,
                         dropped_features=dropped_features)

    def test_jagged_image_sizes(self):
        data = load_flowers_dataset()
        model = create_dummy_model(data)
        test_data = data
        class_names = data[ImageColumns.LABEL.value].unique()
        task_type = ModelTask.IMAGE_CLASSIFICATION
        run_rai_insights(model, test_data, ImageColumns.LABEL,
                         task_type, class_names)


def run_rai_insights(model, test_data, target_column,
                     task_type, classes=None, test_explainer=False,
                     test_error_analysis=False,
                     image_mode=None, dropped_features=None):
    feature_metadata = None
    if dropped_features:
        feature_metadata = FeatureMetadata(dropped_features=dropped_features)
    rai_insights = RAIVisionInsights(model, test_data,
                                     target_column,
                                     task_type=task_type,
                                     classes=classes,
                                     image_mode=image_mode,
                                     feature_metadata=feature_metadata)
    # Note: this seems too resource-intensive
    # TODO: re-add when we get beefier test machines
    if test_explainer:
        rai_insights.explainer.add()
    if test_error_analysis:
        rai_insights.error_analysis.add()
    if test_explainer or test_error_analysis:
        rai_insights.compute()
    rai_insights.get_data()
    # Validate
    validate_rai_vision_insights(
        rai_insights, test_data,
        target_column, task_type)
