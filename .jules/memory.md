
## Archived: 2026-11-02
* The development environment is initialized using `./setup.sh`, which creates a Python virtual environment, installs dependencies, initializes the IPC files, and sets up systemd service templates.
* Always initiate a 'deep planning mode' before making changes: ask clarifying questions using message tools to verify all assumptions, create a plan using `set_plan` only when expectations are absolutely clear, and then execute the plan autonomously.
* The repository 'LoRa_Sibyl' implements an 'Aether-Agent', a Python-based Local Intelligence Gateway bridging a Meshtastic network with an AI agent.
* The project's architecture uses a file-based IPC pattern, communicating between the hardware radio bridge (`radio_bridge.py`) and intelligence agent (`agent.py`) via `/tmp/mesh_inbox.json` and `/tmp/mesh_outbox.txt`.
