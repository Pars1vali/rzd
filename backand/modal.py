from rnnoise_wrapper import RNNoise
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os, json
import nemo.collections.asr as nemo_asr
# asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/stt_ru_conformer_transducer_large")

def transribation(audio_file):
    #Папка где хранятся файлы служебного переговора
    output_directory = "output"
    #очищенная от шума аудидорожка
    clear_audio = _remove_noise(audio_file)
    #разделение аудиодорожки на куски с речью
    count_speech_voices = _trim_audio_speech(clear_audio, output_directory)
    #распознование речи в кусках текста
    # text = _voice_recognition_audio(output_directory)
    return count_speech_voices#, text

def _remove_noise(audio_file_name):
    denoiser = RNNoise()
    audio = denoiser.read_wav(audio_file_name)
    denoised_audio = denoiser.filter(audio)
    noise_audio_file_name = f"rm_noise_{audio_file_name}"
    denoiser.write_wav(noise_audio_file_name, denoised_audio)
    return noise_audio_file_name

def _trim_audio_speech(clear_audio, output_directory):
    def _export_nonsilent_chunks(audio_segment, nonsilent_ranges, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        for i, (start, end) in enumerate(nonsilent_ranges):
            chunk = audio_segment[start:end]
            chunk.export(f"{output_dir}/chunk_{i}.wav", format="wav")

    audio = AudioSegment.from_file(clear_audio, format="wav")
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-50)
    _export_nonsilent_chunks(audio, nonsilent_ranges, output_dir=output_directory)
    return len(nonsilent_ranges),

def _volume_up():
    pass

# def _voice_recognition_audio(directory_path):
#     def _voice_recognition(speech_file):
#
#         text = asr_model.transcribe([speech_file])
#         return text[0][0]
#     output = dict()
#     counter = 0
#     for file_name in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, file_name)
#         if os.path.isfile(file_path):
#             text = _voice_recognition(file_path)
#             output[counter]=text
#             counter+=1
#     return output


