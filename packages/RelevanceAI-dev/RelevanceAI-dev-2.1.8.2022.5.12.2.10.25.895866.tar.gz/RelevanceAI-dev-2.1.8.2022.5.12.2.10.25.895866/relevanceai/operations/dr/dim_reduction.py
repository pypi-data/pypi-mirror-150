# -*- coding: utf-8 -*-

from abc import abstractmethod
import pandas as pd
import numpy as np
import json

from doc_utils import DocUtils

from typing import List, Union, Dict, Any, Tuple, Optional
from typing_extensions import Literal
from relevanceai.client.helpers import Credentials

from relevanceai.utils.base import _Base
from relevanceai.utils.logger import LoguruLogger
from relevanceai.operations.cluster.constants import (
    DIM_REDUCTION,
    DIM_REDUCTION_DEFAULT_ARGS,
)


class DimReductionBase(LoguruLogger, DocUtils):
    def __call__(self, *args, **kwargs):
        return self.fit_predict(*args, **kwargs)

    # @abstractmethod
    def fit_transform(self, *args, **kw) -> np.ndarray:
        raise NotImplementedError

    def fit(self, *args, **kw):
        raise NotImplementedError

    def transform(self, *args, **kw):
        raise NotImplementedError

    def transform_documents(self, vector_field: str, documents: List[Dict]):
        vectors = self.get_field_across_documents(vector_field, documents)
        return self.transform(documents)

    def fit_documents(self, vector_field: str, documents: List[Dict]):
        vectors = self.get_field_across_documents(
            vector_field, documents, missing_treatment="skip"
        )
        return self.fit(vectors)

    def get_dr_vector_field_name(self, vector_field: str, alias: str):
        return ".".join(
            [
                "_dr_",
                alias,
                vector_field,
            ]
        )

    def fit_transform_documents(
        self,
        vector_field: str,
        documents: List[Dict],
        alias: str,
        exclude_original_vectors: bool = True,
        dims: int = 3,
    ):
        documents = list(self.filter_docs_for_fields([vector_field], documents))
        vectors = np.array(
            self.get_field_across_documents(
                vector_field, documents, missing_treatment="skip"
            )
        )
        dr_vectors = self.fit_transform(vectors, dims=dims)
        dr_vector_field_name = self.get_dr_vector_field_name(vector_field, alias)
        self.set_field_across_documents(dr_vector_field_name, dr_vectors, documents)
        if exclude_original_vectors:
            dr_docs = self.subset_documents(["_id", dr_vector_field_name], documents)
        return dr_docs


class PCA(DimReductionBase):
    def fit(self, vectors: np.ndarray, dims: int = 3, *args, **kw):
        from sklearn.decomposition import PCA as SKLEARN_PCA

        pca = SKLEARN_PCA(n_components=min(dims, vectors.shape[1]))
        return pca.fit(vectors)

    def fit_transform(
        self,
        vectors: np.ndarray,
        dr_args: Optional[Dict[Any, Any]] = DIM_REDUCTION_DEFAULT_ARGS["pca"],
        dims: int = 3,
    ) -> np.ndarray:
        from sklearn.decomposition import PCA as SKLEARN_PCA

        self.logger.debug(f"{dr_args}")
        vector_length = len(vectors[0])
        pca = SKLEARN_PCA(n_components=min(dims, vector_length), **dr_args)
        return pca.fit_transform(vectors)


class TSNE(DimReductionBase):
    def fit_transform(
        self,
        vectors: np.ndarray,
        dr_args: Optional[Dict[Any, Any]] = DIM_REDUCTION_DEFAULT_ARGS["tsne"],
        dims: int = 3,
    ) -> np.ndarray:
        from sklearn.decomposition import PCA
        from sklearn.manifold import TSNE

        pca = PCA(n_components=min(10, vectors.shape[1]))
        data_pca = pca.fit_transform(vectors)
        self.logger.debug(f"{dr_args}")
        tsne = TSNE(n_components=dims, **dr_args)
        return tsne.fit_transform(data_pca)


class UMAP(DimReductionBase):
    def fit_transform(
        self,
        vectors: np.ndarray,
        dr_args: Optional[Dict[Any, Any]] = DIM_REDUCTION_DEFAULT_ARGS["umap"],
        dims: int = 3,
    ) -> np.ndarray:
        try:
            from umap import UMAP
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"{e}\nInstall umap\n \
                pip install -U relevanceai[umap]"
            )
        self.logger.debug(f"{dr_args}")
        umap = UMAP(n_components=dims, **dr_args)
        return umap.fit_transform(vectors)


class Ivis(DimReductionBase):
    def fit_transform(
        self,
        vectors: np.ndarray,
        dr_args: Optional[Dict[Any, Any]] = DIM_REDUCTION_DEFAULT_ARGS["ivis"],
        dims: int = 3,
    ) -> np.ndarray:
        try:
            from ivis import Ivis
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"{e}\nInstall ivis\n \
                CPU: pip install -U ivis-cpu\n \
                GPU: pip install -U ivis-gpu"
            )
        self.logger.debug(f"{dr_args}")
        ivis = Ivis(embedding_dims=dims, **dr_args)
        if ivis.batch_size > vectors.shape[0]:
            ivis.batch_size = vectors.shape[0]
        vectors_dr = ivis.fit(vectors).transform(vectors)
        return vectors_dr


class DimReduction(_Base, DimReductionBase):
    def __init__(self, credentials: Credentials):
        super().__init__(credentials)

    @staticmethod
    def dim_reduce(
        vectors: np.ndarray,
        dr: Union[DIM_REDUCTION, DimReductionBase],
        dr_args: Union[None, dict],
        dims: Literal[2, 3],
    ) -> np.ndarray:
        """
        Dimensionality reduction
        """
        if isinstance(dr, str):
            if dr_args is None:
                dr_args = DIM_REDUCTION_DEFAULT_ARGS[dr]
            if dr == "pca":
                return PCA().fit_transform(vectors=vectors, dr_args=dr_args, dims=dims)
            elif dr == "tsne":
                return TSNE().fit_transform(vectors=vectors, dr_args=dr_args, dims=dims)
            elif dr == "umap":
                return UMAP().fit_transform(vectors=vectors, dr_args=dr_args, dims=dims)
            elif dr == "ivis":
                return Ivis().fit_transform(vectors=vectors, dr_args=dr_args, dims=dims)
            raise ValueError("not suppported")
        elif isinstance(dr, DimReductionBase):
            return dr().fit_transform(vectors=vectors, dr_args=dr_args, dims=dims)
        return np.array([])
