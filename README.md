# Smart Audio (Simulador de Voz do Porteiro Eletrônico)

## Requisitos
- Python 3.11+
- Docker e Docker Compose

## Instruções

1. Suba o MySQL:
    ```bash
    docker-compose up -d
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Rode o sistema:
    ```bash
    python main.py
    ```

Os áudios capturados serão armazenados na pasta `audio/`.
