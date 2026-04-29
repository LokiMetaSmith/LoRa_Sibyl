# LoRa Sibyl "Aether-Agent" - To-Do List

## 1. Agent Logic & AI Integration
- [ ] **OpenClaw Integration:** Replace the placeholder `call_openclaw_llm` function in `agent.py` with actual API calls to the OpenClaw / LLM service.
- [ ] **Context Management:** Give the agent context about previous messages or a short-term memory to handle conversational queries.
- [ ] **Role Specialization:** Implement logic for the different agent roles discussed:
  - "The Watchdog": Monitor node density and noise floor.
  - "The Historian": Map signal dead zones and manage OKC maker space access.
  - "The Dispatcher": Provide real-time tactical updates and local weather alerts at events (BSides).

## 2. Advanced Triggers & Telemetry
- [ ] **Glitter Computation Tie-in:** Add specific monitoring for the remote fiber alignment jigs ("Glitter"). If a jig goes out of alignment or reports bad telemetry, trigger a high-priority mesh alert.
- [ ] **Shadowrun Automation:** Implement triggers that detect nodes becoming active to automatically spin up combat simulators or pre-load character XML data.
- [ ] **Raw JSON parsing:** Expand the trigger logic in `agent.py` to parse non-text payloads (like GPS location, environmental telemetry, and node info) directly from the packet object.

## 3. Architecture & Infrastructure
- [ ] **Hardware Migration (Concentrator):** Transition the `radio_bridge.py` from connecting to a standard single-frequency node to interfacing with a multi-channel RAK2287 concentrator or SDR (via Meshpoint/meshtasticd).
- [ ] **Robust IPC:** The current "File Trick" (`/tmp/mesh_inbox.json`) is simple but can suffer from race conditions or infinite growth. Implement:
  - A cleaner file-locking mechanism.
  - An SQLite database or Redis backend if the message throughput becomes high.
- [ ] **Production Deployment:** Solidify the `systemd` setup for running permanently at the Open Innovation Lab (Project 3810). Include automated log rotation and restart mechanisms.
- [ ] **Network Backhaul:** Set up integration hooks so the agent can bridge mesh messages to the internet (e.g., Slack/Discord alerts for Maker Space access) when an ethernet/WiFi connection is present.
