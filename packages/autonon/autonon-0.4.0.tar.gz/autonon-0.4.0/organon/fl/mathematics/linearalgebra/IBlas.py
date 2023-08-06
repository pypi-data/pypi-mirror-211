# pylint: skip-file
"""Module Definition."""
import abc
import numpy as np


class IBlas(metaclass=abc.ABCMeta):
    """Class Definition."""
    @staticmethod
    @abc.abstractmethod
    def saxpy(n: int, a: np.single, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def daxpy(n: int, a: np.double, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def saxpby(n: int, a: np.single, x: np.ndarray, incx: int, b: np.single, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def daxpby(n: int, a: np.double, x: np.ndarray, incx: int, b, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def scopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def scopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def sdot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def ddot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def snrm2(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dnrm2(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def sscal(n: int, a: np.single, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dscal(n: int, a: np.double, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def sswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def isamax(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def idamax(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def isamin(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def idamin(n: int, x: np.ndarray, incx: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vssub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdsub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vssqr(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdsqr(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsabs(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdabs(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsdiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vddiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vssqrt(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdsqrt(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vspow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdpow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vspowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdpowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsexp(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdexp(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsexp2(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdexp2(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsexp10(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdexp10(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsln(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdln(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vslog2(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdlog2(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vslog10(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdlog10(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vserf(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vderf(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vserfc(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vderfc(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vscdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdcdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vserfinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vderfinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vserfcinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vderfcinv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vscdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdcdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vslgamma(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdlgamma(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vstgamma(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdtgamma(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsexpint1(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdexpint1(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsfloor(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdfloor(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsceil(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdceil(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vstrunc(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdtrunc(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsround(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdround(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsrint(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdrint(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsfrac(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdfrac(n: int, a: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vsminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def vdminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_s_mv(operation: int, m: int, k: int, alpha: np.single, val: np.ndarray, indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, descr, x: np.ndarray, beta: np.single,
                    y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_d_mv(operation: int, m: int, k: int, alpha: np.double, val: np.ndarray, indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, descr, x: np.ndarray, beta: np.double,
                    y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_s_mm(operation: int, m: int, n: int, k: int, alpha: np.single, descr, layout: int, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.single,
                    y: np.ndarray, ldy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_d_mm(operation: int, m: int, n: int, k: int, alpha: np.double, descr, layout: int, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.double,
                    y: np.ndarray, ldy: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_s_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_d_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_s_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        pass

    @staticmethod
    @abc.abstractmethod
    def sparse_d_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        pass

    @staticmethod
    @abc.abstractmethod
    def scsrmv(transa: int, m: int, k: int, alpha: np.single, matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.single, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcsrmv(transa: int, m: int, k: int, alpha: np.double, matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.double, y: np.ndarray):
        pass

    @staticmethod
    @abc.abstractmethod
    def scsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.single, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.single,
               c: np.ndarray, ldc: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.double, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.double,
               c: np.ndarray, ldc: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def scsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def scsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.single, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        pass

    @staticmethod
    @abc.abstractmethod
    def dcsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.double, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        pass
