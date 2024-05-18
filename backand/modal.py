from rnnoise_wrapper import RNNoise
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os, json
import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/stt_ru_conformer_transducer_large")

def transribation(audio_file):
    speech_valid = True
    type_problem = ["special_word"]
    #Папка где хранятся файлы служебного переговора
    output_directory = "output"

    #очищенная от шума аудидорожка
    clear_audio = _remove_noise(audio_file, output_directory)
    #увеличить громкость голоса говорящих
    louder_audio = _volume_up(clear_audio, output_directory, 10)
    #разделение аудиодорожки на куски с речью
    chunks_path = _trim_audio_speech(louder_audio, output_directory)
    #распознование речи в кусках текста
    text = _voice_recognition_audio(chunks_path)

    return speech_valid, type_problem, text

def _remove_noise(audio_file_name, output_directory):
    denoiser = RNNoise()
    audio = denoiser.read_wav(audio_file_name)
    denoised_audio = denoiser.filter(audio)
    noise_audio_file_name = f"rm_noise_{audio_file_name}"
    denoiser.write_wav(f"{output_directory}/{noise_audio_file_name}", denoised_audio)
    return noise_audio_file_name

def _volume_up(input_file_path, output_directory, increase_by_db):
    output_file_path = f"louder_{input_file_path}"
    audio = AudioSegment.from_file(f"{output_directory}/{input_file_path}")
    louder_audio = audio + increase_by_db
    louder_audio.export(f"{output_directory}/{output_file_path}", format="wav")
    return output_file_path

def _trim_audio_speech(clear_audio, output_directory):
    def _export_nonsilent_chunks(audio_segment, nonsilent_ranges, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for i, (start, end) in enumerate(nonsilent_ranges):
            chunk = audio_segment[start:end]
            chunk.export(f"{output_dir}/chunk_{i}.wav", format="wav")

    audio = AudioSegment.from_file(f"{output_directory}/{clear_audio}", format="wav")
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-50)
    _export_nonsilent_chunks(audio, nonsilent_ranges, "chunks")
    return f"{output_directory}/chunks"

def _voice_recognition_audio(directory_path):
    def _voice_recognition(speech_file):

        text = asr_model.transcribe([speech_file])
        return text[0][0]
    output = dict()
    counter = 0
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            text = _voice_recognition(file_path)
            output[counter]=text
            counter+=1
    return output


