FROM python:3.13-slim

# Install required dependencies including build tools
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    g++ \
    make \
    python3-dev \
    pkg-config \
    libssl-dev \
    openssl \
    libprotobuf-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Add target for cross-compilation
RUN rustup target add aarch64-unknown-linux-gnu

# Install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# Set up your project
WORKDIR /app

# Copy project files
COPY . .

# Set environment variables for OpenSSL
ENV OPENSSL_DIR=/usr
ENV OPENSSL_INCLUDE_DIR=/usr/include
ENV OPENSSL_LIB_DIR=/usr/lib/aarch64-linux-gnu
ENV OPENSSL_STATIC=1
ENV PDM_BUILD_SCM_VERSION=2.0.2

# Create symlink for OpenSSL libs if needed
RUN ln -s /usr/lib/aarch64-linux-gnu /usr/lib/x86_64-linux-gnu || true

# Install dependencies using PDM with --no-self option
RUN pdm install --no-self
RUN eval $(pdm venv activate)

# Use ENTRYPOINT and CMD in array syntax
ENTRYPOINT ["pdm", "run", "neurons/validator.py"]
CMD ["--netuid", "242", "--subtensor.network", "test", "--wallet.name", "validator", "--wallet.hotkey", "default", "--logging.debug"]