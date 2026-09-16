

from dataenum import *


# contains decoding information, makes table object
import decode 
import decMU80 
import decMU50
import decSYXG50 
import decMU90 
from decBase import PrintTableInfo

# makes S-YXG50 using table object
import makeSYXG50 

# converts tables (used by makeSYXG50)
import cnv_fromMU50 
import cnv_fromMU80
import cnv_fromMU90
import cnv_fromSYXG50

from utils import WriteBytesToFile, WriteTXT, FileExists, Dejumble, Friendly_error

from pathlib import Path


def Convert(mu_src : MU, mu_tgt : MU, out_path : str, program_roms : list[Path], wave_roms : list[Path] ) : 

    in_wave_bytes = bytes()
    match mu_src : 
 
        case MU.MU80 : 

            # todo 
            # unknown significance of the second bit in the sample format (never DPCM, always 1 with s16 drums?)
            # two of the pad samples can't fit into the 16 bit loop offset, and click when they loop
            # could be cleaned up by hand with a new loop point (with more body offset to fit the whole sample)
            # (and targeting vampire will probably fix it properly) 
            new_table_version='SXG MU80' # 16 bytes max
            new_table_name='SXGMU80a1.TBL' # ?? max
            new_waverom_name='SXGMU80a1.UPCM' # 15 bytes max
  
            table_decoder = decMU80.MU80.From_Bytes(Dejumble(open( program_roms[0], mode='rb').read() ) )
            table_converter=cnv_fromMU80.fromMU80(MU.MU80)
            
            for path in wave_roms : 
                in_wave_bytes = in_wave_bytes + bytes(open(path, mode='rb').read() )


        case MU.MU50 : 

            new_table_version='SXGMU50a1'
            new_table_name=f'{new_table_version}.TBL'
            new_waverom_name='SXGMU50a1.UPCM'
    
            table_decoder = decMU50.MU50.From_Bytes(Dejumble(open( program_roms[0], mode='rb').read() ) )
            table_converter=cnv_fromMU50.fromMU50(MU.MU50)
            for path in wave_roms : 
                in_wave_bytes = in_wave_bytes + bytes(open(path, mode='rb').read() )
 
        case MU.SYXG50 : 
            
            new_table_version='S-YXG50a1'
            new_table_name=f'{new_table_version}.TBL'
            new_waverom_name='SYXGTESTa1.UPCM'

            table_decoder = decSYXG50.SYXG50.From_Bytes(open( program_roms[0], mode='rb').read() )
            table_converter=cnv_fromSYXG50.fromSYXG50(MU.SYXG50)
            for path in wave_roms : 
                in_wave_bytes = in_wave_bytes + bytes(open(path, mode='rb').read() )
                     
        case MU.MU90 : 

            # ! not currently working
            # todo 
            # haven't totally figured out the interleaved waveroms
            # reverse samples have to be reconstructed
            # ? 1 new byte of totally unknown function, it's present in both drum voice and wavedata tables
            # drum voices that make use of new EG parameters can be reconstructed as ext voices, possibly
            # (but no way will they all fit in S-YXG50, wavedata entries is at 243/255 already)
            # MU90 has also found a new way to break the S-YXG50's bank map table (100% fixable)

            new_table_version='SXG MU90'
            new_table_name='SXGMU90t.TBL'
            new_waverom_name='SXGMU90.UPCM'

            table_decoder = decMU90.MU90.From_Bytes(Dejumble(open( program_roms[0], mode='rb').read() ) )
            table_converter=cnv_fromMU90.fromMU90(MU.MU90)

            # todo wrong
            for path in wave_roms : 
                in_wave_bytes = in_wave_bytes + bytes(open(path, mode='rb').read() )
 
        case _ : 
            raise NotImplementedError()

    table = decode.Create_Table(table_decoder, mu_src, table_decoder.data, wave_roms)
    PrintTableInfo(table)


    table_bin, samplemonster = makeSYXG50.MakeSYXG50(table, 
                                in_waves=in_wave_bytes,
                                tablecnv=table_converter, 
                                new_table_version=new_table_version,
                                new_table_name=new_table_name,
                                new_waverom_name=new_waverom_name)



    WriteBytesToFile(table_bin, new_table_name, root_dir=out_path)


    # create rehex (debug)
    out_table_decoder = decSYXG50.SYXG50.From_Bytes(table_bin)
    WriteTXT(out_table_decoder.get_rehex_json(), new_table_name+r'.rehex-meta', root_dir=out_path)

    if FileExists(new_waverom_name, root_dir=out_path) : 
        Friendly_error(f'\'{new_waverom_name}\' already exists, exiting early')
        exit(1)

    # * construct our (deferred) new waverom
    waverom = samplemonster.Generate()
    WriteBytesToFile(waverom, new_waverom_name, root_dir=out_path)


