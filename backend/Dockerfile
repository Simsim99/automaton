FROM python:3.13-bookworm AS builder
WORKDIR /app
RUN python -m venv /opt/venv

# Tell the container to look for commands (python, pip, gunicorn)
# inside our venv first. This does not change the host's PATH.
# Prepend the venv's bin directory to the container's existing PATH (not the host's PATH).
# This makes commands like python, pip, and gunicorn use the venv's executables first.
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
# Installs Flask, Gunicorn, and their dependencies into that virtual environment.
RUN pip install -r requirements.txt

# purpose of the whole split: the builder's gcc, apt cache, pip cache, and headers stay behind. 
FROM python:3.13-slim-bookworm
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# useradd -r: creates a system account( used by sevices/apps instaed of humans)
# -u 1000: give it id number 1000
# notes is the username
RUN useradd -r -u 1000 notes
# Copy the src folder from your computer into a src folder inside the Docker image.
# in this image: /app/src/what gets copied from host's src sits here
WORKDIR /app/src 
COPY src/ .
#  run the application as the notes user we ceated above - all lines above this needed root
USER notes
EXPOSE 8000
CMD ["gunicorn", "app:create_app()"]
