import logging

LOGGER: logging.Logger = logging.getLogger(__name__)

class JobCriteria:

    def __init__(self, salary, tenure, WFH):
        self.salary=salary
        self.tenure=tenure
        self.WFH=WFH

    def print_options(self):
        LOGGER.info(f"If interested, define the {self.salary} within {type(self).__name__}, as well as {self.tenure} and {self.WFH} options")