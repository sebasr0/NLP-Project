# Proyecto de Procesamiento de Texto de quejas bancarias con Spark NLP

Este proyecto utiliza Spark NLP para el procesamiento y análisis de texto de quejas bancarias. A continuación, se describe la estructura y los componentes del proyecto.

---

## Estructura del Proyecto

El proyecto se organiza en los siguientes directorios y archivos:

- **`/app`**: Contiene la aplicación en Streamlit y el código principal.
  - **`requirements.txt`**: Dependencias necesarias para ejecutar la aplicación en un contenedor Docker.
  - **`models`**: Modelos entrenados, incluyendo CountVectorizer, IDF, LDA, LogisticRegression y DecisionTree.
  - **`Dockerfile`**: Configuración para generar el contenedor a partir del repositorio clonado.
- **`/config/`**: Archivos de configuración para EMR.
- **`/sparknlp-complaints`**: Notebooks de Jupyter que contienen análisis, creación de funciones, y pipelines de Spark NLP. Incluye el uso de MlFlow para el seguimiento de modelos.
  - **`mlruns`**: Registro de experimentos y modelos en MlFlow.

---

## Componentes del Proyecto

1. **CountVectorizer**: Representa textos en una matriz de frecuencias de tokens.
2. **IDF**: Ajusta la frecuencia de tokens, reduciendo la importancia de palabras comunes.
3. **LDA**: Agrupa documentos en tópicos basados en la frecuencia de tokens.
4. **Logistic Regression**: Clasificación supervisada para predecir categorías de texto.
5. **DecisionTreeClassifier**: Clasificación mediante árbol de decisiones basado en contenido.
6. **Notebook de Jupyter**: Ejemplo interactivo del uso de Spark NLP.

---

## Resultados

### Asignación de Etiquetas

#### Modelos de Tópicos (LDA)

- **Tema 0: Hipotecas y Bienes Raíces**  
  - Términos predominantes: `['loan', 'mortgage', 'home', 'modification', 'property', 'payment']`
  - Categoría: "Préstamos Hipotecarios y Propiedades"

- **Tema 1: Operaciones Bancarias y Transacciones**  
  - Términos predominantes: `['check', 'deposit', 'fund', 'account', 'branch', 'bank']`
  - Categoría: "Operaciones Bancarias y Sucursales"

- **Tema 2: Informes de Crédito y Disputas**  
  - Términos predominantes: `['report', 'credit', 'inquiry', 'dispute', 'consumer']`
  - Categoría: "Reportes de Crédito y Protección del Consumidor"

- **Tema 3: Tarjetas de Crédito y Cargos de Intereses**  
  - Términos predominantes: `['payment', 'fee', 'balance', 'card', 'account']`
  - Categoría: "Tarjetas de Crédito y Cargos Financieros"

- **Tema 4: Fraude y Disputas de Transacciones**  
  - Términos predominantes: `['charge', 'fraud', 'transaction', 'claim', 'card']`
  - Categoría: "Fraude y Disputas de Transacciones"

---

### Predicción de Etiquetas

Se utilizaron los siguientes modelos para la prediccion de nuevas etiquetas.

- **Logistic Regression**
  - Test Set Accuracy = 0.799
  - Test Set F1 Score = 0.799

- **Decision Tree**
  - Test Set Accuracy = 0.539
  - Test Set F1 Score = 0.538

El modelo de **Logistic Regression** fue seleccionado para la aplicación.

---

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

### Instalar aplicacion con Docker (Cualquier SO o instancia EC2)

* Ejecuta el siguiente comando para hacer pull de la imagen docker que contiene la aplicacion:
```bash
docker pull sebasr0/complaints-spark-app:latest
```
#### Instalar Docker en EC2

Si su instancia de Aazon Linux 2 no tiene docker instalado, puede instalarlo siguiendo estos comandos en orden:

```bash
sudo yum update -y
```
```bash
sudo amazon-linux-extras install docker -y
```
```bash
sudo service docker start
```
```bash
sudo usermod -aG docker ec2-user
```
```bash
newgrp docker
```
## Ejecución

1. Ejecuta el siguiente comando para abrir el puerto requerido por la aplicacion de streamlit y ejecutar la aplicacion:
```bash
docker run -p 8501:8501 sebasr0/complaints-spark-app:latest
```

2. Acceder a la direccion http://localhost:8501/ en el navegador para desplegar la aplicacion (La inicializacion toma varios segundos puesto que descarga la libreria SparkNLP al iniciar la sesion de Spark).

![Aplicacion][app]

Nota: Si se ejecuta desde una instancia EC2 con Amazon Linux 2, asegurarse de configurar los puertos de entrada del grupo de seguridad de la instacia 
para que coincidan con los del puerto de la app (8501) y que la instancia tenga accseso a internet.

### Proceso para ejecutar el notebook de analisis en Amazon EMR 6.14.0

1. Crear un cluster en Amazon EMR con la version 6.14.0 con las aplicaciones Livy, Hadoop, Spark, JupyterEnterpriseGateway.

![Aplicaciones necesarias][def]

2. Para configurar el cluster correctamente, es necesario especificar boostrap actions y software settings tal y como se contienen en los archivos `/config/configemr.json` y `/config/sparknlp.sh` respectivamente, deben estar cargados en un bucket de s3 previamente.

Las configuraciones de software permiten instalar la version de Java 11 en todas las aplicaciones de los nodos, esta version es compatible con SparkNLP, adicionalmente configura la libreria SparkNLP al iniciar una sesion de Spark para el cluster, y los nodos correspondientes.

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




