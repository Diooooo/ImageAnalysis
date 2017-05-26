image = dicomread('./testdata/hw2/PCA_001.dcm');    %读取第一张dcm图
[m, n] = size(image);                               %获取矩阵维度
result = zeros(m, n);                               %创建输出矩阵，维度同读取图像

Files = dir(strcat('./testdata/hw2/', '*.dcm'));    %读取所有待处理dcm图
LengthFiles = length(Files);
%MIP算法操作330张dcm图像
for i = 1:LengthFiles
    path = strcat('./testdata/hw2/', Files(i).name);
    image = dicomread(path);
    for j = 1:m
        for k = 1:n
           result(j, k) = max(result(j, k), image(j, k)); 
        end
    end
end
%显示并储存结果图像
imshow(result/max(result(:)))
saveImage = result/max(result(:));
imwrite(saveImage, './outputdata/hw2/result.bmp');

