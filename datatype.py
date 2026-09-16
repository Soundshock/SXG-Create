# from dataclasses import dataclass
# from typing import Literal, override
# # from enum import Enum

# # * this is old as shit 
# # this was intended for making keys for extracting and abstracting AWM2 data in one fell swoop
# # it fell apart because the AWM2 data is confusing and my sources are highly contradictory
# # on what the values mean

# # but this idea might make a comeback


# # * example of mass encoding back to bytearray
# # byte_array = b''.join([b.value_encode() for b in list_of_datatypes])

# BYTE_ORDERS = Literal['little', 'big']

# # helper functions
# def bytes_and(a1 : bytes | bytearray, a2 : bytes | bytearray) : 
#     return bytes(map(lambda a,b : a & b, a1, a2))

# def bytes_or(a1 : bytes | bytearray, a2 : bytes | bytearray) : 
#     return bytes(map(lambda a,b : a | b, a1, a2))

# # todo might trim the fat here and just keep the value_decode / decode_bytes and value_encode
# # ? @staticmethod, 
# # ? ... maybe not actually since the object will still need to be instantiated 
# # ? before it can be passed around, and staticmethods won't have access to defined parameters
# @dataclass
# class datatype() : 
#     byteorder : BYTE_ORDERS = 'little'
#     signed : bool = False
#     len : int = 1

#     # * Hold value. this is messy and kinda experimental
#     value : int = 0
#     initial_offset : int = -99999 # ! goofy, just for debugging our table deconstruction

#     @classmethod
#     def from_bytes(cls, data : bytes | bytearray, offset : int) : 
#         new_obj = cls()
#         new_obj.value = new_obj.decode_bytes(data, offset)
#         new_obj.initial_offset = offset # ! goofy, remove when we are done with it
#         return new_obj

#     def __len__(self) -> int :  # is this confusing? Would anyone ever len(int)?? (I think it errors??) object.len feels weird, so idk
#         return self.len

#     # helper function
#     def clamp(self, value : int, minval : int, maxval : int) -> int :
#         return max(minval, min(value, maxval))

#     # * take encoded value and return decoded
#     def decode(self, value : int) -> int : 
#         # print('decode base')
#         return value

#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return int.from_bytes(array[idx:idx+self.len], byteorder=self.byteorder, signed=self.signed)

#     def value_decode(self) -> int : 
#         return self.decode(self.value)

#     def value_decode_bytes(self, array : bytearray, idx : int) -> None : 
#         self.decode_bytes(array, idx)


#     def encode(self, value : int) -> bytes : 
#         return value.to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)

#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = value.to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)

#     def value_encode(self) -> bytes : 
#         return self.encode(self.value)

#     def value_encode_bytes(self, array : bytearray, idx : int) -> None : 
#         self.encode_bytearray(self.value, array, idx)

#     def encoded_fmt(self, value : int) -> str :
#         ba = self.encode(value)
#         s : str = ''
#         for b in ba : 
#             s = s + '{:02X}'.format(b)
#         return s
    
#     def value_encoded_fmt(self) -> str : 
#         return self.encoded_fmt(self.value)


# # will have to be a special case, shouldn't be too many of these though hopefully
# @dataclass 
# class string(datatype) : 
#     byteorder : BYTE_ORDERS = 'big' # I think?
#     len : int = 1
#     @override
#     def decode(self, value : int) -> int : 
#         raise Exception('Error: datatype string needs special behavior')
#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         raise Exception('Error: datatype string needs special behavior')
#     @override
#     def encode(self, value : int) -> bytes :
#         raise Exception('Error: datatype string needs special behavior')
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         raise Exception('Error: datatype string needs special behavior')

    
# class u8(datatype) : 
#     pass

# class u7(datatype) : 
#     @override
#     def decode(self, value : int) -> int : 
#         return value & 0x7F
    
#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return array[idx] & 0x7F

#     @override
#     def encode(self, value : int) -> bytes :
#         return (value & 0x7F).to_bytes(self.len, byteorder=self.byteorder)
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], (value & 0x7F).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )

# # 7-bit ubyte that ranges from -64 to +63. middle=64 / 0x40
# class s7(datatype) : 
#     @override
#     def decode(self, value : int) -> int : 
#         value = (value & 0x7F) - 64
#         value = self.clamp(value, -64, 63)
#         return value
#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         value = (array[idx] & 0x7F) - 64
#         return self.clamp(value, -64, 63)
    
#     @override
#     def encode(self, value : int) -> bytes :
#         # if value > 63 | value < -64 : raise ValueError
#         value = self.clamp(value,-64,63)
#         value = value + 64
#         return value.to_bytes(self.len, byteorder=self.byteorder, signed=False)
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         value = self.clamp(value,-64,63)
#         value = value + 64
#         # array[idx:idx+self.len] = value.to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], (value & 0x7F).to_bytes(self.len, byteorder=self.byteorder, signed=False) )


# class s8(datatype) : 
#     signed = True
#     @override
#     def encode(self, value : int) -> bytes : 
#         # if value > 127 | value < -128 : raise ValueError
#         value = self.clamp(value, -128, 127)
#         return value.to_bytes(1, signed=True)
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         value = self.clamp(value, -128, 127)
#         array[idx:idx+self.len] = value.to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)

    
# @dataclass
# class u16(datatype) :
#     byteorder : BYTE_ORDERS = 'little'
#     sii16gned : bool = False
#     len : int = 2

# @dataclass
# class u24(datatype) :
#     byteorder : BYTE_ORDERS = 'big' # * big by default
#     signed : bool = False
#     len : int = 3

# @dataclass
# class u32(datatype) :
#     byteorder : BYTE_ORDERS = 'little' # * big by default
#     signed : bool = False
#     len : int = 4

# @dataclass
# class u12_0FFF(datatype) : 
#     byteorder : BYTE_ORDERS = 'big'
#     signed : bool = False
#     len : int = 2 # 1.5...

#     @override
#     def decode(self, value : int) -> int : 
#         return value & 0x0FFF
    
#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return array[idx] & 0x0FFF
    
#     @override
#     def encode(self, value : int) -> bytes :
#         return (value & 0x0FFF).to_bytes(self.len, byteorder=self.byteorder)
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], (value & 0x0FFF).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )


# # 00000001
# class bit(datatype) : 
#     @override
#     def decode(self, value : int) -> int : 
#         return value & 0x01
    
#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return array[idx] & 0x01
    
#     @override
#     def encode(self, value : int) -> bytes :
#         return (value & 0x01).to_bytes(self.len, byteorder=self.byteorder)
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], (value & 0x01).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )



# class bit_10000000(datatype) : 
#     @override
#     def decode(self, value : int) -> int : 
#         return (value & 0x80) >> 7

#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return (array[idx] & 0x80) >> 7
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], (value << 7).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )

#     @override
#     def encode(self, value : int) -> bytes : 
#         return (value << 7).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)


# class bit_01000000(datatype) : 

#     @override
#     def decode(self, value : int) -> int : 
#         return (value & 0x40) >> 6

#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return (array[idx] & 0x40) >> 6
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], ((value & 0x01) << 6).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )

#     @override
#     def encode(self, value : int) -> bytes : 
#         return ((value & 0x01) << 6).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)


# class bit_00100000(datatype) : 

#     @override
#     def decode(self, value : int) -> int : 
#         return (value & 0x20) >> 5

#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return (array[idx] & 0x20) >> 5
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], ((value & 0x01) << 5).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )

#     @override
#     def encode(self, value : int) -> bytes : 
#         return ((value & 0x01) << 5).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)

# class bit_00010000(datatype) : 

#     @override
#     def decode(self, value : int) -> int : 
#         return (value & 0x10) >> 4

#     @override
#     def decode_bytes(self, array : bytes | bytearray, idx : int) -> int : 
#         return (array[idx] & 0x10) >> 4
    
#     @override
#     def encode_bytearray(self, value : int, array : bytearray, idx : int) -> None : 
#         array[idx:idx+self.len] = bytes_or(array[idx:idx+self.len], ((value & 0x01) << 4).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed) )

#     @override
#     def encode(self, value : int) -> bytes : 
#         return ((value & 0x01) << 4).to_bytes(self.len, byteorder=self.byteorder, signed=self.signed)


# # debug
# def main() : 
#     def fmtbyte(b) -> str : return '{:02x}'.format(b)
#     def fmtbytes(ba) -> str : 
#         s : str = ''
#         for b in ba : 
#             s = s + '{:02X}'.format(b) + ' '
#         return s


#     bytes : bytearray = bytearray.fromhex("00 00 00 00 00 00 00 00")

#     print(fmtbytes(bytes))

#     byte7 = u7()
#     bit1 = bit_10000000()

#     value7 = 0x7F
#     value1 = 1

#     # byte7.encode_bytearray(value7, bytes, 0)
#     # print(fmtbytes(bytes))
#     # bit1.encode_bytearray(value1, bytes, 0)
#     # print(fmtbytes(bytes))

#     # print(bit_10000000().decoded(0x80))
    
#     print(u12_0FFF().decode(0x0fff))

#     # bytes.



# if __name__ == "__main__":
#     main()




