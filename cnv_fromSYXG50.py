

from table import DrumVoice, Voice, WaveBank, Wave, Sample
from dataenum import *
from cnv_fromBASE import TableConverter
from typing import Literal, override

class fromSYXG50(TableConverter) : 

    source : MU = MU.SYXG50

    # modifies elements. the voice's header is simple enough it will be handled in the main loop
    # * wavebank must be handled (and wavedata index assigned) before this
    @override
    def ConvertElements(self, voice : Voice, wavebanks : list[WaveBank], target : MU) -> None : 

        # * already formatted correctly, all that's necessary is to insert the new wavedata.index
        assert target == MU.SYXG50

        assert len(wavebanks) == len(voice.elements)

        for i, e in enumerate(voice.elements) : 
            assert e.format == MU.SYXG50
            assert len(e.data) == 78

            new_data = bytearray(e.data)

            assert wavebanks[i].index < 256 and wavebanks[i].index >= 0
            new_data[0] = wavebanks[i].index

            e.data = bytes(new_data)
            e.format = MU.SYXG50

        voice.converted = True

