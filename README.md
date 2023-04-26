# Presentación del proyecto

### Integrantes:
- Yuluka Gigante Muriel
- Dennis Masso Macías

---
# Tabla de contenidos
1. [Información general sobre ChatGPT](#chatgpt)
2. [Acerca del proyecto](#acerca-del-proyecto)
3. [Recursos empleados](#recursos-empleados-en-la-construcción-del-proyecto)
4. [Crisp-DM](#crisp-dm)
	1. [Entendimiento del negocio](#entendimiento-del-negocio)
5. [Smart Questions](#smart-questions)
---

# ChatGPT
ChatGPT es un modelo de lenguaje artificial diseñado para procesar y generar texto en múltiples idiomas y tareas, entrenado por OpenAI utilizando una red neuronal de última generación llamada GPT-3.5.
Es capaz de cosas tales como realizar tareas como responder preguntas, traducir texto, resumir documentos y generar contenido creativo, generar código en distintos lenguajes, entre otros.

# Acerca del proyecto
La idea del proyecto es la de crear un asistente virtual, manejado por voz, con capacidades más avanzadas que las que tiene cualquier otro asistente de este estilo. 
Se busca poder interactuar con ChatGPT por medio de la voz y que, a su vez, este responda por el mismo medio. 
A este nuevo asistente lo hemos llamado Jarvis, basándonos en la IA creada por Tony Stark en los comics. 

# Recursos empleados en la construcción del proyecto
Para el desarrollo de Jarvis hemos usado la API de OpenAI, que permite hacer uso de distintos modelos para  funciones de chat, predicción de texto, generación de imágenes, edición de imágenes, etc. 
Además de eso, para la interacción por voz hemos usado la API de Google Cloud Speech-to-text, que permite la transcripción de audio en transmisión continua,  audios cortos, y audios largos, tanto en la nube como de manera local. 

# CRISP-DM
1. ## Entendimiento del negocio
	 1. Determinar los objetivos del negocio.
		 1. Background.
			OpenAI es una compañía de investigación de inteligencia artificial, que busca lograr la creación de IA beneficiosa para la humanidad.

			Bajo este contexto, ha desarrollado un chatbot, llamado ChatGPT, usando el modelo Generative Pre-trained Transformer 3.5 (GPT 3.5), que tiene la capacidad de mantener conversaciones, en lenguaje natural, complejas y sumamente similares a las que se podrían tener con un humano. Además, ChatGPT es capaz de responder una gran variedad de preguntas específicas.

			Por esta razón, pensamos que la implementación de una interfaz por voz, en la que se le hable de manera verbal, y este responde de igual forma, podría ser de suma utilidad. En suma a eso, la utilización de la API de OpenAI, que es la manera que hemos encontrado para llegar a tal objetivo, permite la inclusión de funcionalidades como la generación de imágenes dada una descripción, la modificación de imágenes ya existentes dadas una imagen inicial y una descripción, la búsqueda de artículos en la web, entre otros, desde una misma plataforma y de manera más cómoda (punto falente de ChatGPT).
			
		2. Business objectives.
			Como ya se mencionó previamente, buscamos la implementación de una interfaz por voz para ChatGPT, en donde las consultas se le hagan mediante el habla, y sus respuestas sean, de igual forma, verbales.

			Además de eso, también queremos integrar ciertas funcionalidades, como la generación de imágenes, que no se encuentran en ChatGPT.
			
		3. Business success criterio.
			Consideramos que el proyecto podrá llamarse “exitoso” cuando podamos usarlo como un asistente similar a Jarvis, de donde viene su nombre, en nuestra vida personal.
			
	 2. Evaluar la situación.
		 1. Inventario de recursos.
			 Los recursos con los que contamos son:
			 
			 - Una API proporcionada por OpenAI que permite el uso de varios modelos, entre las 3.5 y 3.5 turbo de GPT.
			 - Varias API de reconocimiento de voz, pero la que usaremos es la de Google cloud speech-to-text.
			 - Documentaciones completas de ambas APIs.
			 - Conocimientos acerca del uso de Python para implementaciones que incluyen IA.
			 - Apoyo de profesionales en el tema (profesores de la materia).
			 - Jupyter notebook como entorno de desarrollo.

		2. Requerimientos, suposiciones y restricciones.

			Los requerimientos que tenemos en nuestro proyecto son:
			
			- Se requiere poder hacer consultas a ChatGPT mediante la voz sin estar en su página.
			- Se requiere recibir las respuestas de ChatGPT mediante voz.
			- Se requiere poder convertir la voz a texto mediante el uso de la API de Google Cloud speech-to-text.
			- Se requiere usar la API de OpenAI para usar el texto generado en el ítem anterior como consulta.
			- Se requiere usar alguna API para convertir las respuestas que proporcione el modelo en voz.
			- Se requiere crear una interfaz gráfica no muy compleja en la que se pueda: revisar el historial de la conversación, y ver las imágenes generadas.

			Las suposiciones son:
			
			- Suponemos que las documentaciones de las API a usar están disponibles y son correctas.
			- Suponemos que las documentaciones nos proporcionarán una buena, y útil, explicación de cómo usar las APIs.

			Las restricciones son:
			- No podemos hacer una aplicación extremadamente compleja debido a la disponibilidad temporal.
			- No podemos hacer una aplicación preparada para un despliegue muy amplio debido a la disponibilidad temporal y de recursos.

		3. Riesgos y contingencias.
			Realmente, el mayor riesgo presente en el proyecto es que las APIs que usaremos dejen de estar disponibles al público y no podamos acceder a estas.

			Otro posible riesgo es encontrarnos con algún obstáculo demasiado complejo para nuestro nivel actual.

			En el primer caso, tenemos pensado buscar APIs alternativas que cumplan la misma función.

			En el segundo caso, tenemos pensado recurrir a los profesionales con los que contamos para que estos nos ayuden.

		4. Terminología.
			No hay una terminología específica que debamos entender, para poder realizar el proyecto, aparte de la normalmente usada en los ámbitos de desarrollo de software y por los mismos desarrolladores.
			
		5. Costos y beneficios.
			En cuanto al costo del proyecto, tenemos una ventana medianamente limitada para poder hacerlo sin incurrir en ningún gasto económico, dadas las restricciones del uso gratuito de las APIs.

			El costo más grande, en realidad, es el tiempo, pues nos enfrentamos a un tipo de problemas que jamás habíamos tratado, como lo es el uso de APIs e integración de distintos programas y lenguajes de programación.

			Por otro lado, a priori, no esperamos tener beneficios económicos derivados del proyecto. Sin embargo, consideramos que el hecho de contar con un asistente virtual, que sea tan avanzado como lo es ChatGPT, es el mayor de los beneficios.

	 3. Determinar los objetivos de la analítica.
		 1. Data mining goals.
			 Puesto que nuestro proyecto no necesita un database, este punto no aplica.
			 
		 2. Data mining success criteria. 
			 Como ya lo mencionamos, consideramos que el proyecto será exitoso en la medida en que podamos usarlo como asistente virtual en nuestro día a día.
			 
	 4. Hacer plan del proyecto.
		 1. Plan del proyecto.
			 - **Etapa 1:** Búsqueda de APIs necesarias. Esta etapa consiste en la búsqueda de las APIs que servirán para cumplir los requerimientos del proyecto. Por ahora, hemos determinado que usaremos la API de OpenAI y la de Google Cloud speech-to-text.
			 - **Etapa 2:** Estudio de las APIs. Una vez determinadas las APIs que usaremos, debemos hacer un estudio concienzudo de estas, haciendo uso de sus documentaciones disponibles. De esta manera sabremos cómo funcionan y cómo podremos usarlas en nuestro proyecto.
			 - **Etapa 3:** Práctica. Ya sabiendo de qué manera podemos interactuar con las APIs, consideramos pertinente practicar y “jugar” con estas.
			 - **Etapa 4:** Implementación. Después de haber interactuado lo suficiente con las APIs, será necesario iniciar la implementación del proyecto usándolas.
			 - **Etapa 5:** Validación y mejora. Esta es una etapa sombrilla, ya que, teniendo las implementaciones que hemos hecho, debemos validar la calidad de las respuestas y del software en general para así, poder mejorar las falencias y fallas que tenga.
			 - **Etapa 6:** Despliegue. Por último, teniendo una implementación suficientemente buena, procederemos al despliegue del software que, en principio, será para nuestro uso propio.

		 2. Evaluación inicial de las herramientas técnicas. 
			 - Búsqueda de APIs: El propio ChatGPT puede servirnos para encontrar recomendaciones de APIs que cumplan con las características que precisamos.
			 - Estudio de las APIs: Las documentaciones y sitios oficiales de las APIs a usar nos proporcionan todo el conocimiento necesario para el entendimiento de estas.
			 - Práctica e Implementación: Podemos hacer uso de Python para la implementación de algunos ejemplos de uso sencillos, y de la versión final. 
				Además, podemos usar otros lenguajes como FXML, CSS, o Java, para la implementación de las otras partes del proyecto tales como la interfaz gráfica.

# Smart Questions
Las Smart Questions planteadas son las siguientes:

- ¿Cuál es la diferencia entre nuestro producto y los asistentes virtuales convencionales de la última década?
- ¿Cómo podría nuestro producto aportar más valor a los asistentes virtuales?