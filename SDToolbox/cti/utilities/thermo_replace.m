% Shock and Detonation Toolbox Utility Program
%
% thermo_replace.m 
% Replaces thermo data for specified species in a file formatted
% in nasa 7 (chemkin-style) format.  Replacement data are in subdirectory in
% individual files labeled by species name and created by thermo_refit.m,
% thermo_fit or partition.m.
% The file BadSpecies.txt contains the species name list in the format
% generated by check_thermo.py
% File containing substituted thermo data is thermo-refit.dat
% ################################################################################
% Theory, numerical methods and applications are described in the following report:
% 
%     Numerical Solution Methods for Shock and Detonation Jump Conditions, S.
%     Browne, J. Ziegler, and J. E. Shepherd, GALCIT Report FM2006.006 - R3,
%     California Institute of Technology Revised September, 2018.
% 
% Please cite this report and the website if you use these routines. 
% 
% Please refer to LICENCE.txt or the above report for copyright and disclaimers.
% 
% http://shepherd.caltech.edu/EDL/PublicResources/sdt/
% 
% ################################################################################ 
% Updated September 2018
% Tested with: 
%     MATLAB 2017b and 2018a, Cantera 2.3 and 2.4
% Under these operating systems:
%     Windows 8.1, Windows 10, Linux (Debian 9)
%% 
clear; clc; close all
%% The  following variables must be set by the user
newfile = true;  %  read in file of new data and replace old data, otherwise just check for species
dir_NAME ='GRI30-x'; % directory with the replacement and main thermo files 
thermo_FILE = 'thermo30.dat';  % file containing original thermo data
%% Open text file with species list
fileID = fopen('BadSpecies.txt','r');  % this is the file generated by check_thermo.py or a text editor.
format = '%s';
S = textscan(fileID, format);
fclose(fileID);
Lines = char([S{1}]);
[nl, nc] = size(Lines);
nsp = floor(nl/4);
sps = struct('name',[],'Tmin',[],'Tmid',[],'Tmax',[]);
for i = 1:nsp
    k = 4*(i-1) + 1;
    sps(i).name = strtrim(Lines(k,:));
    sps(i).Tmin = Lines(k+1,:);
    sps(i).Tmid = Lines(k+2,:);
    sps(i).Tmax = Lines(k+3,:);
end
display(['Found ',num2str(nsp), ' valid species in BadSpecies.txt'])
clearvars Lines, S;
%% open therm.dat file containing species data to be replaced
% read as text, each Line(i,:) contains text of line i of the file
original_thermo = [dir_NAME,'/',thermo_FILE];
fileID = fopen(original_thermo,'r');
format = '%s';
S = textscan(fileID, format,'delimiter','\n');
fclose(fileID);
Lines = char([S{1}]);
[nl, nc] = size(Lines);
%% find the species location within therm.dat
nfound = 0;
for lnum = 1:nl
    line = strtrim(strcat(Lines(lnum,1:18)));
    %    if ((Lines(ln,1:1) ~= '!') || ~isempty(strcat(Lines(ln,:)))) %skip comments and empty lines
    for j=1:nsp  % check to see if species name is a match in first 18 characters
        species = strtrim(strcat(sps(j).name));
        nj = length(species);
        possible = strncmp(line,species,nj);
        if (possible)
            if (nj == length(line));  % check match for length
                sps(j).line = lnum;
                display(['Species ',species,' starts on line ',num2str(lnum)]);
                nfound = nfound + 1;
            else
                np = nj+1;
                if (line(np:np) == ' ')  % check to see if extra characters are not part of name
                    sps(j).line = lnum;
                    display(['Species ',species,' starts on line ',num2str(lnum)]);
                    nfound = nfound + 1;
                    for k = np:18
                        Lines(lnum,k:k) = ' ';
                    end
                end
            end
        end
    end
    % end
end
display(['Found ',num2str(nfound),' species in therm.dat'])
%% read in new data and replace old data in file
if (newfile)
    clearvars S;
    for j = 1:nsp
        if (sps(j).line < nl)
            species_clean = strrep(sps(j).name,'*','star');
            speciesdatafilename =[dir_NAME,'/',species_clean,'.dat'];
            spdfile = fopen(speciesdatafilename, 'r');
            if (spdfile)
                format = '%s';
                S = textscan(spdfile, format, 'delimiter','\n');
                fclose(spdfile);
                dLines = char([S{1}]);
                [nld, ncd] = size(dLines);
                display(['Found species data file ',sps(j).name,' number of lines ',num2str(nld)]);
                jj = sps(j).line;
                for ii = 1:4
                    Lines(jj+ii-1,1:80) = dLines(ii,1:80);
                end
            else
                display(['Species data file ',sps(j).name,' not found']);
            end
        end
    end
    
    %% write out therm file with replaced data
    new_thermo = [dir_NAME,'/','thermo-refit.dat'];
    fileNEW = fopen(new_thermo,'w');
    format = '%s\n';
    for k =1:nl
        str = strtrim(Lines(k,:));
        if (~isempty(str) && (Lines(k,1:1) ~= '!'))    % don't modify comments or empty lines
            lens = 80 - length(str);
            space = '';
            if ((k > 2) && (k <= nl) && (lens > 0))
                if (lens == 1)
                    space = ' ';
                elseif (lens == 2)
                    space = '  ';
                end
                str =[space,str];   %leading spaces can get dropped during input
            end
        end
        fprintf(fileNEW,format,str);
    end
    fclose(fileNEW);
    display(['Sucessfully replaced ',num2str(nsp),' species thermo data in ','therm-refit.dat'])
end
