#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=protected-access

import os
from typing import Any, Optional, Sequence, Union

import pandas as pd
from py4j.java_gateway import JavaClass, get_java_class  # type: ignore
from pyspark.sql import DataFrame, SparkSession

SPARK_API_JAR = os.path.join(os.path.dirname(__file__), "lib", "scoring-code-spark-api.jar")
SPARK_API_JAR = os.environ.get("SPARK_API_JAR", SPARK_API_JAR)


class SparkScoringCodeModel:
    def __init__(self, jar_path: Optional[str] = None, allow_models_in_classpath: bool = False):
        """
        Create a new instance of SparkScoringCodeModel

        Parameters
        ----------
        jar_path: Optional[str]
            The path to a Scoring Code jar file to load.
            If None, the Scoring Code jar will be loaded from the classpath

        allow_models_in_classpath: bool
            Having models in the classpath while loading a model from the filesystem using the
            jar_path argument can lead to unexpected behavior so this is not allowed by default but
            can be forced using allow_models_in_classpath.
            If True, models already present in the classpath will be ignored.
            If False, a ValueError will be raised if models are detected in the classpath.
        """

        session = SparkSession.getActiveSession()
        if not session:
            raise ValueError("Failed to get active spark session")
        self._spark = session

        jvm = self._spark._jvm
        if not jvm:
            raise Exception("Can't access jvm")
        self._jvm = jvm

        self._sc = self._spark._sc

        if jar_path and not allow_models_in_classpath:
            predictors_class = self._jvm.com.datarobot.prediction.Predictors
            if (
                isinstance(predictors_class, JavaClass)
                and predictors_class.getAllPredictors().hasNext()
            ):
                raise ValueError(
                    "Trying to load model from jar file but there are already models present "
                    "in classpath. This can cause issues. Remove models from classpath or "
                    "instantiate model with allow_models_in_classpath=True"
                )

        self._sc._jsc.addJar(SPARK_API_JAR)
        self._disable_url_connection_cache()

        self._class_loader = self._create_url_class_loader(
            [SPARK_API_JAR],
            parent=self._jvm.java.lang.Thread.currentThread().getContextClassLoader(),
        )

        predictors_class = self._class_loader.loadClass(
            "hidden.com.datarobot.prediction.spark.Predictors"
        )

        if jar_path:
            self._init_from_filesystem(jar_path, predictors_class)
        else:
            self._init_from_classpath(predictors_class)

    def _init_from_classpath(self, predictors_class: Any) -> None:
        self.predictor = self._invoke_java_method(
            "getPredictor",
            jobject=None,
            clazz=predictors_class,
        )

    def _init_from_filesystem(self, jar_path: str, predictors_class: Any) -> None:
        current_thread = self._jvm.java.lang.Thread.currentThread()

        model_id = self._get_model_id_from_jar(jar_path)
        original_loader = current_thread.getContextClassLoader()
        try:
            current_thread.setContextClassLoader(self._class_loader)
            self.predictor = self._invoke_java_method(
                "getPredictor",
                jobject=None,
                clazz=predictors_class,
                arguments=[jar_path, model_id],
                argument_types=[
                    self._jvm.java.lang.String,
                    self._jvm.java.lang.String,
                ],
            )
        finally:
            current_thread.setContextClassLoader(original_loader)

    def predict(self, data_frame: Union[DataFrame, pd.DataFrame]) -> DataFrame:
        """
        Get predictions from the Scoring Code Spark model.

        Parameters
        ----------
        data_frame: Union[pyspark.sql.DataFrame, pandas.DataFrame]
            Input data.

        Returns
        -------
        pyspark.sql.DataFrame
            Prediction output.

        """

        if isinstance(data_frame, pd.DataFrame):
            data_frame = self._spark.createDataFrame(data_frame)

        java_dataframe = self._invoke_java_method(
            "transform",
            self.predictor,
            arguments=[data_frame._jdf],
            argument_types=[self._jvm.org.apache.spark.sql.Dataset],
        )

        return DataFrame(java_dataframe, self._spark)

    @property
    def model_id(self) -> str:
        """
        Get the model id.

        Returns
        -------
        str
            The model id.
        """

        model = self._invoke_java_method(
            "getModel",
            self.predictor,
        )

        info_class = self._class_loader.loadClass("com.datarobot.prediction.IPredictorInfo")
        model_id = self._invoke_java_method("getModelId", jobject=model, clazz=info_class)

        return str(model_id)

    def _disable_url_connection_cache(self) -> None:
        # Call setDefaultUseCaches which will disable caching for all URLs. This makes it possible
        # to overwrite a jar file with a new version and instantiate the new model. When caching
        # is enabled, the old file will be reused in some cases and weird things happen.
        url = self._jvm.java.io.File(SPARK_API_JAR).toURI().toURL()
        conn = url.openConnection()
        conn.setDefaultUseCaches(False)

    def _get_model_id_from_jar(self, jar_path: str) -> str:
        loader = self._create_url_class_loader([jar_path])
        predictors_class = loader.loadClass("com.datarobot.prediction.Predictors")
        predictor = self._invoke_java_method(
            "getPredictor",
            jobject=None,
            clazz=predictors_class,
            arguments=[loader],
            argument_types=[self._jvm.java.lang.ClassLoader],
        )

        info_class = loader.loadClass("com.datarobot.prediction.IPredictorInfo")
        return str(self._invoke_java_method("getModelId", jobject=predictor, clazz=info_class))

    def _create_url_class_loader(self, paths: Sequence[str], parent: Any = "default") -> Any:
        urls = [self._jvm.java.io.File(path).toURI().toURL() for path in paths]
        url_array = self._new_array(urls, jtype=self._jvm.java.net.URL)

        if parent == "default":
            return self._jvm.java.net.URLClassLoader(url_array)

        return self._jvm.java.net.URLClassLoader(url_array, parent)

    def _invoke_java_method(
        self,
        method_name: str,
        jobject: Any = None,
        clazz: Any = None,
        arguments: Any = None,
        argument_types: Any = None,
    ) -> Any:
        if clazz is None:
            clazz = jobject.getClass()
        if arguments is None:
            arguments = []
        if argument_types is None:
            argument_types = []

        method = clazz.getMethod(
            method_name,
            self._new_array(
                [get_java_class(t) for t in argument_types], jtype=self._jvm.java.lang.Class
            ),
        )
        return method.invoke(jobject, self._new_array(arguments))

    def _new_array(self, contents: Sequence[Any], jtype: Any = None) -> Any:
        if jtype is None:
            jtype = self._jvm.java.lang.Object

        if not self._sc._gateway:
            raise Exception("Gateway not valid")

        arr = self._sc._gateway.new_array(jtype, len(contents))
        for i, el in enumerate(contents):
            arr[i] = el

        return arr
