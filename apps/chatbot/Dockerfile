# Specify base image
# Specify base directory in the container (/app)
# Copy project files, then source code to image
# Get dependencies by running uv, for production use
# Include venv in PATH and application in PYTHONPATH
# Create an application user with the right permissions to run the application
# Switch to the application user, and
# Run uvicorn
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy workspace root files for dependency resolution
COPY pyproject.toml uv.lock ./

#Copy package files and sources
COPY apps/chatbot ./apps/chatbot

ENV UV_COMPILE_BYTECODE=1

#Install dependencies including workspace packages
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --package chatbot

#Enable bytecode compilation and Python optimisation
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

#Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/apps/chatbot/src:$PYTHONPATH"

# Create non-root user and set permissions
RUN addgroup --system app && \
    adduser  --system --ingroup app app && \
    chown -R app:app /app && \
    mkdir -p /home/app && \
    mkdir -p /home/app/.streamlit && \
    mkdir -p /home/app/.streamlit/data && \
    mkdir -p /home/app/.streamlit/cache && \
    chown -R app:app /home/app/.streamlit && \
    mkdir -p /home/app/.cache && \
    mkdir -p /home/app/.cache/uv && \
    chown -R app:app /home/app/.cache

ENV HOME=/home/app

#Switch to non-root user
USER app

#Expose the Streamlit port
EXPOSE 8501

WORKDIR /app/apps/chatbot/src

#Run the application
CMD ["uv", "run", "streamlit", "run", "chatbot/app.py", "--server.address=0.0.0.0"]