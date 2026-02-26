from gateway.backend import LlamaCppBackend, EchoBackend, BackendClient
from gateway.schema import ModelName


def get_backend(backend_name: ModelName) -> BackendClient:
    backends = {
        ModelName.llama_cpp: LlamaCppBackend,
        ModelName.echo: EchoBackend,
    }
    return backends[backend_name]()