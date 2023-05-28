import wave
from io import BytesIO

import lameenc
import numpy as np

_SAMPLERATE = 8000
_NUMPY_SIGNED_INT_MAX = np.iinfo(np.int16).max

_TABLE = dict()

# Latin characters
_TABLE.update({
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
})

# Numbers
_TABLE.update({
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
})

# Punctuation
_TABLE.update({
    ".": "......",
    ",": ".-.-.-",
    ":": "---...",
    ";": "-.-.-.",
    "(": "-.--.-",
    ")": "-.--.-",
    "'": ".----.",
    '"': ".-..-.",
    "-": "-....-",
    "\\": "-..-.",
    "_": "..--.-",
    "?": "..--..",
    "!": "--..--",
    "+": ".-.-.",
    "@": ".--.-.",
})

# Cyrillic characters
_TABLE.update({
    "а": _TABLE["a"],  # ".-"
    "б": _TABLE["b"],  # "-..."
    "в": _TABLE["w"],  # ".--"
    "г": _TABLE["g"],  # "--."
    "д": _TABLE["d"],  # "-.."
    "е": _TABLE["e"],  # "."
    "ё": _TABLE["e"],  # "."
    "ж": _TABLE["v"],  # "...-"
    "з": _TABLE["z"],  # "--.."
    "и": _TABLE["i"],  # ".."
    "й": _TABLE["j"],  # ".---"
    "к": _TABLE["k"],  # "-.-"
    "л": _TABLE["l"],  # ".-.."
    "м": _TABLE["m"],  # "--"
    "н": _TABLE["n"],  # "-."
    "о": _TABLE["o"],  # "---"
    "п": _TABLE["p"],  # ".--."
    "р": _TABLE["r"],  # ".-."
    "с": _TABLE["s"],  # "..."
    "т": _TABLE["t"],  # "-"
    "у": _TABLE["u"],  # "..-"
    "ф": _TABLE["f"],  # "..-."
    "х": _TABLE["h"],  # "...."
    "ц": _TABLE["c"],  # "-.-."
    "ч": "---.",
    "ш": "----",
    "щ": _TABLE["q"],  # "--.-"
    "ы": _TABLE["y"],  # "-.--"
    "ь": _TABLE["x"],  # "-..-"
    "ъ": _TABLE["x"],  # "-..-"
    "э": "..-..",
    "ю": "..--",
    "я": ".-.-",
})


def text_to_morse(message: str) -> str:
    """ Translates text to morse """

    pause_signals = " "
    pause_letters = pause_signals*3
    pause_words = pause_signals*7

    # TODO Ugly code
    words = (
        pause_letters.join(
            pause_signals.join(_TABLE[character])
            for character in word
            # TODO what about characters not in _TABLE.keys?
            if character in _TABLE.keys()
        )
        for word in message.lower().split()
    )

    return pause_words.join(words)


def _sine_wave(frequency, duration, volume=1.0, samplerate=_SAMPLERATE) -> bytes:
    """ Generates bytes representing a sine wave """
    size = int(samplerate*duration)
    array = np.arange(size)/samplerate  # Generate float64 array
    array = np.sin(2*np.pi*array*frequency)  # Sine function
    array *= _NUMPY_SIGNED_INT_MAX  # Normalize
    array *= volume  # Set volume
    array = array.astype(np.int16)  # Convert to 16 bit PCM
    return array.tobytes()


def _silence(duration, samplerate=_SAMPLERATE) -> bytes:
    """ Generates silence """
    size = int(samplerate*duration)
    zeros = np.zeros(size, dtype=np.int16)
    return zeros.tobytes()


def _encode_to_mp3(pcm_data: BytesIO):
    """ Encode pcm sound to mp3 """
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(32)
    encoder.set_in_sample_rate(_SAMPLERATE)
    encoder.set_channels(1)
    encoder.set_quality(7)  # 2-highest, 7-fastest
    encoded = encoder.encode(pcm_data)
    encoded += encoder.flush()
    return encoded


def morse_to_sound(message: str,
                        frequency: float = 1000.0,
                        volume: float = 0.25) -> bytes:
    """ Build Morse sound message from its text representation """
    dot_duration = 0.075  # Base length of 1 dot
    dash_duration = 3*dot_duration  # A dash is equal to 3 dots

    tones = {
        ".": _sine_wave(frequency, dot_duration, volume=volume),
        "-": _sine_wave(frequency, dash_duration, volume=volume),
        " ": _silence(dot_duration),
    }

    with BytesIO() as buffer:
        with wave.open(buffer, "wb") as wave_object:
            wave_object.setnchannels(1)
            wave_object.setsampwidth(2)
            wave_object.setframerate(_SAMPLERATE)
            wave_object.writeframes(_silence(0.25))
            for signal in message:
                wave_object.writeframes(tones[signal])
            wave_object.writeframes(_silence(1))
        buffer.seek(44)  # skip WAV header
        wave_data = buffer.read()
    return _encode_to_mp3(wave_data)
