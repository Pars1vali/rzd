from rnnoise_wrapper import RNNoise


def transribation(audio_file_name):
    noise_audio_file_name  = _remove_noise(audio_file_name)
    return noise_audio_file_name

def _remove_noise(audio_file_name):
    denoiser = RNNoise()
    audio = denoiser.read_wav(audio_file_name)
    denoised_audio = denoiser.filter(audio)
    noise_audio_file_name = f"rm_noise_{audio_file_name}"
    denoiser.write_wav(noise_audio_file_name, denoised_audio)
    return noise_audio_file_name



