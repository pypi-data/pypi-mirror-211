# Detects colors in images 10 x faster than Numpy 

### pip install locate-pixelcolor-c

#### Tested against Windows 10 / Python 3.10 / Anaconda



### How to use it in Python 

```python
import numpy as np
import cv2
from locate_pixelcolor_c import search_colors
# 4525 x 6623 x 3 picture https://www.pexels.com/pt-br/foto/foto-da-raposa-sentada-no-chao-2295744/
picx = r"C:\Users\hansc\Downloads\pexels-alex-andrews-2295744.jpg"
pic = cv2.imread(picx)
colors0 = np.array([[255, 255, 255]],dtype=np.uint8)
resus0 = search_colors(pic=pic, colors=colors0)
colors1=np.array([(66,  71,  69),(62,  67,  65),(144, 155, 153),(52,  57,  55),(127, 138, 136),(53,  58,  56),(51,  56,  54),(32,  27,  18),(24,  17,   8),],dtype=np.uint8)
resus1 =  search_colors(pic=pic, colors=colors1)
####################################################################
%timeit search_colors(pic=pic, colors=colors0)
17.6 ms ± 245 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# last update: 16.3 ms

b,g,r = pic[...,0],pic[...,1],pic[...,2]
%timeit np.where(((b==255)&(g==255)&(r==255)))
150 ms ± 209 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
####################################################################
%timeit resus1 =  search_colors(pic=pic, colors=colors1)
138 ms ± 10 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# last update: 117 ms


%timeit np.where(((b==66)&(g==71)&(r==69))|((b==62)&(g==67)&(r==65))|((b==144)&(g==155)&(r==153))|((b==52)&(g==57)&(r==55))|((b==127)&(g==138)&(r==136))|((b==53)&(g==58)&(r==56))|((b==51)&(g==56)&(r==54))|((b==32)&(g==27)&(r==18))|((b==24)&(g==17)&(r==8)))
1 s ± 16.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
####################################################################
```


### The C Code 

```c

void colorsearch(unsigned char *pic, unsigned char *colors, int width, int totallengthpic, int totallengthcolor, int *outputx, int *outputy, int *lastresult)
{
    int counter = 0;

    for (int i = 0; i <= totallengthcolor; i += 3)
    {
        int r = colors[i];
        int g = colors[i + 1];
        int b = colors[i + 2];
        for (int j = 0; j <= totallengthpic; j += 3)
        {
            if ((r == pic[j]) && (g == pic[j + 1]) && (b == pic[j + 2]))
            {

                int dividend = j / 3;
                int quotient = dividend / width;
                int remainder = dividend % width;
                int upcounter = counter;
                outputx[upcounter] = quotient;
                outputy[upcounter] = remainder;
                lastresult[0] = upcounter;
                counter++;
            }
        }
    }
}
// gcc -O2 -fPIC -shared -o cloop.so cloop.c
```