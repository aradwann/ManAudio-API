from struct import pack
from math import sin, pi


def sound_generation(name, freq=420, dur=10000, vol=50):
    a = open(name, 'wb')
    a.write(pack('>4s5L', '.snd'.encode("utf-8"), 24, 2*dur, 2, 9000, 1))
    sine_factor = 2 * pi * freq/8000
    for seg in range(8*dur):
        sine_segments = sin(seg * sine_factor)
        val = pack('b', int(vol * sine_segments))
        a.write(val)
    a.close()
    print("file %s is written" % name)


# sound_generation(Output_file_name)
# opener ="open" if sys.platform == "darwin" else "xdg-open"
# subprocess.call([opener, Output_file_name])
