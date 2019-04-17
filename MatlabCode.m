clear; close all, clc;
generalPath = '../../../../../../PycharmProjects/CN-community/A3-networks';
files=dir(generalPath);

for k=1:length(files)
    if length(strfind(files(k).name,'net')) ~= 0
        string = strcat('../../../../../../PycharmProjects/CN-community/Matlab/',files(k).name);
        fileID = fopen(string,'w');
        string2 = strcat('../../../../../../PycharmProjects/CN-community/A3-networks/',files(k).name);
        fileID2 = fopen(string2,'r');
        info = fgetl(fileID2);
        num_vertices = '';
        entra = 1;
        for i=length(info):-1:1
            if entra == 1
                num_vertices = strcat(info(i), num_vertices);
            end
            if info(i) == ' '
                entra = 0;
            end
        end
        num_vertices = str2double(num_vertices);
        info = 'NewString';
        while strcmp(info(1:6),'*Edges')==0
            info = fgetl(fileID2);
            info = strcat(info,'NewString');
        end
        adjacency = zeros(num_vertices,num_vertices);
        nospace = 0;
        if strcmp(files(k).name,'airports_UW.net')==1
            while ~feof(fileID2)
            info = fgetl(fileID2);
            nums = strsplit(info,' ');
            if row == 999
                nospace = 1;
            end
            if nospace == 0
                row = str2double(nums(2));
                column = str2double(nums(3));
                weight = str2double(nums(4));
            else
                row = str2double(nums(1));
                column = str2double(nums(2));
                weight = str2double(nums(3));
            end
            adjacency(row, column) = weight;
            adjacency(column, row) = weight;
            end
        elseif strcmp(files(k).name,'cat_cortex_sim.net')==1 || strcmp(files(k).name,'graph3+1+3.net')==1 || strcmp(files(k).name,'graph4+4.net')==1
           while ~feof(fileID2)
            info = fgetl(fileID2);
            nums = strsplit(info,' ');
            row = str2double(nums(2));
            column = str2double(nums(3));
            weight = str2double(nums(4));
            adjacency(row, column) = weight;
            adjacency(column, row) = weight;
           end            
        else
           while ~feof(fileID2)
            info = fgetl(fileID2);
            nums = strsplit(info,' ');
            row = str2double(nums(1));
            column = str2double(nums(2));
            weight = str2double(nums(3));
            adjacency(row, column) = weight;
            adjacency(column, row) = weight;
           end 
        end
        class_labels = GCDanon(adjacency);
        for i=1:length(class_labels)
            fprintf(fileID, strcat('\n',num2str(class_labels(i))));
        end
        fclose(fileID);
        fclose(fileID2);
    end
end