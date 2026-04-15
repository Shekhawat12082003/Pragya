"""
dashboard_server.py — Backend for dashboard only (no voice conflicts)
Runs WebSocket server for dashboard communication
"""

import asyncio
import websockets
import json
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brain import process_command

_clients = set()
_loop = None

async def _handler(ws):
    _clients.add(ws)
    print(f"[WS] Dashboard connected")
    try:
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") == "command":
                text = data.get("text", "")
                print(f"[Command] {text}")
                broadcast({"type": "command", "text": text})
                broadcast({"type": "state", "state": "thinking"})
                
                try:
                    result = process_command(text)
                except Exception as e:
                    result = f"Error: {e}"
                    print(f"[Error] {e}")
                
                broadcast({"type": "response", "text": result})
                broadcast({"type": "state", "state": "idle"})
                print(f"[Response] {result}")
                
            elif data.get("type") == "ping":
                broadcast({"type": "pong"})
                
    except Exception as e:
        print(f"[WS Error] {e}")
    finally:
        _clients.discard(ws)
        print(f"[WS] Dashboard disconnected")

def broadcast(data):
    if not _clients or not _loop:
        return
    msg = json.dumps(data)
    asyncio.run_coroutine_threadsafe(_broadcast(msg), _loop)

async def _broadcast(msg):
    dead = set()
    for ws in _clients:
        try:
            await ws.send(msg)
        except Exception:
            dead.add(ws)
    _clients.difference_update(dead)

async def _serve():
    print("=" * 50)
    print("  PRAGYA DASHBOARD SERVER")
    print("  WebSocket: ws://localhost:8765")
    print("  Dashboard: http://localhost:5175")
    print("=" * 50)
    
    async with websockets.serve(_handler, "localhost", 8765):
        await asyncio.Future()

def start_dashboard_server():
    global _loop
    _loop = asyncio.new_event_loop()
    t = threading.Thread(target=lambda: _loop.run_until_complete(_serve()), daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    start_dashboard_server()
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Server] Shutting down...")
