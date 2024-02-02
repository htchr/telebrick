# GIX / T-Mobile construction launch project

copy the rasp-pi folder to the raspbery pi

run with:

```bash
python bin_cam.py
```

on the server:

```bash
docker build -t telebrick .
```

```bash
docker run --name telebrick -p 80:80 telebrick
```
