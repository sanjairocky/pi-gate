sudo cp ./pi-gate.service /etc/systemd/system/pi-gate.service
sudo systemctl daemon-reload
sudo systemctl enable pi-gate.service
sudo systemctl start pi-gate.service
