"""
LLM Router — Groq (primary, free) → Ollama (fallback, offline)
"""
import os
import requests
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(_env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")

def _call_groq(messages):
    if not GROQ_API_KEY:
        raise ValueError("No GROQ_API_KEY")
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.2, "max_tokens": 200},
        timeout=15
    )
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()

def _call_ollama(messages):
    res = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": OLLAMA_MODEL, "messages": messages, "stream": False, "options": {"temperature": 0.2}},
        timeout=60
    )
    res.raise_for_status()
    return res.json()["message"]["content"].strip()

def chat(messages):
    if GROQ_API_KEY:
        try:
            reply = _call_groq(messages)
            print("[LLM] Groq ✓")
            return reply
        except Exception as e:
            print(f"[LLM] Groq failed: {e} — trying Ollama...")
    try:
        reply = _call_ollama(messages)
        print("[LLM] Ollama ✓")
        return reply
    except Exception as e:
        raise RuntimeError(f"Both LLMs failed: {e}")
