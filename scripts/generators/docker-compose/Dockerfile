FROM python:3.13-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY createComposeFile.py .

COPY docker-compose.j2 .

RUN chown -R appuser:appgroup /app && chmod +x createComposeFile.py
USER appuser

# Define the default entrypoint to run the script
ENTRYPOINT ["python", "createComposeFile.py", "--template", "/app/docker-compose.j2"]
