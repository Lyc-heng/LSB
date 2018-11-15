

a = imread('20-0.bmp');
a = rgb2gray(a);
 

b = imread('20-1.bmp')
b = rgb2gray(b);

peaksnr = psnr(a,b)