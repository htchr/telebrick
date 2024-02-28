# GIX / T-Mobile construction launch project

## Use

1. Do not plug in the raspberry pi before everything is physically installed in the correct place. The pi will begin sending data as soon as it has power. We are on the free tier of Groundlight AI and should conserve usage.

2. Ensure the Azure container is running

3. Plug in the power cord from the case. The pi should automatically connect to the Azure container and begin sending data

4. Open your browser and navigate to 20.120.139.81 to see the results

## Test

### on the "server" laptop

```bash
docker build --build-arg GRND_KEY='your_groundlight_api_key' -t telebrick .
```

```bash
docker run --name tele-back -p 80:80 telebrick
```

### on the raspberry pi

quit the automatic python script, change the ip address in `/home/pi/telebrick/rasp-pi/bin_cam.py`

run with:

```bash
python bin_cam.py
```

