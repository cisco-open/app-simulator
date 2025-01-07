FROM python:3.13-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY createManifests.py .

COPY templates ./templates
COPY deployments ./deployments

RUN chown -R appuser:appgroup /app && chmod +x createManifests.py
USER appuser

VOLUME [ "/app/deployments" ]

# Define the default entrypoint to run the script
ENTRYPOINT ["python", "createManifests.py"]
