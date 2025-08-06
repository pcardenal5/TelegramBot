from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

from logging import Logger


class YoutubeDownloader:
    def __init__(self, logs : Logger) -> None:
        self.logs = logs

    def downloadYoutubeVideo(
            self, 
            url : str,
            outputFolder : str = 'output/YoutubeOutput'
        ) -> str | None:

        self.logs.info(f'Se ha recibido una petición de descarga con la URL {url}')
        yt = YouTube(url, on_progress_callback=on_progress)

        ys = yt.streams.get_audio_only()
        if ys is None:
            self.logs.error(f'downloadYoutubeVideo - Error descargando vídeo {url}')
            return
        os.makedirs(outputFolder, exist_ok = True )
        ys.download(
            filename_prefix = f'{outputFolder}/'
        )

        # Once downloaded check the output folder to return file name
        return os.path.join(outputFolder,os.listdir(outputFolder)[0])


if __name__ == '__main__':
    import logging
    yt = YoutubeDownloader(logging.getLogger(__name__))
    yt.downloadYoutubeVideo('https://www.youtube.com/watch?v=sjlKVU5AAsc&list=RDsjlKVU5AAsc&start_radio=1&pp=oAcB0gcJCa0JAYcqIYzv')