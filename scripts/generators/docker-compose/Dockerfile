#checkov:skip=CKV_DOCKER_2:This is a run once container
FROM python:3.13-alpine@sha256:b6f01a01e34091438a29b6dda4664199e34731fb2581ebb6fe255a2ebf441099

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY createComposeFile.py .

COPY docker-compose.j2 .

RUN chown -R appuser:appgroup /app && chmod +x createComposeFile.py
USER appuser

# Define the default entrypoint to run the script
ENTRYPOINT ["python", "createComposeFile.py", "--template", "docker-compose.j2"]
