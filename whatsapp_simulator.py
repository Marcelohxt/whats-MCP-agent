import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import requests
import json
from datetime import datetime
import threading
import time
import os
import base64
import sounddevice as sd
import numpy as np
from media_processor import MediaProcessor

class WhatsAppSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador WhatsApp")
        self.root.geometry("600x800")
        
        # Inicializa o processador de mídia
        self.media_processor = MediaProcessor()
        
        # Número do telefone e botão limpar
        frame_top = ttk.Frame(self.root)
        frame_top.pack(pady=10, padx=10, fill='x')
        
        # Frame para número do telefone (à esquerda)
        frame_phone = ttk.Frame(frame_top)
        frame_phone.pack(side='left', fill='x', expand=True)
        
        ttk.Label(frame_phone, text="Seu número:").pack(side='left')
        self.phone_number = ttk.Entry(frame_phone)
        self.phone_number.insert(0, "5511930779357")  # Número padrão
        self.phone_number.pack(side='left', padx=5, fill='x', expand=True)
        
        # Botão limpar (à direita)
        ttk.Button(
            frame_top, 
            text="Limpar Conversa", 
            command=self.clear_chat
        ).pack(side='right', padx=5)
        
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20)
        self.chat_area.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Área de mensagem e botões de mídia
        frame_msg = ttk.Frame(self.root)
        frame_msg.pack(pady=10, padx=10, fill='x')
        
        # Botões de mídia
        frame_media = ttk.Frame(frame_msg)
        frame_media.pack(side='left', fill='y')
        
        # Botão de gravação de áudio
        self.record_button = ttk.Button(
            frame_media, 
            text="🎤", 
            command=self.toggle_recording,
            width=3
        )
        self.record_button.pack(side='left', padx=2)
        
        # Botão de imagem
        ttk.Button(
            frame_media, 
            text="📷", 
            command=self.send_image,
            width=3
        ).pack(side='left', padx=2)
        
        # Campo de mensagem
        self.message_entry = ttk.Entry(frame_msg)
        self.message_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        ttk.Button(frame_msg, text="Enviar", command=self.send_message).pack(side='right', padx=5)
        
        # Status do servidor
        self.status_label = ttk.Label(self.root, text="Status: Desconectado")
        self.status_label.pack(pady=5)
        
        # Bind Enter key
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Inicia verificação de status
        self.check_server_status()
        
        # Mensagem inicial
        self.add_message("Bem-vindo ao Simulador WhatsApp! Digite sua mensagem abaixo.", False)
        
        # Variáveis para gravação de áudio
        self.is_recording = False
        self.recording = None
        self.recording_thread = None
        self.recording_start_time = None
        self.recording_duration = 0
    
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        try:
            self.is_recording = True
            self.record_button.config(text="⏺️")  # Muda para ícone de gravação
            self.recording = []
            self.recording_start_time = time.time()
            self.recording_duration = 0
            
            def record_audio():
                def callback(indata, frames, time, status):
                    if status:
                        print(status)
                    self.recording.append(indata.copy())
                    
                    # Atualiza a duração da gravação
                    self.recording_duration = time.time() - self.recording_start_time
                    
                    # Verifica se atingiu o tempo máximo
                    if self.recording_duration > self.media_processor.max_audio_duration:
                        self.root.after(0, self.stop_recording)
                
                with sd.InputStream(samplerate=self.media_processor.audio_sample_rate, 
                                  channels=self.media_processor.audio_channels, 
                                  callback=callback):
                    while self.is_recording:
                        sd.sleep(100)
            
            self.recording_thread = threading.Thread(target=record_audio)
            self.recording_thread.start()
            
        except Exception as e:
            self.is_recording = False
            self.record_button.config(text="🎤")
            self.add_message(f"Erro ao iniciar gravação: {str(e)}", False)
    
    def stop_recording(self):
        try:
            self.is_recording = False
            self.record_button.config(text="🎤")  # Volta para ícone de microfone
            
            if self.recording_thread:
                self.recording_thread.join()
            
            if self.recording:
                # Processa o áudio
                audio_bytes = self.media_processor.process_audio(
                    self.recording, 
                    self.media_processor.audio_sample_rate
                )
                
                if audio_bytes:
                    # Converte para base64
                    base64_audio = self.media_processor.audio_to_base64(audio_bytes)
                    
                    # Prepara os dados para enviar
                    data = {
                        "messages": [{
                            "from": self.phone_number.get(),
                            "type": "audio",
                            "body": base64_audio,
                            "filename": "audio.mp3"
                        }]
                    }
                    
                    # Adiciona mensagem ao chat
                    self.add_message("🎤 Áudio enviado")
                    
                    # Inicia thread para enviar mídia
                    threading.Thread(target=self._send_message_thread, args=(data,)).start()
                
        except Exception as e:
            self.add_message(f"Erro ao processar gravação: {str(e)}", False)
    
    def send_image(self):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            try:
                # Processa a imagem
                image_bytes = self.media_processor.process_image(file_path)
                
                if image_bytes:
                    # Converte para base64
                    base64_image = self.media_processor.image_to_base64(image_bytes)
                    
                    # Prepara os dados para enviar
                    data = {
                        "messages": [{
                            "from": self.phone_number.get(),
                            "type": "image",
                            "body": base64_image,
                            "filename": os.path.basename(file_path)
                        }]
                    }
                    
                    # Adiciona mensagem ao chat
                    self.add_message(f"📷 Imagem enviada: {os.path.basename(file_path)}")
                    
                    # Inicia thread para enviar mídia
                    threading.Thread(target=self._send_message_thread, args=(data,)).start()
                
            except Exception as e:
                self.add_message(f"Erro ao processar imagem: {str(e)}", False)
    
    def clear_chat(self):
        """Limpa o histórico da conversa e adiciona a mensagem de boas-vindas"""
        self.chat_area.delete(1.0, tk.END)
        self.add_message("Bem-vindo ao Simulador WhatsApp! Digite sua mensagem abaixo.", False)
    
    def add_message(self, message, is_sent=True):
        timestamp = datetime.now().strftime("%H:%M")
        prefix = "Você" if is_sent else "Bot"
        self.chat_area.insert(tk.END, f"[{timestamp}] {prefix}: {message}\n\n")
        self.chat_area.see(tk.END)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Limpa o campo de mensagem
        self.message_entry.delete(0, tk.END)
        
        # Adiciona a mensagem ao chat
        self.add_message(message)
        
        # Prepara os dados para enviar
        data = {
            "messages": [{
                "from": self.phone_number.get(),
                "type": "text",
                "body": message
            }]
        }
        
        # Inicia thread para enviar mensagem
        threading.Thread(target=self._send_message_thread, args=(data,)).start()
    
    def _send_message_thread(self, data):
        try:
            # Envia para o webhook
            response = requests.post(
                "http://localhost:8000/webhook",
                headers={"Content-Type": "application/json"},
                json=data
            )
            
            if response.status_code == 200:
                # Simula um pequeno delay para parecer mais natural
                time.sleep(1)
                
                # Obtém a resposta do SerralheriaAgent
                agent_response = self.get_agent_response(data["messages"][0]["body"])
                
                # Adiciona a resposta do bot ao chat
                self.root.after(0, lambda: self.add_message(agent_response, False))
            else:
                self.root.after(0, lambda: self.add_message(
                    f"Erro ao enviar mensagem: {response.status_code}", False))
        
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.add_message(
                "Erro: Não foi possível conectar ao servidor", False))
    
    def get_agent_response(self, message):
        try:
            from serralheria_agent import SerralheriaAgent
            agent = SerralheriaAgent()
            return agent.processar_mensagem(message)
        except Exception as e:
            return f"Erro ao processar mensagem: {str(e)}"
    
    def check_server_status(self):
        try:
            response = requests.get("http://localhost:8000/api/status")
            if response.status_code == 200:
                self.status_label.config(text="Status: Conectado")
            else:
                self.status_label.config(text="Status: Erro na conexão")
        except:
            self.status_label.config(text="Status: Servidor offline")
        
        # Agenda próxima verificação
        self.root.after(5000, self.check_server_status)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WhatsAppSimulator()
    app.run() 