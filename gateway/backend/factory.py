from gateway.backend import LlamaCppBackend, EchoBackend, BackendClient
from loguru import logger


def get_backend(backend_name: str = "echo") -> BackendClient:
    if backend_name == "llama_cpp":
        return LlamaCppBackend()
    elif backend_name == "echo":
        return EchoBackend()
    else:
        logger.warning(f"Invalid backend name: {backend_name}")
        return EchoBackend()