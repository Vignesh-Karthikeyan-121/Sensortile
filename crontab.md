```bash
sudo crontab -r //removes crontab files
sudo crontab -e // edit crontab files
```

```bash
@reboot sudo sh /home/pi/pollution.sh >/home/pi/Pollution_Sensing_IOT/logs/cronlog 2>&1
@reboot sudo python /home/pi/Pollution_Sensing_IOT/rpi_image.py
```

