# Listen on all network interfaces inside the container.
# This allows Gunicorn to accept connections coming through Docker's network.
# Without 0.0.0.0, Gunicorn would only listen on the container's own localhost (127.0.0.1),
# and Docker's port forwarding (8000:8000) would not be able to reach it.
bind = ["0.0.0.0:8000"]
workers = 2
accesslog = "-"
errorlog = "-"
timeout = 30
