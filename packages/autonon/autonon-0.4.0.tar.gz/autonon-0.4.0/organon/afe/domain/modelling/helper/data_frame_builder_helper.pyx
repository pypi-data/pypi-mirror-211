# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: language_level=3
# cython: linetrace=False
# distutils: define_macros=CYTHON_TRACE_=0


from libcpp.algorithm cimport sort
from libc.math cimport isnan
from libcpp cimport bool as bool_t
from libcpp.map cimport map as cmap
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.set  cimport set
from cython.operator import dereference
import numpy as np
cimport numpy as c_np
from organon.afe.domain.enums.afe_operator import AfeOperator
from organon.afe.dataaccess.services.transaction_file_record_reader import TransactionFileRecordReader

cdef:
    int DENSITY_INDEX = 0
    int MIN_INDEX = 1
    int MAX_INDEX = 2
    int SUM_INDEX = 3
    int FREQUENCY_INDEX = 4
    int COUNT_DISTINCT_INDEX = 5
    int MODE_INDEX = 6
    int TIME_SINCE_FIRST_INDEX = 7
    int TIME_SINCE_LAST_INDEX = 8

    c_np.float32_t NAN_VAL = np.nan
    agg_index_map = {
        AfeOperator.Density.value:0,
        AfeOperator.Min.value:1,
        AfeOperator.Max.value:2,
        AfeOperator.Sum.value:3,
        AfeOperator.Frequency.value:4,
        AfeOperator.CountDistinct.value:5,
        AfeOperator.Mode.value:6,
        AfeOperator.TimeSinceFirst.value:7,
        AfeOperator.TimeSinceLast.value:8,

    }
    cmap[int, int] AGGREGATE_INDEX_MAP = agg_index_map
    int RATIO_KEY = AfeOperator.Ratio.value
    int TIMESINCEFIRST_KEY = AfeOperator.TimeSinceFirst.value
    int TIMESINCELAST_KEY = AfeOperator.TimeSinceLast.value
    int SUM_KEY = AfeOperator.Sum.value
    int DENSITY_KEY = AfeOperator.Density.value
    int FREQUENCY_KEY = AfeOperator.Frequency.value
    int COUNT_DISTINCT_KEY = AfeOperator.CountDistinct.value
    int MODE_KEY = AfeOperator.Mode.value

    int UNKNOWN_DIMENSION_VALUE = TransactionFileRecordReader.UNKNOWN_DIMENSION_VALUE

def execute(
        float[:,:] result_frame,
        int c_num_threads,
        int date_col_index,
        int d_index,
        int q_index,
        int[:,:] splits,
        vector[int] horizons,
        int offset,
        int resolution,
        cmap[short, short] &index_map,
        c_np.int64_t[:,:] &trx_dates,
        c_np.float32_t[:,:] &trx_q_arrays,
        c_np.int8_t[:,:] &trx_d_arrays,
        cmap[int, c_np.int32_t[:]] &entity_index_map,
        c_np.int64_t[:] &target_dates ,
        vector[int] included_operators,
        vector[int] included_operator_set_one,
        vector[int] included_operator_set_two,
        cmap[long long, int] &column_name_map,
        int nearest_exponent,
        int dim_group_id = -1,
        bool_t for_afe_columns = False,
        bool_t is_no_dim_col = False
        ):
    cdef :
        int splits_size = splits.shape[0]
        int i

    for i in range(splits_size):
        exec_for_split(
            result_frame,
            i,
            splits_size,
            splits[i],
            date_col_index,
            d_index, q_index,
            offset,
            horizons,
            resolution,
            index_map,
            trx_dates,
            trx_q_arrays,
            trx_d_arrays,
            entity_index_map,
            target_dates,
            included_operators,
            included_operator_set_one,
            included_operator_set_two,
            column_name_map,
            nearest_exponent,
            dim_group_id,
            for_afe_columns,
            is_no_dim_col
            )

cdef void exec_for_split(
        float[:,:] &result_frame,
        int split_index,
        int split_count,
        int[:] &pair_list,
        int date_col_index,
        int d_index,
        int q_index,
        int offset,
        vector[int] &horizons,
        int resolution,
        cmap[short, short] &index_map,
        c_np.int64_t[:,:] &trx_dates,
        c_np.float32_t[:,:] &trx_q_arrays,
        c_np.int8_t[:,:] &trx_d_arrays,
        cmap[int, c_np.int32_t[:]] &entity_index_map,
        c_np.int64_t[:] &target_dates,
        vector[int] &included_operators,
        vector[int] &included_operator_set_one,
        vector[int] &included_operator_set_two,
        cmap[long long, int] &column_name_map,
        int nearest_exponent,
        int dim_group_id,
        bool_t is_scoring,
        bool_t is_no_dim_col
        ) nogil :

    cdef:
        int index, record_index, entity_id_int, pair_index
        c_np.int64_t event_date
        set[int] hor_set = set[int]()
        vector[int] local_horizon_list = horizons
        set[short] distinct_index_map_values = set[short]()
    get_distinct_values(distinct_index_map_values, index_map)
    cdef int s = distinct_index_map_values.size()

    cdef int h, th, distinct_horizon
    if is_scoring:
        for h in range(horizons.size()):
            hor_set.insert(horizons[h])
        local_horizon_list.clear()
        for distinct_horizon in hor_set:
            local_horizon_list.push_back(distinct_horizon)

    cdef:
        int horizon_count = local_horizon_list.size()
        float[:,:,:] _dict
    with gil:
        _dict = np.full((s, horizon_count, 9), NAN_VAL, dtype=np.float32)

    cdef:
        int min_horizon = get_min(local_horizon_list)
        int max_horizon = get_max(local_horizon_list)
        int max_horizon_for_fill_row = get_max(horizons)

    for pair_index in range(pair_list.shape[0]):
        index = split_index+pair_index*split_count

        record_index = pair_list[pair_index]

        if record_index == -1:
            break
        entity_id_int = record_index
        event_date = target_dates[record_index]

        if entity_index_map.count(entity_id_int) > 0:
                get_aggregates_and_fill_row(_dict,
                                    index, result_frame, entity_id_int, event_date, horizons,
                                    index_map, entity_index_map[entity_id_int], resolution, offset,
                                    trx_dates, trx_q_arrays, trx_d_arrays, date_col_index, d_index, q_index,
                                    included_operators,
                                    included_operator_set_one, included_operator_set_two,
                                    column_name_map, nearest_exponent, local_horizon_list,
                                    distinct_index_map_values, min_horizon, max_horizon, max_horizon_for_fill_row,
                                    dim_group_id, is_scoring, is_no_dim_col)



    #printf("%d %d %d\n", min_horizon, max_horizon, entity_index_map.size())

cdef void get_aggregates_and_fill_row(
        float[:,:,:] _dict,
        int row_index,
        float[:,:] &result_frame,
        int entity_id_int,
        c_np.int64_t event_date,
        vector[int] &horizons,
        cmap[short, short] &index_map,
        c_np.int32_t[:] &entity_index_list,
        int resolution, int offset,
        c_np.int64_t[:,:] &trx_dates,
        c_np.float32_t[:,:] &trx_q_arrays,
        c_np.int8_t[:,:] &trx_d_arrays,
        int date_col_index,
        int d_index,
        int q_index,
        vector[int] &included_operators,
        vector[int] &included_operator_set_one,
        vector[int] &included_operator_set_two,
        cmap[long long, int] &column_name_map,
        int nearest_exponent,
        vector[int] &local_horizon_list,
        set[short] &distinct_index_map_values,
        int min_horizon,
        int max_horizon,
        int max_horizon_for_fill_row,
        int dim_group_id,
        bool_t is_scoring,
        bool_t is_no_dim_col
        ) nogil :

    if entity_index_list.shape[0] == 0:
        return

    cdef:
        cmap[short, pair[float, float]] time_histogram
        cmap[int, double] mode_by_horizon
        cmap[int, double] count_distinct_by_horizon
        int curr_horizon = -1
        cmap[short, int] c_val_indices = cmap[short, int]()
        cmap[int, short] c_val_reverse_indices = cmap[int, short]()
        cmap[int, int] horizon_indices = cmap[int, int]()
        cmap[int, int] horizon_reverse_indices = cmap[int, int]()
        cmap[short, cmap[int, short]] calculated_dims_and_horizons = cmap[short, cmap[int, short]]()
        cdef set[int] hor_set = set[int]()

    _dict[:,:,:] =  NAN_VAL

    cdef:
        int s = distinct_index_map_values.size()
        int horizon_count = local_horizon_list.size()
        c_np.int64_t grid_last_date = event_date
        c_np.int64_t grid_first_date = event_date
        vector[int] grid_horizons = local_horizon_list
        int grid_max_horizon = max_horizon
        c_np.int64_t grid_offset_last_date = 0
        vector[pair[c_np.int64_t, int]] grid_dates_ascended = vector[pair[c_np.int64_t, int]]()

    partition(grid_dates_ascended, &grid_offset_last_date, &grid_first_date, grid_last_date, offset, resolution,
              grid_horizons, grid_max_horizon)

    cdef:
        int index = 0
        pair[short, short] c_val_pair
        short val
    for val in distinct_index_map_values:
        c_val_indices[val] = index
        c_val_reverse_indices[index] = val
        calculated_dims_and_horizons[val] = cmap[int, short]()
        index += 1

    #printf("Entity index list size for %d : %d\n", entity_id_int, entity_index_list.shape[0])

    cdef:
        int horizon_index = 0
        int tmp_hor
        int lhli
    for lhli in range(local_horizon_list.size()):
        tmp_hor = local_horizon_list[lhli]
        horizon_indices[tmp_hor] = horizon_index
        horizon_reverse_indices[horizon_index] = tmp_hor
        horizon_index += 1

    cdef:
        int record_index, d_val, c_val_index, horizon, hor_index, last_horizon, i, j, hor, entity_index_list_i
        c_np.int64_t record_date
        c_np.float32_t q_val
        short c_val, tmp_c_val
        float[:] pre
        float[:] *curr_dict
        float span
        bool_t ratio_op_exists = contains(included_operators, RATIO_KEY)
        bool_t count_distinct_op_exists = contains(included_operators, COUNT_DISTINCT_KEY)
        bool_t mode_op_exists = contains(included_operators, MODE_KEY)
        bool_t check_for_dimension = is_scoring and not ratio_op_exists and not is_no_dim_col and not (count_distinct_op_exists or mode_op_exists)
        cmap[int, int] d_val_dict = cmap[int, int]()
    # For RATIO operator, all dimensions should be aggregated. Dimension group should not be checked if dimension_column is "NOD"


    for entity_index_list_i in range(entity_index_list.shape[0]):

        record_index = entity_index_list[entity_index_list_i]
        record_date = 0

        if date_col_index != -1:
            record_date = trx_dates[record_index][date_col_index]
            if is_scoring:
                if record_date > grid_offset_last_date:
                    continue
            else:
                if record_date >= grid_offset_last_date:
                    continue

            if record_date < grid_first_date:
                break

        q_val = trx_q_arrays[record_index][q_index]

        if is_scoring:
            if isnan(q_val) or q_val <= 0:
                continue
        else:
            if q_val <= 0:
                continue

        d_val = trx_d_arrays[record_index][d_index]
        if count_distinct_op_exists or mode_op_exists:
            if d_val_dict.count(d_val) > 0:
                d_val_dict[d_val] = d_val_dict[d_val] + 1
            else:
                d_val_dict[d_val] = 1
        c_val = index_map[d_val]
        c_val_index = c_val_indices[c_val]
        #with gil:
            #print("%d %d %d\n", d_val, c_val, c_val_index)
        if  date_col_index != -1:
            horizon = get_horizon(grid_offset_last_date, grid_dates_ascended, record_date, is_scoring)
        else:
            horizon = 1

        if check_for_dimension and c_val != dim_group_id:
            continue

        #printf("Record : %d %d %d %f\n", entity_id_int, horizon, c_val, q_val)


        hor_index = horizon_indices[horizon]


        span = get_span(resolution, grid_last_date, record_date)

        if time_histogram.count(c_val) > 0:
            time_histogram[c_val] = pair[float,float](max(time_histogram[c_val].first, span), min(time_histogram[c_val].second, span))
        else:
            time_histogram[c_val] = pair[float, float](span, span)

        if horizon != curr_horizon:
            if curr_horizon != -1:
                for i in range(s):
                    tmp_c_val = c_val_reverse_indices[i]
                    if calculated_dims_and_horizons.count(tmp_c_val) > 0 and calculated_dims_and_horizons[tmp_c_val].size() > 0:
                        last_horizon = dereference(calculated_dims_and_horizons[tmp_c_val].rbegin()).first
                        pre = _dict[i][horizon_indices[last_horizon]]
                        for j in range(local_horizon_list.size()):  # pylint: disable=not-an-iterable
                            hor = local_horizon_list[j]
                            if horizon > hor > last_horizon:
                                _dict[i][horizon_indices[hor]] = pre
                        _dict[i][horizon_indices[horizon]] = pre

                last_horizon = dereference(count_distinct_by_horizon.rbegin()).first
                for j in range(local_horizon_list.size()):  # pylint: disable=not-an-iterable
                    hor = local_horizon_list[j]
                    if horizon > hor > last_horizon:
                        count_distinct_by_horizon[horizon_indices[hor]] =  count_distinct_by_horizon[last_horizon]
                        mode_by_horizon[horizon_indices[hor]] = mode_by_horizon[last_horizon]

            if calculated_dims_and_horizons[c_val].size() > 0:
                _dict[c_val_index][hor_index][MIN_INDEX] = min( _dict[c_val_index][hor_index][MIN_INDEX], q_val)
                _dict[c_val_index][hor_index][MAX_INDEX] = max( _dict[c_val_index][hor_index][MAX_INDEX], q_val)
                _dict[c_val_index][hor_index][SUM_INDEX] += q_val
                _dict[c_val_index][hor_index][FREQUENCY_INDEX] += 1
                _dict[c_val_index][hor_index][DENSITY_INDEX] =  _dict[c_val_index][hor_index][SUM_INDEX] /  _dict[c_val_index][hor_index][FREQUENCY_INDEX]

            else:
                _dict[c_val_index][hor_index][DENSITY_INDEX] = q_val
                _dict[c_val_index][hor_index][MIN_INDEX] = q_val
                _dict[c_val_index][hor_index][MAX_INDEX] = q_val
                _dict[c_val_index][hor_index][SUM_INDEX] = q_val
                _dict[c_val_index][hor_index][FREQUENCY_INDEX] = 1.0
            curr_horizon = horizon

        else:
            if calculated_dims_and_horizons[c_val].size() > 0:
                _dict[c_val_index][hor_index][MIN_INDEX] = min( _dict[c_val_index][hor_index][MIN_INDEX], q_val)
                _dict[c_val_index][hor_index][MAX_INDEX] = max( _dict[c_val_index][hor_index][MAX_INDEX], q_val)
                _dict[c_val_index][hor_index][SUM_INDEX] += q_val
                _dict[c_val_index][hor_index][FREQUENCY_INDEX] += 1
                _dict[c_val_index][hor_index][DENSITY_INDEX] =  _dict[c_val_index][hor_index][SUM_INDEX] /  _dict[c_val_index][hor_index][FREQUENCY_INDEX]
            else:
                _dict[c_val_index][hor_index][DENSITY_INDEX] = q_val
                _dict[c_val_index][hor_index][MIN_INDEX] = q_val
                _dict[c_val_index][hor_index][MAX_INDEX] = q_val
                _dict[c_val_index][hor_index][SUM_INDEX] = q_val
                _dict[c_val_index][hor_index][FREQUENCY_INDEX] = 1.0
        if count_distinct_op_exists :
            count_distinct_by_horizon[hor_index] = d_val_dict.size()
        if mode_op_exists:
            mode_by_horizon[hor_index] = get_mode(d_val_dict)

        calculated_dims_and_horizons[c_val][horizon] = True

    if curr_horizon < max_horizon:
        for i in range(s):
            tmp_c_val = c_val_reverse_indices[i]

            if calculated_dims_and_horizons.count(tmp_c_val)>0 and calculated_dims_and_horizons[tmp_c_val].size() > 0:
                last_horizon = dereference(calculated_dims_and_horizons[tmp_c_val].rbegin()).first
                pre = _dict[i][horizon_indices[last_horizon]]
                for j in range(local_horizon_list.size()):  # pylint: disable=not-an-iterable
                    hor = local_horizon_list[j]
                    if max_horizon >= hor > curr_horizon:
                        _dict[i][horizon_indices[hor]] = pre

        last_horizon = dereference(count_distinct_by_horizon.rbegin()).first
        for j in range(local_horizon_list.size()):  # pylint: disable=not-an-iterable
            hor = local_horizon_list[j]
            if max_horizon >= hor > curr_horizon:
                count_distinct_by_horizon[horizon_indices[hor]] =  count_distinct_by_horizon[last_horizon]
                mode_by_horizon[horizon_indices[hor]] = mode_by_horizon[last_horizon]
    cdef:
        float tsf, tsl
        float[:,:] aggregates
        int aggregates_size = _dict.shape[0]
        float[:,:] aggregate_by_horizon
        float[:] aggregate
        pair[float, float] time_pair
        pair[short, pair[float, float]] time_key_pair


    for time_key_pair in time_histogram:
        time_pair = time_key_pair.second
        aggregates = _dict[c_val_indices[time_key_pair.first]]
        for hor_index_pair in horizon_indices:
            aggregates[hor_index_pair.second][TIME_SINCE_FIRST_INDEX] = time_pair.first
            aggregates[hor_index_pair.second][TIME_SINCE_LAST_INDEX] = time_pair.second
        _dict[c_val_indices[time_key_pair.first]] = aggregates


    for c_val_index in range(aggregates_size):
        c_val = c_val_reverse_indices[c_val_index]
        aggregate_by_horizon = _dict[c_val_index]

        for hor_index in range(aggregate_by_horizon.shape[0]):
            aggregate = aggregate_by_horizon[hor_index]
            if mode_op_exists :
                aggregate[MODE_INDEX] = mode_by_horizon[hor_index]

            if count_distinct_op_exists :
                aggregate[COUNT_DISTINCT_INDEX] = count_distinct_by_horizon[hor_index]
            aggregate_by_horizon[hor_index] = aggregate

    if is_scoring:
        if not ratio_op_exists:
            fill_row(result_frame, date_col_index, d_index, q_index,
                    row_index, _dict, local_horizon_list,
                    max_horizon_for_fill_row, min_horizon, is_scoring, c_val_reverse_indices, horizon_reverse_indices,
                    horizon_indices,
                    included_operators, included_operator_set_one, included_operator_set_two,
                    column_name_map, nearest_exponent, dim_group_id, is_no_dim_col
                    )
        else:
            fill_row_for_ratio_column(result_frame,  date_col_index, d_index, q_index, row_index, _dict,
            local_horizon_list, max_horizon, min_horizon, is_scoring,
            c_val_reverse_indices, horizon_reverse_indices, horizon_indices, column_name_map,
            nearest_exponent, dim_group_id, horizons[0],
            is_no_dim_col)
    else:
        fill_row(result_frame,  date_col_index, d_index, q_index, row_index, _dict, local_horizon_list,
                max_horizon, min_horizon, is_scoring, c_val_reverse_indices, horizon_reverse_indices, horizon_indices,
                included_operators, included_operator_set_one, included_operator_set_two,
                column_name_map, nearest_exponent, dim_group_id,is_no_dim_col
                )

cdef void fill_row_for_ratio_column(
    float[:,:] &frame,
    int date_col_index,
    int d_index,
    int q_index,
    int row_index,
    float[:,:,:] &aggregates, vector[int] &horizons,
    int max_horizon, int min_horizon, bool_t is_scoring,
    cmap[int, short] &c_val_reverse_indices,
    cmap[int, int] &horizon_reverse_indices,
    cmap[int, int] &horizon_indices,
    cmap[long long, int] &column_name_map,
    int nearest_exponent,
    int ratio_dimension_group,
    int ratio_horizon,
    bool_t is_no_dim_col
    ) nogil :
    cdef:
        int i, hor
        cmap[int, float] totals = cmap[int, float]()

    for i in range(horizons.size()):
        hor = horizons[i]
        totals.insert(pair[int, float](hor, 0.0))

    cdef:
        cmap[int, cmap[int, float]] ratio_hist = cmap[int, cmap[int, float]]()
        int c_val
        int aggregates_size = aggregates.shape[0]
        float sum_val, i_value
        float[:,:] aggregate_by_horizon
        float[:] aggregate
        float total_val

    for c_val_index in range(aggregates_size):
        c_val = c_val_reverse_indices[c_val_index]
        aggregate_by_horizon = aggregates[c_val_index]
        ratio_hist[c_val] = cmap[int, float]()

        for hor_index in range(aggregate_by_horizon.shape[0]):
            horizon = horizon_reverse_indices[hor_index]
            aggregate = aggregate_by_horizon[hor_index]
            sum_val = aggregate[SUM_INDEX]
            if not isnan(sum_val):
                totals[horizon] += sum_val
            ratio_hist[c_val][horizon] = sum_val
    if ratio_hist.count(ratio_dimension_group) > 0 and ratio_hist[ratio_dimension_group].count(ratio_horizon) > 0:
        i_value = ratio_hist[ratio_dimension_group][ratio_horizon]
        total_val = totals[ratio_horizon]
        if not isnan(i_value) and total_val > 0 :
            frame_set_value(frame, column_name_map, row_index, i_value/total_val,  nearest_exponent,
            ratio_dimension_group, RATIO_KEY, date_col_index, ratio_horizon)


cdef void fill_row(
    float[:,:] &frame,
    int date_col_index,
    int  d_index,
    int q_index,
    int row_index,
    float[:,:,:] &aggregates, vector[int] &horizons,
    int max_horizon, int min_horizon, bool_t is_scoring,
    cmap[int, short] &c_val_reverse_indices,
    cmap[int, int] &horizon_reverse_indices,
    cmap[int, int] &horizon_indices,
    vector[int] &included_operators,
    vector[int] &included_operator_set_one,
    vector[int] &included_operator_set_two,
    cmap[long long, int] &column_name_map,
    int nearest_exponent,
    int dim_group_id,
    bool_t is_no_dim_col
    ) nogil :

    cdef:
        int min_horizon_index = horizon_indices[min_horizon]
        int i,  hor
        cmap[int, float] totals = cmap[int, float]()

    for i in range(horizons.size()):
        hor = horizons[i]
        totals.insert(pair[int, float](hor, 0.0))

    cdef:
        cmap[int, cmap[int, float]] ratio_hist = cmap[int, cmap[int, float]]()
        int c_val, horizon, column_index, op_name, time_window
        float[:,:] aggregate_by_horizon
        float[:] aggregate
        float sum_val, val, total_val
        int aggregates_size = aggregates.shape[0]
        bool_t count_distinct_op_exists = contains(included_operators, COUNT_DISTINCT_KEY)
        bool_t mode_op_exists = contains(included_operators, MODE_KEY)
        bool_t check_for_dimension = is_scoring and not is_no_dim_col and not ( count_distinct_op_exists or mode_op_exists)
        int op_i, c_val_index, hor_index

    for c_val_index in range(aggregates_size):
        c_val = c_val_reverse_indices[c_val_index]
        if check_for_dimension and c_val != dim_group_id:
            continue
        aggregate_by_horizon = aggregates[c_val_index]
        ratio_hist[c_val] = cmap[int, float]()

        for hor_index in range(aggregate_by_horizon.shape[0]):
            horizon = horizon_reverse_indices[hor_index]
            aggregate = aggregate_by_horizon[hor_index]
            sum_val = aggregate[SUM_INDEX]
            if not isnan(sum_val):
                totals[horizon] += sum_val
            ratio_hist[c_val][horizon] = sum_val
            for op_i in range(included_operator_set_one.size()):
                op_name = included_operator_set_one[op_i]
                val = aggregate[AGGREGATE_INDEX_MAP[op_name]]
                frame_set_value(frame,  column_name_map, row_index, val, nearest_exponent, c_val, op_name,
                                date_col_index, horizon)
        for op_i in range(included_operator_set_two.size()):
            op_name = included_operator_set_two[op_i]

            val = aggregate_by_horizon[min_horizon_index][AGGREGATE_INDEX_MAP[op_name]]
            frame_set_value(frame, column_name_map, row_index, val, nearest_exponent, c_val, op_name,
                            date_col_index, horizon)

    if not is_scoring:
        if contains(included_operators,RATIO_KEY):

            for c_val_val_pair in ratio_hist:
                for hor_val_pair in c_val_val_pair.second:
                    total_val = totals[hor_val_pair.first]
                    if not isnan(hor_val_pair.second) and total_val > 0 :
                        frame_set_value(frame,  column_name_map, row_index, hor_val_pair.second/total_val,
                        nearest_exponent, c_val_val_pair.first, RATIO_KEY, date_col_index, hor_val_pair.first)



cdef void frame_set_value(float[:,:] &frame, cmap[long long, int] &column_name_map, int row_index, float val,
            int nearest_exponent, int group_id, int afe_operator, int date_col_index, int horizon) nogil :
    if group_id == UNKNOWN_DIMENSION_VALUE:
        return
    cdef:
        int hash_val  = get_hash_value(nearest_exponent, group_id, afe_operator, horizon)
        int column_index = column_name_map[hash_val]
    frame[row_index][column_index] = val

cdef int get_hash_value(int nearest_exponent, int group_id, int afe_operator, int horizon) nogil :
    cdef:
        int val = nearest_exponent ** 2 * group_id + nearest_exponent * afe_operator + horizon
    return val

cdef bool_t contains(vector[int] &vec, int val) nogil :
    cdef:
        int i, v
    for i in range(vec.size()):
        v = vec[i]
        if val == v:
            return True
    return False

cdef set[short] get_distinct_values(set[short] &s, cmap[short, short] &_map) nogil :
    cdef:
        pair[short, short] p
    for p in _map:
        s.insert(p.second)
    return s

cdef c_np.int64_t add_offset(c_np.int64_t to_sub, c_np.int64_t last_date, int step) nogil :
    return last_date - to_sub*step

cdef c_np.int64_t get_resolution_in_seconds(int resolution) nogil :
    cdef c_np.int64_t to_sub = 1000 #overflow olmaması için int64 tanımlanıp onun üzerinden işlem yapılmalı
    if resolution == 0:
        to_sub *=  (365*24*60*60)
    elif resolution == 1:
        to_sub *= (30*24*60*60)
    elif resolution == 2:
        to_sub *= (24*60*60)
    elif resolution == 3:
        to_sub *= (60*60)
    elif resolution == 4:
        to_sub *= (60)
    elif resolution == 5:
        to_sub *= 1
    else:
        raise NotImplementedError("Resolution not recognized: " + resolution)
    return to_sub

cdef float get_span(int resolution, c_np.int64_t last_date,  c_np.int64_t dt) nogil :
    cdef:
        c_np.int64_t val = last_date-dt
        c_np.int64_t to_divide = 1000
    if resolution == 0:
        to_divide *= (365*24*60*60)
    elif resolution == 1:
        to_divide *= (30*24*60*60)
    elif resolution == 2:
        to_divide *= (24*60*60)
    elif resolution == 3:
        to_divide *= (60*60)
    elif resolution == 4:
        to_divide *= (60)
    elif resolution == 5:
        to_divide *= 1
    else:
        raise NotImplementedError("Resolution not recognized: " + resolution)
    return val*1.0 / to_divide

cdef void partition(vector[pair[c_np.int64_t, int]] &dates_ascended, c_np.int64_t *offset_last_date,
                    c_np.int64_t *first_date, c_np.int64_t last_date, int offset, int resolution,
                    vector[int] &horizons, int max_horizon) nogil :
    cdef:
        c_np.int64_t resolution_in_seconds = get_resolution_in_seconds(resolution)
        int i, j
    offset_last_date[0] = add_offset(resolution_in_seconds , last_date, offset)
    dates_ascended.push_back(pair[c_np.int64_t, int](offset_last_date[0], horizons[0]))
    cdef int initial = horizons.size() - 1
    for j in range(initial):
        i = initial - j
        dates_ascended.push_back(pair[c_np.int64_t, int](add_offset(resolution_in_seconds, last_date, horizons[i - 1] + offset), horizons[i]))
    sort(dates_ascended.begin(), dates_ascended.end())
    first_date[0] = add_offset(resolution_in_seconds, last_date, max_horizon + offset)

cdef int get_horizon(c_np.int64_t offset_last_date, vector[pair[c_np.int64_t, int]] &dates_ascended,
    c_np.int64_t date, bool_t allow_equal_to_last_date=False) nogil :

    if allow_equal_to_last_date and date == offset_last_date:
        return dates_ascended[dates_ascended.size()-1].second
    for pair in dates_ascended:
        if date < pair.first:
            return pair.second
    raise ValueError("Date {0} is out of range".format(date))

cdef int get_min(vector[int] vec) nogil :
    cdef:
        int min_val = vec[0]
        int val
    for val in vec:
        if val < min_val:
            min_val = val
    return min_val

cdef int get_max(vector[int] vec) nogil :
    cdef:
        int val
        int max_val = vec[0]
    for val in vec:
        if val > max_val:
            max_val = val
    return max_val

cdef pair[int, int] find_entry_with_largest_value(cmap[int,int] map) nogil :
    cdef:
        pair[int, int] entryWithMaxValue
    entryWithMaxValue.first = 0
    entryWithMaxValue.second = 0

    for currentEntry in map:
            if (currentEntry.second> entryWithMaxValue.second) :
                entryWithMaxValue.first = currentEntry.first
                entryWithMaxValue.second = currentEntry.second

    return entryWithMaxValue


cdef int get_mode(cmap[int,int] map) nogil :
    cdef:
        pair[int, int] entry_with_max_value = find_entry_with_largest_value(map);
        int max_key = entry_with_max_value.first
    return max_key

