from src.observability import get_logger

logger = get_logger(__name__)

logger.info("Enterprise Logger Initialized")

logger.warning("This is a warning.")

logger.error("This is an error.")