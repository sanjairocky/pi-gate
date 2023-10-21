docker build . -t sanjai/pi-gate:1.0.0 --build-arg CACHEBUST=$(date +%s)

helm uninstall pi-gate -n pi-gate

helm upgrade -n pi-gate -i pi-gate helm/pi-gate --create-namespace