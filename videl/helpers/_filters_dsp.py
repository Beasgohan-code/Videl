# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl FFmpeg Audio Equalizer & DSP Effects Engine

DSP_PRESETS = {
    "normal": "",
    "bassboost": "-af bass=g=10:f=110:w=0.6",
    "superbass": "-af bass=g=18:f=90:w=0.8",
    "nightcore": "-af asetrate=48000*1.25,atempo=1.05",
    "slowed": "-af atempo=0.85,aecho=0.8:0.88:60:0.4",
    "8d": "-af apulsator=hz=0.125",
    "vaporwave": "-af aresample=48000,asetrate=48000*0.82",
    "treble": "-af treble=g=8:f=3000",
    "soft": "-af lowpass=f=3000",
}


def get_dsp_ffmpeg_param(preset: str) -> str:
    """Returns the FFmpeg audio filter parameter for the given preset."""
    return DSP_PRESETS.get(preset.lower(), "")
