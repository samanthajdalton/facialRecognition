from findtools.find_files import (find_files, Match)
import collect_facial_points

#Creating training dataset

infile_path = '/Users/dev/Desktop/repos/faces/CFD2/images2/'
outfile_path = '/Users/dev/Desktop/repos/faces/CFD2/cropped/'
sh_files_pattern = Match(filetype='f', name='*N.jp*')
sh_files_pattern1 = Match(filetype='f', name='*HO.jp*')
found_files = list(find_files(path=infile_path, match=sh_files_pattern)) + list(find_files(path=infile_path, match=sh_files_pattern1))

training_raw = collect_facial_points.create_crops_points(found_files, outfile_path)

