from datetime import datetime

from loguru import logger


class ExcutionLogger:

    DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

    def start(self) -> None:
        self.start = datetime.now()

    def log_start(self) -> None:
        logger.info("Execution started at", self.start.isoformat())

    def log_end(self, text: str) -> None:
        finish = datetime.now()
        duration_program = self.__calc_exeution_duration(finish)
        logger.info(
            f"""{text}, Start: {self.start.strftime(ExcutionLogger.DATETIME_FORMAT)}, End: {finish.strftime(ExcutionLogger.DATETIME_FORMAT)}, Duration: {duration_program}"""
        )

    def __calc_exeution_duration(self, finish):
        duration_program = (finish - self.start).seconds / 60
        return duration_program
