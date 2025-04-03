# gunicorn.conf.py
bind = "0.0.0.0:$PORT"  # Will use the PORT environment variable provided by Render
workers = 2
timeout = 180  # Increased timeout for video processing
preload_app = True 