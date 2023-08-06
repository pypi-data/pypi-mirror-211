import uuid

from typing import Union
import numpy as np
import geodesic
import shapely.wkb as wkb
from boson.boson_v1_pb2 import RasterResponse, WarpRequest, BandID, SearchRequest
from boson.features_pb2 import FeatureMsg, FeatureCollectionMsg, LinkMsg, AssetMsg


def feature_collection_to_proto(fc: geodesic.FeatureCollection) -> FeatureCollectionMsg:
    features = []
    for feature in fc.features:
        features.append(feature_to_proto(feature))

    links = []
    for link in fc.links:
        links.append(link_to_proto(link))

    return FeatureCollectionMsg(features=features, links=links)


def feature_to_proto(feature: geodesic.Feature) -> FeatureMsg:
    geom_wkb = feature.geometry.wkb

    assets = feature.get("assets")

    if assets is not None:
        assetsMsg = {}
        for asset_name, asset in assets.items():
            assetsMsg[asset_name] = AssetMsg(
                title=asset.title,
                description=asset.description,
                type=asset.type,
                href=asset.href,
                roles=asset.roles,
            )
    else:
        assetsMsg = None

    fid = feature.get("id", str(uuid.uuid4()))
    return FeatureMsg(
        id=fid,
        geometry=geom_wkb,
        properties=feature.properties,
        links=feature.links,
        assets=assetsMsg,
    )


def link_to_proto(link: dict) -> LinkMsg:
    return LinkMsg(
        href=link.get("href"), rel=link.get("rel"), type=link.get("type"), title=link.get("title")
    )


def search_request_to_kwargs(request: SearchRequest) -> dict:
    bbox = request.bbox
    datetime = request.datetime
    filter = request.filter
    collections = request.collections
    feature_ids = request.feature_ids
    fields = None
    if request.fields is not None:
        fields = {
            "include": request.fields.include,
            "exclude": request.fields.exclude,
        }

    intersects = None
    if request.intersects:
        intersects = wkb.loads(request.intersects)

    return {
        "bbox": tuple(bbox) if bbox else None,
        "datetime": datetime,
        "filter": filter,
        "collections": collections,
        "feature_ids": feature_ids,
        "fields": fields,
        "intersects": intersects,
        "limit": request.limit,
        "page": request.page,
        "token": request.token,
    }


def numpy_to_raster_response(x: np.ndarray) -> RasterResponse:
    _, descr = x.dtype.descr[0]

    return RasterResponse(data=x.tobytes(), content_type="raw", pixel_type=descr, shape=x.shape)


def warp_request_to_kwargs(request: WarpRequest) -> dict:
    bbox = request.output_extent
    bbox84 = request.output_extent_wgs84
    pixel_size = request.output_pixel_size
    shape = request.output_shape

    asset_bands = []
    if request.asset_bands is not None:
        asset_bands = [
            {"asset": ab.asset, "bands": tuple([convert_band_id(band_id) for band_id in ab.bands])}
            for ab in request.asset_bands
        ]

    return dict(
        bbox=bbox,
        bbox84=bbox84,
        pixel_size=tuple(pixel_size),
        shape=tuple(shape),
        output_srs=request.output_spatial_reference,
        bbox_srs=request.output_extent_spatial_reference,
        time_instant=request.time_instant,
        time_range=request.time_range,
        asset_bands=asset_bands,
        input_filepaths=request.input_filepaths,
        filter=request.filter,
    )


def convert_band_id(band_id: BandID) -> Union[str, int]:
    if band_id.name is not None:
        return band_id.name
    return band_id.id
