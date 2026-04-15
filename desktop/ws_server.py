"""
WebSocket server — bridges Python backend to the dashboard.
Dashboard connects to ws://localhost:8765
"""
import asyncio
import websockets
import json
import threading

_clients = set()
_loop = None

async def _handler(ws):
    _clients.add(ws)
    try:
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") == "command":
                # Import here to avoid circular
                from brain import process_command
                from voice import speak
                text = data.get("text", "")
                broadcast({"type": "command", "text": text})
                broadcast({"type": "state", "state": "thinking"})
                try:
                    result = process_command(text)
                except Exception as e:
                    result = f"Error: {e}"
                broadcast({"type": "response", "text": result})
                broadcast({"type": "state", "state": "idle"})
                speak(result)
    except Exception:
        pass
    finally:
        _clients.discard(ws)

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
    async with websockets.serve(_handler, "localhost", 8765):
        await asyncio.Future()

def start_ws_server():
    global _loop
    _loop = asyncio.new_event_loop()
    t = threading.Thread(target=lambda: _loop.run_until_complete(_serve()), daemon=True)
    t.start()
    print("[WS] Dashboard server running on ws://localhost:8765")
