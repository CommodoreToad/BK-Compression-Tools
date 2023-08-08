# BK-Compression-Tools

Requirements:
1) Python 3
2) C compiler

Instructions
1) Make a backup of your ISO
2) Download BK-decode.py, BK-encode.py, LZSS.c
3) Compile LZSS.c into LZSS.exe and store with the other python scripts
4) Extract BK files from the ISO
5) To decompress a BK file, run the following command in the console "py 'path'\BK-decode.py 'path'\'FILENAME'" This will create a decompressed file with "_decoded" appended. "index.bin" must be located in the same folder as all other files.
6) To decompcompress all files, run the following command in the console "py 'path'\BK-decode.py 'path to files'' -a". "index.bin" must be located in the same folder as all of the other files.
7) If the file size changes, index.bin will need to be edited.
8) Recompress the file in the console with this command "py <path>/BK-encode.py <path>/<FILENAME>_decoded" This will recompress the file with "_c" appended
9) Replace the new compressed file and use another utility to remake the ISO
