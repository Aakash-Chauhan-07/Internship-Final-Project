from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def get_default_audio_device():
    """Get the default audio device"""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    """Get the current volume level as a percentage"""
    volume = get_default_audio_device()
    current_volume = volume.GetMasterVolumeLevelScalar()
    return int(current_volume * 100)

def set_volume(level):
    """Set the volume level (0 to 100)"""
    volume = get_default_audio_device()
    if 0 <= level <= 100:
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        print(f"Volume set to {level}%")
    else:
        raise ValueError("Volume level must be between 0 and 100")

