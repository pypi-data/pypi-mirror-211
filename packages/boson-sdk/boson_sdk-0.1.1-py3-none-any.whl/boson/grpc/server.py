import os
import logging
import grpc
from types import FunctionType
from concurrent import futures

from boson import BaseProvider
from boson.grpc.boson_v1_pb2_grpc import (
    BosonProviderV1Servicer,
    add_BosonProviderV1Servicer_to_server,
)
from boson.boson_v1_pb2 import (
    DatasetInfoRequest,
    DatasetInfoResponse,
    SearchRequest,
    SearchResponse,
    WarpRequest,
    RasterResponse,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

__all__ = ["serve"]


class BosonProviderServicer(BosonProviderV1Servicer, BaseProvider):
    def DatasetInfo(
        self, request: DatasetInfoRequest, context: grpc.ServicerContext
    ) -> DatasetInfoResponse:
        return self.dataset_info(request)

    def Search(self, request: SearchRequest, context: grpc.ServicerContext) -> SearchResponse:
        try:
            return super().search(request)
        except Exception as e:
            details = f"unable to run search function: {str(e)}"
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(details)
            return SearchResponse()

    def Warp(self, request: WarpRequest, context: grpc.ServicerContext) -> RasterResponse:
        try:
            return super().warp(request)
        except Exception as e:
            details = f"unable to run warp function: {str(e)}"
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(details)
            return RasterResponse()


def serve(search_func: FunctionType, warp_func: FunctionType, **kwargs) -> grpc.Server:
    logger.info("initializing server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = BosonProviderServicer(search_func=search_func, warp_func=warp_func, **kwargs)
    add_BosonProviderV1Servicer_to_server(servicer, server)

    port = os.getenv("PROVIDER_PORT")
    if port is None or port == "":
        port = "8000"
    logger.info("initializing starting boson provider server on %s", f"[::]:{port}")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("server started")
    server.wait_for_termination()
