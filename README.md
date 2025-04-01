# readme
## start
llm用のサーバー起動

```
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

モデルのダウンロード
```
docker exec -it ollama ollama run gemma3:1b
```

uv インストール
```
pip install uv
uv sync
```

mcpの起動
```
uvx mcpo --port 8080 --host 0.0.0.0 --config mcp_config.json
```


UIの起動
```
docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda
```