docker image rm sanjai/pi-gate:1.0.0

docker build . -t sanjai/pi-gate:1.0.0

docker image push sanjai/pi-gate:1.0.0

helm upgrade -n pi-gate -i pi-gate helm/pi-gate --create-namespace