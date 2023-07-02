import argparse
import sys
import traceback
from enum import IntEnum

from genesis.service_data_layer.genesis_pinecone_store import GenesisPineconeVectorStore
from genesis.service_infra.genesis_context import GenesisRuntimeContext
from genesis.service_infra.genesis_environment import GenesisEnvironment
from genesis.service_infra.genesis_logger import logger


class GenesisReturnValue(IntEnum):
    Success = 0
    InvalidCmd = -1
    RuntimeFailure = -2
    CriticalFailure = -3

def genesis_genai_launch_engine(genesis_context: GenesisRuntimeContext):
    pass


def genesis_genai_validate_runtime_context(genesis_context: GenesisRuntimeContext):
    assert genesis_context.pinecone_environment is not None
    assert genesis_context.pinecone_api_key is not None
    assert genesis_context.openai_api_key is not None
    assert genesis_context.model_name is not None
    assert genesis_context.model_tokens is not None
    assert genesis_context.model_chunk_overlap is not None
    assert genesis_context.model_dimension is not None
    assert genesis_context.model_metric is not None
    assert genesis_context.gpt_model_name is not None
    assert genesis_context.client_id is not None


def genesis_genai_initialize_model_context(genesis_context: GenesisRuntimeContext, cmdline: argparse.Namespace) -> None:
    genesis_context.client_id = cmdline.client_id
    genesis_context.model_name = cmdline.model_name
    genesis_context.model_tokens = int(cmdline.model_tokens)
    genesis_context.model_chunk_overlap = int(cmdline.model_chunk_overlap)
    genesis_context.model_dimension = int(cmdline.model_dimension)
    genesis_context.model_metric = cmdline.model_metric
    genesis_context.gpt_model_name = cmdline.gpt_model


def genesis_genai_initialize_environment_context(genesis_context: GenesisRuntimeContext) -> None:
    genesis_context.pinecone_environment = GenesisEnvironment.pinecone_environment()
    genesis_context.pinecone_api_key = GenesisEnvironment.pinecone_api_key()
    genesis_context.openai_api_key = GenesisEnvironment.openai_api_key()


def genesis_genai_parse_command_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model-name", help="The model used for text embeddings", default="text-embedding-ada-002")
    parser.add_argument("--model-tokens", help="The number of tokens allowed by the model", default="3800")
    parser.add_argument("--model-chunk-overlap", help="The number of tokens to overlap between chunks", default="100")
    parser.add_argument("--model-dimension", help="The model dimension of text embeddings", default="1536")
    parser.add_argument("--model-metric", help="", default="cosine")
    parser.add_argument("--gpt-model-name", help="", default="gpt-4")
    parser.add_argument("--client-id", help="The Genesis client identifier (model index name)", required=True)
    return parser.parse_args()


def genesis_genai_entry_point() -> GenesisReturnValue:
    rv = GenesisReturnValue.Success

    try:
        genesis_context = GenesisRuntimeContext()

        logger.info("[Genesis-AI] (Alpha): Interpreting Command Line arguments.")
        genesis_cmdline = genesis_genai_parse_command_line()

        logger.info("[Genesis-AI] (Alpha): Initializing Genesis model context.")
        genesis_genai_initialize_model_context(genesis_context, genesis_cmdline)

        logger.info("[Genesis-AI] (Alpha): Initializing Genesis environment context.")
        genesis_genai_initialize_environment_context(genesis_context)

        logger.info("[Genesis-AI] (Alpha): Validating Genesis runtime context.")
        genesis_genai_validate_runtime_context(genesis_context)

        logger.info("[Genesis-AI] (Alpha): Launching Genesis interactive engine.")
        genesis_genai_launch_engine(genesis_context)

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
    sys.exit(genesis_genai_entry_point().value)
