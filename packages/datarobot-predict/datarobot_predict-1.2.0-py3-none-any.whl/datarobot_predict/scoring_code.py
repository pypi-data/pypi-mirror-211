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
# pylint: disable=import-error,import-outside-toplevel,invalid-name
import datetime
import enum
import glob
import os.path
import re
import socket
import sys
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Sequence, Tuple

import click
import pandas as pd
from dateutil.parser import isoparse
from py4j.java_gateway import JavaGateway, find_jar_path  # type: ignore


class ModelType(enum.Enum):
    CLASSIFICATION = "IClassificationPredictor"
    REGRESSION = "IRegressionPredictor"
    TIME_SERIES = "ITimeSeriesRegressionPredictor"


class TimeSeriesType(enum.Enum):
    FORECAST = 1
    HISTORICAL = 2


BATCH_PROCESSOR_JAR = os.path.join(os.path.dirname(__file__), "lib", "batch-processor.jar")

BATCH_PROCESSOR_JAR = os.environ.get("BATCH_JAR", BATCH_PROCESSOR_JAR)


class ScoringCodeModel:
    def __init__(
        self,
        jar_path: Optional[str] = None,
        _json_path: Optional[str] = None,
        _classpath: Optional[List[str]] = None,
        _factory_class: Optional[str] = None,
    ):
        """
        Constructor for ScoringCodeModel

        Parameters
        ----------
        jar_path
            path to a jar file
        _json_path
            For internal usage
        _classpath
            For internal usage
        """
        if not _json_path and jar_path and not os.path.exists(jar_path):
            raise ValueError(f"File not found: {jar_path}")

        enable_java_stderr = os.getenv("ENABLE_JAVA_STDERR", "False").lower() in (
            "true",
            "1",
        )
        classpath = [BATCH_PROCESSOR_JAR]
        if jar_path:
            classpath += [jar_path]
        if _classpath:
            classpath += _classpath

        jvm_args = os.getenv("JVM_ARGS", "").split()

        self.gateway = JavaGateway.launch_gateway(
            javaopts=jvm_args,
            classpath=os.pathsep.join(classpath),
            redirect_stderr=(sys.stderr if enable_java_stderr else None),
            jarpath=_find_py4j_jar(),
        )

        if not enable_java_stderr:
            self.gateway.jvm.java.lang.System.setProperty(
                "hidden.org.slf4j.simpleLogger.defaultLogLevel", "off"
            )
        if _json_path:
            if not _factory_class:
                _factory_class = "com.datarobot.prediction.internal.BlueprintFacadeModel"
            factory_class = getattr(self.gateway.jvm, _factory_class)
            self._predictor = factory_class.loadFromFilesystem(_json_path)
        else:
            self._predictor = self.gateway.jvm.com.datarobot.prediction.Predictors.getPredictor()

        self.server_socket = self.gateway.jvm.java.net.ServerSocket(
            0, 0, self.gateway.jvm.java.net.InetAddress.getLoopbackAddress()
        )
        self.server_socket.setReuseAddress(True)

        self._executor = ThreadPoolExecutor(max_workers=2)

    def predict(
        self,
        data_frame: pd.DataFrame,
        max_explanations: int = 0,
        threshold_high: Optional[float] = None,
        threshold_low: Optional[float] = None,
        time_series_type: TimeSeriesType = TimeSeriesType.FORECAST,
        forecast_point: Optional[datetime.datetime] = None,
        predictions_start_date: Optional[datetime.datetime] = None,
        predictions_end_date: Optional[datetime.datetime] = None,
        prediction_intervals_length: Optional[int] = None,
    ) -> pd.DataFrame:

        """
        Get predictions from Scoring Code model.

        Parameters
        ----------
        data_frame: pd.DataFrame
            Input data.
        max_explanations: int
            Number of prediction explanations to compute.
            If 0, prediction explanations are disabled.
        threshold_high: Optional[float]
            Only compute prediction explanations for predictions above this threshold.
            If None, the default value will be used.
        threshold_low: Optional[float]
            Only compute prediction explanations for predictions below this threshold.
            If None, the default value will be used.
        time_series_type: TimeSeriesType
            Type of time series predictions to compute.
            If TimeSeriesType.FORECAST, predictions will be computed for a single
            forecast point specified by forecast_point.
            If TimeSeriesType.HISTORICAL, predictions will be computed for the range of
            timestamps specified by predictions_start_date and predictions_end_date.
        forecast_point: Optional[datetime.datetime]
            Forecast point to use for time series forecast point predictions.
            If None, the forecast point is detected automatically.
            If not None and time_series_type is not TimeSeriesType.FORECAST,
            ValueError is raised
        predictions_start_date: Optional[datetime.datetime]
            Start date in range for historical predictions.
            If None, predictions will start from the earliest date in the input that
            has enough history.
            If not None and time_series_type is not TimeSeriesType.HISTORICAL,
            ValueError is raised
        predictions_end_date: Optional[datetime.datetime]
            End date in range for historical predictions.
            If None, predictions will end on the last date in the input.
            If not None and time_series_type is not TimeSeriesType.HISTORICAL,
            ValueError is raised
        prediction_intervals_length: Optional[int]
            The percentile to use for the size for prediction intervals. Has to be an
            integer between 0 and 100(inclusive).
            If None, prediction intervals will not be computed.
        Returns
        -------
        pd.DataFrame
            Prediction output
        """

        if prediction_intervals_length is not None and (
            prediction_intervals_length < 1 or prediction_intervals_length > 100
        ):
            raise ValueError("Prediction intervals length must be >0 and <=100")

        if threshold_high and not max_explanations:
            raise ValueError(
                "threshold_high does not make sense without specifying max_explanations"
            )
        if threshold_low and not max_explanations:
            raise ValueError(
                "threshold_low does not make sense without specifying max_explanations"
            )

        _validate_input(data_frame)

        time_series_options = None
        if self.model_type == ModelType.TIME_SERIES:
            if time_series_type == TimeSeriesType.FORECAST:
                if predictions_start_date:
                    raise ValueError(
                        "Predictions start date is not supported when time_series_type is FORECAST"
                    )
                if predictions_end_date:
                    raise ValueError(
                        "Predictions end date is not supported when time_series_type is FORECAST"
                    )
            else:
                if forecast_point:
                    raise ValueError(
                        "Forecast point is not supported when time_series_type is HISTORICAL"
                    )
            time_series_options = self._build_ts_options(
                time_series_type,
                forecast_point,
                predictions_start_date,
                predictions_end_date,
                prediction_intervals_length,
            )

        else:
            if forecast_point:
                raise ValueError("forecast_point is not supported by non time series models")

            if time_series_type != TimeSeriesType.FORECAST:
                raise ValueError("time_series_type is not supported by non time series models")

            if predictions_start_date:
                raise ValueError(
                    "predictions_start_date is not supported by non time series models"
                )

            if predictions_end_date:
                raise ValueError("predictions_end_date is not supported by non time series models")

        return self._predict(
            data_frame,
            max_explanations,
            threshold_high,
            threshold_low,
            time_series_options,
        )

    @property
    def model_type(self) -> ModelType:
        """
        Get the model type.

        Returns
        -------
        ModelType
            One of: ModelType.CLASSIFICATION, ModelType.REGRESSION, ModelType.TIME_SERIES
        """
        clazz = self._predictor.getPredictorClass().getSimpleName()
        return ModelType(clazz)

    @property
    def model_info(self) -> Optional[Dict[str, str]]:
        """
        Get model metadata.

        Returns
        -------
        Optional[Dict[str, str]]
            Dictionary with metadata if model has any, else None
        """
        info = self._predictor.getModelInfo()
        if not info:
            return None
        return {str(key): str(val) for key, val in info.items()}

    @property
    def date_column(self) -> Optional[str]:
        """
        Get the date column for a Time Series model.

        Returns
        -------
        Optional[str]
            Name of date column if model has one, else None.
        """
        return (
            str(self._predictor.getDateColumnName())
            if self.model_type == ModelType.TIME_SERIES
            else None
        )

    @property
    def series_id_column(self) -> Optional[str]:
        """
        Get the name of the series id column for a Time Series model.

        Returns
        -------
        Optional[str]
            Name of the series id column if model has one, else None.
        """
        return (
            str(self._predictor.getSeriesIdColumnName())
            if self.model_type == ModelType.TIME_SERIES
            else None
        )

    @property
    def time_step(self) -> Optional[Tuple[int, str]]:
        """
        Get the time step for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, str]]
            Time step as (quantity, time unit) if model has this, else None.
            Example: (3, "DAYS")
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        step = self._predictor.getTimeStep()
        return int(step.getKey()), str(step.getValue())

    @property
    def feature_derivation_window(self) -> Optional[Tuple[int, int]]:
        """
        Get the feature derivation window for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, int]]
            Feature derivation window as (begin, end) if model has this, else None.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        window = self._predictor.getFeatureDerivationWindow()
        return int(window.getKey()), int(window.getValue())

    @property
    def forecast_window(self) -> Optional[Tuple[int, int]]:
        """
        Get the forecast window for a Time Series model.

        Returns
        -------
        Optional[Tuple[int, int]]
            Forecast window as (begin, end) if model has this, else None.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None

        window = self._predictor.getForecastWindow()
        return int(window.getKey()), int(window.getValue())

    @property
    def date_format(self) -> Optional[str]:
        """
        Get the date format for a Time Series model.

        Returns
        -------
        Optional[str]
            Date format having the syntax expected by datetime.strftime() or None
            if model is not time series.
        """
        if self.model_type != ModelType.TIME_SERIES:
            return None
        return _java_date_format_to_python(str(self._predictor.getDateFormat()))

    @property
    def class_labels(self) -> Optional[Sequence[str]]:
        """
        Get the class labels for the model.

        Returns
        -------
        Optional[Sequence[str]]
            List of class labels if model is a classification model, else None.
        """
        return (
            [str(label) for label in self._predictor.getClassLabels()]
            if self.model_type == ModelType.CLASSIFICATION
            else None
        )

    @property
    def features(self) -> Dict[str, type]:
        """
        Get features names and types for the model.

        Returns
        -------
        OrderedDict[str, type]
            Dictionary mapping feature name to feature type, where feature type is
            either str or float. The ordering of features is the same as it was during
            model training.
        """

        def feature_type(java_type: Any) -> type:
            simple = java_type.getSimpleName()
            if simple == "Double":
                return float
            if simple == "String":
                return str
            raise RuntimeError(f"Unexpected java type {simple}")

        features = OrderedDict()
        for key, val in self._predictor.getFeatures().items():
            features[key] = feature_type(val)
        return features

    @property
    def model_id(self) -> str:
        """
        Get the model id.

        Returns
        -------
        str
            The model id.
        """
        return str(self._predictor.getModelId())

    def __del__(self) -> None:
        if hasattr(self, "gateway"):
            self.gateway.shutdown()
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False)

    def _predict(
        self,
        data_frame: pd.DataFrame,
        max_explanations: int,
        threshold_high: Optional[float],
        threshold_low: Optional[float],
        time_series_options: Any,
    ) -> pd.DataFrame:
        explanation_params = None
        if max_explanations:
            explanation_params = (
                self._predictor.getDefaultPredictionExplanationParams().withMaxCodes(
                    max_explanations
                )
            )
            if threshold_high:
                explanation_params = explanation_params.withThresholdHigh(float(threshold_high))
            if threshold_low:
                explanation_params = explanation_params.withThresholdLow(float(threshold_low))

        batch_executor = self._build_batch_executor(explanation_params, time_series_options)

        result = self._run_batch_executor(batch_executor, data_frame)

        if time_series_options:
            result["Timestamp"] = pd.to_datetime(result["Timestamp"])
            result["Forecast Point"] = pd.to_datetime(result["Forecast Point"])
            result["Series Id"] = result["Series Id"].fillna("")

        return result

    def _run_batch_executor(self, batch_executor: Any, data_frame: pd.DataFrame) -> pd.DataFrame:
        ReaderFactory = self.gateway.jvm.hidden.com.datarobot.batch.processor.io.ReaderFactory
        CallbackFactory = (
            self.gateway.jvm.hidden.com.datarobot.batch.processor.engine.callback.CallbackFactory
        )

        try:
            address = (
                self.server_socket.getInetAddress().getHostAddress(),
                self.server_socket.getLocalPort(),
            )

            writer_future = self._executor.submit(_write_dataframe, data_frame, address)
            writer_java_socket = self.server_socket.accept()
            input_reader = self.gateway.jvm.java.io.InputStreamReader(
                writer_java_socket.getInputStream()
            )

            # Reader is spawned after writer connection has been accepted. This
            # ensures that reader/writer connections are not mixed up.
            reader_future = self._executor.submit(_read_dataframe, address)
            reader_java_socket = self.server_socket.accept()
            reader = ReaderFactory().getCsvReader(input_reader, ",")
            callback = CallbackFactory().getStreamCallback(
                reader_java_socket.getOutputStream(),
                ",",
                self.gateway.jvm.java.nio.charset.StandardCharsets.UTF_8,
            )

            batch_executor.execute(reader, callback)

            # Close reader socket to make Java workers shutdown
            reader_java_socket.close()

            writer_future.result(timeout=1)

            res = reader_future.result(timeout=3)
            return res

        finally:
            writer_java_socket.close()
            reader_java_socket.close()

    def _build_ts_options(
        self,
        time_series_type: TimeSeriesType,
        forecast_point: Optional[datetime.datetime],
        predictions_start_date: Optional[datetime.datetime],
        predictions_end_date: Optional[datetime.datetime],
        prediction_intervals_length: Optional[int],
    ) -> Any:
        TimeSeriesOptions = self.gateway.jvm.com.datarobot.prediction.TimeSeriesOptions

        builder = TimeSeriesOptions.newBuilder()
        if prediction_intervals_length:
            builder.computeIntervals(True)
            builder.setPredictionIntervalLength(prediction_intervals_length)

        assert self.date_format is not None
        if time_series_type == TimeSeriesType.FORECAST:
            if forecast_point:
                options = builder.buildSingleForecastPointRequest(
                    forecast_point.strftime(self.date_format)
                )
            else:
                options = builder.buildSingleForecastPointRequest()
        else:
            start_date = (
                predictions_start_date.strftime(self.date_format)
                if predictions_start_date
                else None
            )
            end_date = (
                predictions_end_date.strftime(self.date_format) if predictions_end_date else None
            )
            options = builder.buildForecastDateRangeRequest(start_date, end_date)

        return options

    def _build_batch_executor(self, explanation_params: Any, ts_options: Any) -> Any:
        BatchExecutorBuilder = (
            self.gateway.jvm.hidden.com.datarobot.batch.processor.engine.BatchExecutorBuilder
        )

        builder = BatchExecutorBuilder(self._predictor)
        builder.timeSeriesBatchProcessing(self.model_type == ModelType.TIME_SERIES)
        builder.tsOptions(ts_options)
        if explanation_params:
            builder.explanationsParams(explanation_params)
        return builder.build()


def _find_py4j_jar() -> str:
    path: str = find_jar_path()

    if path:
        return path

    # This is a workaround to find py4j jar on Databricks. Databricks adds their own
    # version which is already imported when the notebook is started. Their version
    # of py4j is inside a zipfile at '/databricks/spark/python/lib/py4j-0.10.9.5-src.zip'
    # Py4j fails to load its own jar since it is in the zipfile.
    # Here we try to find the jar that is provided by the py4j version that is installed
    # by pip as a dependency to datarobot-predict. We cross our fingers and hope that
    # it is compatible with the imported py4j version.
    paths = glob.glob(os.path.join(sys.prefix, "share/py4j/py4j*.jar"))
    if paths and os.path.exists(paths[0]):
        return paths[0]

    return ""


def _write_dataframe(data_frame: pd.DataFrame, address: Tuple[str, int]) -> None:
    with socket.socket() as s:
        s.connect(address)
        with s.makefile("w") as f:
            data_frame.to_csv(f)


def _read_dataframe(address: Tuple[str, int]) -> pd.DataFrame:
    with socket.socket() as s:
        s.connect(address)
        with s.makefile("r") as f:
            df = pd.read_csv(f, float_precision="round_trip")
            return df


def _validate_input(data_frame: pd.DataFrame) -> None:
    for column in data_frame.columns:
        if pd.api.types.is_datetime64_any_dtype(data_frame[column]):  # type: ignore
            raise ValueError(
                f"Column {column} has unsupported type {data_frame[column].dtype}. "
                f"Date/time columns must be converted to string. "
                f"The expected date/time format can be queried "
                f"using ScoringCodeModel.date_format"
            )


def _java_date_format_to_python(java_format: str) -> str:
    # The order is important. Longer identifiers needs to come before shorter ones
    # yyyy before yy and MM before M
    replace = OrderedDict(
        [
            ("%", "%%"),
            ("yyyy", "%Y"),
            ("yy", "%y"),
            ("a", "%p"),
            ("E", "%a"),
            ("dd", "%d"),
            ("MM", "%m"),
            ("M", "%b"),
            ("HH", "%H"),
            ("hh", "%I"),
            ("mm", "%M"),
            ("S", "%f"),
            ("ss", "%S"),
            ("Z", "%z"),
            ("z", "%Z"),
            ("D", "%j"),
            ("w", "%U"),
            ("'T'", "T"),
            ("'Z'", "Z"),
        ]
    )

    return re.sub("|".join(replace.keys()), lambda match: replace[match[0]], java_format)


@click.command()
@click.argument("model", type=click.Path(exists=True))
@click.argument("input_csv", type=click.File(mode="r"))
@click.argument("output_csv", type=click.File(mode="w"))
@click.option("--forecast_point")
@click.option("--predictions_start_date")
@click.option("--predictions_end_date")
@click.option("--with_explanations", is_flag=True)
@click.option("--prediction_intervals_length")
def cli(
    model: str,
    input_csv: TextIOWrapper,
    output_csv: TextIOWrapper,
    forecast_point: Optional[str],
    predictions_start_date: Optional[str],
    predictions_end_date: Optional[str],
    with_explanations: bool,
    prediction_intervals_length: int,
) -> None:
    """
    Command Line Interface main function.

    Parameters
    ----------
    model
    input_csv
    output_csv
    forecast_point
    predictions_start_date
    predictions_end_date
    with_explanations
    prediction_intervals_length
    """
    scoring_code_model = ScoringCodeModel(model)

    ts_type = (
        TimeSeriesType.HISTORICAL
        if (predictions_start_date or predictions_end_date)
        else TimeSeriesType.FORECAST
    )

    df = pd.read_csv(input_csv, dtype="str")
    start = time.time()
    result = scoring_code_model.predict(
        df,
        forecast_point=(isoparse(forecast_point) if forecast_point else None),
        predictions_start_date=(
            isoparse(predictions_start_date) if predictions_start_date else None
        ),
        predictions_end_date=(isoparse(predictions_end_date) if predictions_end_date else None),
        time_series_type=ts_type,
        max_explanations=(3 if with_explanations else 0),
        prediction_intervals_length=prediction_intervals_length,
    )
    print(f"Scoring took: {time.time() - start}")

    result.to_csv(output_csv, index=False, date_format="%Y-%m-%dT%H:%M:%S.%fZ")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
