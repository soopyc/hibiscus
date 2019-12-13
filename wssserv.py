#!/usr/bin/env python

# WS server example
import time
import asyncio
import websockets

def rec(a):
    print(f'📥 {a}')
def send(a):
    print(f'📤 {a}')

async def main(websocket, path):
    while True:
        command = await websocket.recv()
        rec(command)
        args = command.split(' ')
        if args[0] == "echo":
            a = ''
            if len(args) == 1:
                await websocket.send('Error: Nothing to echo.')
                send('Error: Nothing to echo.')
            else:
                for i in range(1,len(args)+1):
                    a += args[i]
                await websocket.send(a)
                send(a)
        elif args[0] == 'bye':
            await websocket.send('Bye!')
            send('Bye!')
            break
        elif args[0] == 'die':
            await websocket.send('Bye!')
            send('Bye!')
            print('Killing Server...')
            exit(0)
        elif args[0] == 'help':
            h = "\nAvailable Commands\n"
            # Write commands help here.
            '''Format:
            h += "command - help for command\n"
            '''
            h += "echo - Echo whatever thing sent back.\n"
            h += "bye - Disconnect WebSocket\n"
            h += "die - Kills the WebSocket Server"

            h += "help - This command\n--END--" # Do not remove
            send(h)
            await websocket.send(h)
        else:
            await websocket.send('Invalid Command. Run "help" and see the available commands.')

start_server = websockets.serve(main, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()