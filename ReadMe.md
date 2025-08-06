# TelegramBot

TODO: Add actual documentation. This is a collection of commands used to create the image and extract the files from the container


```sh
docker build -t pcardenal/telegram-bot .
```


```sh
docker run -d -v /data/DockerVolumes/TelegramBot:/app/output:rw -d  --name TelegramBot pcardenal/telegram-bot:latest
```