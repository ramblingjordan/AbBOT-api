FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set working directory
WORKDIR /workspace/project

# Download model weights
COPY ./download_weights.py ./
RUN python download_weights.py

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

# Move into app working directory and copy in files
WORKDIR /workspace/project/api
COPY ./api /workspace/project/api

# Port to serve inference engine on
EXPOSE 5000

CMD ["python", "api.py"]