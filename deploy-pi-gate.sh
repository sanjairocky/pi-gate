sudo systemctl stop pi-gate.service
sudo systemctl disable pi-gate.service
sudo rm /etc/systemd/system/pi-gate.service
sudo rm /etc/systemd/system/pi-gate.service # and symlinks that might be related
sudo rm /usr/lib/systemd/system/pi-gate.servie 
sudo rm /usr/lib/systemd/system/pi-gate.service # and symlinks that might be related
systemctl daemon-reload
systemctl reset-failed
npm i
sudo cp ./pi-gate.service /etc/systemd/system/pi-gate.service
sudo systemctl daemon-reload
sudo systemctl enable pi-gate.service
sudo systemctl start pi-gate.service
