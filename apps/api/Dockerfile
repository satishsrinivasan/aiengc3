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
COPY apps/api ./apps/api

ENV UV_COMPILE_BYTECODE=1

#Install dependencies including workspace packages
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --package api

#Enable bytecode compilation and Python optimisation
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

#Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/apps/api/src:$PYTHONPATH"

#Create non-root user and set permissions
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

#Switch to non-root user
USER app

#Expose the FastAPI port
EXPOSE 8000

WORKDIR /app/apps/api/src

#Run the application
ENTRYPOINT ["uvicorn", "api.app:app"]
CMD ["--host", "0.0.0.0", "--port", "8000", "--reload"]