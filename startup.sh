#!/bin/bash

echo "🚀 Starting LLM server in background..."
python start_llm_server.py &
SERVER_PID=$!

echo "⏳ Waiting for server to start up..."
# Wait for server to be ready
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -f http://127.0.0.1:8000/docs > /dev/null 2>&1; then
        echo "✅ Server is ready!"
        break
    fi
    echo "Waiting for server... ($((attempt + 1))/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Server failed to start within timeout"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo "🔄 Running main pipeline..."
python run.py

echo "🛑 Shutting down server..."
kill $SERVER_PID 2>/dev/null

echo "✅ Pipeline completed!"
