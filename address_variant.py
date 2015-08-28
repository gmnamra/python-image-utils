import sys

class address_variant:
    def __init__(self, str):
        self.str=str
        self.int16=address_variant.str16(str)

    @staticmethod
    def str_hex(xstr):
          "returns string converted to int 16"
          return int(xstr, 16)
    @staticmethod
    def str16 (xstr):
          "returns a tuple str, bitcount, int 16, high byte and low byte"      
          int16 = address_variant.str_hex(xstr)
          bc = address_variant.bitCount(int16)
          return xstr, bc, int16, int16 >> 8 & 0xFF, int16 & 0xFF
    @staticmethod
    def str8 (xstr):
          "returns a tuple str, bitcount, and byte" 
          int16 = address_variant.str_hex(xstr)
          bc = address_variant.bitCount(int16)
          return xstr, bc, int16 & 0xFF

    @staticmethod
    def bitCount(int_type):
       count = 0
       while(int_type):
          int_type &= int_type - 1
          count += 1
       return(count)
