# -*- coding: utf-8 -*-

"""
Raw ctypes wrappers of the cuBLAS library (v7.0)
For documentation see:
http://docs.nvidia.com/cuda/cublas/index.htm
cublas_api.h and cublas_v2.h
"""

import platform
import ctypes
import ctypes.util
import enum
from ctypes import *

### cuBLAS Library ###
libname = ctypes.util.find_library('cublas')
if platform.system()=='Microsoft': 
    libcublas = ctypes.windll.LoadLibrary(libname)
elif platform.system()=='Linux':     
    libcublas = ctypes.CDLL(libname, ctypes.RTLD_GLOBAL)
else:
    libcublas = ctypes.cdll.LoadLibrary(libname)


## cuBLAS Datatypes ##

#cublasStatus_t
class cublasStatus_t(enum.IntEnum):
    CUBLAS_STATUS_SUCCESS         =0
    CUBLAS_STATUS_NOT_INITIALIZED =1
    CUBLAS_STATUS_ALLOC_FAILED    =3
    CUBLAS_STATUS_INVALID_VALUE   =7
    CUBLAS_STATUS_ARCH_MISMATCH   =8
    CUBLAS_STATUS_MAPPING_ERROR   =11
    CUBLAS_STATUS_EXECUTION_FAILED=13
    CUBLAS_STATUS_INTERNAL_ERROR  =14
    CUBLAS_STATUS_NOT_SUPPORTED   =15

#cublasFillMode_t
class cublasFillMode_t(enum.IntEnum):
    CUBLAS_FILL_MODE_LOWER=0 
    CUBLAS_FILL_MODE_UPPER=1
c_cublasFillMode_t = c_int

#cublasDiagType_t
class cublasDiagType_t(enum.IntEnum):
    CUBLAS_DIAG_NON_UNIT=0
    CUBLAS_DIAG_UNIT=1
c_cublasDiagType_t = c_int

#cublasSideMode_t
class cublasSideMode_t(enum.IntEnum):
    CUBLAS_SIDE_LEFT =0 
    CUBLAS_SIDE_RIGHT=1
c_cublasSideMode_t = c_int

#cublasOperation_t
class cublasOperation_t(enum.IntEnum):
    CUBLAS_OP_N=0
    CUBLAS_OP_T=1
    CUBLAS_OP_C=2
c_cublasOperation_t = c_int

#cublasPointerMode_t
class cublasPointerMode_t(enum.IntEnum):
    CUBLAS_POINTER_MODE_HOST   = 0
    CUBLAS_POINTER_MODE_DEVICE = 1
c_cublasPointerMode_t = c_int

#cublasAtomicsMode_t
class cublasAtomicsMode_t(enum.IntEnum):
    CUBLAS_ATOMICS_NOT_ALLOWED   = 0
    CUBLAS_ATOMICS_ALLOWED       = 1
c_cublasAtomicsMode_t = c_int

#/* Opaque structure holding CUBLAS library context */
# struct cublasContext;
# typedef struct cublasContext *cublasHandle_t;
class _opaque(ctypes.Structure):
    pass
cublasHandle_t = POINTER(_opaque)
cublasHandle_t.__name__ = 'cublasHandle_t'


## cuBLAS Helper Functions ##

# cublasStatus_t cublasCreate(cublasHandle_t *handle)
cublasCreate = libcublas.cublasCreate_v2
cublasCreate.restype = cublasStatus_t
cublasCreate.argtypes = [POINTER(cublasHandle_t)]

# cublasStatus_t cublasDestroy(cublasHandle_t handle)
cublasDestroy = libcublas.cublasDestroy_v2
cublasDestroy.restype = cublasStatus_t
cublasDestroy.argtypes = [cublasHandle_t]

# cublasStatus_t cublasGetVersion(cublasHandle_t handle, int *version)
cublasGetVersion = libcublas.cublasGetVersion_v2
cublasGetVersion.restype = cublasStatus_t
cublasGetVersion.argtypes = [cublasHandle_t, POINTER(c_int)]


# cublasStatus_t cublasGetPointerMode(cublasHandle_t handle, cublasPointerMode_t *mode)
cublasGetPointerMode = libcublas.cublasGetPointerMode_v2
cublasGetPointerMode.restype = cublasStatus_t
cublasGetPointerMode.argtypes = [cublasHandle_t, POINTER(c_cublasPointerMode_t)]

# cublasStatus_t cublasSetPointerMode(cublasHandle_t handle, cublasPointerMode_t mode)
cublasSetPointerMode = libcublas.cublasSetPointerMode_v2
cublasSetPointerMode.restype = cublasStatus_t
cublasSetPointerMode.argtypes = [cublasHandle_t, c_cublasPointerMode_t]


# cublasStatus_t cublasSetAtomicsMode(cublasHandlet handle, cublasAtomicsMode_t mode)
cublasGetAtomicsMode = libcublas.cublasGetAtomicsMode
cublasGetAtomicsMode.restype = cublasStatus_t
cublasGetAtomicsMode.argtypes = [cublasHandle_t, POINTER(c_cublasAtomicsMode_t)]

# cublasStatus_t cublasSetAtomicsMode(cublasHandlet handle, cublasAtomicsMode_t mode)
cublasSetAtomicsMode = libcublas.cublasSetAtomicsMode
cublasSetAtomicsMode.restype = cublasStatus_t
cublasSetAtomicsMode.argtypes = [cublasHandle_t, c_cublasAtomicsMode_t]


## cuBLAS Level-1 Functions ##
memory_pointer = ctypes.c_void_p

# cublasStatus_t cublasIsamax(cublasHandle_t handle, int n,
#                             const float *x, int incx, int *result)
# cublasStatus_t cublasIdamax(cublasHandle_t handle, int n,
#                             const double *x, int incx, int *result)
# cublasStatus_t cublasIcamax(cublasHandle_t handle, int n,
#                             const cuComplex *x, int incx, int *result)
# cublasStatus_t cublasIzamax(cublasHandle_t handle, int n,
#                             const cuDoubleComplex *x, int incx, int *result)
cublasIsamax = libcublas.cublasIsamax_v2
cublasIdamax = libcublas.cublasIdamax_v2
cublasIcamax = libcublas.cublasIcamax_v2
cublasIzamax = libcublas.cublasIzamax_v2
for funct in [cublasIsamax, cublasIdamax, cublasIcamax, cublasIzamax]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                      memory_pointer, c_int, POINTER(c_int)]

# cublasStatus_t cublasIsamin(cublasHandle_t handle, int n,
#                             const float *x, int incx, int *result)
# cublasStatus_t cublasIdamin(cublasHandle_t handle, int n,
#                             const double *x, int incx, int *result)
# cublasStatus_t cublasIcamin(cublasHandle_t handle, int n,
#                             const cuComplex *x, int incx, int *result)
# cublasStatus_t cublasIzamin(cublasHandle_t handle, int n,
#                             const cuDoubleComplex *x, int incx, int *result)
cublasIsamin = libcublas.cublasIsamin_v2
cublasIdamin = libcublas.cublasIdamin_v2
cublasIcamin = libcublas.cublasIcamin_v2
cublasIzamin = libcublas.cublasIzamin_v2
for funct in [cublasIsamin, cublasIdamin, cublasIcamin, cublasIzamin]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                      memory_pointer, c_int, POINTER(c_int)]

# cublasStatus_t  cublasSasum(cublasHandle_t handle, int n,
#                             const float           *x, int incx, float  *result)
# cublasStatus_t  cublasDasum(cublasHandle_t handle, int n,
#                             const double          *x, int incx, double *result)
# cublasStatus_t cublasScasum(cublasHandle_t handle, int n,
#                             const cuComplex       *x, int incx, float  *result)
# cublasStatus_t cublasDzasum(cublasHandle_t handle, int n,
#                             const cuDoubleComplex *x, int incx, double *result)
cublasSasum  = libcublas.cublasSasum_v2
cublasDasum  = libcublas.cublasDasum_v2
cublasScasum = libcublas.cublasScasum_v2
cublasDzasum = libcublas.cublasDzasum_v2
for (funct, result_type) in [(cublasSasum, c_float), (cublasDasum, c_double), 
                            (cublasScasum, c_float), (cublasDzasum, c_double)]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                      memory_pointer, c_int, POINTER(result_type)]

# cublasStatus_t cublasSaxpy(cublasHandle_t handle, int n,
#                            const float           *alpha,
#                            const float           *x, int incx,
#                            float                 *y, int incy)
# cublasStatus_t cublasDaxpy(cublasHandle_t handle, int n,
#                            const double          *alpha,
#                            const double          *x, int incx,
#                            double                *y, int incy)
# cublasStatus_t cublasCaxpy(cublasHandle_t handle, int n,
#                            const cuComplex       *alpha,
#                            const cuComplex       *x, int incx,
#                            cuComplex             *y, int incy)
# cublasStatus_t cublasZaxpy(cublasHandle_t handle, int n,
#                            const cuDoubleComplex *alpha,
#                            const cuDoubleComplex *x, int incx,
#                            cuDoubleComplex       *y, int incy)
cublasSaxpy = libcublas.cublasSaxpy_v2
cublasDaxpy = libcublas.cublasDaxpy_v2
cublasCaxpy = libcublas.cublasCaxpy_v2
cublasZaxpy = libcublas.cublasZaxpy_v2
for funct in [cublasSaxpy, cublasDaxpy, cublasCaxpy, cublasZaxpy]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                      memory_pointer,
                      memory_pointer, c_int,
                      memory_pointer, c_int]

# cublasStatus_t cublasScopy(cublasHandle_t handle, int n,
#                            const float           *x, int incx,
#                            float                 *y, int incy)
# cublasStatus_t cublasDcopy(cublasHandle_t handle, int n,
#                            const double          *x, int incx,
#                            double                *y, int incy)
# cublasStatus_t cublasCcopy(cublasHandle_t handle, int n,
#                            const cuComplex       *x, int incx,
#                            cuComplex             *y, int incy)
# cublasStatus_t cublasZcopy(cublasHandle_t handle, int n,
#                            const cuDoubleComplex *x, int incx,
#                            cuDoubleComplex       *y, int incy)
cublasScopy = libcublas.cublasScopy_v2
cublasDcopy = libcublas.cublasDcopy_v2
cublasCcopy = libcublas.cublasCcopy_v2
cublasZcopy = libcublas.cublasZcopy_v2
for funct in [cublasScopy, cublasDcopy, cublasCcopy, cublasZcopy]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                      memory_pointer, c_int,
                      memory_pointer, c_int]

# cublasStatus_t cublasSdot (cublasHandle_t handle, int n,
#                            const float           *x, int incx,
#                            const float           *y, int incy,
#                            float           *result)
# cublasStatus_t cublasDdot (cublasHandle_t handle, int n,
#                            const double          *x, int incx,
#                            const double          *y, int incy,
#                            double          *result)
# cublasStatus_t cublasCdotu(cublasHandle_t handle, int n,
#                            const cuComplex       *x, int incx,
#                            const cuComplex       *y, int incy,
#                            cuComplex       *result)
# cublasStatus_t cublasCdotc(cublasHandle_t handle, int n,
#                            const cuComplex       *x, int incx,
#                            const cuComplex       *y, int incy,
#                            cuComplex       *result)
# cublasStatus_t cublasZdotu(cublasHandle_t handle, int n,
#                            const cuDoubleComplex *x, int incx,
#                            const cuDoubleComplex *y, int incy,
#                            cuDoubleComplex *result)
# cublasStatus_t cublasZdotc(cublasHandle_t handle, int n,
#                            const cuDoubleComplex *x, int incx,
#                            const cuDoubleComplex *y, int incy,
#                            cuDoubleComplex       *result)
cublasSdot = libcublas.cublasSdot_V2
cublasDdot = libcublas.cublasDdot_V2
cublasCdotu = libcublas.cublasCdotu_v2
cublasCdotc = libcublas.cublasCdotc_v2
cublasZdotu = libcublas.cublasZdotu_v2
cublasZdotc = libcublas.cublasZdotc_v2
for funct in [cublasSdot, cublasDdot, 
              cublasCdotu, cublasCdotc,
              cublasZdotu, cublasZdotc]:
    funct.restype = cublasStatus_t
    funct.argtypes = [cublasHandle_t, c_int,
                     memory_pointer, c_int,
                     memory_pointer, c_int,
                     result_pointer]


