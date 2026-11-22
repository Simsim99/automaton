FROM python:3.13-bookworm AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

# urpose of the whole split: the builder's gcc, apt cache, pip cache, and headers stay behind. 
FROM python:3.13-slim-bookworm
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Copy the src folder from your computer into a src folder inside the Docker image.
# in this image: /app/src/what gets copied from host's src sits here
WORKDIR /app/src 
COPY src/ . 
EXPOSE 8000
CMD ["gunicorn", "app:create_app()"]
