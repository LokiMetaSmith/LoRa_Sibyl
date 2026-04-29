import time
import json
import os
import threading
import traceback
import sys
from typing import Dict, Any

# We use the meshtastic library to interface with the node
import meshtastic
import meshtastic.tcp_interface
import meshtastic.serial_interface
from pubsub import pub

INBOX_FILE = "/tmp/mesh_inbox.json"
OUTBOX_FILE = "/tmp/mesh_outbox.txt"

def on_receive(packet: Dict[Any, Any], interface: Any):
    """Callback for receiving a message from the mesh."""
    try:
        # Check if the packet has a text payload
        if 'decoded' in packet and 'text' in packet['decoded']:
            message_text = packet['decoded']['text']
            sender = packet.get('fromId', 'Unknown')

            # Form the message object
            msg_obj = {
                "timestamp": time.time(),
                "sender": sender,
                "text": message_text,
                "packet": packet  # keep original packet for advanced triggers
            }

            print(f"Received message from {sender}: {message_text}")

            # Read existing inbox
            inbox = []
            if os.path.exists(INBOX_FILE):
                try:
                    with open(INBOX_FILE, 'r') as f:
                        content = f.read()
                        if content.strip():
                            inbox = json.loads(content)
                except Exception as e:
                    print(f"Error reading inbox file: {e}")
                    inbox = []

            # Append new message
            inbox.append(msg_obj)

            # Write back
            with open(INBOX_FILE, 'w') as f:
                json.dump(inbox, f, indent=2)

    except Exception as e:
        print(f"Error processing received packet: {e}")
        traceback.print_exc()

def outbox_monitor(interface: Any):
    """Monitors the outbox file and sends any messages found."""
    print(f"Monitoring {OUTBOX_FILE} for outgoing messages...")
    while True:
        try:
            if os.path.exists(OUTBOX_FILE):
                with open(OUTBOX_FILE, 'r') as f:
                    lines = f.readlines()

                if lines:
                    # Clear the file immediately to avoid sending multiple times
                    with open(OUTBOX_FILE, 'w') as f:
                        f.write("")

                    for line in lines:
                        line = line.strip()
                        if line:
                            print(f"Sending message: {line}")
                            interface.sendText(line)
                            time.sleep(1) # Small delay between sends

            time.sleep(2) # Poll every 2 seconds
        except Exception as e:
            print(f"Error monitoring outbox: {e}")
            time.sleep(5)

def main():
    print("Starting LoRa Sibyl Radio Bridge...")

    # Initialize the interface
    interface = None
    try:
        # Try to connect via Serial first (default for locally attached nodes)
        print("Attempting to connect via Serial...")
        interface = meshtastic.serial_interface.SerialInterface()
        print("Connected via Serial.")
    except Exception as e:
        print(f"Serial connection failed: {e}")
        print("Attempting to connect via TCP (localhost)...")
        try:
            interface = meshtastic.tcp_interface.TCPInterface(hostname="localhost")
            print("Connected via TCP.")
        except Exception as e:
            print(f"TCP connection failed: {e}")
            print("Could not connect to a Meshtastic node. Please ensure a node is connected.")
            sys.exit(1)

    # Subscribe to message receive events
    pub.subscribe(on_receive, "meshtastic.receive")

    # Start the outbox monitoring thread
    monitor_thread = threading.Thread(target=outbox_monitor, args=(interface,), daemon=True)
    monitor_thread.start()

    print("Bridge is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping bridge...")
    finally:
        if interface:
            interface.close()

if __name__ == "__main__":
    main()
