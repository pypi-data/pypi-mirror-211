# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import shutil

from responsibleai_vision import RAIVisionInsights, ModelTask
from responsibleai_vision.common.constants import ImageColumns
from rai_vision_insights_validator import validate_rai_vision_insights
from responsibleai._internal.constants import ManagerNames

from common_vision_utils import (
    load_imagenet_dataset,
    create_image_classification_pipeline,
    load_imagenet_labels,
    ImageClassificationPipelineSerializer)

TRAIN_JSON = 'train.json'
TEST_JSON = 'test.json'
DATA = 'data'


class TestRAIVisionInsightsSaveAndLoadScenarios(object):

    def test_rai_insights_empty_save_load_save(self):
        data = load_imagenet_dataset()
        pred = create_image_classification_pipeline()
        task_type = ModelTask.IMAGE_CLASSIFICATION
        class_names = load_imagenet_labels()
        test = data[:3]
        label = ImageColumns.LABEL
        serializer = ImageClassificationPipelineSerializer()

        rai_insights = RAIVisionInsights(
            pred, test, label,
            task_type=task_type,
            classes=class_names,
            serializer=serializer)

        with TemporaryDirectory() as tmpdir:
            save_1 = Path(tmpdir) / "first_save"
            save_2 = Path(tmpdir) / "second_save"

            # Save it
            rai_insights.save(save_1)
            assert len(os.listdir(save_1 / ManagerNames.EXPLAINER)) == 0
            assert not os.path.exists(save_1 / DATA / TRAIN_JSON)
            assert os.path.exists(save_1 / DATA / TEST_JSON)

            # Load
            rai_2 = RAIVisionInsights.load(save_1)

            # Validate
            validate_rai_vision_insights(
                rai_2, test,
                label, task_type)

            # Save again
            rai_2.save(save_2)
            assert len(os.listdir(save_2 / ManagerNames.EXPLAINER)) == 0
            assert not os.path.exists(save_2 / DATA / TRAIN_JSON)
            assert os.path.exists(save_2 / DATA / TEST_JSON)

    def test_loading_rai_insights_without_model_file(self):
        data = load_imagenet_dataset()
        pred = create_image_classification_pipeline()
        task_type = ModelTask.IMAGE_CLASSIFICATION
        class_names = load_imagenet_labels()
        test = data[:3]
        label = ImageColumns.LABEL
        serializer = ImageClassificationPipelineSerializer()

        rai_insights = RAIVisionInsights(
            pred, test, label,
            task_type=task_type,
            classes=class_names,
            serializer=serializer)

        with TemporaryDirectory() as tmpdir:
            assert rai_insights.model is not None
            save_path = Path(tmpdir) / "rai_insights"
            rai_insights.save(save_path)

            # Remove the model.pkl file to cause an exception to occur
            # while loading the model.
            model_name = 'image-classification-model'
            model_pkl_path = Path(tmpdir) / "rai_insights" / model_name
            shutil.rmtree(model_pkl_path)
            match_msg = 'No file or directory found'
            with pytest.raises(OSError, match=match_msg):
                without_model_rai_insights = RAIVisionInsights.load(save_path)
                assert without_model_rai_insights.model is None
