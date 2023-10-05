docker build . -t sanjai/pi-gate:1.0.0 --build-arg CACHEBUST=$(date +%s)

docker image push sanjai/pi-gate:1.0.0

docker image prune -a

helm uninstall pi-gate -n pi-gate

helm upgrade -n pi-gate -i pi-gate helm/pi-gate --create-namespace