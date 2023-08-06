import ctypes
import numpy as np
import os
cppfile = 'clooppra.dll'
dllpath = os.path.normpath(os.path.join(os.path.dirname(__file__),cppfile))
lib = ctypes.CDLL(dllpath)
cpp_function = "colorsearch"
colorsearch = lib.__getattr__(cpp_function)
cpp_function2 = "colorsearch2"
colorsearch2 = lib.__getattr__(cpp_function2)
cppcode = r"""
#include <omp.h>
#include <atomic>  
std::atomic<int> value(0);
int create_id() {
    return value++;
    }


extern "C" __declspec(dllexport) void colorsearch(unsigned char *pic, unsigned char *colors, int width, int totallengthpic, int totallengthcolor, int *outputx, int *outputy, int *lastresult)
{
    value = 0;
    int counter = 0;

#pragma omp parallel reduction(+ : counter)
    {


        for (int i = 0; i <= totallengthcolor; i += 3)
        {
            int r = colors[i];
            int g = colors[i + 1];
            int b = colors[i + 2];
#pragma omp for schedule(static)            
            for (int j = 0; j <= totallengthpic; j += 3)
            {
                if ((r == pic[j]) && (g == pic[j + 1]) && (b == pic[j + 2]))
                {

#pragma omp critical
                    {
                        int dividend = j / 3;
                        int quotient = dividend / width;
                        int remainder = dividend % width;
                        int upcounter = create_id();
                        outputx[upcounter] = quotient;
                        outputy[upcounter] = remainder;
                        lastresult[0] = upcounter;
                    }
                }
            }
        }
    }
}


extern "C" __declspec(dllexport) void colorsearch2(unsigned char *pic, unsigned char *colors, int width, int totallengthpic, int totallengthcolor, int *outputx, int *outputy, int *lastresult)
{
    value=0;
    int counter = 0;

#pragma omp parallel reduction(+ \
                               : counter)
    {

#pragma omp for schedule(static)
        for (int i = 0; i <= totallengthcolor; i += 3)
        {
        int r = colors[i];
        int g = colors[i + 1];
        int b = colors[i + 2];
            for (int j = 0; j <= totallengthpic; j += 3)
            {
                 if ((r == pic[j]) && (g == pic[j + 1]) && (b == pic[j + 2]))
                {

#pragma omp critical
                    {
                        int dividend = j / 3;
                        int quotient = dividend / width;
                        int remainder = dividend % width;
                        int upcounter = create_id();
                        outputx[upcounter] = quotient;
                        outputy[upcounter] = remainder;
                        lastresult[0] = upcounter;
                    }
                }
            }
        }
    }
}
// Compile:
// cl.exe /std:c++20 /fp:fast /EHsc /MT /Og /Oi /Ot /Oy /Ob3 /GF /Gy /MD /openmp /LD clooppra.cpp /Fe:clooppra.dll
// or
// cl.exe /std:c++20 /fp:fast /EHsc /O2 /MD /openmp /LD clooppra.cpp /Fe:clooppra.dll
// https://download.visualstudio.microsoft.com/download/pr/8b92f460-7e03-4c75-a139-e264a770758d/26C2C72FBA6438F5E29AF8EBC4826A1E424581B3C446F8C735361F1DB7BEFF72/VC_redist.x64.exe
"""

def search_colors(
        pic, colors, cpus=4,
):
    r"""
import numpy as np
import cv2
from locate_pixelcolor_cpppragma import search_colors
# 4525 x 6623 x 3 picture https://www.pexels.com/pt-br/foto/foto-da-raposa-sentada-no-chao-2295744/
picx = r"C:\Users\hansc\Downloads\pexels-alex-andrews-2295744.jpg"
pic = cv2.imread(picx)
colors0 = np.array([[255, 255, 255]],dtype=np.uint8)
resus0 = search_colors(pic=pic, colors=colors0, cpus=5)
colors1=np.array([(66,  71,  69),(62,  67,  65),(144, 155, 153),(52,  57,  55),(127, 138, 136),(53,  58,  56),(51,  56,  54),(32,  27,  18),(24,  17,   8),],dtype=np.uint8)
resus1 =  search_colors(pic=pic, colors=colors1, cpus=4)
print(resus1)

%timeit resus0 = search_colors(pic=pic, colors=colors0, cpus=5)
%timeit resus1 =  search_colors(pic=pic, colors=colors1, cpus=4)
23.4 ms ± 40.6 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
46.6 ms ± 988 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

    """
    if not pic.flags['C_CONTIGUOUS']:
        pic=np.ascontiguousarray(pic)
    os.environ["OMP_NUM_THREADS"] = str(cpus)
    if not isinstance(colors, np.ndarray):
        colors = np.array(colors, dtype=np.uint8)
    if not colors.flags['C_CONTIGUOUS']:
        colors=np.ascontiguousarray(colors)
    totallengthcolor = (colors.shape[0] * colors.shape[1])-1
    totallenghtpic = (pic.shape[0] * pic.shape[1] * pic.shape[2])-1
    outputx = np.zeros(totallenghtpic, dtype=np.int32)
    outputy = np.zeros(totallenghtpic, dtype=np.int32)
    endresults = np.zeros(1, dtype=np.int32)
    width = pic.shape[1]

    picb = pic.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    colorsb = colors.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    totallengthpicb = ctypes.c_int(totallenghtpic)
    totallengthcolorcb = ctypes.c_int(totallengthcolor)
    outputxb = outputx.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    outputyb = outputy.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    endresultsb = endresults.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    widthb = ctypes.c_int(width)
    if totallengthcolor == 2:
        colorsearch(
            picb,
            colorsb,
            widthb,
            totallengthpicb,
            totallengthcolorcb,
            outputxb,
            outputyb,
            endresultsb,
        )
    else:
        colorsearch2(
            picb,
            colorsb,
            widthb,
            totallengthpicb,
            totallengthcolorcb,
            outputxb,
            outputyb,
            endresultsb,
        )
    return np.dstack([outputx[:endresults[0]+1], outputy[:endresults[0]+1]])[0]