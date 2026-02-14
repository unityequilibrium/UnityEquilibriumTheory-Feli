# Build Stage
# Build Stage
FROM rust:slim-bookworm as builder

WORKDIR /app

# Install build dependencies (if needed, e.g. for rusqlite bundled or lancedb)
RUN apt-get update && apt-get install -y pkg-config libssl-dev protobuf-compiler

# Copy Cargo workspace files
COPY Cargo.toml Cargo.lock ./
COPY uet_core ./uet_core
COPY uet_kb ./uet_kb

# Build the release binary
# We target the specific binary to avoid building everything if not needed
RUN cargo build --release -p uet_kb

# Runtime Stage
FROM debian:bookworm-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/target/release/uet_kb /usr/local/bin/uet_kb

# Copy any necessary assets (like config or scripts)
# COPY config.toml . 

# Environment variables
ENV RUST_LOG=info

# Expose port (if we add server later, e.g. 3000)
# EXPOSE 3000

# Default command
CMD ["uet_kb", "--help"]
