docker stop front back mc
docker rm front back mc
docker run -p 8081:8081 -d --name front antonkuznetsov/front
docker run --net=container:front -d --name back antonkuznetsov/back
docker run --net=container:back -d --name mc koshi8bit/mc