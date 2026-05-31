import structlog, logging
from src.config import settings

def setup_logging():
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    processors = [structlog.contextvars.merge_contextvars, structlog.stdlib.filter_by_level,
                  structlog.stdlib.add_logger_name, structlog.stdlib.add_log_level,
                  structlog.processors.TimeStamper(fmt="iso"), structlog.processors.StackInfoRenderer()]
    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    structlog.configure(processors=processors, wrapper_class=structlog.stdlib.BoundLogger,
                        logger_factory=structlog.stdlib.LoggerFactory(), cache_logger_on_first_use=True)
    logging.root.setLevel(log_level)

setup_logging()
