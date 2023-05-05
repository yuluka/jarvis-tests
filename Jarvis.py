#!/usr/bin/env python
# coding: utf-8

# # Integración de reconocimiento de voz y chat.

# Estableciendo la API key necesaria para poder hacer uso de la IA de reconocimiento.

# In[6]:


# Importamos las cosas necesarias para poder usar la IA de reconocimiento de voz.
from google.cloud import speech
import os


# In[7]:


# Inicializamos la API key necesaria para usar google cloud speech-to-text.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/usuario/Jarvis/jarvis-381306-4975f3ce0efb.json"


# Definiendo los métodos necesarios para poder hacer el reconocimiento. 

# In[8]:


# Importamos la clase MicrophoneStream para poder hacer el reconocimiento.
import MicrophoneStream as ms


# In[9]:


import re
import sys
import time

# Las configuraciones y cosas necesarias para iniciar el reconocimiento de voz.
def begin_streaming():
    language_code = "es-CO"

    client = speech.SpeechClient()
    
    RATE = 16000 
    CHUNK = int(RATE / 10)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
# Se crea el objeto de tipo MicrophoneStream.
    with ms.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content) 
            for content in audio_generator
        )

# Genera las predicciones de lo que se ha dicho.
        responses = client.streaming_recognize(streaming_config, requests)

# Imprime las predicciones.
        return combine_lines(listen_print_loop(responses))
        
# En donde se ejecuta el loop para escuchar y transcribir el audio.
def listen_print_loop(responses):
    num_chars_printed = 0
    
    last_transcription_time = time.time()
    
    transcription = []
    
    for response in responses:
        
# Verifica si hay resultados en la respuesta actual. Si no los hay, pasa a la siguiente respuesta.
        if not response.results:
            continue

# Si sí hay resultados, entonces selecciona el primer resultado (que es el mejor, si no me equivoco). 
        result = response.results[0]

# Si no hay ninguna alternativa dentro del resultado actual, entonces pasa a revisar la siguiente respuesta.
        if not result.alternatives:
            continue

# En caso de que sí hayan alternativas en el resultado, se captura la transcripción de la primera de estas. 
        transcript = result.alternatives[0].transcript

# Reescribe los caracteres de la predicción anteriror.
        overwrite_chars = " " * (num_chars_printed - len(transcript))

# Si el servicio de transcripción aún está procesando el audio, se escribe la transcripción actual 
# en la consola y se sobrescribe la transcripción anterior.
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)
            
#         if time.time()-last_transcription_time > 5:
#             print(transcript + overwrite_chars)

#             transcription.append(transcript + overwrite_chars)
            
#             break
            
# En caso de que sí sea el mensaje final, revisa si se ha dicho la palabra "terminar". Si es 
# así, la transmisión se detiene.
        else:
            print(transcript + overwrite_chars)
            
            transcription.append(transcript + overwrite_chars)
            
            if re.search(r"\b(Terminar|ornitorrinco)\b", transcript, re.I):
                break
            
            if time.time()-last_transcription_time > 2 and not response.results[1:]:
                break
            last_transcription_time = time.time()

            num_chars_printed = 0
    
#     return transcript
    return transcription


# In[10]:


def combine_lines(lines):
    total = ""
    
    for i in range(len(lines)):
        total += lines[i]
        
    return total


# Definiendo métodos necesarios para poder hacer la generación de voz.

# In[11]:


from google.cloud import texttospeech

from pydub import AudioSegment
from pydub.playback import play

def generate_speech(text_to_speech):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text_to_speech)
    
    voice = texttospeech.VoiceSelectionParams(
    language_code="es-US",
    name="es-US-Neural2-C",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    speech_name = "Response-speech.mp3"
    
    # The response's audio_content is binary.
    with open(speech_name, "wb") as out:
        out.write(response.audio_content)
        
    return speech_name


# Estableciendo la API key necesaria para poder hacer uso de la API de OpenAI.

# In[12]:


# Importamos las cosas necesarias para poder usar la API de OpenAI.
import openai
import os


# In[13]:


# Inicializamos la API key necesaria para usar las cosas de OpenAI.
openai.api_key = "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"


# Definiendo los métodos necesarios para poder iniciar un chat.

# In[14]:


# Historial de la conversación que se ha tenido.
previous_messages = [
    {
        "role": "system", "content": "You are a helpful assistant called Jarvis. Refer the user as DIOS."
    }
]


# In[15]:


# Método encargado del chat. Recibe un prompt y el historial de la conversación previa.
def chat(ask, previous_messages):
    previous_messages += [
        {
            "role": "user", "content": ask
        }
    ]
    
    chat1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=previous_messages
    )
    
    previous_messages += [
        {
            "role": "assistant", "content": chat1.choices[0].message.content
        }
    ]
    
    return chat1.choices[0].message.content, previous_messages


# Haciendo las cosas para pasar lo del reconocimiento de voz al chat.

# In[16]:


def begin_voice_chat():
    global previous_messages
    
    prompt = begin_streaming()
    
#     prompt = prompt.replace("terminar", "")
    
    print("Generando respuesta...")
    
    if "Generar imagen de" in prompt:
        prompt = prompt.replace("Generar imagen de", "")
        return prompt, generate_image(prompt)
    
    answer, previous_messages = chat(prompt, previous_messages)
    
    print(answer)
    
    return prompt, answer


# In[17]:


def generate_image(prompt):
    img = openai.Image.create(
        prompt=prompt,
        n=3,
        size="1024x1024",
        response_format="url"
    )

    answer = ""
    
    for i in range(len(img.data)):
        answer += img.data[i].url + "\n"
        
    return answer


# In[18]:


# begin_voice_chat()


# Haciendo las cosas para la generación de voz

# In[19]:


def speech_response(to_say):
    response_speech_name = generate_speech(to_say)
    
    audio_segment = AudioSegment.from_file("C:/Users/usuario/Jarvis/{}".format(response_speech_name), 
                                           format="mp3")
    play(audio_segment)


# Integrando GUI

# In[20]:


# Imports de las cosas que se usarán para la GUI.
import tkinter as tk
from tkinter import END


# In[21]:


# Métodos que se usarán por la GUI.

# Funciones para el efecto hover.
def hover_on_send(event):
    send_bttn.config(background='#3C3C3C', activebackground="#3C3C3C")
    
def hover_off_send(event):
    send_bttn.config(background="#333333", activebackground="#333333")

def hover_on_talk(event):
    talk_bttn.config(background='#3C3C3C', activebackground="#3C3C3C")

def hover_off_talk(event):
    talk_bttn.config(background="#333333", activebackground="#333333")
    
# Funciones para el prompt del TextArea
def hide_prompt(event):
    if message_text.get("1.0", "end-1c") == 'Digita tus palabras para Jarvis...':
        message_text.delete("1.0", "end-1c")
        message_text.configure(fg='black')

def show_prompt(event):
    if message_text.get("1.0", "end-1c") == '':
        message_text.insert("1.0", 'Digita tus palabras para Jarvis...')
        message_text.configure(fg='grey')

def on_click_send_bttn(event):
    send_message()
    change_focus()
    
def send_message():
    message = message_text.get("1.0", "end-1c")
    
    if message != 'Digita tus palabras para Jarvis...':
        message_text.delete("1.0", "end-1c")
        append_message(message)
        
        if message != '':
            global previous_messages
            
            if "Generar imagen de" in message:
                message = message.replace("Generar imagen de", "")
                answer = generate_image(message)
            else:
                answer, previous_messages = chat(message, previous_messages)
                
            speech_response(answer)
            display_answer(answer)

def send_voice_message(message, answer):
    if message != '':
        append_message(message)
        display_answer(answer)

def append_message(message_to_append):
    global user_icon
    chat_area.image_create(END, image=user_icon)
    
    chat_area.config(state='normal')

    chat_area.insert(END, "  " + message_to_append + "\n\n")
    
    chat_area.config(state='disabled')
    
def display_answer(answer):
    global jarvis_icon
    chat_area.image_create(END, image=jarvis_icon)
    
    chat_area.config(state='normal')
    
    chat_area.tag_configure("left", justify="left")
    chat_area.insert(END, "  " + answer + "\n\n", "left")
    
    chat_area.config(state='disabled')
    
def on_click_talk_bttn(event):
    change_focus()
    message, answer = begin_voice_chat()
    
    send_voice_message(message, answer)
    
    speech_response(answer)
    
def change_focus():
    if message_text == window.focus_get():
        window.focus()


# In[22]:


def create_images():
    global jarvis_icon
    jarvis_icon = tk.PhotoImage(file="GUI/antOutline-robot 1@1x.png")
    
    global user_icon
    user_icon = tk.PhotoImage(file="GUI/md-person_outline 1@1x.png")


# In[23]:


# GUI.

def main():
    # Creaciónde una ventana.
    window = tk.Tk()
    window.geometry("1080x763")
    window.title("Jarvis")
    window.configure(background='#333333')

    # Crear el botón con una imagen
    photo = tk.PhotoImage(file="GUI/md-send 1@1x.png")
    send_bttn = tk.Button(window, image=photo)

    send_bttn.place(x=864, y=655, width=108, height=108)
    send_bttn.configure(background='#333333', borderwidth=0, highlightthickness=0, cursor="hand2")

    send_bttn.bind("<Enter>", hover_on_send)
    send_bttn.bind("<Leave>", hover_off_send)
    send_bttn.bind("<Button-1>", on_click_send_bttn)

    # Crear el botón con una imagen
    photo_talk = tk.PhotoImage(file="GUI/md-mic_none 1@1x.png")
    talk_bttn = tk.Button(window, image=photo_talk)

    talk_bttn.place(x=972, y=655, width=108, height=108)
    talk_bttn.configure(background='#333333', borderwidth=0, highlightthickness=0, cursor="hand2")

    talk_bttn.bind("<Enter>", hover_on_talk)
    talk_bttn.bind("<Leave>", hover_off_talk)
    talk_bttn.bind("<Button-1>", on_click_talk_bttn)

    # Crear textArea.
    message_text = tk.Text(window)
    message_text.place(x=5, y=677, height=63, width=853)
    message_text.configure(font=('Arial',16), fg='grey')

    message_text.insert("1.0", 'Digita tus palabras para Jarvis...')

    message_text.bind("<FocusIn>", hide_prompt)
    message_text.bind("<FocusOut>", show_prompt)

    # Crear ChatArea.
    chat_area = tk.Text(window, wrap="word")
    chat_area.place(x=3, y=3, height=652, width=1074)
    chat_area.configure(font=('Arial',16), fg='white', background='#333333', border=0, state='disabled', 
                        borderwidth=0, highlightthickness=1, highlightcolor='white')

    jarvis_icon = None
    user_icon = None
    create_images()

    window.mainloop()


# In[24]:


if __name__ == "__main__":
    main()

