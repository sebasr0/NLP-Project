#!/bin/bash
set -x -e

echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

# Actualizar el sistema y paquetes esenciales
sudo yum update -y
sudo yum install -y python3-devel gcc

# Install the s3fs dependency for EMR Notebooks magics 
sudo amazon-linux-extras install epel -y
sudo yum install s3fs-fuse -y

# Actualizar pip para Python 3
sudo python3 -m pip install --upgrade pip

# Instalar paquetes necesarios
sudo python3 -m pip install numpy
#SEBAS PK PUTAS LA KITASTE :(
sudo python3 -m pip install spark-nlp
sudo python3 -m pip install nltk
#sudo python3 -m pip install spacy
sudo python3 -m pip install matplotlib
sudo python3 -m pip install --upgrade python-dateutil

# Instalar Spark NLP (si es necesario)
# sudo python3 -m pip install spark-nlp

# Crear directorio de datos de NLTK
sudo mkdir -p /usr/local/share/nltk_data

# Descargar los corpora necesarios de NLTK
sudo python3 -m nltk.downloader -d /usr/local/share/nltk_data wordnet
sudo python3 -m nltk.downloader -d /usr/local/share/nltk_data omw-1.4

# Ajustar permisos para nltk_data
sudo chmod -R 755 /usr/local/share/nltk_data

# Descargar el modelo 'en_core_web_sm' de spaCy
#sudo python3 -m spacy download en_core_web_sm

# Ajustar permisos para site-packages (opcional y con precaución)
sudo chmod -R a+rw /usr/local/lib/python3.*/site-packages

set +x
exit 0

# ----- DESPUES DE INCIAR EL CLUSTER, EJECUTAR LOS PERMISOS DE LIVY PARA ESCRITURA DESDE SSH ------,

# sudo usermod -a -G hdfsadmingroup livy

# ------ PARA QUE LOS CAMBIOS SURTAN EFECTO REINICIAR EL KERNEL DE PYSPARK DESDE EL NOTEBOOK:-------,

