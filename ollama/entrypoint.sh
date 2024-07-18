# Ollamaサーバーをバックグラウンドで起動
ollama serve &

# サーバーの起動を待つ
until curl -s http://localhost:11434 > /dev/null; do
  echo "Waiting for Ollama server to start..."
  sleep 1
done

# モデルをプル
ollama pull llama3

# uvicornをフォアグラウンドで起動
uvicorn app:app --reload --host 0.0.0.0 --port 9000