from gateway.backend import EchoBackend, BackendClient
from gateway.schema import ModelName
from gateway.backend.llama_cpp import LocalLlamaCppBackendFactory, LlamaCppModalBackend

def get_backend(backend_name: ModelName) -> BackendClient:
    backends = {
        ModelName.local_llama_cpp: LocalLlamaCppBackendFactory,
        ModelName.modal_llama_cpp: LlamaCppModalBackend,
        ModelName.echo: EchoBackend,
    }
    return backends[backend_name]()