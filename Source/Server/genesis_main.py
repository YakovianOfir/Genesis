import argparse
import sys
import traceback
from enum import IntEnum

from genesis.Source.Server.service_infra.genesis_context import GenesisRuntimeContext
from genesis.Source.Server.service_infra.genesis_environment import GenesisEnvironment
from genesis.Source.Server.service_infra.genesis_logger import logger


class GenesisReturnValue(IntEnum):
    Success = 0
    InvalidCmd = -1
    RuntimeFailure = -2
    CriticalFailure = -3

def genesis_launch_interactive_engine(genesis_context: GenesisRuntimeContext):
    pass


def genesis_initialize_runtime_context(genesis_cmdline: argparse.Namespace) -> GenesisRuntimeContext:
    genesis_context = dict(
        {
            "pinecone_environment": GenesisEnvironment.pinecone_environment(),
            "pinecone_api_key": GenesisEnvironment.pinecone_api_key(),
            "openai_api_key": GenesisEnvironment.openai_api_key(),
            "model_chunk_overlap": int(genesis_cmdline.model_chunk_overlap),
            "model_dimension": int(genesis_cmdline.model_dimension),
            "model_tokens": int(genesis_cmdline.model_tokens),
            "model_metric": genesis_cmdline.model_metric,
            "gpt_model_name": genesis_cmdline.gpt_model,
            "model_name": genesis_cmdline.model_name,
            "client_id": genesis_cmdline.client_id,
        }
    )
    return GenesisRuntimeContext(**genesis_context)


def genesis_parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model-name", help="The model used for text embeddings", default="text-embedding-ada-002")
    parser.add_argument("--model-tokens", help="The number of tokens allowed by the model", default="3800")
    parser.add_argument("--model-chunk-overlap", help="The number of tokens to overlap between chunks", default="100")
    parser.add_argument("--model-dimension", help="The model dimension of text embeddings", default="1536")
    parser.add_argument("--model-metric", help="", default="cosine")
    parser.add_argument("--gpt-model-name", help="", default="gpt-4")
    parser.add_argument("--client-id", help="The Genesis client identifier (model index name)", required=True)
    return parser.parse_args()


def genesis_platform_entry_point() -> GenesisReturnValue:
    rv = GenesisReturnValue.Success

    try:
        logger.info("[Genesis-AI] (Alpha): Interpreting Genesis command line arguments.")
        genesis_cmdline = genesis_parse_command_line()

        logger.info("[Genesis-AI] (Alpha): Initializing Genesis runtime context.")
        genesis_context = genesis_initialize_runtime_context(genesis_cmdline)

        logger.info("[Genesis-AI] (Alpha): Launching Genesis interactive engine.")
        genesis_launch_interactive_engine(genesis_context)

        logger.info("[Genesis-AI] (Alpha): Done (OK).")

    except Exception as e:
        logger.error(f"[Genesis-AI] (Alpha): (Runtime-Error) [(Fault -> [{str(e)}])].")
        rv = GenesisReturnValue.RuntimeFailure
        traceback.print_exc()

    except:
        logger.critical(f"[Genesis-AI] (Alpha): (Critical-Error) [(Fault -> {str(sys.exc_info())})].")
        rv = GenesisReturnValue.CriticalFailure
        traceback.print_exc()

    return rv


if __name__ == "__main__":
    sys.exit(genesis_platform_entry_point().value)
