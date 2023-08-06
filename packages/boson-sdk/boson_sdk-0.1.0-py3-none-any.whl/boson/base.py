from types import FunctionType
from typing import Optional

from boson.boson_v1_pb2 import (
    DatasetInfoRequest,
    DatasetInfoResponse,
    WarpRequest,
    RasterResponse,
    SearchRequest,
    SearchResponse,
)
from boson.features_pb2 import CollectionMsg
from boson.conversion import (
    search_request_to_kwargs,
    warp_request_to_kwargs,
    feature_collection_to_proto,
    numpy_to_raster_response,
)


class BaseProvider:
    def __init__(
        self,
        name: str = "remote",
        alias: str = "Remote Boson Provider",
        description: str = "a remote Boson provider",
        license: str = "(unknown)",
        extent: Optional[dict] = None,
        search_func: Optional[FunctionType] = None,
        warp_func: Optional[FunctionType] = None,
    ) -> None:
        self.name = name
        self.alias = alias
        self.description = description
        self.license = license
        self.extent = extent
        if self.extent is None:
            self.extent = {
                "spatial": {"bbox": [[-180.0, -90.0, 180.0, 90.0]]},
                "temporal": {"interval": [[None, None]]},
            }

        if search_func is not None and not callable(search_func):
            raise ValueError("search_func must be a callable or None")

        self.search_func = search_func

        if warp_func is not None and not callable(warp_func):
            raise ValueError("warp_func must be a callable or None")
        self.warp_func = warp_func
        super().__init__()

    def dataset_info(self, _: DatasetInfoRequest) -> DatasetInfoResponse:
        return DatasetInfoResponse(
            name=self.name,
            alias=self.alias,
            links=[],
            conforms_to=[
                "https://api.stacspec.org/v1.0.0/core",
                "https://api.stacspec.org/v1.0.0/item-search",
                "https://api.stacspec.org/v1.0.0/ogcapi-features",
                "https://api.stacspec.org/v1.0.0/collections",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
            ],
            collections=CollectionMsg(**self._collection),
        )

    def _collection(self) -> dict:
        return {
            "version": "v1.0.0",
            "id": self.name,
            "title": self.alias,
            "description": self.description,
            "license": self.license,
        }

    def warp(self, request: WarpRequest) -> RasterResponse:
        warp_kwargs = warp_request_to_kwargs(request)

        x = self.warp_func(**warp_kwargs)

        return numpy_to_raster_response(x)

    def search(self, request: SearchRequest) -> SearchResponse:
        search_kwargs = search_request_to_kwargs(request)

        res = self.search_func(**search_kwargs)
        token = ""
        if len(res) == 2:
            fc, token = res
        else:
            fc = res

        fc_proto = feature_collection_to_proto(fc)

        return SearchResponse(feature_collection=fc_proto, token=token)
