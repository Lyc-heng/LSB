G = imread('11-0.jpg');
wm_image = imread('test.jpg');
% a = rgb2gray(wm_image);
t = imread('test1.jpg');
% b = rgb2gray(t);

psnr1 = psnr(G,wm_image);
psnr2 = psnr(G,t);


figure('name','��1��д'),
    subplot(1,3,1),imshow(G), title('Original');
    subplot(1,3,2),imshow(wm_image), title(strcat('LSB�滻, PSNR=',num2str(psnr1)));
    subplot(1,3,3),imshow(wm_image), title(strcat('LSBƥ��, PSNR=',num2str(psnr2)));
figure('name','��1��д histogram'),
    subplot(1,3,1),histogram(G),title('Original');
    subplot(1,3,2),histogram(wm_image),title('LSB�滻');
    subplot(1,3,3),histogram(t),title('LSBƥ��');