docker image rm pi-gate:1.0.0

docker build . -t pi-gate:1.0.0

helm upgrade --install pi-gate helm/pi-gate