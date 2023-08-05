# SPDX-License-Identifier: Apache-2.0

import sys
import unittest
import pandas
import numpy
from pyspark.ml.linalg import Vectors
from pyspark.ml.regression import GBTRegressor
from onnxmltools import convert_sparkml
from onnxmltools.convert.common.data_types import FloatTensorType
from onnx.defs import onnx_opset_version
from onnxconverter_common.onnx_ex import DEFAULT_OPSET_NUMBER
from tests.sparkml.sparkml_test_utils import save_data_models, run_onnx_model, compare_results
from tests.sparkml import SparkMlTestCase


TARGET_OPSET = min(DEFAULT_OPSET_NUMBER, onnx_opset_version())


class TestSparkmTreeEnsembleClassifier(SparkMlTestCase):

    @unittest.skipIf(sys.platform == 'win32',
                     reason="UnsatisfiedLinkError")
    @unittest.skipIf(sys.version_info < (3, 8),
                     reason="pickle fails on python 3.7")
    def test_gbt_regressor(self):
        data = self.spark.createDataFrame([
            (1.0, Vectors.dense(1.0)),
            (0.0, Vectors.sparse(1, [], []))
        ], ["label", "features"])
        gbt = GBTRegressor(maxIter=5, maxDepth=2, seed=42)
        model = gbt.fit(data)
        feature_count = data.first()[1].size
        model_onnx = convert_sparkml(model, 'Sparkml GBTRegressor', [
            ('features', FloatTensorType([None, feature_count]))
        ], spark_session=self.spark, target_opset=TARGET_OPSET)
        self.assertTrue(model_onnx is not None)
        # run the model
        predicted = model.transform(data)
        data_np = data.toPandas().features.apply(lambda x: pandas.Series(x.toArray())).values.astype(numpy.float32)
        expected = [
            predicted.toPandas().prediction.values.astype(numpy.float32),
        ]
        paths = save_data_models(data_np, expected, model, model_onnx,
                                    basename="SparkmlGBTRegressor")
        onnx_model_path = paths[-1]
        output, output_shapes = run_onnx_model(['prediction'], data_np, onnx_model_path)
        compare_results(expected, output, decimal=5)


if __name__ == "__main__":
    unittest.main()
