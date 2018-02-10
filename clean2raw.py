
# coding: utf-8

"""
This is a google style docs.
 Author: SongZhirui
 
 E-mail: songzhiruifly@hotmail.com
 
 Parameters:
   param1 - file: Clean.fq.gz
   param2 - file: Raw.fq.gz 
   param3 - int: DupReads
      
 Returns:
   outfile - : Raw.fq.gz added the DupReads.
 
 Raises:
   error: if any errors happend, you need to check the script and ask help.

 Example:
   eg: python clean2raw.py Clean.fq.gz Raw.fq.gz 1000
"""
import gzip
import sys

clean = gzip.open(sys.argv[1], "r")
raw = gzip.open(sys.argv[2], "w")
dup_counts = int(sys.argv[3])

def get_xy(read_name):
    read_name = read_name.split()[0].split(":")
    location = slice(5,7)
    x, y = read_name[location]
    return (x, y)

def dup_reads(alist, x, y):
    blist = []
    blist.append(alist[0].replace(x, y))
    blist + alist[1:]
    return blist

index = 0
count = 1
a_tmp = []
b_tmp = []
for line in clean:
    index += 1
    if (index % 8) in [1,2,3,4]:
        a_tmp.append(line) 
    else:
        b_tmp.append(line) 
    if index % 8 == 0 and count <=dup_counts:
        x1, y1 = get_xy(a_tmp[0])
        x2, y2 = get_xy(b_tmp[0])
        x0 = str(int(sum([int(x1),int(x2)])/2))
        y0 = str(int(sum([int(y1),int(y2)])/2))
        xx = str(int(sum([int(x1),int(x2)])/4))
        yy = str(int(sum([int(y1),int(y2)])/4))
        c_tmp = dup_reads(a_tmp, x1+":"+y1, x0+":"+y0)
        d_tmp = dup_reads(a_tmp, x1+":"+y1, xx+":"+yy)
        all_info = a_tmp + d_tmp + c_tmp + b_tmp
        raw.writelines(all_info)
        a_tmp = []
        b_tmp = []
        count += 2
    elif index % 8 == 0 and count > dup_counts:
        all_info = a_tmp + b_tmp
        raw.writelines(all_info)
        a_tmp = []
        b_tmp = []
clean.close()
raw.close()
print("all work done!")

