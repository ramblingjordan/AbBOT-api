FROM python:3

# Set working directory
WORKDIR /workspace/project

# Install requirements
RUN pip install --no-cache-dir pipenv
COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

# Download model weights
COPY download_weights.py ./download_weights.py
RUN python3 download_weights.py

# Copy code over
COPY api/ ./api/
COPY data/ ./data/
COPY helpers/ ./helpers/
COPY main.py ./main.py

# Exposes the specified port, or 5000, to Docker.
ENV API_PORT=5000
EXPOSE ${API_PORT}

CMD ["python3", "main.py"]
