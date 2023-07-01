from __future__ import annotations

import logging
import sys

from chatty.service_infra.chatty_constants import CHATTY_TRACE_LEVEL_VERBOSE, CHATTY_COMPONENT_SUBSYSTEM

logger = logging.getLogger(f"chatty.ai.{CHATTY_COMPONENT_SUBSYSTEM}")

if CHATTY_TRACE_LEVEL_VERBOSE:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.setLevel(logging.INFO)
