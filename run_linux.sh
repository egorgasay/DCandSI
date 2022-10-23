docker rm -f dcsi
docker run -d=true --network host -it --name=dcsi dcsi
docker exec -it dcsi python3 DCSI.py
