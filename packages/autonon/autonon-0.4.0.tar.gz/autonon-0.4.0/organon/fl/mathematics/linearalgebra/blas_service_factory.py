"""Includes BlasServiceFactory class."""
from organon.fl.mathematics.linearalgebra.IBlas import IBlas
from organon.fl.mathematics.linearalgebra.MklFunctions import MklFunctions, MKL_FOUND
from organon.fl.mathematics.linearalgebra.blas_service_type import BlasServiceType
from organon.fl.mathematics.linearalgebra.scipy_blas_service import ScipyBlasService


class BlasServiceFactory:
    """Factory for IBlas implementations."""

    @staticmethod
    def get_blas_service(blas_type: BlasServiceType = None) -> IBlas:
        """Returns a service with IBlas implementations according to given blas_type."""
        if blas_type is None:
            if MKL_FOUND:
                return MklFunctions()
            return ScipyBlasService()
        if blas_type == BlasServiceType.MKL_BLAS:
            return MklFunctions()
        if blas_type == BlasServiceType.SCIPY_BLAS:
            return ScipyBlasService()
        raise NotImplementedError
