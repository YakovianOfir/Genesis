from __future__ import annotations

import logging
import sys

from genesis.Source.Server.service_infra.genesis_constants import GENESIS_COMPONENT_SUBSYSTEM, GENESIS_TRACE_LEVEL_VERBOSE

logger = logging.getLogger(f"genesis.ai.{GENESIS_COMPONENT_SUBSYSTEM}")

if GENESIS_TRACE_LEVEL_VERBOSE:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.setLevel(logging.INFO)
