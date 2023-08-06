"""Includes ScipyBlasService class."""
import numpy as np
from scipy.linalg import blas

from organon.fl.mathematics.linearalgebra.IBlas import IBlas


class ScipyBlasService(IBlas):
    """IBlas implementation using scipy."""
    # pylint: disable=no-member,too-many-arguments,too-many-public-methods

    @staticmethod
    def saxpy(n: int, a: np.single, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.saxpy(x, y, n, a, incx=incx, incy=incy)

    @staticmethod
    def daxpy(n: int, a: np.double, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.daxpy(x, y, n, a, incx=incx, incy=incy)

    @staticmethod
    def saxpby(n: int, a: np.single, x: np.ndarray, incx: int, b: np.single, y: np.ndarray, incy: int):
        ScipyBlasService.sscal(n, b, y, incy)
        ScipyBlasService.saxpy(n, a, x, incx, y, incy)

    @staticmethod
    def daxpby(n: int, a: np.double, x: np.ndarray, incx: int, b, y: np.ndarray, incy: int):
        ScipyBlasService.dscal(n, b, y, incy)
        ScipyBlasService.daxpy(n, a, x, incx, y, incy)

    @staticmethod
    def scopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.scopy(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def dcopy(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.dcopy(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def scopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        y[:n * incy:incy] = x[np.logical_not(np.isnan(x))][:n * incx:incx]

    @staticmethod
    def dcopynan(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        y[:n * incy:incy] = x[np.logical_not(np.isnan(x))][:n * incx:incx]

    @staticmethod
    def sdot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        return blas.sdot(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def ddot(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        return blas.ddot(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def snrm2(n: int, x: np.ndarray, incx: int):
        return blas.snrm2(x, n=n, incx=incx)

    @staticmethod
    def dnrm2(n: int, x: np.ndarray, incx: int):
        return blas.dnrm2(x, n=n, incx=incx)

    @staticmethod
    def sscal(n: int, a: np.single, x: np.ndarray, incx: int):
        blas.sscal(a, x, n=n, incx=incx)

    @staticmethod
    def dscal(n: int, a: np.double, x: np.ndarray, incx: int):
        blas.dscal(a, x, n=n, incx=incx)

    @staticmethod
    def sswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.sswap(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def dswap(n: int, x: np.ndarray, incx: int, y: np.ndarray, incy: int):
        blas.dswap(x, y, n=n, incx=incx, incy=incy)

    @staticmethod
    def isamax(n: int, x: np.ndarray, incx: int):
        return blas.isamax(x, n=n, incx=incx)

    @staticmethod
    def idamax(n: int, x: np.ndarray, incx: int):
        return blas.idamax(x, n=n, incx=incx)

    @staticmethod
    def isamin(n: int, x: np.ndarray, incx: int):
        raise NotImplementedError

    @staticmethod
    def idamin(n: int, x: np.ndarray, incx: int):
        raise NotImplementedError

    @staticmethod
    def vsadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdadd(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vssub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdsub(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vssqr(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdsqr(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdmul(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsabs(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdabs(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdfmod(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdremainder(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsdiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vddiv(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vssqrt(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdsqrt(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vspow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdpow(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vspowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdpowx(n: int, a: np.ndarray, b: np.single, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsexp(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdexp(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsexp2(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdexp2(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsexp10(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdexp10(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsln(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdln(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vslog2(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdlog2(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vslog10(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdlog10(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vserf(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vderf(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vserfc(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vderfc(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vscdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdcdfnorm(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vserfinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vderfinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vserfcinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vderfcinv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vscdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdcdfnorminv(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vslgamma(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdlgamma(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vstgamma(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdtgamma(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsexpint1(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdexpint1(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsfloor(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdfloor(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsceil(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdceil(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vstrunc(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdtrunc(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsround(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdround(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdnearbyint(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsrint(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdrint(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdmodf(n: int, a: np.ndarray, y: np.ndarray, z: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsfrac(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdfrac(n: int, a: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdfmax(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdfmin(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdmaxmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vsminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def vdminmag(n: int, a: np.ndarray, b: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def sparse_s_mv(operation: int, m: int, k: int, alpha: np.single, val: np.ndarray, indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, descr, x: np.ndarray, beta: np.single, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def sparse_d_mv(operation: int, m: int, k: int, alpha: np.double, val: np.ndarray, indx: np.ndarray,
                    pntrb: np.ndarray, pntre: np.ndarray, descr, x: np.ndarray, beta: np.double, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def sparse_s_mm(operation: int, m: int, n: int, k: int, alpha: np.single, descr, layout: int, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.single,
                    y: np.ndarray, ldy: int):
        raise NotImplementedError

    @staticmethod
    def sparse_d_mm(operation: int, m: int, n: int, k: int, alpha: np.double, descr, layout: int, val: np.ndarray,
                    indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, ldx: int, beta: np.double,
                    y: np.ndarray, ldy: int):
        raise NotImplementedError

    @staticmethod
    def sparse_s_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        raise NotImplementedError

    @staticmethod
    def sparse_d_spmm(operation, request, sort, m, n, k, a, ja, ia, b, jb, ib, c, jc, ic, nzmax, info):
        raise NotImplementedError

    @staticmethod
    def sparse_s_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        raise NotImplementedError

    @staticmethod
    def sparse_d_add(operation, request, sort, m, n, a, ja, ia, beta, b, jb, ib, c, jc, ic, nzmax, info):
        raise NotImplementedError

    @staticmethod
    def scsrmv(transa: int, m: int, k: int, alpha: np.single, matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.single, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def dcsrmv(transa: int, m: int, k: int, alpha: np.double, matdescra: np.ndarray, val: np.ndarray, indx: np.ndarray,
               pntrb: np.ndarray, pntre: np.ndarray, x: np.ndarray, beta: np.double, y: np.ndarray):
        raise NotImplementedError

    @staticmethod
    def scsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.single, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.single,
               c: np.ndarray, ldc: int):
        raise NotImplementedError

    @staticmethod
    def dcsrmm(transa: np.char, m: int, n: int, k: int, alpha: np.double, matdescra: np.ndarray, val: np.ndarray,
               indx: np.ndarray, pntrb: np.ndarray, pntre: np.ndarray, b: np.ndarray, ldb: int, beta: np.double,
               c: np.ndarray, ldc: int):
        raise NotImplementedError

    @staticmethod
    def scsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        raise NotImplementedError

    @staticmethod
    def dcsrmult(trans: np.char, request: int, sort: int, m: int, n: int, k: int, a: np.ndarray, ja: np.ndarray,
                 ia: np.ndarray, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                 ic: np.ndarray, nzmax: int, info: int):
        raise NotImplementedError

    @staticmethod
    def scsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.single, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        raise NotImplementedError

    @staticmethod
    def dcsradd(trans: np.char, request: int, sort: int, m: int, n: int, a: np.ndarray, ja: np.ndarray, ia: np.ndarray,
                beta: np.double, b: np.ndarray, jb: np.ndarray, ib: np.ndarray, c: np.ndarray, jc: np.ndarray,
                ic: np.ndarray, nzmax: int, info: int):
        raise NotImplementedError
