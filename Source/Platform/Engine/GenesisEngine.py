import argparse
import sys
import traceback
from enum import IntEnum

from Source.Platform.Engine.Settings.GenesisContext import GenesisRuntimeContext
from Source.Platform.Engine.Infrastructure.GenesisEnvironment import GenesisEnvironment
from Source.Platform.Engine.Infrastructure.GenesisLogger import logger


class GenesisEngineReturnValue(IntEnum):
    Success = 0
    InvalidCmd = -1
    RuntimeFailure = -2
    CriticalFailure = -3

def genesis_engine_launch_applicative_engine(genesis_context: GenesisRuntimeContext):
    pass


def genesis_engine_initialize_runtime_context(genesis_cmdline: argparse.Namespace) -> GenesisRuntimeContext:
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


def genesis_engine_parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model-name", help="The model used for text embeddings", default="text-embedding-ada-002")
    parser.add_argument("--model-tokens", help="The number of tokens allowed by the model", default="3800")
    parser.add_argument("--model-chunk-overlap", help="The number of tokens to overlap between chunks", default="100")
    parser.add_argument("--model-dimension", help="The model dimension of text embeddings", default="1536")
    parser.add_argument("--model-metric", help="", default="cosine")
    parser.add_argument("--gpt-model-name", help="", default="gpt-4")
    parser.add_argument("--client-id", help="The Genesis client identifier (model index name)", required=True)
    return parser.parse_args()


def genesis_server_entry_point() -> GenesisEngineReturnValue:
    rv = GenesisEngineReturnValue.Success

    try:
        logger.info("[Genesis-Engine]: Interpreting command line arguments.")
        genesis_cmdline = genesis_engine_parse_command_line()

        logger.info("[Genesis-Engine]: Initializing Genesis runtime context.")
        genesis_context = genesis_engine_initialize_runtime_context(genesis_cmdline)

        logger.info("[Genesis-Engine]: Launching Genesis interactive engine.")
        genesis_engine_launch_applicative_engine(genesis_context)

        logger.info("[Genesis-Engine]: Done (OK).")

    except Exception as e:
        logger.error(f"[Genesis-Engine]: (Runtime-Error) [(Fault -> [{str(e)}])].")
        rv = GenesisEngineReturnValue.RuntimeFailure
        traceback.print_exc()

    except:
        logger.critical(f"[Genesis-Engine]: (Critical-Error) [(Fault -> {str(sys.exc_info())})].")
        rv = GenesisEngineReturnValue.CriticalFailure
        traceback.print_exc()

    return rv


if __name__ == "__main__":
    sys.exit(genesis_server_entry_point().value)
