import requests as r
from markdownify import markdownify
from datetime import date
import os
from logging import Logger

class WebToMarkdown:
    def __init__(self, logs : Logger) -> None:
        self.logs = logs


    def downloadUrl(
            self, 
            url : str,
            outputFolder : str = 'output/WebOutput',
            fileName : str = f'{date.today()}.md'
        ) -> str | None:

        try:
            with r.get(url) as request:
                html = request.content
        except Exception as e:
            self.logs.error(f'downloadUrl - Error accediendo a la web {url} : {str(e)}')
            return

        if request.status_code != 200:
            self.logs.error(f'downloadUrl - Error accediendo a la web {url} : Estado inválido {request.status_code}')

        text = markdownify(html, strip = ['img'])

        outputFileName = self.__makeOutputFile__(outputFolder, fileName)
        try:
            with open(outputFileName, 'w', encoding="utf-8") as output:
                output.write(text)
            return outputFileName

        except Exception as e:
            self.logs.error(f'downloadUrl - Error generando fichero de salida de la web {url} : {str(e)}')


    def __makeOutputFile__(self, outputFolder : str, fileName : str) -> str:
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        if not fileName.endswith('.md'):
            fileName += '.md'

        if not fileName.startswith(outputFolder):
            fileName = os.path.join(outputFolder, fileName)

        return fileName
