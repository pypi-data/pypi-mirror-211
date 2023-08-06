"""Module for FastModelBuilder"""
import numpy as np
from scipy.stats import t, f

from organon.fl.mathematics.linearalgebra.blas_service_factory import BlasServiceFactory
from organon.fl.mathematics.sweep.covariance_generator import CovarianceGenerator
from organon.fl.mathematics.sweep.data_classes.linear_regression_algorithm_settings import \
    LinearRegressionAlgorithmSettings
from organon.fl.mathematics.sweep.data_classes.linear_regression_parameter import LinearRegressionParameter
from organon.fl.mathematics.sweep.data_classes.linear_regression_results import LinearRegressionResults
from organon.fl.mathematics.sweep.data_classes.linear_regression_step import LinearRegressionStep
from organon.fl.mathematics.sweep.data_classes.selected_attribute import SelectedAttribute
from organon.fl.mathematics.sweep.data_classes.transformation import Transformation
from organon.fl.mathematics.sweep.enums import AttributeSelectionStatus, TestStatisticsType, \
    RegressionAttributeSelectionMethod
from organon.fl.mathematics.sweep.matrices.i_matrix import IMatrix
from organon.fl.mathematics.sweep.sweep_operator import SweepOperator


class FastModelBuilder:
    """This is the class where everything gets together. It takes an input matrix. Calculates the attributes
    to be included or excluded every step according to settings. And of the method it returns the independent
    attributes that defines the target
    See ftp://public.dhe.ibm.com/software/analytics/spss/support/Stats/Docs/Statistics/Algorithms/13.0/regression.pdf
    for the more details."""

    def __init__(self, settings: LinearRegressionAlgorithmSettings, inputs: IMatrix, validation: IMatrix):
        """Initializes the model."""
        self._settings = settings
        self._inputs = inputs
        self._validation = validation
        self._target = self._settings.target
        self._weight = self._settings.weight

        bool(self._validation is not None)

        cols = self._inputs.shape[1]

        self._transformations = []
        for _col in range(cols):
            self._transformations.append(Transformation(0, 0, 0, False))

        blas_service = BlasServiceFactory.get_blas_service()

        self._training_sigma_generator = CovarianceGenerator(False, inputs, self._transformations, self._weight,
                                                             blas_service)
        self._training_sigma_generator.initialize()
        self._training_covariances = self._training_sigma_generator.covariance_info
        self._validation_covariances = None
        if self._validation is not None:
            self._validation_sigma_generator = CovarianceGenerator(False, validation, self._transformations,
                                                                   self._weight, blas_service)
            self._validation_sigma_generator.initialize()
            self._validation_covariances = self._validation_sigma_generator.covariance_info

        self._sweep_operator = SweepOperator(self._training_covariances.correlation_matrix,
                                             self._training_covariances.covariance_matrix, self._target, blas_service)

        self._regression_report = []
        self._regression_results = None

        self._swept = None
        self._non_swept = None

    def _validate(self):
        """Validates the inputs for the Model"""
        if self._settings is None:
            raise ValueError("Algorithm Settings can not be None as argument to Linear Regression object")

        if self._inputs is None:
            raise ValueError("Input matrix can not be None as argument to Linear Regression object")

        if self._target not in range(self._inputs.shape[1]):
            raise IndexError("Target is out of bounds for input matrix")

        if self._weight is None:
            raise ValueError("Weight can not be None as argument to Linear Regression object")

        if self._weight.shape[0] != self._inputs.shape[1]:
            raise ValueError("Weight shape and input shape don't fit. "
                             f"Weight should include {self._inputs.shape[1]} elements")

    def build_model(self):
        """Builds the model. Initializes the variables and calculates the diagonal entries of the covariance
        matrix and the target row and column. Starts the selection method according to settings. Then
        calculates the results. Finally sweep back the correlation matrix to initial matrix."""
        print("Building Model...")
        self._validate()
        self._training_sigma_generator.compute_variances()
        self._training_sigma_generator.compute_covariances(self._target)

        if self._validation is not None:
            self._validation_sigma_generator.compute_variances()
            self._validation_sigma_generator.compute_covariances(self._target)
        print("Variances and Covariances of target calculated")

        eligible_inputs = self._training_covariances.get_non_zero_variance_attributes()
        eligible_inputs.remove(self._target)
        self._swept = set()
        self._non_swept = set(eligible_inputs)

        if self._settings.attribute_selection_method == RegressionAttributeSelectionMethod.FORWARD:
            print("Forward Selection")
            self._forward_selection()

        if self._settings.attribute_selection_method == RegressionAttributeSelectionMethod.STEPWISE:
            print("Stepwise selection")
            self._stepwise_selection()
        print("Getting results...")
        self._regression_results = self._get_linear_regression_results()
        print("Sweeping back correlation matrix")
        self._sweep_fast_row(self._training_covariances.correlation_matrix, self._target, self._swept)

    @staticmethod
    def _tolerance_check(correlation_matrix: np.ndarray, swept: set, k: int, tolerance: float) -> bool:
        """Checks if the attribute can pass the tolerance check."""
        if correlation_matrix[k, k] < tolerance:
            return False

        for i in swept:
            if (correlation_matrix[i, i] - correlation_matrix[i, k] * correlation_matrix[k, i]) \
                    / correlation_matrix[k, k] * tolerance > 1.0:
                return False

        return True

    def _forward_selection(self):
        """Every time it gets the attribute. If there is no attribute that pass the conditions then selection
        is complete"""
        step = self._get_next_step()

        while True:
            print("Step = ", step)
            included = self._include_step()
            if included is None:
                break
            print("Including", included.attribute_name)
            self._update_reg_report(step, included)
            step += 1

    def _stepwise_selection(self):
        """Every step calculates the including and excluding attributes to the model. If there is not then exit.
        If they are the same we are in loop. Exit."""
        step = self._get_next_step()

        while True:
            print("Step = ", step)
            included = self._include_step()
            if included is not None:
                print("Including", included.attribute_name)
                self._update_reg_report(step, included)
                step += 1

            excluded = self._exclude_step()
            if excluded is not None:
                print("Excluding", excluded.attribute_name)
                self._update_reg_report(step, excluded)
                step += 1

            if included is None and excluded is None:
                break

            if excluded is not None and included is not None and excluded.attribute_name == included.attribute_name:
                break

    def _get_next_step(self) -> int:
        """Gets the step number according to the report."""
        return 1 if len(self._regression_report) == 0 else len(self._regression_report)

    def _update_reg_report(self, step: int, attribute: SelectedAttribute):
        """Updates the report with the new attribute"""
        anova = self._get_linear_regression_results()
        regression_step = LinearRegressionStep(step=step, selected_attribute=attribute, anova=anova)

        self._regression_report.append(regression_step)

    def _get_f_index_k_pairs(self, correlation_matrix, p_star):
        """Calculates the f_enter k pairs with f_enter values are eligible. Then returns the sorted list with
         highest f_enter value attribute first."""
        f_index_k_pairs = []
        for k in self._non_swept:
            # print("target = {}, k = {}".format(target, k))
            # print("calculating f_enter for ", k)
            v_k = correlation_matrix[self._target, k] * correlation_matrix[k, self._target] / correlation_matrix[k, k]
            delta = np.abs(correlation_matrix[self._target, self._target] - v_k)

            f_enter = float('+inf')
            # print("Delta for {0} = {1}".format(k, delta))

            if delta > np.finfo('float').eps:
                f_enter = (self._training_covariances.total_case_weight - p_star - 1) * v_k / delta

            if f_enter < self._settings.inclusion_f_statistics:
                continue

            base_condition = FastModelBuilder._tolerance_check(correlation_matrix, self._swept, k,
                                                               self._settings.tolerance)

            if correlation_matrix[self._target, k] > 0 and base_condition \
                    if self._settings.use_positive_coefficients else base_condition:
                f_index_k_pairs.append((f_enter, k))

        return sorted(f_index_k_pairs, key=lambda x: x[0], reverse=True)

    def _get_included_attribute(self, correlation_matrix, f_index_k_pairs, pre_r2_training, pre_r2_validation):
        """For the values that are eligible it returns the first element that changes the performance large
        enough according to sweep operator"""
        for pair in f_index_k_pairs:
            f_statistics = pair[0]
            k = pair[1]
            print(f"Got {k} with {f_statistics}")

            post_r2_training = self._get_training_r_squared(correlation_matrix, self._target, k)
            r2_delta_training = post_r2_training - pre_r2_training

            if r2_delta_training < self._settings.min_r_squared_change_in_train_set:
                break

            max_vif = FastModelBuilder._get_max_v_if(FastModelBuilder.updated_diagonals(correlation_matrix,
                                                                                        self._swept, k))

            if max_vif > self._settings.maximum_vif:
                continue

            if self._settings.use_positive_coefficients:
                updated_target_row = FastModelBuilder._updated_target_row(correlation_matrix, self._swept, self._target,
                                                                          k)
                if not FastModelBuilder._all_positive(updated_target_row):
                    continue
            self._training_sigma_generator.compute_covariances(k)
            if self._validation is not None:
                self._validation_sigma_generator.compute_covariances(k)
            # print("before sweep for ", k)
            # print(self._training_covariances.correlation_matrix)
            self._sweep_operator.sweep(k)
            # print("after sweep for ", k)
            # print(self._training_covariances.correlation_matrix)
            self._include(k)

            performance_change_is_large = True
            post_r2_validation = float('nan')
            r2_delta_validation = float('nan')

            if self._validation is not None:
                post_r2_validation = self._get_validation_r_squared()
                r2_delta_validation = post_r2_validation - pre_r2_validation

                if r2_delta_validation < self._settings.min_r_squared_change_in_validation_set:
                    performance_change_is_large = False

            if performance_change_is_large:
                print(f"performance change for {k} is okay")
                return SelectedAttribute(
                    attribute_name=k,
                    selection_status=AttributeSelectionStatus.INCLUDED,
                    selection_test_statistics=TestStatisticsType.F_STATISTICS,
                    selection_statistics=f_statistics,
                    updated_training_performance=post_r2_training,
                    updated_validation_performance=post_r2_validation if self._validation is not None else float('nan'),
                    performance_change_in_training_set=r2_delta_training,
                    performance_change_in_validation_set
                    =r2_delta_validation if self._validation is not None else float('nan')
                )

            # print("Sweep back for", k)
            self._sweep_operator.sweep(k)
            self._exclude(k)
        return None

    def _include_step(self) -> SelectedAttribute:
        """It selects the included attribute according to f_enter,k pairs and the performance change with sweep
        operator."""
        print("Checking any variable to be included")
        p_star = 1 + len(self._swept) if self._settings.use_intercept else len(self._swept)

        correlation_matrix = self._training_covariances.correlation_matrix

        pre_r2_training = 0.0
        pre_r2_validation = 0.0

        if len(self._swept) > 0:
            pre_r2_training = self._get_training_r_squared(correlation_matrix, self._target)

            if self._validation is not None:
                pre_r2_validation = self._get_validation_r_squared()

        f_index_k_pairs = self._get_f_index_k_pairs(correlation_matrix, p_star)

        return self._get_included_attribute(correlation_matrix, f_index_k_pairs, pre_r2_training, pre_r2_validation)

    def _exclude_step(self) -> SelectedAttribute:
        """Does the same thing with the include step according to f_remove values."""
        print("Checking any variable to be excluded")

        p_star = 1 + len(self._swept) if self._settings.use_intercept else len(self._swept)

        correlation_matrix = self._training_covariances.correlation_matrix

        f_out = self._settings.exclusion_f_statistics

        f_index_k_pairs = []

        for k in self._swept:

            v_k = np.abs(correlation_matrix[self._target, k] * correlation_matrix[k, self._target]
                         / correlation_matrix[k, k])

            f_remove = ((self._training_covariances.total_case_weight - p_star) * v_k
                        / correlation_matrix[self._target, self._target])

            if f_remove < f_out:
                f_index_k_pairs.append((f_remove, k))

        if len(f_index_k_pairs) <= 0:
            print("Nothing excluded")
            return None

        min_pair = min(f_index_k_pairs, key=lambda x: x[0])

        selected_index = min_pair[1]
        f_out_statistics = min_pair[0]

        print(f"Got {selected_index} with {f_out_statistics}")

        pre_r2_training = 0.0
        pre_r2_validation = 0.0

        if len(self._swept) > 0:
            pre_r2_training = self._get_training_r_squared(correlation_matrix, self._target)

            if self._validation is not None:
                pre_r2_validation = self._get_validation_r_squared()

        self._sweep_operator.sweep(selected_index)
        self._exclude(selected_index)

        post_r2_training = self._get_training_r_squared(correlation_matrix, self._target)
        post_r2_validation = self._get_validation_r_squared()

        return SelectedAttribute(attribute_name=selected_index,
                                 selection_status=AttributeSelectionStatus.EXLUDED,
                                 selection_test_statistics=TestStatisticsType.F_STATISTICS,
                                 selection_statistics=f_out_statistics,
                                 updated_training_performance=post_r2_training,
                                 updated_validation_performance
                                 =post_r2_validation if self._validation is not None else float(
                                     'nan'),
                                 performance_change_in_training_set=post_r2_training - pre_r2_training,
                                 performance_change_in_validation_set
                                 =post_r2_validation - pre_r2_validation if self._validation is not None else float(
                                     'nan'))

    @staticmethod
    def _get_training_r_squared(correlation_matrix: np.ndarray, target: int, *arg) -> float:
        """Returns the training r squared. See the paper."""
        if len(arg) == 0:
            swept_r = correlation_matrix
            return 1.0 - swept_r[target, target]

        if len(arg) == 1:
            non_swept_r = correlation_matrix
            k = arg[0]

            return 1.0 - non_swept_r[target, target] + non_swept_r[target, k] * non_swept_r[k, target] / non_swept_r[
                k, k]
        return None

    def _include(self, attribute: int):
        """Includes the attribute"""
        self._swept.add(attribute)
        self._non_swept.remove(attribute)

    def _exclude(self, attribute: int):
        """Excludes the attribute"""
        self._swept.remove(attribute)
        self._non_swept.add(attribute)

    def _get_validation_r_squared(self) -> float:
        """Returns the validation r squared"""
        model = self._get_linear_regression_results()

        linear_form = {x: model.parameters[x].estimate for x in model.parameters}

        covariance = self._validation_covariances.get_covariances(linear_form, self._target)
        target_variance = self._validation_covariances.covariance_matrix[self._target, self._target]
        linear_form_variance = self._validation_covariances.get_variances(linear_form)

        target_variance_is_non_zero = ~np.isinf(target_variance) and ~np.isnan(target_variance) and target_variance > 0
        linear_form_variance_is_non_zero = (~np.isinf(linear_form_variance) and ~np.isnan(linear_form_variance) and
                                            linear_form_variance > 0)
        covariance_is_not_extreme = ~np.isinf(covariance) and ~np.isnan(covariance)

        if target_variance_is_non_zero and linear_form_variance_is_non_zero and covariance_is_not_extreme:
            rho = covariance / np.sqrt(linear_form_variance * target_variance)
            rho_is_not_extreme = ~np.isinf(rho) and ~np.isnan(rho)
            return rho * rho if rho_is_not_extreme else 0.0

        return 0.0

    @staticmethod
    def _get_max_v_if(updated_diagonals: dict) -> float:
        """Returns the max of the updated diagonals"""
        return float('-inf') if len(updated_diagonals) < 2 else max(updated_diagonals.values())

    @staticmethod
    def updated_diagonals(correlation_matrix: np.ndarray, swept: set, k: int) -> dict:
        """Calculates the updated diagonal values for the correlation matrix"""
        diags = {}
        for i in swept:
            updated_r = correlation_matrix[i, i] - correlation_matrix[i, k] * correlation_matrix[k, i] / \
                        correlation_matrix[k, k]
            diags[i] = updated_r
        diags[k] = 1.0 / correlation_matrix[k, k]

        return diags

    @staticmethod
    def _all_positive(swept_diagonals: dict) -> bool:
        """Check if the all values are positive"""
        return all(value > 0 for value in swept_diagonals.values())

    @staticmethod
    def _updated_target_row(correlation_matrix: np.ndarray, swept: set, target: int, k: int) -> dict:
        """Calculates the updated row for the correlation matrix"""
        diags = {}
        for i in swept:
            updated_r = correlation_matrix[i, i] - correlation_matrix[i, k] * correlation_matrix[k, i] / \
                        correlation_matrix[k, k]
            diags[i] = updated_r
        diags[k] = correlation_matrix[target, k] / correlation_matrix[k, k]

        return diags

    def _get_linear_regression_parameters(self):
        """Calculates the statistical info for the every swept attribute."""
        covariance_matrix = self._training_covariances.covariance_matrix
        correlation_matrix = self._training_covariances.correlation_matrix
        total_case_weight = self._training_covariances.total_case_weight
        p_star = len(self._swept) + 1 if self._settings.use_intercept else len(self._swept)
        parameters = {}
        t_dist = t(total_case_weight - p_star)

        for i in self._swept:
            estimate = correlation_matrix[self._target, i] * np.sqrt(
                covariance_matrix[self._target, self._target] / covariance_matrix[i, i])
            standard_error = np.sqrt(
                correlation_matrix[i, i] * correlation_matrix[self._target, self._target]
                * covariance_matrix[self._target, self._target]) \
                             / (covariance_matrix[i, i] * (total_case_weight - p_star))
            sigma = 0.0 if standard_error <= 0 or np.isnan(standard_error) else standard_error
            t_statistics = float('+inf') if sigma <= 0 else estimate / sigma
            absolute_t_statistics = np.abs(t_statistics)
            vif = correlation_matrix[i, i]
            p_value = 0.0 if np.isinf(absolute_t_statistics) else 1 - t_dist.cdf(absolute_t_statistics)
            parameters[i] = LinearRegressionParameter(estimate, standard_error, t_statistics, p_value, vif,
                                                      float('nan'),
                                                      float('nan'),
                                                      float('nan'))
        return parameters

    def _get_linear_regression_results(self) -> LinearRegressionResults:
        """Calculates the statistical info for the results."""
        covariance_matrix = self._training_covariances.covariance_matrix
        correlation_matrix = self._training_covariances.correlation_matrix
        total_case_weight = self._training_covariances.total_case_weight
        p_star = len(self._swept) + 1 if self._settings.use_intercept else len(self._swept)

        model_detail = LinearRegressionResults()
        model_detail.sample_size = total_case_weight
        model_detail.model_degrees_of_freedom = len(self._swept)
        model_detail.error_degrees_of_freedom = total_case_weight - p_star
        model_detail.r_square = 1 - correlation_matrix[self._target, self._target]
        model_detail.adjusted_r_square = model_detail.r_square - (len(self._swept) * (1.0 - model_detail.r_square)) / (
                total_case_weight - p_star)
        model_detail.residual_sum_of_squares = correlation_matrix[self._target, self._target] \
                                               * (total_case_weight - 1) * covariance_matrix[self._target, self._target]

        model_detail.explained_sum_of_squares = model_detail.r_square * (total_case_weight - 1) * covariance_matrix[
            self._target, self._target]
        model_detail.total_sum_of_squares = (model_detail.residual_sum_of_squares +
                                             model_detail.explained_sum_of_squares)
        model_detail.mean_square_regression = (model_detail.explained_sum_of_squares /
                                               model_detail.model_degrees_of_freedom)
        model_detail.mean_square_error = model_detail.residual_sum_of_squares / model_detail.error_degrees_of_freedom

        if model_detail.model_degrees_of_freedom > 0:
            f_distribution = f(model_detail.model_degrees_of_freedom, model_detail.error_degrees_of_freedom)

            f_statistics = model_detail.mean_square_regression / model_detail.mean_square_error \
                if model_detail.mean_square_error > 0 else float('+inf')
            p_value = 0.0 if np.isinf(f_statistics) else 1.0 - f_distribution.cdf(f_statistics)
            model_detail.f_statistics = f_statistics
            model_detail.f_statistics_p_value = p_value

        model_detail.parameters = self._get_linear_regression_parameters()

        means = self._training_covariances.means
        if self._settings.use_intercept:
            bias = means[self._target]

            for i in model_detail.parameters:
                attribute_mean = means[i]
                bias -= model_detail.parameters[i].estimate * attribute_mean

            model_detail.bias_dict['estimate'] = bias

        else:
            model_detail.bias_dict['estimate'] = 0.0

        model_detail.bias_dict['p_value'] = 0.0
        model_detail.bias_dict['standard_error'] = 0.0
        model_detail.bias_dict['t_statistics'] = 0.0

        return model_detail

    def _sweep_fast_row(self, matrix: np.ndarray, target: int, swept_list: set):
        """Calls sweep algorithm for the sweeping back all the swept attributes."""
        for row in swept_list:
            self._sweep_operator.sweep_fast_row(matrix, row, target, swept_list, matrix.shape[1])
