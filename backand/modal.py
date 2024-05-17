from rnnoise_wrapper import RNNoise
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os


def transribation(audio_file_name):
    noise_audio_file_name  = _remove_noise(audio_file_name)
    count_speech_voices = _trim_audio_speech(noise_audio_file_name)
    return count_speech_voices

def _remove_noise(audio_file_name):
    denoiser = RNNoise()
    audio = denoiser.read_wav(audio_file_name)
    denoised_audio = denoiser.filter(audio)
    noise_audio_file_name = f"rm_noise_{audio_file_name}"
    denoiser.write_wav(noise_audio_file_name, denoised_audio)
    return noise_audio_file_name

def _trim_audio_speech(noise_audio_file_name):
    def _export_nonsilent_chunks(audio_segment, nonsilent_ranges, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        for i, (start, end) in enumerate(nonsilent_ranges):
            chunk = audio_segment[start:end]
            chunk.export(f"{output_dir}/chunk_{i}.wav", format="wav")

    audio = AudioSegment.from_file(noise_audio_file_name, format="wav")
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-50)
    _export_nonsilent_chunks(audio, nonsilent_ranges, output_dir="output")
    return len(nonsilent_ranges)

