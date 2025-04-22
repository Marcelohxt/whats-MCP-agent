import os
import numpy as np
from PIL import Image
import io
import base64
import sounddevice as sd
import scipy.io.wavfile as wav
from pydub import AudioSegment
import tempfile

class MediaProcessor:
    def __init__(self):
        self.max_audio_duration = 30  # segundos
        self.max_audio_size = 5 * 1024 * 1024  # 5MB
        self.max_image_size = 2 * 1024 * 1024  # 2MB
        self.target_image_size = (800, 800)  # dimensões máximas
        self.audio_sample_rate = 16000  # Hz
        self.audio_channels = 1  # mono

    def process_audio(self, audio_data, sample_rate):
        """
        Processa o áudio para otimizar o tamanho e qualidade
        """
        try:
            # Converte para array numpy se necessário
            if isinstance(audio_data, list):
                audio_data = np.concatenate(audio_data, axis=0)
            
            # Converte para mono se estiver em estéreo
            if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Normaliza o áudio
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Converte para int16 para reduzir tamanho
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Salva temporariamente como WAV
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                wav.write(temp_wav.name, sample_rate, audio_data)
                
                # Converte para MP3 para reduzir ainda mais o tamanho
                audio = AudioSegment.from_wav(temp_wav.name)
                audio = audio.set_frame_rate(self.audio_sample_rate)
                audio = audio.set_channels(self.audio_channels)
                
                # Ajusta o volume
                audio = audio.normalize()
                
                # Salva como MP3
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_mp3:
                    audio.export(temp_mp3.name, format="mp3", bitrate="64k")
                    
                    # Lê o arquivo MP3
                    with open(temp_mp3.name, 'rb') as f:
                        audio_bytes = f.read()
                    
                    # Limpa arquivos temporários
                    os.unlink(temp_wav.name)
                    os.unlink(temp_mp3.name)
                    
                    return audio_bytes
                    
        except Exception as e:
            print(f"Erro ao processar áudio: {str(e)}")
            return None

    def process_image(self, image_path):
        """
        Processa a imagem para otimizar o tamanho e qualidade
        """
        try:
            # Abre a imagem
            with Image.open(image_path) as img:
                # Converte para RGB se necessário
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Redimensiona mantendo a proporção
                img.thumbnail(self.target_image_size, Image.Resampling.LANCZOS)
                
                # Otimiza a qualidade
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                
                # Verifica o tamanho
                if output.getbuffer().nbytes > self.max_image_size:
                    # Se ainda for muito grande, reduz mais a qualidade
                    output = io.BytesIO()
                    img.save(output, format='JPEG', quality=70, optimize=True)
                
                return output.getvalue()
                
        except Exception as e:
            print(f"Erro ao processar imagem: {str(e)}")
            return None

    def audio_to_base64(self, audio_bytes):
        """Converte áudio para base64"""
        return base64.b64encode(audio_bytes).decode('utf-8')

    def image_to_base64(self, image_bytes):
        """Converte imagem para base64"""
        return base64.b64encode(image_bytes).decode('utf-8')

    def base64_to_audio(self, base64_string):
        """Converte base64 para áudio"""
        try:
            audio_bytes = base64.b64decode(base64_string)
            return AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        except Exception as e:
            print(f"Erro ao converter base64 para áudio: {str(e)}")
            return None

    def base64_to_image(self, base64_string):
        """Converte base64 para imagem"""
        try:
            image_bytes = base64.b64decode(base64_string)
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            print(f"Erro ao converter base64 para imagem: {str(e)}")
            return None 