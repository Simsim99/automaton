FROM python:3.13-bookworm
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
# Copy the src folder from your computer into a src folder inside the Docker image.
# in this image: /app/src/what gets copied from host's src sits here
COPY src ./src 
EXPOSE 8000
WORKDIR /app/src 
CMD ["gunicorn", "app:create_app()"]
