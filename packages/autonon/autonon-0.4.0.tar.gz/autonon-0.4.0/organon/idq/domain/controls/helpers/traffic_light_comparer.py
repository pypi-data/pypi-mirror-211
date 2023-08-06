"""This module includes TrafficLightComparer class"""
import math
from typing import List

from organon.fl.core.helpers import float_helper
from organon.idq.domain.algorithms.objects.mean_ci_comparison_input import MeanConfidenceIntervalComparisonInput
from organon.idq.domain.algorithms.objects.time_series_comparison_input import TimeSeriesComparisonInput
from organon.idq.domain.algorithms.objects.traffic_light_comparison_input import TrafficLightComparisonInput
from organon.idq.domain.businessobjects.dq_comparison_result import DqComparisonResult
from organon.idq.domain.controls.helpers.algorithms.predictor_factory import PredictorFactory
from organon.idq.domain.controls.helpers.comparison_helper_functions import ComparisonHelperFunctions
from organon.idq.domain.enums.dq_pred_algorithm_type import DqPredAlgorithmType
from organon.idq.domain.enums.signal_type import SignalType


class TrafficLightComparer:
    """Class for TrafficLightComparer"""

    @staticmethod
    def get_dq_comparison_results_for_time_series(comparison_input: TimeSeriesComparisonInput) -> \
            List[DqComparisonResult]:
        """ :returns time series column based comparison results"""
        if TrafficLightComparer.__check_series_all_null(comparison_input.past_series):
            return []
        predictor = PredictorFactory.get_predictor(predictor=DqPredAlgorithmType.RANDOM_FOREST_REG)
        prediction_result = predictor.predict(comparison_input.past_series, comparison_input.current_value)
        nan_indexes = [i for i, val in enumerate(comparison_input.past_series) if math.isnan(val)]
        predictions, actual = prediction_result.predictions, prediction_result.actual
        root_mse = math.sqrt(prediction_result.mean_square_err)

        results = []
        is_current_value_nan = math.isnan(comparison_input.current_value)
        if is_current_value_nan:
            percentage_change = 1
        else:
            percentage_change = ComparisonHelperFunctions.get_percentage_change(predictions[-1], actual[-1])
        tl_signal = ComparisonHelperFunctions.get_traffic_light_signal(
            percentage_change, comparison_input.yellow_threshold, comparison_input.green_threshold)
        add_tl_results = tl_signal is not SignalType.GREEN
        if add_tl_results:
            results.extend(TrafficLightComparer.get_time_series_tl_results(comparison_input, actual, predictions,
                                                                           percentage_change, tl_signal))

        if is_current_value_nan:
            results.extend(TrafficLightComparer.get_time_series_ci_results(comparison_input, actual, predictions,
                                                                           root_mse))
        else:
            add_ci_results = ComparisonHelperFunctions.is_outside_confidence_interval(
                comparison_input.z_score, predictions[-1], root_mse, actual[-1])
            if add_ci_results:
                results.extend(TrafficLightComparer.get_time_series_ci_results(comparison_input, actual, predictions,
                                                                               root_mse))

        if is_current_value_nan:
            results.extend(TrafficLightComparer.get_time_series_ad_results(comparison_input, actual, predictions,
                                                                           float("nan")))
        else:
            abs_errors = TrafficLightComparer.__get_abs_errors(actual, predictions, nan_indexes)
            add_ad_results = abs_errors.index(max(abs_errors)) == len(abs_errors) - 1
            if add_ad_results:
                results.extend(TrafficLightComparer.get_time_series_ad_results(comparison_input, actual, predictions,
                                                                               abs_errors[-1]))

        return results

    @staticmethod
    def __get_abs_errors(actual: List[float], predictions: List[float], nan_indexes: List[int]) -> List[float]:
        abs_errors = []
        for i, val in enumerate(actual):
            predicted = predictions[i]
            if float_helper.is_extreme(val) or float_helper.is_extreme(predicted) or i in nan_indexes:
                err = 0.0
            else:
                err = abs(val - predicted)
            abs_errors.append(err)

        return abs_errors

    @staticmethod
    def __check_series_all_null(series: List[float]):
        for val in series:
            if not math.isnan(val):
                return False
        return True

    @staticmethod
    def get_time_series_ci_results(comparison_input: TimeSeriesComparisonInput, actual: List[float],
                                   predictions: List[float], root_mean_square_err: float) -> \
            List[DqComparisonResult]:
        """ :returns out of confidence interval results"""
        results = []
        result1 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ci_code,
            property_code="CurrentValue",
            message=comparison_input.ci_message)
        result1.signal_type = SignalType.RED
        result1.property_key_numeric = comparison_input.current_value
        results.append(result1)

        result2 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ci_code,
            property_code="PredictedValue",
            message=comparison_input.ci_message)
        result2.signal_type = SignalType.RED
        result2.property_key_numeric = predictions[-1]
        results.append(result2)

        result3 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ci_code,
            property_code="ConfidenceIntervalLowerBound",
            message=comparison_input.ci_message)
        result3.signal_type = SignalType.RED
        result3.property_key_numeric = predictions[-1] - comparison_input.z_score * root_mean_square_err
        results.append(result3)

        result4 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ci_code,
            property_code="ConfidenceIntervalUpperBound",
            message=comparison_input.ci_message)
        result4.signal_type = SignalType.RED
        result4.property_key_numeric = predictions[-1] + comparison_input.z_score * root_mean_square_err
        results.append(result4)

        for actual_val, pred_val in zip(actual, predictions):
            result = DqComparisonResult(
                data_entity=comparison_input.data_entity,
                data_entity_name=comparison_input.data_entity_name,
                test_group=comparison_input.test_group,
                result_code=comparison_input.ci_code,
                property_code="TimeSeriesAndPredictions",
                message=comparison_input.ci_message)
            result.signal_type = SignalType.RED
            result.property_key_nominal = f"({actual_val}, {pred_val})"
            results.append(result)
        return results

    @staticmethod
    def get_time_series_ad_results(comparison_input: TimeSeriesComparisonInput, actual: List[float],
                                   predictions: List[float], abs_error: float) -> \
            List[DqComparisonResult]:
        """ :returns absolute error maximum results"""
        results = []
        result1 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ad_code,
            property_code="CurrentValue",
            message=comparison_input.ad_message)
        result1.signal_type = SignalType.RED
        result1.property_key_numeric = comparison_input.current_value
        results.append(result1)

        result2 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ad_code,
            property_code="PredictedValue",
            message=comparison_input.ad_message)
        result2.signal_type = SignalType.RED
        result2.property_key_numeric = predictions[-1]
        results.append(result2)

        result3 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ad_code,
            property_code="AbsoluteDeviationBetweenActualAndPredicted",
            message=comparison_input.ad_message)
        result3.signal_type = SignalType.RED
        result3.property_key_numeric = abs_error
        results.append(result3)

        result4 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.ad_code,
            property_code="LastDeviationIsTheMaximumDeviation",
            message=comparison_input.ad_message)
        result4.signal_type = SignalType.RED
        results.append(result4)

        for actual_val, pred_val in zip(actual, predictions):
            result = DqComparisonResult(
                data_entity=comparison_input.data_entity,
                data_entity_name=comparison_input.data_entity_name,
                test_group=comparison_input.test_group,
                result_code=comparison_input.ad_code,
                property_code="TimeSeriesAndPredictions",
                message=comparison_input.ad_message)
            result.signal_type = SignalType.RED
            result.property_key_nominal = f"({actual_val}, {pred_val})"
            results.append(result)
        return results

    @staticmethod
    def get_time_series_tl_results(comparison_input: TimeSeriesComparisonInput, actual: List[float],
                                   predictions: List[float], percentage_change: float,
                                   tl_signal: SignalType) -> List[DqComparisonResult]:
        """ :returns out of traffic light results"""
        results = []
        result1 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.tl_code,
            property_code="CurrentValue",
            message=comparison_input.tl_message)
        result1.signal_type = tl_signal
        result1.property_key_numeric = comparison_input.current_value
        results.append(result1)

        result2 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.tl_code,
            property_code="PredictedValue",
            message=comparison_input.tl_message)
        result2.signal_type = tl_signal
        result2.property_key_numeric = predictions[-1]
        results.append(result2)

        result3 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.tl_code,
            property_code="PercentageDeviationBetweenActualAndPredicted",
            message=comparison_input.tl_message)
        result3.signal_type = tl_signal
        result3.property_key_numeric = percentage_change
        results.append(result3)

        result4 = DqComparisonResult(
            data_entity=comparison_input.data_entity,
            data_entity_name=comparison_input.data_entity_name,
            test_group=comparison_input.test_group,
            result_code=comparison_input.tl_code,
            property_code="SignalType",
            message=comparison_input.tl_message)
        result4.signal_type = tl_signal
        result4.property_key_nominal = tl_signal.name
        results.append(result4)

        for actual_val, pred_val in zip(actual, predictions):
            result = DqComparisonResult(
                data_entity=comparison_input.data_entity,
                data_entity_name=comparison_input.data_entity_name,
                test_group=comparison_input.test_group,
                result_code=comparison_input.tl_code,
                property_code="TimeSeriesAndPredictions",
                message=comparison_input.tl_message)
            result.signal_type = tl_signal
            result.property_key_nominal = f"({actual_val}, {pred_val})"
            results.append(result)
        return results

    @staticmethod
    def get_mi_comparison_results(mi_comparison_input: MeanConfidenceIntervalComparisonInput, control_mean: float,
                                  control_std_err: float) -> List[DqComparisonResult]:
        """ :returns confidence interval results"""
        results = []
        if ComparisonHelperFunctions.is_outside_confidence_interval(mi_comparison_input.z_score,
                                                                    control_mean,
                                                                    control_std_err,
                                                                    mi_comparison_input.current_value):
            result = DqComparisonResult(
                data_entity=mi_comparison_input.data_entity,
                data_entity_name=mi_comparison_input.data_entity_name,
                test_group=mi_comparison_input.test_group,
                result_code=mi_comparison_input.result_code,
                property_code="TestValue",
                message=mi_comparison_input.message)
            result.property_key_numeric = mi_comparison_input.current_value
            results.append(result)

            result = DqComparisonResult(
                data_entity=mi_comparison_input.data_entity,
                data_entity_name=mi_comparison_input.data_entity_name,
                test_group=mi_comparison_input.test_group,
                result_code=mi_comparison_input.result_code,
                property_code="LowerConfidenceLevel",
                message=mi_comparison_input.message)
            result.property_key_numeric = control_mean - mi_comparison_input.z_score * control_std_err
            results.append(result)

            result = DqComparisonResult(
                data_entity=mi_comparison_input.data_entity,
                data_entity_name=mi_comparison_input.data_entity_name,
                test_group=mi_comparison_input.test_group,
                result_code=mi_comparison_input.result_code,
                property_code="UpperConfidenceLevel",
                message=mi_comparison_input.message)
            result.property_key_numeric = control_mean + mi_comparison_input.z_score * control_std_err
            results.append(result)
        return results

    @staticmethod
    def get_tl_comparison_results(tl_comparison_input: TrafficLightComparisonInput, control_mean: float) -> \
            List[DqComparisonResult]:
        """:returns traffic light comparison results"""
        percentage_change = ComparisonHelperFunctions.get_percentage_change(tl_comparison_input.current_value,
                                                                            control_mean)
        signal_type = ComparisonHelperFunctions.get_traffic_light_signal(percentage_change,
                                                                         tl_comparison_input.yellow_threshold,
                                                                         tl_comparison_input.green_threshold)
        results = []
        if signal_type in [SignalType.YELLOW, SignalType.RED]:
            result = DqComparisonResult(
                data_entity=tl_comparison_input.data_entity,
                data_entity_name=tl_comparison_input.data_entity_name,
                test_group=tl_comparison_input.test_group,
                result_code=tl_comparison_input.result_code,
                property_code="TrafficLightSignal",
                message=tl_comparison_input.message)
            result.property_key_nominal = signal_type.name
            results.append(result)

            result = DqComparisonResult(
                data_entity=tl_comparison_input.data_entity,
                data_entity_name=tl_comparison_input.data_entity_name,
                test_group=tl_comparison_input.test_group,
                result_code=tl_comparison_input.result_code,
                property_code="ControlValue",
                message=tl_comparison_input.message)
            result.property_key_numeric = control_mean
            results.append(result)

            result = DqComparisonResult(
                data_entity=tl_comparison_input.data_entity,
                data_entity_name=tl_comparison_input.data_entity_name,
                test_group=tl_comparison_input.test_group,
                result_code=tl_comparison_input.result_code,
                property_code="TestValue",
                message=tl_comparison_input.message)
            result.property_key_numeric = tl_comparison_input.current_value
            results.append(result)

            result = DqComparisonResult(
                data_entity=tl_comparison_input.data_entity,
                data_entity_name=tl_comparison_input.data_entity_name,
                test_group=tl_comparison_input.test_group,
                result_code=tl_comparison_input.result_code,
                property_code="PercentageChange",
                message=tl_comparison_input.message)
            result.property_key_numeric = percentage_change
            results.append(result)
        return results

    @staticmethod
    def get_mi_tl_comparison_results(mi_comparison_input: MeanConfidenceIntervalComparisonInput,
                                     tl_comparison_input: TrafficLightComparisonInput) -> List[DqComparisonResult]:
        """ :returns confidence interval_comparison_result"""
        control_mean, control_std_err = ComparisonHelperFunctions.compute_control_mean_std_avg(
            mi_comparison_input.past_series)
        results = []
        results.extend(
            TrafficLightComparer.get_mi_comparison_results(mi_comparison_input, control_mean, control_std_err))
        results.extend(TrafficLightComparer.get_tl_comparison_results(tl_comparison_input, control_mean))
        return results
