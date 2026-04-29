# LoRa_Sibyl

This repository contains the "Aether-Agent" implementation for the LoRa Sibyl project, integrating a local intelligence agent with a Meshtastic network.

It consists of a Python-based radio bridge that interfaces with a connected Meshtastic node, and an intelligence agent script that processes incoming messages and generates AI-driven responses.

## Architecture

The system uses a 3-layer architecture utilizing the "File Trick" for IPC (Inter-Process Communication):

1. **Hardware / Radio layer:** A Meshtastic node (e.g., connected via Serial or TCP).
2. **Radio Bridge (`radio_bridge.py`):** Uses the `meshtastic` python API to listen for incoming messages. It writes these messages to `/tmp/mesh_inbox.json`. It also continuously polls `/tmp/mesh_outbox.txt` to send queued outgoing messages over the mesh.
3. **Intelligence Agent (`agent.py`):** Monitors `/tmp/mesh_inbox.json` for new incoming messages. When triggered (e.g., via `!ask` or `!ping` commands), it processes the payload (utilizing AI agents like OpenClaw, Jules, or Gemini) and writes the response to `/tmp/mesh_outbox.txt`.

## Getting Started

1. **Prerequisites:**
   - A Linux/macOS environment (tested on Raspberry Pi / Debian).
   - Python 3.
   - A connected Meshtastic node (Serial or TCP).

2. **Setup Environment:**
   Run the setup script to initialize the virtual environment, install dependencies, and create the necessary files in `/tmp`:
   ```bash
   ./setup.sh
   ```

3. **Running the System:**

   You must run both scripts in parallel.

   **Terminal 1 (Radio Bridge):**
   ```bash
   source venv/bin/activate
   python radio_bridge.py
   ```

   **Terminal 2 (Intelligence Agent):**
   ```bash
   source venv/bin/activate
   python agent.py
   ```

## Background Execution (systemd)

The `setup.sh` script automatically generates systemd service files. To install and run the agent in the background permanently:

```bash
sudo cp lorasibyl-bridge.service lorasibyl-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now lorasibyl-bridge.service lorasibyl-agent.service
```

## Customization

To implement your own triggers, modify `agent.py`. Specifically, look for the `process_message` function and the `call_openclaw_llm` placeholder function to hook in your specific LLM logic or telemetry triggers.
