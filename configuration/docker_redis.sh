# All credits to
# https://thisdavej.com/how-to-install-redis-on-a-raspberry-pi-using-docker/

# Download and install docker
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
# Add pi to docker group so we can run Docker commands without using sudo
sudo usermod -aG docker pi
# avoid having to log out and log back in for our docker group to take effect
newgrp docker
# Check if working
docker --version
# Example, verify working, fidelity test
docker run hello-world
# Update the Linux kernel overcommit memory setting, this helps in scenarios
# such as memory allocation during the background saving of the Redis database
sudo echo "vm.overcommit_memory = 1" >> /etc/sysctlf.conf

#Create redis docker
mkdir ~/redis; cd $_
REDIS_VERSION=5.0.2
curl -O https://raw.githubusercontent.com/antirez/redis/$REDIS_VERSION/redis.conf

echo "EDIT YOUR PASSWORD IN redis.conf"
vim redis.conf
docker run --name redis -v ~/redis/redis.conf:/usr/local/etc/redis/redis.conf -d -p 0.0.0.0:6379:6379 --restart unless-stopped --network=host arm32v7/redis redis-server /usr/local/etc/redis/redis.conf
# if you need to modify config/password of redis, you can do so by editting the
# local redis.conf and issuing
# docker restart redis

# If you want to stop redis
# docker stop redis
# Remove redis container:
# docker stop redis; docker rm redis
