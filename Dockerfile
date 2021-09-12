FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set working directory
WORKDIR /workspace/project

# Install requirements
RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# Download model weights
COPY ./download_weights.py ./
RUN python3 download_weights.py

# Copy code over
COPY ./api ./
COPY ./data ./
COPY ./helpers ./
COPY ./main.py ./

# Port to serve inference engine on
# Expose port 5000 or whatever is set in API_PORT environment variable
ENV API_PORT=5000
EXPOSE ${API_PORT}

CMD ["python3", "main.py"]