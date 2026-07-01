"""
JavaMentor AI — Telemetry
Basic logging setup. Extend with OpenTelemetry for production.
"""
import logging
import os


def setup_telemetry() -> None:
    """Configure logging for the application."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Quiet down noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("google.auth").setLevel(logging.WARNING)
    logger = logging.getLogger("java_mentor")
    logger.info("JavaMentor AI telemetry initialized")
