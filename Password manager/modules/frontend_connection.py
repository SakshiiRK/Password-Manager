import asyncio
import websockets
from queue import Queue
import threading
import builtins
import json

input_queue = Queue()
socket = None
is_new = False
manager = None

def set_is_new(new_is_new):
    global is_new
    is_new = new_is_new

def set_manager(new_manager):
    global manager
    manager = new_manager


async def alert_frontend(string):
    await socket.send(string)


def simulate_input(prompt=""):
    print(prompt, end="", flush=True)
    
    while input_queue.empty():
        pass
    return input_queue.get()

async def handle_client(websocket):
    global socket
    socket = websocket

    try:
        async for message in websocket:
            print(message)
            if message == "CHECK NEW":
                if is_new:
                    await socket.send("NEW")
                else:
                    await socket.send("EXIST")
                continue
            elif message == "LIST PASSWORDS":
                pwds = await manager.list_passwords()

                pwds = pwds.split("\n")

                await socket.send(json.dumps(
                    {
                        "passwords": pwds
                    }
                ))
                continue

            input_queue.put(message)
            
    except websockets.exceptions.ConnectionClosed as e:
        print("Client disconnected.")

async def websocket_server():
    print("Initiating frontend connection...")
    async with websockets.serve(handle_client, "localhost", 6789):
        await asyncio.Future()  # Keep the server running indefinitely

def start_websocket_server():
    asyncio.run(websocket_server())
    
def start_websocket_server_in_thread():
    thread = threading.Thread(target=start_websocket_server, daemon=True)
    thread.start()
    print("Websocket server started in a separate thread.")