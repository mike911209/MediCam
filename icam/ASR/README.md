# Whisper ASR Server

## Create Systemd Service

```sh
# Link the service files to systemd directory
sudo ln -sf $PWD/whisper_server.service /usr/lib/systemd/system

# Start the service & Enable autostart on boot
sudo systemctl enable --now whisper_server

# After any change
sudo systemctl daemon-reload
sudo systemctl restart whisper_server
```
