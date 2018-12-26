sudo chmod 644 /lib/systemd/system/sensor_reading.service
chmod +x /home/pi/github/jakubbaron/weather_station/src/reading.py
sudo systemctl daemon-reload
sudo systemctl enable sensor_reading.service
sudo systemctl start sensor_reading.service
sudo systemctl status sensor_reading.service
sudo journalctl -f -u sensor_reading.service

### EXAMPLE service
[Unit]
Description=A script to read from DHT11 every minute and log the data to Redis Stream DHT11-stream
After=multi-user.target

[Service]
Type=simple
Environment=REDIS_PASSWD=<PASSWORD>
ExecStart=/usr/bin/python3 /home/pi/github/jakubbaron/weather_station/src/reading.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
