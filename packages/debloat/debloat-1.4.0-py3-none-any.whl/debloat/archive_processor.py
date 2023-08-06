import os
import struct
import utilities.types
import zipfile
import sys

ZIP_MAGIC = 0x4b50
RAR_MAGIC = 0x5261
PE_MAGIC = 0x4D5A

def read_magic_bytes(path) -> str:
    output = []
    file = open(path, 'rb')
    # No need to be end
    file.seek(0, os.SEEK_END)
    end = file.tell()
    file.seek(0, os.SEEK_SET)

    magic  = struct.unpack(utilities.types.uint16, file.read(2))[0]
    if magic == ZIP_MAGIC:
        process_zip(path)
        return "ZIP"
    elif magic == RAR_MAGIC:
        return "RAR"
    elif magic == PE_MAGIC:
        return "PE"
    else:
        return "Not recognized."
    return 0

def process_zip(path):
    sus_zip = zipfile.ZipFile(path)
    for file_info in sus_zip.filelist:
        compression = file_info.file_size / file_info.compress_size * 100
        print(hex(file_info.CRC))
        print("Filename: %s, Compression: %0.3f " % (file_info.filename, compression))



def process_rar():
    pass

def main() -> int:
    magic = read_magic_bytes(sys.argv[1])
    print(magic)

if __name__ == '__main__':
    main()