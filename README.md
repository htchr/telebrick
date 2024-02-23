# GIX / T-Mobile construction launch project

## raspberry pi

```bash
python bin_cam.py
```

## server

```bash
docker build --build-arg GRND_KEY='your_groundlight_api_key' -t tele-back .
```

```bash
docker run --name tele-back -p 80:80 tele-back
```
