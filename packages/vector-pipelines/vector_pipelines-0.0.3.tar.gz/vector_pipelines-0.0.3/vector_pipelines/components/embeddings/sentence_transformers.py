from __future__ import annotations

from typing import Any, Union

from pydantic import BaseModel

from vector_pipelines.components.embeddings.base import Embeddings
from vector_pipelines.components.factory import register_component
from vector_pipelines.components.init import initialized
from vector_pipelines.utils.imports import _SENTENCE_TRANSFORMERS_AVAILABLE

if _SENTENCE_TRANSFORMERS_AVAILABLE:
    from sentence_transformers import SentenceTransformer


class SentenceTransformersEmbeddingsConfig(BaseModel):
    """The configuration for the `SentenceTransformersEmbeddings` class.

    Attributes:
        model_name_or_path: The name of the model to use or the path to a directory
            containing a model.
        device: The device to use for the model. If `cpu`, the CPU will be used. If
            `cuda`, the GPU will be used. If `cuda:X`, the GPU with index `X` will be
            used. Defaults to `cpu`.
        normalize_embeddings: Whether to normalize the embeddings or not. Defaults to
            `False`.
    """

    model_name_or_path: str
    device: str = "cpu"
    normalize_embeddings: bool = False


@register_component("sentence_transformers_embeddings")
class SentenceTransformersEmbeddings(Embeddings):
    """A wrapper for the `sentence-transformers` library to generate embeddings.

    Attributes:
        config: the configuration for the Sentence Transformers model.
        model: The Sentence Transformers model.
    """

    config_cls = SentenceTransformersEmbeddingsConfig
    config: SentenceTransformersEmbeddingsConfig
    model: Union[SentenceTransformer, None] = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        if not _SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "The `sentence-transformers` package is required to use"
                " `SentenceTransformerEmbeddings` class. Install it with `pip install"
                " vector-pipelines[sentence-transformers]`."
            )
        self.config = SentenceTransformersEmbeddingsConfig(**kwargs)

    def init(self) -> None:
        self.model = SentenceTransformer(
            model_name_or_path=self.config.model_name_or_path, device=self.config.device
        )
        super().init()

    @initialized
    def encode(self, data: str | list[str]) -> list[list[int | float]]:
        if isinstance(data, str):
            data = [data]
        embeddings: list[list[int | float]] = self.model.encode(sentences=data).tolist()  # type: ignore
        return embeddings

    @property
    @initialized
    def vector_size(self) -> int:
        embedding_size: int = self.model.get_sentence_embedding_dimension()  # type: ignore
        return embedding_size
