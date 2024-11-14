# Proyecto de Procesamiento de Texto con Spark NLP

Este proyecto utiliza Spark NLP para procesar y analizar texto. A continuación, se describe la estructura y contenido del proyecto.

## Estructura del Proyecto

El proyecto se divide en los siguientes directorios y archivos:

* `app`: Contiene el código principal del proyecto, incluyendo la aplicación Spark.
* `config`: Contiene archivos de configuración, como el archivo `sparknlp.sh` que configura el entorno de Spark NLP.
* `models`: Contiene los modelos entrenados, como el modelo de CountVectorizer.
* `sparknlp-complaints`: Contiene un notebook de Jupyter que demuestra el uso de Spark NLP para procesar texto.
* `requirements.txt`: Contiene las dependencias necesarias para ejecutar el proyecto.

## Contenido del Proyecto

El proyecto incluye los siguientes componentes:

* **CountVectorizer**: Un modelo que convierte una colección de textos en una matriz de frecuencias de tokens.
* **Spark NLP**: Una biblioteca que proporciona funcionalidades para procesar y analizar texto en Spark.
* **Notebook de Jupyter**: Un notebook que demuestra el uso de Spark NLP para procesar texto.

## Requisitos

Para ejecutar el proyecto, se requieren las siguientes dependencias:

* Spark 3.1.2
* Spark NLP 3.4.4
* Python 3.8
* Java 8

## Instalación

Para instalar las dependencias, ejecuta el siguiente comando:
```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el proyecto, ejecuta el siguiente comando:
```bash
spark-submit app/main.py
```

## Uso

El proyecto puede ser utilizado para procesar y analizar texto utilizando Spark NLP. El notebook de Jupyter proporciona un ejemplo de cómo utilizar el proyecto para procesar texto.

## Modelo de CountVectorizer

El modelo de CountVectorizer se encuentra en el directorio `models`. Puede ser cargado utilizando el siguiente código:
```python
cv_model = sparknlp.load("models/count_vectorizer_model")
```

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir, crea un fork del proyecto y envía un pull request con tus cambios.

## Licencia

El proyecto está licenciado bajo la licencia MIT.

## Contacto

Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarme en [tu correo electrónico o en tu perfil de GitHub].
