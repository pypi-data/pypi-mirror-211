# pylint: skip-file
"""Module Doc."""
import ctypes
import ctypes.util as _ctypes_util
from abc import ABC
import numpy as np
from numpy.ctypeslib import ndpointer, as_array
from organon.fl.mathematics.linearalgebra import enums
from organon.fl.mathematics.linearalgebra.IBlas import IBlas


so_file = _ctypes_util.find_library('mkl_rt')
MKL_FOUND = False
mkl = None
if so_file is not None:
    mkl = ctypes.cdll.LoadLibrary(so_file)
    MKL_FOUND = True


class MklFunctions(IBlas, ABC):
    """Class Doc"""
    @staticmethod
    def saxpy(n: int, a: np.single, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_saxpy_argtypes():
            return [ctypes.c_int,
                    ctypes.c_float,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_saxpy.argtypes = mkl_saxpy_argtypes()

        mkl.cblas_saxpy(ctypes.c_int(n),
                        ctypes.c_float(a),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def daxpy(n: int, a: np.double, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_daxpy_argtypes():
            return [ctypes.c_int,
                    ctypes.c_double,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_daxpy.argtypes = mkl_daxpy_argtypes()

        mkl.cblas_daxpy(ctypes.c_int(n),
                        ctypes.c_double(a),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def saxpby(n: int, a: np.single, x: np.ndarray, incx: int, b: np.single, y: np.ndarray, incy: int):
        MklFunctions.sscal(n, b, y, incy)
        MklFunctions.saxpy(n, a, x, incx, y, incy)

    @staticmethod
    def daxpby(n: int, a: np.double, x: np.ndarray, incx: int, b, y: np.ndarray, incy: int):
        MklFunctions.dscal(n, b, y, incy)
        MklFunctions.daxpy(n, a, x, incx, y, incy)

    @staticmethod
    def scopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_scopy_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_scopy.argtypes = mkl_scopy_argtypes()

        mkl.cblas_scopy(ctypes.c_int(n),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def dcopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_dcopy_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_dcopy.argtypes = mkl_dcopy_argtypes()

        mkl.cblas_dcopy(ctypes.c_int(n),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def scopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        y[:n * incy:incy] = x[np.logical_not(np.isnan(x))][:n * incx:incx]

    @staticmethod
    def dcopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        y[:n * incy:incy] = x[np.logical_not(np.isnan(x))][:n * incx:incx]

    @staticmethod
    def sdot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int) -> np.single:
        def mkl_sdot_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_sdot.argtypes = mkl_sdot_argtypes()
        mkl.cblas_sdot.restype = ctypes.c_float

        return mkl.cblas_sdot(ctypes.c_int(n),
                              x,
                              ctypes.c_int(incx),
                              y,
                              ctypes.c_int(incy))

    @staticmethod
    def ddot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int) -> np.double:
        def mkl_ddot_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_ddot.argtypes = mkl_ddot_argtypes()
        mkl.cblas_ddot.restype = ctypes.c_double

        return mkl.cblas_ddot(ctypes.c_int(n),
                              x,
                              ctypes.c_int(incx),
                              y,
                              ctypes.c_int(incy))

    @staticmethod
    def snrm2(n: int, x: np.ndarray, incx: int) -> np.single:
        def mkl_snrm2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_snrm2.argtypes = mkl_snrm2_argtypes()
        mkl.cblas_snrm2.restype = ctypes.c_float

        return mkl.cblas_snrm2(ctypes.c_int(n),
                               x,
                               ctypes.c_int(incx))

    @staticmethod
    def dnrm2(n: int, x: np.ndarray, incx: int) -> np.double:
        def mkl_dnrm2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_dnrm2.argtypes = mkl_dnrm2_argtypes()
        mkl.cblas_dnrm2.restype = ctypes.c_double

        return mkl.cblas_dnrm2(ctypes.c_int(n),
                               x,
                               ctypes.c_int(incx))

    @staticmethod
    def sscal(n: int, a: np.single, x: np.ndarray, incx: int):
        def mkl_sscal_argtypes():
            return [ctypes.c_int,
                    ctypes.c_float,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_sscal.argtypes = mkl_sscal_argtypes()

        mkl.cblas_sscal(ctypes.c_int(n),
                        ctypes.c_float(a),
                        x,
                        ctypes.c_int(incx))

    @staticmethod
    def dscal(n: int, a: np.double, x: np.ndarray, incx: int):
        def mkl_dscal_argtypes():
            return [ctypes.c_int,
                    ctypes.c_double,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_dscal.argtypes = mkl_dscal_argtypes()

        mkl.cblas_dscal(ctypes.c_int(n),
                        ctypes.c_double(a),
                        x,
                        ctypes.c_int(incx))

    @staticmethod
    def sswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_sswap_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_sswap.argtypes = mkl_sswap_argtypes()

        mkl.cblas_sswap(ctypes.c_int(n),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def dswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        def mkl_dswap_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_dswap.argtypes = mkl_dswap_argtypes()

        mkl.cblas_dswap(ctypes.c_int(n),
                        x,
                        ctypes.c_int(incx),
                        y,
                        ctypes.c_int(incy))

    @staticmethod
    def isamax(n: int, x: np.ndarray, incx: int) -> int:
        def mkl_isamax_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_isamax.argtypes = mkl_isamax_argtypes()
        mkl.cblas_isamax.restype = ctypes.c_int

        return mkl.cblas_isamax(ctypes.c_int(n),
                                x,
                                ctypes.c_int(incx))

    @staticmethod
    def idamax(n: int, x: np.ndarray, incx: int) -> int:
        def mkl_idamax_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_idamax.argtypes = mkl_idamax_argtypes()
        mkl.cblas_idamax.restype = ctypes.c_int

        return mkl.cblas_idamax(ctypes.c_int(n),
                                x,
                                ctypes.c_int(incx))

    @staticmethod
    def isamin(n: int, x: np.ndarray, incx: int) -> int:
        def mkl_isamin_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_isamin.argtypes = mkl_isamin_argtypes()
        mkl.cblas_isamin.restype = ctypes.c_int

        return mkl.cblas_isamin(ctypes.c_int(n),
                                x,
                                ctypes.c_int(incx))

    @staticmethod
    def idamin(n: int, x: np.ndarray, incx: int) -> int:
        def mkl_idamin_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_int]

        mkl.cblas_idamin.argtypes = mkl_idamin_argtypes()
        mkl.cblas_idamin.restype = ctypes.c_int

        return mkl.cblas_idamin(ctypes.c_int(n),
                                x,
                                ctypes.c_int(incx))

    @staticmethod
    def vsadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsadd_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsAdd.argtypes = mkl_vsadd_argtypes()

        mkl.vsAdd(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vdadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdadd_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdAdd.argtypes = mkl_vdadd_argtypes()

        mkl.vdAdd(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vssub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vssub_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsSub.argtypes = mkl_vssub_argtypes()

        mkl.vsSub(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vdsub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdsub_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdSub.argtypes = mkl_vdsub_argtypes()

        mkl.vdSub(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vssqr(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vssqr_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsSqr.argtypes = mkl_vssqr_argtypes()

        mkl.vsSqr(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vdsqr(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdsqr_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdSqr.argtypes = mkl_vdsqr_argtypes()

        mkl.vdSqr(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vsmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsmul_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsMul.argtypes = mkl_vsmul_argtypes()

        mkl.vsMul(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vdmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdmul_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdMul.argtypes = mkl_vdmul_argtypes()

        mkl.vdMul(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vsabs(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsabs_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsAbs.argtypes = mkl_vsabs_argtypes()

        mkl.vsAbs(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vdabs(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdabs_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdAbs.argtypes = mkl_vdabs_argtypes()

        mkl.vdAbs(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vsfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsfmod_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsFmod.argtypes = mkl_vsfmod_argtypes()

        mkl.vsFmod(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vdfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdfmod_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdFmod.argtypes = mkl_vdfmod_argtypes()

        mkl.vdFmod(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vsremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsremainder_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsRemainder.argtypes = mkl_vsremainder_argtypes()

        mkl.vsRemainder(ctypes.c_int(n),
                        a,
                        b,
                        y)

    @staticmethod
    def vdremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdremainder_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdRemainder.argtypes = mkl_vdremainder_argtypes()

        mkl.vdRemainder(ctypes.c_int(n),
                        a,
                        b,
                        y)

    @staticmethod
    def vsinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsInv.argtypes = mkl_vsinv_argtypes()

        mkl.vsInv(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vdinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdInv.argtypes = mkl_vdinv_argtypes()

        mkl.vdInv(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vsdiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsdiv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsDiv.argtypes = mkl_vsdiv_argtypes()

        mkl.vsDiv(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vddiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vddiv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdDiv.argtypes = mkl_vddiv_argtypes()

        mkl.vdDiv(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vssqrt(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vssqrt_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsSqrt.argtypes = mkl_vssqrt_argtypes()

        mkl.vsSqrt(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdsqrt(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdsqrt_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdSqrt.argtypes = mkl_vdsqrt_argtypes()

        mkl.vdSqrt(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vspow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vspow_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsPow.argtypes = mkl_vspow_argtypes()

        mkl.vsPow(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vdpow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdpow_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdPow.argtypes = mkl_vdpow_argtypes()

        mkl.vdPow(ctypes.c_int(n),
                  a,
                  b,
                  y)

    @staticmethod
    def vspowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        def mkl_vspowx_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_float,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsPowx.argtypes = mkl_vspowx_argtypes()

        mkl.vsPowx(ctypes.c_int(n),
                   a,
                   ctypes.c_float(b),
                   y)

    @staticmethod
    def vdpowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        def mkl_vdpowx_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.c_double,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdPowx.argtypes = mkl_vdpowx_argtypes()

        mkl.vdPowx(ctypes.c_int(n),
                   a,
                   ctypes.c_double(b),
                   y)

    @staticmethod
    def vsexp(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsexp_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsExp.argtypes = mkl_vsexp_argtypes()

        mkl.vsExp(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vdexp(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdexp_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdExp.argtypes = mkl_vdexp_argtypes()

        mkl.vdExp(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vsexp2(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsexp2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsExp2.argtypes = mkl_vsexp2_argtypes()

        mkl.vsExp2(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdexp2(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdexp2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdExp2.argtypes = mkl_vdexp2_argtypes()

        mkl.vdExp2(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vsexp10(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsexp10_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsExp10.argtypes = mkl_vsexp10_argtypes()

        mkl.vsExp10(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vdexp10(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdexp10_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdExp10.argtypes = mkl_vdexp10_argtypes()

        mkl.vdExp10(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vsln(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsln_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsLn.argtypes = mkl_vsln_argtypes()

        mkl.vsLn(ctypes.c_int(n),
                 a,
                 y)

    @staticmethod
    def vdln(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdln_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdLn.argtypes = mkl_vdln_argtypes()

        mkl.vdLn(ctypes.c_int(n),
                 a,
                 y)

    @staticmethod
    def vslog2(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vslog2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsLog2.argtypes = mkl_vslog2_argtypes()

        mkl.vsLog2(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdlog2(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdlog2_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdLog2.argtypes = mkl_vdlog2_argtypes()

        mkl.vdLog2(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vslog10(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vslog10_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsLog10.argtypes = mkl_vslog10_argtypes()

        mkl.vsLog10(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vdlog10(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdlog10_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdLog10.argtypes = mkl_vdlog10_argtypes()

        mkl.vdLog10(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vserf(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vserf_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsErf.argtypes = mkl_vserf_argtypes()

        mkl.vsErf(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vderf(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vderf_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdErf.argtypes = mkl_vderf_argtypes()

        mkl.vdErf(ctypes.c_int(n),
                  a,
                  y)

    @staticmethod
    def vserfc(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vserfc_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsErfc.argtypes = mkl_vserfc_argtypes()

        mkl.vsErfc(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vderfc(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vderfc_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdErfc.argtypes = mkl_vderfc_argtypes()

        mkl.vdErfc(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vscdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vscdfnorm_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsCdfNorm.argtypes = mkl_vscdfnorm_argtypes()

        mkl.vsCdfNorm(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vdcdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdcdfnorm_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdCdfNorm.argtypes = mkl_vdcdfnorm_argtypes()

        mkl.vdCdfNorm(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vserfinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vserfinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsErfInv.argtypes = mkl_vserfinv_argtypes()

        mkl.vsErfInv(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vderfinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vderfinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdErfInv.argtypes = mkl_vderfinv_argtypes()

        mkl.vdErfInv(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vserfcinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vserfcinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsErfcInv.argtypes = mkl_vserfcinv_argtypes()

        mkl.vsErfcInv(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vderfcinv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vderfcinv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdErfcInv.argtypes = mkl_vderfcinv_argtypes()

        mkl.vdErfcInv(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vscdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vscdfnorminv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsCdfNormInv.argtypes = mkl_vscdfnorminv_argtypes()

        mkl.vsCdfNormInv(ctypes.c_int(n),
                         a,
                         y)

    @staticmethod
    def vdcdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdcdfnorminv_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdCdfNormInv.argtypes = mkl_vdcdfnorminv_argtypes()

        mkl.vdCdfNormInv(ctypes.c_int(n),
                         a,
                         y)

    @staticmethod
    def vslgamma(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vslgamma_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsLGamma.argtypes = mkl_vslgamma_argtypes()

        mkl.vsLGamma(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vdlgamma(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdlgamma_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdLGamma.argtypes = mkl_vdlgamma_argtypes()

        mkl.vdLGamma(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vstgamma(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vstgamma_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsTGamma.argtypes = mkl_vstgamma_argtypes()

        mkl.vsTGamma(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vdtgamma(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdtgamma_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdTGamma.argtypes = mkl_vdtgamma_argtypes()

        mkl.vdTGamma(ctypes.c_int(n),
                     a,
                     y)

    @staticmethod
    def vsexpint1(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsexpint1_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsExpInt1.argtypes = mkl_vsexpint1_argtypes()

        mkl.vsExpInt1(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vdexpint1(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdexpint1_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdExpInt1.argtypes = mkl_vdexpint1_argtypes()

        mkl.vdExpInt1(ctypes.c_int(n),
                      a,
                      y)

    @staticmethod
    def vsfloor(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsfloor_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsFloor.argtypes = mkl_vsfloor_argtypes()

        mkl.vsFloor(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vdfloor(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdfloor_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdFloor.argtypes = mkl_vdfloor_argtypes()

        mkl.vdFloor(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vsceil(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsceil_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsCeil.argtypes = mkl_vsceil_argtypes()

        mkl.vsCeil(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdceil(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdceil_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdCeil.argtypes = mkl_vdceil_argtypes()

        mkl.vdCeil(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vstrunc(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vstrunc_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsTrunc.argtypes = mkl_vstrunc_argtypes()

        mkl.vsTrunc(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vdtrunc(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdtrunc_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdTrunc.argtypes = mkl_vdtrunc_argtypes()

        mkl.vdTrunc(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vsround(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsround_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsRound.argtypes = mkl_vsround_argtypes()

        mkl.vsRound(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vdround(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdround_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdRound.argtypes = mkl_vdround_argtypes()

        mkl.vdRound(ctypes.c_int(n),
                    a,
                    y)

    @staticmethod
    def vsnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsnearbyint_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsNearbyInt.argtypes = mkl_vsnearbyint_argtypes()

        mkl.vsNearbyInt(ctypes.c_int(n),
                        a,
                        y)

    @staticmethod
    def vdnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdnearbyint_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdNearbyInt.argtypes = mkl_vdnearbyint_argtypes()

        mkl.vdNearbyInt(ctypes.c_int(n),
                        a,
                        y)

    @staticmethod
    def vsrint(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsrint_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsRint.argtypes = mkl_vsrint_argtypes()

        mkl.vsRint(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdrint(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdrint_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdRint.argtypes = mkl_vdrint_argtypes()

        mkl.vdRint(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vsmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        def mkl_vsmodf_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsModf.argtypes = mkl_vsmodf_argtypes()

        mkl.vsModf(ctypes.c_int(n),
                   a,
                   y,
                   z)

    @staticmethod
    def vdmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        def mkl_vdmodf_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdModf.argtypes = mkl_vdmodf_argtypes()

        mkl.vdModf(ctypes.c_int(n),
                   a,
                   y,
                   z)

    @staticmethod
    def vsfrac(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vsfrac_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsFrac.argtypes = mkl_vsfrac_argtypes()

        mkl.vsFrac(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vdfrac(n: int, a: np.ndarray, y: np.ndarray):
        def mkl_vdfrac_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdFrac.argtypes = mkl_vdfrac_argtypes()

        mkl.vdFrac(ctypes.c_int(n),
                   a,
                   y)

    @staticmethod
    def vsfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsfmax_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsFmax.argtypes = mkl_vsfmax_argtypes()

        mkl.vsFmax(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vdfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdfmax_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdFmax.argtypes = mkl_vdfmax_argtypes()

        mkl.vdFmax(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vsfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsfmin_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsFmin.argtypes = mkl_vsfmin_argtypes()

        mkl.vsFmin(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vdfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdfmin_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdFmin.argtypes = mkl_vdfmin_argtypes()

        mkl.vdFmin(ctypes.c_int(n),
                   a,
                   b,
                   y)

    @staticmethod
    def vsmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsmaxmag_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsMaxMag.argtypes = mkl_vsmaxmag_argtypes()

        mkl.vsMaxMag(ctypes.c_int(n),
                     a,
                     b,
                     y)

    @staticmethod
    def vdmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdmaxmag_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdMaxMag.argtypes = mkl_vdmaxmag_argtypes()

        mkl.vdMaxMag(ctypes.c_int(n),
                     a,
                     b,
                     y)

    @staticmethod
    def vsminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vsminmag_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_float, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vsMinMag.argtypes = mkl_vsminmag_argtypes()

        mkl.vsMinMag(ctypes.c_int(n),
                     a,
                     b,
                     y)

    @staticmethod
    def vdminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        def mkl_vdminmag_argtypes():
            return [ctypes.c_int,
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_double, ndim=1, flags='C_CONTIGUOUS')]

        mkl.vdMinMag.argtypes = mkl_vdminmag_argtypes()

        mkl.vdMinMag(ctypes.c_int(n),
                     a,
                     b,
                     y)

    # SPARSE FUNCTIONS

    sparse_matrix_t = ctypes.POINTER(enums.SparseMatrix)

    @staticmethod
    def _create_handle(indexing: enums.SparseIndexBaseT, rows: int, cols: int, rows_start: np.ndarray,
                       rows_end: np.ndarray,
                       col_indx: np.ndarray, values: np.ndarray, dtype: np.dtype, sparse_format='csr'):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        if sparse_format == 'csr':
            create_func = mkl.mkl_sparse_s_create_csr if dtype == np.single else mkl.mkl_sparse_d_create_csr
        else:
            create_func = mkl.mkl_sparse_s_create_csc if dtype == np.single else mkl.mkl_sparse_d_create_csc

        create_func.argtypes = [ctypes.POINTER(MklFunctions.sparse_matrix_t),
                                ctypes.c_int,
                                ctypes.c_long,
                                ctypes.c_long,
                                ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                                ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                                ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                                ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS')]
        create_func.restype = ctypes.c_int
        handle = MklFunctions.sparse_matrix_t()
        create_func(ctypes.byref(handle),
                    ctypes.c_int(indexing.value),
                    ctypes.c_long(rows),
                    ctypes.c_long(cols),
                    rows_start,
                    rows_end,
                    col_indx,
                    values)
        return handle

    @staticmethod
    def _sp_optimize_mm(sp_handle: sparse_matrix_t, operation: enums.SparseOperationT,
                        descr: enums.MatrixDescr, layout: enums.SparseLayoutT,
                        dense_size: int,
                        exp_calls: int):
        mkl.mkl_sparse_set_mm_hint.argtypes = [MklFunctions.sparse_matrix_t,
                                               ctypes.c_int,
                                               enums.MatrixDescr,
                                               ctypes.c_int,
                                               ctypes.c_int,
                                               ctypes.c_int]
        mkl.mkl_sparse_set_mm_hint(sp_handle,
                                   ctypes.c_int(operation.value),
                                   descr,
                                   ctypes.c_int(layout.value),
                                   ctypes.c_int(dense_size),
                                   ctypes.c_int(exp_calls))
        mkl.mkl_sparse_optimize.argtypes = [MklFunctions.sparse_matrix_t]
        mkl.mkl_sparse_optimize(sp_handle)

    @staticmethod
    def _export_sparse(sp_handle: sparse_matrix_t, c, jc, ic, dtype: np.dtype, sparse_format='csr'):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        data = ctypes.POINTER(c_dtype)()
        indptrb = ctypes.POINTER(ctypes.c_long)()
        indptren = ctypes.POINTER(ctypes.c_long)()
        indices = ctypes.POINTER(ctypes.c_long)()

        ordering = ctypes.c_int()
        nrows = ctypes.c_long()
        ncols = ctypes.c_long()

        if sparse_format == 'csr':
            out_func = mkl.mkl_sparse_s_export_csr if dtype == np.single else mkl.mkl_sparse_d_export_csr
        else:
            out_func = mkl.mkl_sparse_s_export_csc if dtype == np.single else mkl.mkl_sparse_d_export_csc

        out_func(sp_handle,
                 ctypes.byref(ordering),
                 ctypes.byref(nrows),
                 ctypes.byref(ncols),
                 ctypes.byref(indptrb),
                 ctypes.byref(indptren),
                 ctypes.byref(indices),
                 ctypes.byref(data))

        # ncols = ncols.value
        nrows = nrows.value

        indptrb = as_array(indptrb, shape=(nrows,))
        indptren = as_array(indptren, shape=(nrows,))

        ic[:nrows + 1] = np.insert(indptren, 0, indptrb[0])
        nnz = indptren[-1] - indptrb[0]

        c[:nnz] = np.array(as_array(data, shape=(nnz,)), copy=True)
        jc[:nnz] = np.array(as_array(indices, shape=(nnz,)), copy=True)

        # return sparse.csr_matrix((data, indices, indptren), shape=(nrows, ncols))

    @staticmethod
    def sparse_s_mv(operation: enums.SparseOperationT, m: int, k: int, alpha: np.single,
                    descr: enums.MatrixDescr, val: np.ndarray,
                    indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.single,
                    y: np.ndarray, sparse_format='csr'):
        MklFunctions._sparse_mv(operation, m, k, alpha, descr, val, indx, pntrb, pntre, x, beta, y, np.single,
                                sparse_format)

    @staticmethod
    def sparse_d_mv(operation: enums.SparseOperationT, m: int, k: int, alpha: np.double,
                    descr: enums.MatrixDescr, val: np.ndarray,
                    indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.double,
                    y: np.ndarray, sparse_format='csr'):
        MklFunctions._sparse_mv(operation, m, k, alpha, descr, val, indx, pntrb, pntre, x, beta, y, np.double,
                                sparse_format)

    @staticmethod
    # Sparse matrix dense vector yeni
    def _sparse_mv(operation, m, k, alpha, descr, val, indx, pntrb, pntre, x, beta, y, dtype, sparse_format='csr'):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        ref = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                          m,
                                          k,
                                          pntrb,
                                          pntre,
                                          indx,
                                          val,
                                          dtype,
                                          sparse_format)

        mkl.mkl_sparse_optimize.argtypes = [MklFunctions.sparse_matrix_t]
        mkl.mkl_sparse_optimize(ref)

        sparse_mv = mkl.mkl_sparse_s_mv if dtype == np.single else mkl.mkl_sparse_d_mv

        sparse_mv.argtypes = [ctypes.c_int,
                              c_dtype,
                              MklFunctions.sparse_matrix_t,
                              enums.MatrixDescr,
                              ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                              c_dtype,
                              ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS')]

        sparse_mv(ctypes.c_int(operation.value),
                  c_dtype(alpha),
                  ref,
                  descr,
                  x,
                  c_dtype(beta),
                  y)

        mkl.mkl_sparse_destroy(ref)

    @staticmethod
    def sparse_s_mm(operation: enums.SparseOperationT, m: int, n: int, k: int, alpha: np.single,
                    descr: enums.MatrixDescr, layout: enums.SparseLayoutT, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.single,
                    y: np.ndarray, ldy: int):
        _sparse_mm(operation, m, n, k, alpha, descr, val, indx, pntrb, pntre, layout, x, ldx, beta, y, ldy,
                   np.single)

    @staticmethod
    def sparse_d_mm(operation: enums.SparseOperationT, m: int, n: int, k: int, alpha: np.double,
                    descr: enums.MatrixDescr, layout: enums.SparseLayoutT, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.double,
                    y: np.ndarray, ldy: int):
        _sparse_mm(operation, m, n, k, alpha, descr, val, indx, pntrb, pntre, layout, x, ldx, beta, y, ldy,
                   np.double)

    @staticmethod
    def sparse_s_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        return MklFunctions._sparse_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax,
                                         info, np.single)

    @staticmethod
    def sparse_d_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        return MklFunctions._sparse_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax,
                                         info, np.double)

    @staticmethod
    # Sparse matrix Sparse matrix yeni
    # trans, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info, dtype
    def _sparse_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info, dtype):
        refa = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                           m,
                                           n,
                                           ia[0:-1],
                                           ia[1:],
                                           ja,
                                           a,
                                           dtype)

        refb = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                           n,
                                           k,
                                           ib[0:-1],
                                           ib[1:],
                                           jb,
                                           b,
                                           dtype)

        ref_handle = MklFunctions.sparse_matrix_t()

        mkl.mkl_sparse_spmm(ctypes.c_int(operation.value),
                            refa,
                            refb,
                            ctypes.byref(ref_handle))

        MklFunctions._export_sparse(ref_handle, c, jc, ic, dtype)

    @staticmethod
    def sparse_s_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        return MklFunctions._sparse_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax,
                                        info, np.single)

    @staticmethod
    def sparse_d_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        return MklFunctions._sparse_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax,
                                        info, np.double)

    @staticmethod
    # Sparse matrix plus Sparse matrix yeni
    # trans, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info, dtype
    def _sparse_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info, dtype):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        refa = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                           m,
                                           n,
                                           ia[0:-1],
                                           ia[1:],
                                           ja,
                                           a,
                                           dtype)

        refb = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                           m,
                                           n,
                                           ib[0:-1],
                                           ib[1:],
                                           jb,
                                           b,
                                           dtype)

        ref_handle = MklFunctions.sparse_matrix_t()

        handle = mkl.mkl_sparse_s_add if dtype == np.single else mkl.mkl_sparse_d_add

        handle(ctypes.c_int(operation.value),
               refa,
               c_dtype(beta),
               refb,
               ctypes.byref(ref_handle))

        return MklFunctions._export_sparse(ref_handle, c, jc, ic, dtype)

    @staticmethod
    def scsrmv(transa: ctypes.c_char_p, m: int, k: int, alpha: np.single,
               matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.single, y: np.ndarray):
        MklFunctions._csrmv(transa, m, k, alpha, matdescra, val, indx, pntrb, pntre, x, beta, y, np.single)

    @staticmethod
    def dcsrmv(transa: ctypes.c_char_p, m: int, k: int, alpha: np.double,
               matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.double, y: np.ndarray):
        MklFunctions._csrmv(transa, m, k, alpha, matdescra, val, indx, pntrb, pntre, x, beta, y, np.double)

    @staticmethod
    # Sparse matrix dense vector eski
    def _csrmv(transa, m, k, alpha, matdescra, val, indx, pntrb, pntre, x, beta, y, dtype):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        def mkl_csrmv_argtypes():
            return [ctypes.c_char_p,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(c_dtype),
                    ndpointer(dtype=ctypes.c_char, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(c_dtype),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS')]

        csrmv = mkl.mkl_scsrmv if dtype == np.single else mkl.mkl_dcsrmv

        csrmv.argtypes = mkl_csrmv_argtypes()

        csrmv(transa,
              ctypes.byref(ctypes.c_int(m)),
              ctypes.byref(ctypes.c_int(k)),
              ctypes.byref(c_dtype(alpha)),
              matdescra,
              val,
              indx,
              pntrb,
              pntre,
              x,
              ctypes.byref(c_dtype(beta)),
              y)

    @staticmethod
    def scsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.single, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.single,
               c: np.ndarray, ldc: int):
        MklFunctions._csrmm(transa, m, n, k, alpha, matdescra, val, indx, pntrb, pntre, b, ldb, beta, c, ldc,
                            np.single)

    @staticmethod
    def dcsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.double, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.double,
               c: np.ndarray, ldc: int):
        MklFunctions._csrmm(transa, m, n, k, alpha, matdescra, val, indx, pntrb, pntre, b, ldb, beta, c, ldc,
                            np.double)

    @staticmethod
    # Sparse matrix dense matrix eski
    def _csrmm(transa, m, n, k, alpha, matdescra, val, indx, pntrb, pntre, b, ldb, beta, c, ldc, dtype):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        def mkl_csrmm_argtypes():
            return [ctypes.c_char_p,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(c_dtype),
                    ndpointer(dtype=ctypes.c_char, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=2, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(c_dtype),
                    ndpointer(dtype=c_dtype, ndim=2, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(ctypes.c_int)]

        csrmm = mkl.mkl_scsrmm if dtype == np.single else mkl.mkl_dcsrmm

        csrmm.argtypes = mkl_csrmm_argtypes()

        csrmm(transa,
              ctypes.byref(ctypes.c_int(m)),
              ctypes.byref(ctypes.c_int(n)),
              ctypes.byref(ctypes.c_int(k)),
              ctypes.byref(c_dtype(alpha)),
              matdescra,
              val,
              indx,
              pntrb,
              pntre,
              b,
              ctypes.byref(ctypes.c_int(ldb)),
              ctypes.byref(c_dtype(beta)),
              c,
              ctypes.byref(ctypes.c_int(ldc)))

    @staticmethod
    def scsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        MklFunctions._csrmult(trans, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info, np.single)

    @staticmethod
    def dcsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        MklFunctions._csrmult(trans, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info, np.double)

    @staticmethod
    # Sparse matrix sparse matrix eski
    def _csrmult(trans, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info, dtype):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        def mkl_dcsrmult_argtypes():
            return [ctypes.c_char_p,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(ctypes.c_long),
                    ctypes.POINTER(ctypes.c_int)]

        csrmult = mkl.mkl_scsrmultcsr if dtype == np.single else mkl.mkl_dcsrmultcsr

        csrmult.argtypes = mkl_dcsrmult_argtypes()

        ja += 1
        ia += 1

        jb += 1
        ib += 1

        csrmult(trans,
                ctypes.byref(ctypes.c_int(request)),
                ctypes.byref(ctypes.c_int(sort)),
                ctypes.byref(ctypes.c_int(m)),
                ctypes.byref(ctypes.c_int(n)),
                ctypes.byref(ctypes.c_int(k)),
                a, ja, ia, b, jb, ib,
                c, jc, ic,
                ctypes.byref(ctypes.c_long(nzmax)),
                ctypes.byref(ctypes.c_int(info)))

        ja -= 1
        ia -= 1

        jb -= 1
        ib -= 1

        jc -= 1
        ic -= 1

    @staticmethod
    def scsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.single, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        MklFunctions._csradd(trans, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info, np.single)

    @staticmethod
    def dcsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.double, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        MklFunctions._csradd(trans, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info, np.double)

    @staticmethod
    def _csradd(trans, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info, dtype):
        c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

        def mkl_csradd_argtypes():
            return [ctypes.c_char_p,
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.POINTER(ctypes.c_int),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(c_dtype),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=c_dtype, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ndpointer(dtype=ctypes.c_long, ndim=1, flags='C_CONTIGUOUS'),
                    ctypes.POINTER(ctypes.c_long),
                    ctypes.POINTER(ctypes.c_int)]

        csradd = mkl.mkl_scsradd if dtype == np.single else mkl.mkl_dcsradd

        csradd.argtypes = mkl_csradd_argtypes()

        ja += 1
        ia += 1

        jb += 1
        ib += 1

        csradd(trans,
               ctypes.byref(ctypes.c_int(request)),
               ctypes.byref(ctypes.c_int(sort)),
               ctypes.byref(ctypes.c_int(m)),
               ctypes.byref(ctypes.c_int(n)),
               a, ja, ia,
               ctypes.byref(c_dtype(beta)),
               b, jb, ib,
               c, jc, ic,
               ctypes.byref(ctypes.c_long(nzmax)),
               ctypes.byref(ctypes.c_int(info)))

        ja -= 1
        ia -= 1

        jb -= 1
        ib -= 1

        jc -= 1
        ic -= 1


# Sparse matrix dense matrix yeni
# transa, m, n, k, alpha, matdescra, val, indx, pntrb, pntre, b, ldb, beta, c, ldc, dtype
def _sparse_mm(operation, m, n, k, alpha, descr, val, indx, pntrb, pntre, layout, x, ldx, beta, y, ldy, dtype):
    c_dtype = ctypes.c_float if dtype == np.single else ctypes.c_double

    ref = MklFunctions._create_handle(enums.SparseIndexBaseT.SPARSE_INDEX_BASE_ZERO,
                                      m,
                                      n,
                                      pntrb,
                                      pntre,
                                      indx,
                                      val,
                                      dtype)

    MklFunctions._sp_optimize_mm(ref, operation, descr, layout, n, 1)

    sparse_mm = mkl.mkl_sparse_s_mm if dtype == np.single else mkl.mkl_sparse_d_mm

    sparse_mm.argtypes = [ctypes.c_int,
                          c_dtype,
                          MklFunctions.sparse_matrix_t,
                          enums.MatrixDescr,
                          ctypes.c_int,
                          ndpointer(dtype=c_dtype, ndim=2, flags='C_CONTIGUOUS'),
                          ctypes.c_int,
                          ctypes.c_int,
                          c_dtype,
                          ndpointer(dtype=c_dtype, ndim=2, flags='C_CONTIGUOUS'),
                          ctypes.c_int]

    sparse_mm(ctypes.c_int(operation.value),
              c_dtype(alpha),
              ref,
              descr,
              ctypes.c_int(layout.value),
              x,
              ctypes.c_int(n),
              ctypes.c_int(ldx),
              c_dtype(beta),
              y,
              ctypes.c_int(ldy))

    mkl.mkl_sparse_destroy(ref)
