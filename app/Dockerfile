# Use a Spark image with Python and Java pre-installed
FROM bitnami/spark:3.3.1

# Set the working directory
WORKDIR /app

# Install Python dependencies including Streamlit
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code and models directory
COPY . /app
COPY models /app/models 

# Expose Streamlit port
EXPOSE 8501

# Set environment variable for PySpark
ENV PYSPARK_PYTHON=python3

# Run the Streamlit application
CMD ["python3", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
