#!/bin/sh
# Inicia o servidor Ollama em background
ollama serve &
sleep 5
ollama pull qwen2.5:0.5b
wait
