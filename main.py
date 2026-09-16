import argparse # todo 
from sys import argv 
from pathlib import Path

from dataCRCs import TableIn, ROMLIST
from utils import calccrc32, Friendly_error
from dataenum import MU

import convert

# input: MU roms (in any order)

# * only one target for now
BUILD_TARGET = MU.SYXG50

def Print_Input_Roms() : 
    s = '---- Decode-Supported input roms ----\n'
    for table_ref in ROMLIST : 
        if table_ref.Can_Decode() : 
            s = s + str(table_ref) + '\n'
    print(s)

def main() : 

    files : list[Path] = []

    for file in argv[1:] : 
        f = Path(file)
        if not Path.is_file(f) :
            s = f'input {file} is not a file!'
            # raise Exception(s)
            Friendly_error(s)
            exit(1)
        files.append(Path(file))

    if not files :
        Print_Input_Roms()
        Friendly_error('')
        exit(1)

    print(f'calculating CRC32 ({len(files)} files)...')
    crcs_paths : dict[str, Path] = {calccrc32(x) : x for x in files} # dict comprehension

    print('CRC32 calculation done')


    table_type : TableIn | None = None
    # match input to reference romlist
    for table_reference in ROMLIST : 
        if table_reference.Is_List_Ours(crcs_paths) : 
            table_type = table_reference
            break

    if not table_type : 
        Print_Input_Roms()
        Friendly_error('valid ROMs not found')
        exit(1)

    if not (table_type.support == 'decode' or table_type.support == 'both') : 
        Friendly_error(f'ROM detected, but decode not supported for {table_type.name}!')


    print(f'{table_type.name} detected, targeting {BUILD_TARGET}')

    paths_program, paths_waves = table_type.Order_Pathlists(crcs_paths)

    print(f'program rom(s) = {[p.name for p in paths_program]}')
    print(f'   wave rom(s) = {[p.name for p in paths_waves]}')

    # get output path
    out_path = str(paths_program[0].parent)
    
    convert.Convert(table_type.source, MU.SYXG50, out_path, paths_program, paths_waves)

    Friendly_error('End of Code')

if __name__ == "__main__":
    main()
