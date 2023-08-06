"""Includes helper functions for enum classes."""
from typing import Optional

from organon.fl.core.enums.column_measurement_type import ColumnMeasurementType
from organon.fl.core.enums.column_native_type import ColumnNativeType


def convert_measurement_to_native_type(measurement_type: ColumnMeasurementType) -> Optional[ColumnNativeType]:
    """Converts ColumnMeasurementType to ColumnNativeType"""
    if measurement_type == ColumnMeasurementType.NOMINAL:
        return ColumnNativeType.String
    if measurement_type == ColumnMeasurementType.NUMERIC:
        return ColumnNativeType.Numeric
    if measurement_type == ColumnMeasurementType.DATE:
        return ColumnNativeType.Date
    if measurement_type == ColumnMeasurementType.OTHER:
        return ColumnNativeType.Other
    return None
