# Detect colors in images - 20 x faster than Numpy / 430 x faster than PIL

### pip install locate-pixelcolor-cpppragma

#### Tested against Windows 10 / Python 3.10 / Anaconda

### Important!
The module imports a function from a compiled .dll (C++). 
If you get any import errors, install:  https://download.visualstudio.microsoft.com/download/pr/8b92f460-7e03-4c75-a139-e264a770758d/26C2C72FBA6438F5E29AF8EBC4826A1E424581B3C446F8C735361F1DB7BEFF72/VC_redist.x64.exe


### How to use it in Python 

```python
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

####################################################################
%timeit resus0 = search_colors(pic=pic, colors=colors0, cpus=5)
23.4 ms ± 40.6 µs per loop (mean ± std. dev. of 7 runs, 10 loops each) # 10.9 ms after last update

b,g,r = pic[...,0],pic[...,1],pic[...,2]
%timeit np.where(((b==255)&(g==255)&(r==255)))
150 ms ± 209 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
####################################################################
%timeit resus1 =  search_colors(pic=pic, colors=colors1, cpus=4)
46.6 ms ± 988 µs per loop (mean ± std. dev. of 7 runs, 10 loops each) # 43.6 after last update

%timeit np.where(((b==66)&(g==71)&(r==69))|((b==62)&(g==67)&(r==65))|((b==144)&(g==155)&(r==153))|((b==52)&(g==57)&(r==55))|((b==127)&(g==138)&(r==136))|((b==53)&(g==58)&(r==56))|((b==51)&(g==56)&(r==54))|((b==32)&(g==27)&(r==18))|((b==24)&(g==17)&(r==8)))
1 s ± 16.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
####################################################################
```


### The C++ Code 

```cpp
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