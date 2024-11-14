# Proyecto de Procesamiento de Texto con Spark NLP

Este proyecto utiliza Spark NLP para procesar y analizar texto. A continuación, se describe la estructura y contenido del proyecto.

## Estructura del Proyecto

El proyecto se divide en los siguientes directorios y archivos:

* `app`: Contiene la aplicacion streamlit y el código principal del proyecto.
* `/app/requirements.txt`: Contiene las dependencias necesarias para ejecutar la aplicacion en un container de docker.
* `/app/models`: Contiene los modelos entrenados en Spark, CountVectorizer, IDF, LDA, LogisticRegression, DecisionTree.
* `config`: Contiene archivos de configuración para EMR.
* `sparknlp-complaints`: Contiene un notebook de Jupyter que contiene el analisis y la creacion de funciones para la aplicacion, muestra y describe el uso de pipelines de Spark NLP para procesar texto.
* `Dockerfile`: Para la generacion alternativa del contenedor con el repositorio previamente clonado.

## Contenido del Proyecto

El proyecto incluye los siguientes componentes:

* **CountVectorizer**: Un modelo que convierte una colección de textos en una matriz de frecuencias de tokens. Esto permite representar el texto en función de la cantidad de veces que aparece cada token en el corpus.
* **IDF**:  Un modelo que ajusta la frecuencia de los tokens en función de su aparición en múltiples documentos. Ayuda a reducir la importancia de palabras comunes en el corpus.
* **LDA**: Un modelo de análisis de tópicos que organiza un corpus de documentos en grupos o tópicos basados en las frecuencias de los tokens, identificando temas subyacentes.
* **LogisticRegression**: Un modelo de clasificación supervisado utilizado para predecir categorías. En procesamiento de texto, se emplea junto a otras técnicas para clasificar documentos en función de su contenido.
* **DecisionTreeClassifier**: Un modelo de clasificación supervisado que utiliza un árbol de decisiones para segmentar los datos. Es útil para clasificar textos en categorías basándose en reglas derivadas del contenido.
* **Notebook de Jupyter**: Un notebook de demostración que muestra cómo utilizar Spark NLP para procesar y analizar texto de forma interactiva en un entorno de Jupyter.

## Requisitos

### Software

Para ejecutar el proyecto, se requieren las siguientes aplicaciones:

* Docker

Para ejecutar los notebooks en un entorno diferente como Amazon EMR o Ubuntu, se deben tener las siguientes dependencias y paquetes:

* Spark 3.3.1
* Spark NLP 5.5.0
* Python 3.8
* Java 8 o 11
* JupyerHub o Notebook interactivo
* MlFlow


### Hardware

#### Aplicacion
##### Windows o Ubuntu
* Procesador = 4 cores min
* Ram = 8gb.
* Espacio en disco = 3gb

#### Notebook

##### EMR
* Cluster MX5.large con 1 ejecutor y 1 core.
##### Ubuntu
* Procesador = 4 cores min
* Ram = 16gb (recomendado 32gb).
* Espacio en disco = 5gb

## Instalación

### Instalar aplicacion con Docker (Cualquier SO)

* Ejecuta el siguiente comando para hacer pull de la imagen docker que contiene la aplicacion:
```bash
docker pull sebasr0/complaints-spark-app:latest
```

## Ejecución

1. Ejecuta el siguiente comando para abrir el puerto requerido por la aplicacion de streamlit y ejecutar la aplicacion:
```bash
docker run -p 8501:8501 sebasr0/complaints-spark-app:latest
```

2. Acceder a la direccion http://localhost:8501/ en el navegador para desplegar la aplicacion (La inicializacion toma varios segundos puesto que descarga la libreria SparkNLP al iniciar la sesion de Spark).

![Aplicacion][app]

### Proceso para EMR 6.14.0

1. Crear un cluster en Amazon EMR con la version 6.14.0 con las aplicaciones Livy, Hadoop, Spark, JupyterEnterpriseGateway.

![Aplicaciones necesarias][def]

2. Para configurar el cluster correctamente, es necesario especificar boostrap actions y software settings tal y como se contienen en los archivos `/config/configemr.json` y `/config/sparknlp.sh` respectivamente, deben estar cargados en un bucket de s3 previamente.

Las configuraciones de software permiten instalar la version de Java 11, configurar la libreria SparkNLP al iniciar una sesion de Spark para el cluster, y los nodos correspondientes, compatible con la libreria SparkNLP.

![Software Settings][soft]

El script de Boostrapactions genera los permisos necesarios de la libreria SparkNLP y descarga otras librerias necesarias para el procesamiento de lenguaje.

![Boostrap Actions][boot]

3. Una vez iniciado el cluster, crear o acceder a un WorkSpace de EMR Studio, luego enlazar el cluster en la sesion del WorkSpace.  

![EMR Studio][note]

4. Carga el archivo a la sesion interactiva que se acaba de iniciar y ejecuta las celdas.

![Sesion Interactiva][int]

## Uso

El proyecto puede ser utilizado para procesar y analizar texto utilizando Spark NLP. El notebook de Jupyter proporciona un ejemplo de cómo utilizar el proyecto para procesar texto.

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir, crea un fork del proyecto y envía un pull request con tus cambios.

## Licencia

El proyecto está licenciado bajo la licencia MIT.

## Contacto

Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarme en [tu correo electrónico o en tu perfil de GitHub].


[def]: /img/cluster.png
[soft]: /img/softwaresettings.png
[boot]: /img/boostrap.png
[note]: /img/notebook.png
[int]: /img/int.png
[app]: /img/app.png