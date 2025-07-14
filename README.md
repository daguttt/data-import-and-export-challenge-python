# Python Data Import and Export Challenge

## Local Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.13
- `uv` (Package Manager for Python written in Rust)
    - You can install it [here](https://docs.astral.sh/uv/getting-started/installation/).

### Unix-based OS Usage

The project uses a [`Makefile`](https://makefiletutorial.com/) to ease the execution of the commands.

> [!NOTE]
> The Makefile is not cross-platform compatible. If you are using Windows, you can follow the instructions [below](#windows-usage).

```bash
make setup
make start
```

### Windows Usage

1. Create virtual environment and install dependencies
    ```bash
    uv sync
    ```

2. Generate sample data
    ```bash
    uv run scripts/generate_sample_data.py
    ```

3. Setup environment variables, start the Database container, and run the main script to import and export the customers data.
    ```bash
    copy .env.example .env
    docker compose up -d
    uv run main.py
    ```