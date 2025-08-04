import logging

class LogService:


    def __init__(
            self,
            logName : str = 'PayoBot'
        ) -> None:
        
        logging.basicConfig(
            filemode = 'a',
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
            level=logging.INFO,
            filename = f'{logName}.log'
        )

        # set higher logging level for httpx to avoid all GET and POST requests being logged
        logging.getLogger("httpx").setLevel(logging.WARNING)

        self.log = logging.getLogger(logName)
