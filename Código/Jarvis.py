#!/usr/bin/env python
# coding: utf-8

# # Jarvis

# ---

# ## Tabla de contenidos
# 
# 1. [Reconocimiento de voz](#Reconocimiento-de-voz)
#     1. [API de Google cloud](#API-key-de-Google-cloud:)
#     2. [Función begin_streaming](#Función-begin_streaming():)
#     3. [Función listen_print_loop](#Función-listen_print_loop():)
#     4. [Función combine_lines](#Función-combine_lines():)
# 
# 2. [Conversión de texto a voz](#Conversión-de-texto-a-voz)
#     1. [Función generate_speech](#Función-generate_speech():)
#     2. [API key de ElevenLabs](#API-key-de-ElevenLabs:)
#     3. [Función generate_speech_eleven](#Función-generate_speech_eleven():)
#     4. [Función speech_response](#Función-speech_response():)
#     
# 3. [Chat usando OpenAI](#Chat-usando-el-modelo-de-OpenAI)
#     1. [API key de OpenAI](#API-key-de-OpenAI:)
#     2. [Historial de mensajes](#Historial-de-mensajes:)
#     3. [Función chat](#Función-chat():)
#     4. [Contexto del modelo](#Contexto-del-modelo:)
#     5. [Función clasify_prompt](#Función-clasify_prompt():)
#     
# 4. [Generación de imágenes](#Generación-de-imágenes)
#     1. [Función generate_image](#Función-generate_image():)
#     
# 5. [Interacción entre GUI y Chat](#Interacción-entre-GUI-y-el-Chat)
#     1. [Función begin_chat](#Función-begin_chat():)
#     2. [Función begin_voice_chat](#Función-begin_voice_chat():)
#     
# 6. [GUI](#GUI)
#     1. [Funciones y procedimientos de la GUI](#Funciones-y-procedimientos-de-la-GUI:)
#     2. [Función create_images](#Función-create_images():)
#     3. [Creación de la GUI](#Creación-de-la-GUI:)

# ---

# ##  Reconocimiento de voz

# ### API key de Google cloud:
# 
# Establecemos la API key de google cloud para pder hacer uso del modelo de reconocimiento de voz, así como el de transformación de texto a voz.

# In[2]:


# Importamos las cosas necesarias para poder usar la IA de reconocimiento de voz.
from google.cloud import speech
import os


# In[3]:


# Inicializamos la API key necesaria para usar google cloud speech-to-text.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/usuario/Jarvis/Código/jarvis-381306-4975f3ce0efb.json"


# ---

# A continuación se encuentran las funciones utilizadas para el reconocimiento de voz por medio de transmisión continua a través del micrófono.
# 
# `MicrophoneStream` es la clase que permite activar el micrófono para que detecte lo que estamos diciendo.
# 
# ### Función `begin_streaming()`:
# 
# Dentro de la función `begin_streaming()` se establecen las configuraciones del modelo que usaremos.
# 
# Inicialmente, seleccionamos el lenguaje que el modelo va a detectar. Tras eso, establecemos los parámetros técnicos del audio que vamos a transmitir (tales como su bit rate o la cantidad de frames que se almacenarán en el buffer).
# 
# Seguido de las configuraciones pertinentes, se inicia la transmisión mediante el micrófono del dispositivo y se hace uso de un loop que es el que se encarga de la transcripción de las cosas que el micrófono capta.
# 
# ### Función `listen_print_loop()`:
# 
# Esta función recibe el audio que se ha captado mediante el micrófono del dispositvos y se encarga de hacer la transcripción de este audio. Para esto, y debido a que no hace toda la transcripción de una sola, usamos un arreglo llamado `transcription` que después uniremos en unsa sola cadena de texto.
# 
# El modelo de Speech To Text hace varias predicciones para lo que decimos y las guarda en un arreglo, ordenadas en función de su probabilidad de ser la correcta. Lo que hace esta función, entonces, es recorrer este arreglo y seleccionar las alternativas con mayor probabilidad para construir la predicción final.
# 
# Ademas de eso, se va encargando de imprimir lo que se dice, a medida que se dice, en la GUI.

# In[4]:


# Importamos la clase MicrophoneStream para poder hacer el reconocimiento.
import MicrophoneStream as ms


# In[5]:


import re
import sys
import time

# Esta función se encarga de las configuraciones y cosas necesarias para iniciar el reconocimiento de voz.
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
        
# En donde se ejecuta el loop para transcribir el audio.
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
#             sys.stdout.write(transcript + overwrite_chars + "\r")
#             sys.stdout.flush()
            
            # Va escribiendo lo que detecta en el Text para escribir mensajes.
            message_text.delete('1.0', END)
            message_text.insert(END,transcript + overwrite_chars)
            
            num_chars_printed = len(transcript)
            
        # En caso de que sí sea el mensaje final, revisa si se ha dicho la palabra "terminar". Si es 
        # así, la transmisión se detiene.
        else:
#             print(transcript + overwrite_chars)
            
            message_text.delete('1.0', END)
            message_text.insert(END,transcript + overwrite_chars)
    
            transcription.append(transcript + overwrite_chars)
            
            if time.time()-last_transcription_time > 2 and not response.results[1:]:
                break
            last_transcription_time = time.time()

            num_chars_printed = 0
    
    return transcription


# ### Función `combine_lines()`:
# 
# Lo que hace esta función es convertir todos los pedacitos del arreglo que contiene la transcripción en una sola cadena de texto.

# In[6]:


# Como la transcripción está almacenada en un array, tenemos que combinar lo que hay en cada index
# para hacer un solo string. 
def combine_lines(lines):
    total = ""
    
    for i in range(len(lines)):
        total += lines[i]
        
    return total


# ---

# ## Conversión de texto a voz

# ### Función `generate_speech()`:
# 
# Esta función se encarga de recibir el texto que se quiere convertir a texto (las respuestas de Jarvis) y convertirlas a voz.
# 
# Inicialmente, configura el usuario para usar el modelo de Text to Speech. Tras eso, hace la configuración de la voz que se usará (para este caso, Google cloud ofrece ciertas voces entre las que se puede escoger). 
# 
# Después de eso, configura el formato del audio que generará y hace la solicitud para la conversión del texto a voz.
# 
# Por último, guarda el archivo de audio generado con el nombre almacenado en la variable `speech_name` y retorna este nombre para, posteriormente, poder hacer la reproducción.

# In[7]:


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


# ### API key de ElevenLabs:
# 
# Establecemos la API key de Eleven labs para poder hacer uso de sus servicios de conversión de texto a voz.

# In[8]:


from elevenlabs import generate, play, set_api_key, voices, Models
from pydub import AudioSegment
from pydub.playback import play
import requests

elevenlabs_api_key = "bda4bf2d76534665d063d8bde1fb0c78"
set_api_key(elevenlabs_api_key)


# ### Función `generate_speech_eleven()`:
# 
# Esta es una función que, en síntensis, hace lo mismo que la anterior, pero usanod un servicio distinto. 
# 
# Esta función hace uso del servicio de ElevenLabs y sirve como altenativa a la función anterior.
# 
# Inicialmente, se escoge la voz deseada y se almacena su ID en la variable `voice`. Después de esto, se hacen todas las configuraciones pertinentes para poder hacer solicitudes al servicio.
# 
# Por último, se hace la solicitud y se guarda el archivo generado con el nombre almacenado en la variable `speech_name`. Esta variable, igual que en el caso anterior, se retorna para poder hacer la reproducción del audio.

# In[9]:


def generate_speech_eleven(text_to_speech):
    voice = "TxGEqnHWrfWFTfGW9XjX"
    
    # streaming chunk size
    CHUNK_SIZE = 1024

    XI_API_KEY = elevenlabs_api_key

    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": elevenlabs_api_key
    }

    data = {
        "text": text_to_speech,
        "model_id" : "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    speech_name = "Response-speech.mp3"
    
    response = requests.post(url, headers=headers, json=data)

    with open(speech_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                
    return speech_name


# Estas líneas sirven para imprimir la lista de voces, junto con sus ID's, para poder seleccionar la que se desea usar.

# In[10]:


# voice_list = voices()
# voice_labels = [voice.category + " voice: " + voice.name + " id: " + voice.voice_id for voice in voice_list]

# voice_labels


# ### Función `speech_response()`:
# 
# Esta función recibe el texto que se quiere convertir a voz y hace uso de las funciones anteriormente explicadas para convertirlo a voz. Luego de esto, recibe el nombre del archivo donde se guardó el audio generado y hace uso la función `play()`, de la librería `pydub`, para reproducirlo.

# In[11]:


def speech_response(to_say):
    response_speech_name = generate_speech(to_say)
   
#     response_speech_name = generate_speech_eleven(to_say)

#     audio_segment = AudioSegment.from_file("C:/Users/usuario/Jarvis/Código/{}".format(response_speech_name), 
#                                            format="mp3")

    audio_segment = AudioSegment.from_file(response_speech_name, 
                                           format="mp3")
    
    play(audio_segment)


# ---

# ## Chat usando el modelo de OpenAI

# ### API key de OpenAI:
# 
# Establecemos la API key necesaria para poder hacer solicitudes a los modelos de OpenAI.

# In[12]:


# Importamos las cosas necesarias para poder usar la API de OpenAI.
import openai
import os


# In[13]:


# Inicializamos la API key necesaria para usar las cosas de OpenAI.
openai.api_key = "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"


# ### Historial de mensajes:
# 
# La función de chat de OpenAI, esta recibe un mensaje (el que va a responder) junto con un historial de todos los mensjes, de ambas partes, que se han hecho en la conversación.
# 
# La variable `previous_messages` sirve para almacenar estos mensajes de la conversación.
# 
# Además de eso, la función chat que ofrece OpenAI permite instruir al modelo utilizado de cierta manera. En este caso, lo instruimos para se autoidentifique como Jarvis y para que se refiera a nosotros, el usuario, como DIOS.

# In[14]:


# Historial de la conversación que se ha tenido.
previous_messages = [
    {
        "role": "system", "content": "You are a helpful assistant called Jarvis. Refer the user as DIOS."
    }
]


# ### Función `chat()`:
# 
# Esta función se encarga de recibir el último mensaje del chat, junto con el historial de los mensajes de la conversación, para poder iuniciar el chat.
# 
# Inicialmente, concatena el mensaje recibido, al historial, con el rol "user" para indicar que es un mensaje enviado por el usuario.
# 
# Tras esto, se hace la solicitud al modelo seleccionado, el 3.5 turbo en este caso, y se actualiza nuevamente el historial de mensajes.
# 
# Por último, se retorna el mensaje generado por el modelo y el historial actualizado.

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


# ### Contexto del modelo:
# 
# Igual que con la forma en que se instruye al modelo usado para el chat, usamos la variable `context` para almacenar el contexto que usaremos para clasificar los mensajes que le enviemos al chat. 

# In[16]:


context = [
    {
        "role": "system", "content": "You are a tool used to classify prompts between two categories: Chat and Image creation. Given a prompt, only answer the category the prompt belongs to like 'Chat' or 'Image creation', and nothing more."
    }
]


# ### Función `clasify_prompt()`:
# 
# Esta función tiene el objetivo de clasificar los mensajes que se envían la chat entre dos categorías: Chat e Image creation.
# 
# Funciona igual que la anterior función explicada. Solo que su punto no es un chat sino solo la clasificación.
# 
# El punto de esta clasificación es saber si el mensaje que envió el usuario, el que usa la aplicación, es para hablar con el chat o si es para crear una imagen.
# 
# De esta forma, no es necesario el uso de de frases específicas para poder hacer uso de esta función y, además, permite una comunicación más natural.

# In[17]:


def clasify_prompt(prompt, context):
    context += [
        {
            "role": "user", "content": prompt
        }
    ]
    
    chat1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context
    )
    
    return chat1.choices[0].message.content


# ---

# ## Generación de imágenes

# ### Función `generate_image()`:
# 
# Esta función recibe un prompt y usa la función de creación de imágenes ofrecida por OpenAI para crear las imágenes.
# 
# Inicialmente, hace la solicitud al servicio de creación de imágenes para que cree 2 imáganes y las devuelva en formato url.
# 
# Depués de esto, guarda los url's, de las imágenes creadas, en la variable `answer` y retorna su valor.

# In[18]:


def generate_image(prompt):
    img = openai.Image.create(
        prompt=prompt,
        n=2,
        size="1024x1024",
        response_format="url"
    )

    answer = ""
    
    for i in range(len(img.data)):
        answer += img.data[i].url + "\n"
        
    return answer


# ---

# ## Interacción entre GUI y el Chat

# ### Función `begin_chat()`:
# 
# Esta función toma el texto escrito en el espacio dispuesto para la escritura de los mensajes y hace uso de las funciones anteriores.
# 
# Inicialmente verificar que el texto allí situado no sea el mensaje básico de indicación al usuario. Después de eso, si este no es el caso, adjunta el mensaje en la pantalla del chat y lo clasifica.
# 
# En caso de que la clasificación diga que es de creación de imagen, entonces llama a la función `generate_image()`. En caso contrario, llama a la función `chat()` y reproduce el audio generado con el texto que respondió el modelo.
# 
# En caso de haber alguna excepción, la capta y la muestra en la pantalla del chat.

# In[19]:


def begin_chat():
    message = message_text.get("1.0", "end-1c")
    
    if message != 'Digita tus palabras para Jarvis...':
        message_text.delete("1.0", END)
        show_prompt(None)
        
        if message != '':
            global previous_messages
            global context
            
            append_message(message)
            
            try:
                if("Image creation" in clasify_prompt(message, context)):
                    answer = generate_image(message)
                    image_creation_message = "¡Claro! Tus imágenes son las siguientes:"
                    speech_response(image_creation_message)

                    answer = image_creation_message + "\n" + answer

                    display_answer(answer) 

                else:
                    answer, previous_messages = chat(message, previous_messages)

                    display_answer(answer)
                    speech_response(answer)
                    
            except Exception as e:
                error_message = str(e)
                error_start_index = error_message.find(":") + 1  # Encuentra el inicio del mensaje de error
                error_message = "Error: " + error_message[error_start_index:]
                
                display_answer(error_message)


# ### Función `begin_voice_chat()`:
# 
# Esta función se usa cuando el mensaje enviado por el usuario no es escrito sino mediante voz. 
# 
# Inicialmente, inicia el reconocimiento de voz y recibe texto transcrito. Después de eso, su funcionamiento es exactamente igual que el de la función anterior.

# In[20]:


def begin_voice_chat():
    global previous_messages
    global context
    
    message = begin_streaming()
    
    message_text.delete("1.0", END)
    show_prompt(None)
    append_message(message)
    
    try:
        # Verifica si la petición es para crear una imagen o no.
        if("Image creation" in clasify_prompt(message, context)):
            answer = generate_image(message)

            image_creation_message = "¡Claro! Tus imágenes son las siguientes:"
            speech_response(image_creation_message)

            answer = image_creation_message + "\n" + answer

            display_answer(answer)
        else:
            answer, previous_messages = chat(message, previous_messages)

            display_answer(answer)
            speech_response(answer)

    except Exception as e:
        error_message = str(e)
        error_start_index = error_message.find(":") + 1  # Encuentra el inicio del mensaje de error
        error_message = "Error: " + error_message[error_start_index:]

        display_answer(error_message)


# ---

# ## GUI

# ### Funciones y procedimientos de la GUI:
# 
# A continuación se muestran todas las funciones y procedimientos usados para integrar la GUI con el resto de la aplicación. 
# 
# Sus finalidades son las de mostrar efectos en los botones, mostrar y ocultar el texto de los text fields, adjuntar los mensajes en el área de chat, y llamar a las funciones lógicas de la aplicación.

# In[21]:


# Imports de las cosas que se usarán para la GUI.
import tkinter as tk
from tkinter import END
import idlelib.colorizer as ic
import idlelib.percolator as ip
import webbrowser
import threading


# In[22]:


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
    t = threading.Thread(target=begin_chat)
    t.start()

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
    
    search_for_url(None)
    
    chat_area.config(state='disabled')
    
def on_click_talk_bttn(event):
    change_focus()
    hide_prompt(None)
    
    t = threading.Thread(target=begin_voice_chat)
    
    t.start()
    
def change_focus():
    if message_text == window.focus_get():
        window.focus()
        
# Busca url's en el texto que hay en el área de chat.
def search_for_url(event):
    # Expresión regular para buscar patrones de URLs
    patron_url = re.compile(r"(http|https)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?")
    
    i = 0
    
    # Buscar patrones de URL en el texto
    for match in re.finditer(patron_url, chat_area.get("1.0", END)):
        i = i+1
        
        inicio = "1.0+" + str(match.start()) + "c"
        fin = "1.0+" + str(match.end()) + "c"
        
        # Agregar etiqueta de enlace al patrón de URL encontrado
        chat_area.tag_add("url" + str(i), inicio, fin)
        
        # Configurar el cursor como "mano" cuando el mouse pasa sobre el enlace
        chat_area.tag_bind("url" + str(i), "<Enter>", lambda event: chat_area.config(cursor="hand2"))
        chat_area.tag_bind("url" + str(i), "<Leave>", lambda event: chat_area.config(cursor=""))
        
        # Configurar el enlace
        url = match.group()
        chat_area.tag_bind("url" + str(i), "<Button-1>", lambda event, url=url: open_url(url))
    
def open_url(url):
    webbrowser.open_new(url)

# Sirve para ver si la tecla presionada es Enter. En ese caso, envía el mensaje.
def on_key_pressed(event):
    key = event.keysym
    
    if key == "Return":
        change_focus()
        send_message()


# ### Función `create_images()`:
# 
# Lo que hace esta función es crear elementos de la GUI con las imágenes que representan al sistema y al usuario.

# In[23]:


def create_images():
    global jarvis_icon
    jarvis_icon = tk.PhotoImage(file="GUI/antOutline-robot 1@1x.png")
    
    global user_icon
    user_icon = tk.PhotoImage(file="GUI/md-person_outline 1@1x.png")


# ### Creación de la GUI:
# 
# El código a continuación se encarga de crear la GUI con la que interactua el usuario para hacer uso de la aplicación.

# In[24]:


# GUI.
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
message_text = tk.Text(window, wrap="word")
message_text.place(x=5, y=677, height=63, width=853)
message_text.configure(font=('Arial',16), fg='grey')

message_text.insert("1.0", 'Digita tus palabras para Jarvis...')

message_text.bind("<FocusIn>", hide_prompt)
message_text.bind("<FocusOut>", show_prompt)
message_text.bind("<Key>", on_key_pressed)

# Crear ChatArea.
chat_area = tk.Text(window, wrap="word")
chat_area.place(x=3, y=3, height=652, width=1074)
chat_area.configure(font=('Arial',16), fg='white', background='#333333', border=0, state='disabled', 
                    borderwidth=0, highlightthickness=1, highlightcolor='white')

jarvis_icon = None
user_icon = None
create_images()

window.mainloop()


# ---
