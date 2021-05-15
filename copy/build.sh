cd /home/test/mc/
docker build -t mc src/
echo n2i4nh92gn224@H356h361#2tg | docker login --username koshi8bit --password-stdin
docker tag mc koshi8bit/mc
docker push koshi8bit/mc