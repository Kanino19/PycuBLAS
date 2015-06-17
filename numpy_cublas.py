# -*- coding: utf-8 -*-

"""
Python functions to cuBLAS
For documentation see:
http://docs.nvidia.com/cuda/cublas/index.htm
"""

import ctypes
import pycublas
import pycuda.gpuarray
import numpy

class pycublasContext(object):
    def __init__(self):
        self._handle = pycublas.cublasHandle_t()
        self._cublasStatus = pycublas.cublasCreate(self._handle)
        
        self.CheckStatusFunction = None
    def __del__(self):
        self.cublasStatus = pycublas.cublasDestroy(self._handle)
    
    ## cublasStatus Check ##
    @property
    def cublasStatus(self):
        return self._cublasStatus
    @cublasStatus.setter
    def cublasStatus(self, status):
        if isinstance(status, pycublas.cublasStatus_t):
            self._cublasStatus = status
        if callable(self.CheckStatusFunction):
            self.CheckStatusFunction(self._cublasStatus)
        
    ## cuBLAS Helper Functions ##
    @property
    def Version(self):
        version = ctypes.c_int()
        self.cublasStatus = pycublas.cublasGetVersion(self._handle, version)
        return version.value
    

    ## cuBLAS Level-1 Functions ##
    def cublasI_amax(self, array, incx = 1):
        result = ctypes.c_int()
        if not(isinstance(array, pycuda.gpuarray.GPUArray)):
            array = pycuda.gpuarray.to_gpu( numpy.atleast_1d(array) )
        
        I_amax_function = {'float32'    : pycublas.cublasIsamax,
                           'float64'    : pycublas.cublasIdamax,
                           'complex64'  : pycublas.cublasIcamax,
                           'complex128' : pycublas.cublasIzamax
                           }[array.dtype.name]
        
        self.cublasStatus = I_amax_function(self._handle, array.size,
                                            int(array.gpudata), incx, result)
        return result.value - 1        
        
    def cublasI_amin(self, array, incx = 1):
        result = ctypes.c_int()
        if not(isinstance(array, pycuda.gpuarray.GPUArray)):
            array = pycuda.gpuarray.to_gpu( numpy.atleast_1d(array) )
        
        I_amin_function = {'float32'    : pycublas.cublasIsamin,
                           'float64'    : pycublas.cublasIdamin,
                           'complex64'  : pycublas.cublasIcamin,
                           'complex128' : pycublas.cublasIzamin
                           }[array.dtype.name]
        
        self.cublasStatus = I_amin_function(self._handle, array.size,
                                            int(array.gpudata), incx, result)
        return result.value - 1  
         
    def cublas_asum(self, array, incx = 1):
        if not(isinstance(array, pycuda.gpuarray.GPUArray)):
            array = pycuda.gpuarray.to_gpu( numpy.atleast_1d(array) )
        
        asum_function = {'float32'    : pycublas.cublasSasum, 
                         'float64'    : pycublas.cublasDasum,
                         'complex64'  : pycublas.cublasScasum,
                         'complex128' : pycublas.cublasDzasum
                         }[array.dtype.name]
        result_type = {'float32'    : ctypes.c_float,
                       'float64'    : ctypes.c_double,
                       'complex64'  : ctypes.c_float,
                       'complex128' : ctypes.c_double
                       }[array.dtype.name]   
                         
        result = result_type()
        self.cublasStatus = asum_function(self._handle, array.size,
                                          int(array.gpudata), incx, result)
        return result.value
        
