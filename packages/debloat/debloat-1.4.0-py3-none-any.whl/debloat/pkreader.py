import os
import struct
import utilities.types
import zipfile
import sys
import zlib
from bitstring import BitArray

ZIP_MAGIC = 0x4b50
RAR_MAGIC = 0x5261
PE_MAGIC = 0x4D5A

def readString(self):
    """Reading String on 8bits"""
    # Reading String length
    length = self.readInt()
    # XXX Some Length are two big...
    if length > self.dataSize - self.data.tell():
        return None
    return self.data.read(length).decode('utf-8', 'ignore')

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
    file = open(path, 'rb')
    # No need to be end
    file.seek(0, os.SEEK_END)
    end = file.tell()
    file.seek(0, os.SEEK_SET)
    header_signature = struct.unpack(utilities.types.uint32, file.read(4))[0]
    version_extract = struct.unpack(utilities.types.uint16, file.read(2))[0]
    general_flag = struct.unpack(utilities.types.uint16, file.read(2))[0]
    compression_method = struct.unpack(utilities.types.uint16, file.read(2))[0]
    file_last_modifyTime = struct.unpack(utilities.types.uint16, file.read(2))[0]
    file_last_modifyDate = struct.unpack(utilities.types.uint16, file.read(2))[0]
    crc32 = struct.unpack(utilities.types.uint32, file.read(4))[0]
    compressed_size = struct.unpack(utilities.types.uint32, file.read(4))[0]
    uncompressed_size = struct.unpack(utilities.types.uint32, file.read(4))[0]
    file_name_length = struct.unpack(utilities.types.uint16, file.read(2))[0]
    extra_field_length = struct.unpack(utilities.types.uint16, file.read(2))[0]
    file_name = file.read(file_name_length)
    extra_field = file.read(extra_field_length)
    compress_file_contents = file.read(compressed_size)
    compressed_as_bits = BitArray(compress_file_contents).bin

    block_header = compressed_as_bits[0:1]
    if block_header == '01':
        block_header = compressed_as_bits[1]
    
    print(block_header)
    


def process_rar():
    pass

def main() -> int:
    magic = read_magic_bytes(sys.argv[1])
    print(magic)

if __name__ == '__main__':
    main()