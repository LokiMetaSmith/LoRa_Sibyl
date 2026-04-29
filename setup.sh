#!/bin/bash
set -e

echo "Setting up LoRa_Sibyl Aether-Agent..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Initialize IPC files
echo "Initializing IPC files in /tmp..."
touch /tmp/mesh_inbox.json
if [ ! -s /tmp/mesh_inbox.json ]; then
    # Initialize with an empty JSON array if empty
    echo "[]" > /tmp/mesh_inbox.json
fi
touch /tmp/mesh_outbox.txt

# Create systemd service templates
echo "Creating systemd service templates..."

CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

cat << EOF > lorasibyl-bridge.service
[Unit]
Description=LoRa Sibyl Radio Bridge
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/radio_bridge.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > lorasibyl-agent.service
[Unit]
Description=LoRa Sibyl Intelligence Agent
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/agent.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "Setup complete!"
echo ""
echo "To run manually:"
echo "  source venv/bin/activate"
echo "  python radio_bridge.py &"
echo "  python agent.py &"
echo ""
echo "To install systemd services (optional):"
echo "  sudo cp lorasibyl-bridge.service lorasibyl-agent.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable --now lorasibyl-bridge.service lorasibyl-agent.service"
