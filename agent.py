import time
import json
import os

INBOX_FILE = "/tmp/mesh_inbox.json"
OUTBOX_FILE = "/tmp/mesh_outbox.txt"

# Keep track of the timestamp of the last message we processed
# to avoid processing the same message multiple times.
last_processed_timestamp = 0

def call_openclaw_llm(prompt: str) -> str:
    """
    Placeholder for OpenClaw / LLM integration.
    You can replace this with actual API calls to Gemini, OpenAI, or OpenClaw.
    """
    print(f"[OpenClaw Placeholder] Processing prompt: '{prompt}'")
    # In a real implementation, you would do something like:
    # response = openclaw.complete(prompt)
    # return response

    return f"Aether-Agent processed: '{prompt}'"

def send_response(text: str):
    """
    Appends a message to the outbox file so the radio bridge will send it.
    """
    try:
        with open(OUTBOX_FILE, 'a') as f:
            f.write(text + "\n")
        print(f"Queued response: {text}")
    except Exception as e:
        print(f"Error writing to outbox: {e}")

def process_message(msg: dict):
    """
    Process an incoming message and trigger logic based on its contents.
    """
    text = msg.get("text", "").strip()
    sender = msg.get("sender", "Unknown")

    # Example trigger 1: !ask command
    if text.startswith("!ask "):
        query = text[5:].strip()
        print(f"Trigger '!ask' detected from {sender}. Query: {query}")

        # Call the LLM
        response = call_openclaw_llm(query)

        # Send the response back
        send_response(f"@{sender} - {response}")

    # Example trigger 2: !ping command
    elif text == "!ping":
        print(f"Trigger '!ping' detected from {sender}.")
        send_response(f"@{sender} - pong! Aether-Agent is online.")

    # Additional triggers (e.g. telemetry alerts, glitter monitoring)
    # can be added here.

def main():
    global last_processed_timestamp
    print("Starting LoRa Sibyl Intelligence Agent...")
    print(f"Monitoring {INBOX_FILE} for incoming messages...")

    # Initialize timestamp to current time to ignore old messages
    # (or you could process them if you want a backlog)
    last_processed_timestamp = time.time()

    while True:
        try:
            if os.path.exists(INBOX_FILE):
                with open(INBOX_FILE, 'r') as f:
                    content = f.read()
                    if content.strip():
                        inbox = json.loads(content)

                        # Process new messages
                        new_messages_processed = False
                        for msg in inbox:
                            msg_time = msg.get("timestamp", 0)
                            if msg_time > last_processed_timestamp:
                                process_message(msg)
                                last_processed_timestamp = msg_time
                                new_messages_processed = True

                        # Optional: truncate the inbox file if it gets too large
                        # to prevent the JSON from growing indefinitely.
                        if len(inbox) > 1000:
                            print("Inbox large, keeping only the last 100 messages.")
                            with open(INBOX_FILE, 'w') as f:
                                json.dump(inbox[-100:], f, indent=2)

        except json.JSONDecodeError:
            # File might be mid-write, just skip this iteration
            pass
        except Exception as e:
            print(f"Error reading inbox: {e}")

        time.sleep(1) # Poll every 1 second

if __name__ == "__main__":
    main()
