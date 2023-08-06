import logging

LEVEL = logging.INFO

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"
    underline = "\x1b[4m"
    
    debug_bg_color = "\x1b[48;5;10m"
    debug_fg_color = "\x1b[38;5;10m"
    
    info_bg_color = "\x1b[48;5;33m"
    info_fg_color = "\x1b[38;5;33m"
    
    warning_bg_color = "\x1b[48;5;227m"
    warning_fg_color = "\x1b[38;5;227m"
    
    error_bg_color = "\x1b[48;5;208m"
    error_fg_color = "\x1b[38;5;208m"
    
    critical_bg_color = "\x1b[48;5;9m"
    critical_fg_color = "\x1b[38;5;9m"
    
    reset_bg_color = "\x1b[49m"
    reset_fg_color = "\x1b[39m"
    
    debug_format = f"{bold} [%(filename)15s:%(lineno)4d] {reset} {grey} %(message)s"
    info_format = f"{bold} [%(filename)15s:%(lineno)4d] {reset} {grey} %(message)s"
    warning_format = f"{bold} [%(filename)15s:%(lineno)4d] {reset} {warning_fg_color} %(message)s"
    error_format = f"{bold} [%(filename)15s:%(lineno)4d] {reset} {error_fg_color} %(message)s"
    critical_format = f"{bold} [%(filename)15s:%(lineno)4d] {reset} {critical_fg_color} %(message)s"
    
    FORMATS = {
        logging.DEBUG: debug_format + reset,
        logging.INFO: info_format + reset,
        logging.WARNING: warning_format + reset,
        logging.ERROR: error_format + reset,
        logging.CRITICAL: critical_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


LOGGER = logging.getLogger("LLaMA")
LOGGER.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

LOGGER.addHandler(ch)