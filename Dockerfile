FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Install the package
RUN uv pip install --no-deps .

# Create non-root user
RUN useradd --create-home --shell /bin/bash climber
USER climber

# Set up config directory
RUN mkdir -p /home/climber/.config/climber

# Default command
ENTRYPOINT ["uv", "run", "climber"]
CMD ["--help"]