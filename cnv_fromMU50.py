

from table import DrumVoice, Voice, WaveBank, Wave, Sample
from dataenum import *
from cnv_fromBASE import TableConverter
from typing import Literal, override

class fromMU50(TableConverter) : 

    source : MU = MU.MU50
    
    # pre requirements
    # * 1. handle sample associated with this drum voice first
    # * 2. update sample information
    # * 3. If ext voice, update associated voice
    # * 4. lastly, call this and update drum voice using sample / voice
    @override
    def ConvertDrumVoice(self, drum : DrumVoice, sample : Sample | None, ext_voice : Voice | None, target : MU) : 
        # * good for MU80, MU50, S-YXG50
        assert drum.format == MU.MU50 or drum.format == MU.SYXG50 or drum.format == MU.MU80
        assert len(drum.data) == 30
        assert target == MU.SYXG50

        # update addresses beforehand
        assert sample or ext_voice
        if sample : 
            assert sample.format == MU.SYXG50 
            assert sample.out_loop_address >= 0
        
        # MU50 and S-YXG50 drumvoice tables are exactly the same.
        # MU80 tables are close enough to work too.
        # all multi-byte values are big endian
        new_data = bytearray(drum.data)

        # +16: external voice seqID MSB 
        # +17: external voice seqID LSB
        if ext_voice : 
            assert ext_voice.converted
            assert ext_voice.extvoice_index >= 0
            new_data[16:16+2] = ext_voice.extvoice_index.to_bytes(2, byteorder='big', signed=False)

            #  if ext voice is used, the rest of the table should be blank
            for i in range(18, 30) : 
                new_data[i] = 0x00

        elif sample : 
            assert sample.out_sample_type != SampleFormat.UNKNOWN
            # sample_format = get_SampleFormat_Target(sample.sample_type, MU.MU50, MU.SYXG50)

            # +16 0xFFFF means use internal sample 
            new_data[16] = 0xFF
            new_data[17] = 0xFF

            # +19: offset negative
            # +20: offset negative
            new_data[19:19+2] = drum.offset_negative.to_bytes(2, byteorder='big', signed=False)

            # +21: offset positive msb, maybe
            # +22: offset positive
            # +23: offset positive
            new_data[21:21+3] = drum.offset_positive.to_bytes(3, byteorder='big', signed=False)

            # +24: loop address
            # +25: loop address
            # +26: loop address
            new_data[24:24+3] = sample.out_loop_address.to_bytes(3, byteorder='big', signed=False)

            # +27: sample type
            # new_data[27] = SampleFormat_to_Byte_SYXG50(sample.sample_type)
            new_data[27] = SampleFormat_to_Byte_SYXG50(sample.out_sample_type)
        
        drum.data = bytes(new_data)
        drum.format = MU.SYXG50


    # modifies elements. the voice's header is simple enough it will be handled in the main loop
    # * wavebank must be handled (and wavedata index assigned) before this
    @override
    def ConvertElements(self, voice : Voice, wavebanks : list[WaveBank], target : MU) -> None : 
        assert target == MU.SYXG50

        assert len(wavebanks) == len(voice.elements)

        # * S-YXG50 element format is a slightly condensed version of the MU50
        # * from 80 -> 78 bytes

        for i, e in enumerate(voice.elements) : 
            assert e.format == MU.MU50
            assert len(e.data) == 80

            # wavedata_index = wavedata_indexes[i]
            wavedata_index = wavebanks[i].index
            assert wavedata_index < 256 and wavedata_index >= 0

            new_data = bytearray(78)
            # MU50 +0 / +1: 8-bit waveID, but with the top bit in +0
            # S-YXG50: combined into a single byte at +0
            new_data[0] = wavedata_index

            # same
            new_data[1:5] = e.data[2:6]

            # MU50 +6: 1-bit LFO something-or-other
            # S-YXG50: condensed into top bit of +5
            LFOthing = e.data[6] << 7
            new_data[5] = LFOthing + e.data[7]

            # MU50 +8 - +80 same as S-YXG50 +6 to +78 (72 bytes)
            new_data[6:78] = e.data[8:80]

            e.data = bytes(new_data)
            e.format = MU.SYXG50

        voice.converted = True

