FROM python:3.6

WORKDIR /app
COPY . .
RUN chmod +x /app/entrypoint.sh
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["/app/entrypoint.sh"]