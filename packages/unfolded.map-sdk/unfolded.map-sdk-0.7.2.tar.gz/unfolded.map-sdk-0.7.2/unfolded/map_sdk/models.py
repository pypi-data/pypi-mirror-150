import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from unfolded.map_sdk.enums import ActionType, FilterType, LayerType
from unfolded.map_sdk.transfer_utils import normalize_data

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None

# Literal is included in the stdlib as of Python 3.8
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class CamelCaseBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

        @staticmethod
        def to_camel_case(snake_str: str) -> str:
            """Convert snake_case string to camelCase
            https://stackoverflow.com/a/19053800
            """
            components = snake_str.split("_")
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            return components[0] + "".join(x.title() for x in components[1:])

        alias_generator = to_camel_case


# TODO: do we expose this class at all?
# class MapOptions(BaseModel):
#     mapUrl: Optional[str]
#     mapUUID: Optional[UUID]
#     appendToId: Optional[str]
#     id: Optional[str]
#     embed: Optional[bool]
#     onLoad: Optional[() => void]
#     onTimelineIntervalChange: Optional[(currentTimeInterval: List[float>) => void]
#     onLayerTimelineTimeChange: Optional[(currentTime: float) => void]
#     appendToDocument: bool
#     width: float
#     height: float

# class MapInstance(BaseModel):
#     iframe: HTMLCanvasElement

FilterValueType = Union[List[float], List[str], bool, Any]


class FilterChangeEvent(CamelCaseBaseModel):
    """Information on filter changes passed to onFilter callbacks

    Kwargs:
        id: Filter ID
        name: Field names the filter applies to
        data_id: Dataset UUID
        prop: Filter property that is changed: 'value', 'name', etc
        type: FilterType
        value: Value of the filter
    """

    id: str
    name: List[str]
    data_id: UUID
    prop: str
    type: FilterType
    value: FilterValueType


class ClickEvent(CamelCaseBaseModel):
    """Information on the object passed to on_click

    Kwargs:
        index: Data row index
        coordinate: Geospatial coordinates [lng, lat]
        x: Mouse position x relative to the viewport
        y: Mouse position y relative to the viewport
        layer_id: The layer id that the picked object belongs to
        data: Picked object in the layer
    """

    index: int
    coordinate: Tuple[float, float]
    x: float
    y: float
    layer_id: Optional[str]
    data: Optional[Dict[str, Any]]


class HoverEvent(CamelCaseBaseModel):
    """Information on the object passed to on_hover

    Kwargs:
        index: Data row index
        coordinate: Geospatial coordinates [lng, lat]
        x: Mouse position x relative to the viewport
        y: Mouse position y relative to the viewport
        layer_id: The layer id that the picked object belongs to
        data: Picked object in the layer
    """

    index: int
    coordinate: Tuple[float, float]
    x: float
    y: float
    layer_id: Optional[str]
    data: Optional[Dict[str, Any]]


class Geometry(CamelCaseBaseModel):
    """GeoJSON geometry object`"""

    type: str
    coordinates: Any


class Feature(CamelCaseBaseModel):
    """GeoJSON feature object`"""

    id: str
    properties: Any
    geometry: Geometry


class GeometrySelectionEvent(CamelCaseBaseModel):
    """Information on the object passed to on_geometry_selection

    Kwargs:
        features: List of drawn GeoJSON shapes
    """

    features: List[Feature]


OnLoadHandlerType = Optional[Callable[[None], None]]
OnTimelineIntervalChangeHandlerType = Optional[Callable[[List[int]], None]]
OnLayerTimelineTimeChangeHandlerType = Optional[Callable[[int], None]]
OnFilterHandlerType = Optional[Callable[[FilterChangeEvent], None]]
OnHoverHandlerType = Optional[Callable[[HoverEvent], None]]
OnClickHandlerType = Optional[Callable[[ClickEvent], None]]
OnGeometrySelectionHandlerType = Optional[Callable[[GeometrySelectionEvent], None]]


class MapEventHandlers(CamelCaseBaseModel):
    """Event handlers which can be registered for receiving notifications of certain map events."""

    on_load: OnLoadHandlerType
    on_timeline_interval_change: OnTimelineIntervalChangeHandlerType
    on_layer_timeline_time_change: OnLayerTimelineTimeChangeHandlerType
    on_filter: OnFilterHandlerType
    on_hover: OnHoverHandlerType
    on_click: OnClickHandlerType
    on_geometry_selection: OnGeometrySelectionHandlerType


class Layer(CamelCaseBaseModel):
    """Layer info returned by `get_layers()`"""

    label: str
    id: str
    is_visible: bool


Bounds = Tuple[float, float, float, float]


class ViewState(CamelCaseBaseModel):
    """Map viewport state for use with `set_view_state()`"""

    longitude: Optional[float]
    latitude: Optional[float]
    zoom: Optional[float]
    min_zoom: Optional[float]
    max_zoom: Optional[float]
    max_bounds: Optional[Bounds]


class TimelineInfo(CamelCaseBaseModel):
    """Timeline control state returned by `get_timeline_info()`"""

    data_id: List[UUID]
    domain: List[float]
    is_visible: bool
    enlarged_histogram: List[Any]
    histogram: List[Any]
    value: List[float]
    speed: float
    step: float
    is_animating: bool


class TimeInterval(CamelCaseBaseModel):
    """Time interval for use with `set_timeline_config()`"""

    start_time: float
    end_time: float


class TimelineConfig(CamelCaseBaseModel):
    """Time configuration for use with `set_timeline_config()`"""

    idx: int
    current_time_interval: Optional[TimeInterval]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


class LayerTimelineInfo(CamelCaseBaseModel):
    """Layer timeline state returned by `get_layer_timeline_info()`"""

    current_time: float
    default_time_format: str
    domain: List[float]
    duration: float
    is_visible: bool
    is_animating: bool
    speed: float
    time_format: str
    time_steps: Any
    timezone: str


class LayerTimelineConfig(CamelCaseBaseModel):
    """Layer timeline configuration for use with `set_layer_timeline_config()`"""

    current_time: Optional[float]
    is_visible: Optional[bool]
    is_animating: Optional[bool]
    speed: Optional[float]
    timezone: Optional[str]
    time_format: Optional[str]


VectorTilesetType = Literal["vector-tile"]
RasterTilesetType = Literal["raster-tile"]

TilesetType = Union[VectorTilesetType, RasterTilesetType]


class VectorMeta(CamelCaseBaseModel):
    """Vector tileset metadata"""

    data_url: str
    metadata_url: str


class VectorTileset(CamelCaseBaseModel):
    name: str
    type: VectorTilesetType
    meta: VectorMeta


class RasterMeta(CamelCaseBaseModel):
    """Raster tileset metadata"""

    # image_url is currently unused
    image_url: str = ""
    metadata_url: str


class RasterTileset(CamelCaseBaseModel):
    name: str
    type: RasterTilesetType
    meta: RasterMeta


# NOTE: this is weaker typing than we have on the TS side: you could supply type='vector-tile' but
# raster tile metadata to `meta`. Pydantic only added discriminator support in the latest version:
# 1.9.
# We might want to just expose separate `RasterTileset` and `VectorTileset` models, and use
# `parse_obj` from the _add_tileset function.
class Tileset(CamelCaseBaseModel):
    """Tileset configuration for use with `add_tileset`"""

    name: str
    type: TilesetType
    meta: Union[VectorMeta, RasterMeta]


class LayerConfig(CamelCaseBaseModel):
    """Layer configuration for use with `add_layer` or `add_dataset`.
    `LayerConfig` is part of `LayerSpec`.
    """

    data_id: UUID
    label: Optional[str]
    columns: Dict[str, Any]
    is_visible: Optional[bool]
    vis_config: Optional[Dict[str, Any]]
    color_field: Optional[Dict[str, Any]]
    color_scale: Optional[str]
    color_ui: Optional[Dict[str, Any]] = Field(alias="colorUI")


class LayerSpec(CamelCaseBaseModel):
    """Layer configuration for use with `add_layer` or `add_dataset`"""

    id: str
    type: LayerType
    config: LayerConfig
    visual_channels: Optional[Dict[str, Any]]


class Dataset(CamelCaseBaseModel):
    """Dataset configuration for use with `add_dataset`.
    Kwargs:
        uuid: Unique identifier of the dataset (will be auto-generated when not provided).
        data: (Optional) CSV, JSON, DataFrame or GeoDataFrame data for the dataset.
    """

    uuid: UUID = Field(default_factory=uuid4)
    label: str = "Untitled"
    data: Optional[Union[str, DataFrame]]

    @validator("data", pre=True, always=True)
    # pylint: disable=no-self-argument
    def set_data_normalized(
        cls, data: Optional[Union[str, DataFrame]]
    ) -> Optional[str]:
        return normalize_data(data)

    class Config:
        # to prevent "No validator for DataFrame"
        arbitrary_types_allowed = True
        validate_assignment = True


class MapConfigInternal(CamelCaseBaseModel):
    """Internal map configuration"""

    mapState: Any
    mapStyle: Any
    visState: Any


class MapConfig(CamelCaseBaseModel):
    """Versioned map configuration returned in `get_map_config(), used in set_map_config`"""

    version: str
    config: MapConfigInternal


class FilterInfo(CamelCaseBaseModel):
    """Filter settings for use with `set_filter`"""

    id: str
    data_id: Optional[UUID]
    field: str
    value: FilterValueType


class ThemeOptions(CamelCaseBaseModel):
    """Theme options for use with `set_theme`"""

    background_color: Optional[str]


class Action(CamelCaseBaseModel):
    """Base Action payload class"""

    type: ActionType
    message_id: UUID = Field(default_factory=uuid4)


class SetViewState(Action):
    """Action payload sent with `set_view_state`calls"""

    type: ActionType = ActionType.SET_VIEW_STATE
    view_state: ViewState


class GetLayers(Action):
    """Action payload sent with `get_layers`calls"""

    type: ActionType = ActionType.GET_LAYERS


class SetLayerVisibility(Action):
    """Action payload sent with `set_layer_visibility`calls"""

    type: ActionType = ActionType.SET_LAYER_VISIBILITY
    layer_id: str
    is_visible: bool


class SetTheme(Action):
    """Action payload sent with `set_theme`calls"""

    type: ActionType = ActionType.SET_THEME
    theme: Literal["light", "dark"]
    options: Optional[ThemeOptions]


class GetTimelineInfo(Action):
    """Action payload sent with `get_timeline_info`calls"""

    type: ActionType = ActionType.GET_TIMELINE_INFO
    idx: int


class ToggleTimelineAnimation(Action):
    """Action payload sent with `toggle_timeline_animation`calls"""

    type: ActionType = ActionType.TOGGLE_TIMELINE_ANIMATION
    idx: int


class ToggleTimelineVisibility(Action):
    """Action payload sent with `toggle_timeline_visibility`calls"""

    type: ActionType = ActionType.TOGGLE_TIMELINE_VISIBILITY
    idx: int


class SetTimelineInterval(Action):
    """Action payload sent with `set_timeline_interval`calls"""

    type: ActionType = ActionType.SET_TIMELINE_INTERVAL
    idx: int
    start_time: float
    end_time: float


class SetTimelineAnimationSpeed(Action):
    """Action payload sent with `set_timeline_animation_speed`calls"""

    type: ActionType = ActionType.SET_TIMELINE_SPEED
    idx: int
    speed: float


class SetTimelineConfig(Action):
    """Action payload sent with `set_timeline_config` calls"""

    type: ActionType = ActionType.SET_TIMELINE_CONFIG
    config: TimelineConfig


class RefreshMapData(Action):
    """Action payload sent with `refresh_map_data` calls"""

    type: ActionType = ActionType.REFRESH_MAP_DATA


class GetLayerTimelineInfo(Action):
    """Action payload sent with `get_layer_timeline_info` calls"""

    type: ActionType = ActionType.GET_LAYER_TIMELINE_INFO


class SetLayerTimelineConfig(Action):
    """Action payload sent with `set_layer_timeline_config` calls"""

    type: ActionType = ActionType.SET_LAYER_TIMELINE_CONFIG
    config: LayerTimelineConfig


class AddTileset(Action):
    """Action payload sent with `add_tileset` calls"""

    type: ActionType = ActionType.ADD_TILESET_TO_MAP
    tileset: Union[RasterTileset, VectorTileset]


class AddDataset(Action):
    """Action payload sent with `add_dataset` calls"""

    type: ActionType = ActionType.ADD_DATASET_TO_MAP
    dataset: Dataset
    auto_create_layers: bool
    center_map: bool


class RemoveDataset(Action):
    """Action payload sent with `remove_dataset` calls"""

    type: ActionType = ActionType.REMOVE_DATASET_FROM_MAP
    uuid: UUID


class ReplaceDataset(Action):
    """Action payload sent with `replace_dataset` calls"""

    type: ActionType = ActionType.REPLACE_DATASET
    dataset: Dataset
    existing_dataset: Dataset


class AddLayer(Action):
    """Action payload sent with `add_layer` calls"""

    type: ActionType = ActionType.ADD_LAYER
    layer: LayerSpec


class RemoveLayer(Action):
    """Action payload sent with `remove_layer` calls"""

    type: ActionType = ActionType.REMOVE_LAYER
    id: str


class RemoveFilter(Action):
    """Action payload sent with `remove_filter` calls"""

    type: ActionType = ActionType.REMOVE_FILTER
    id: str


class SetFilter(Action):
    """Action payload sent with `set_filter` calls"""

    type: ActionType = ActionType.SET_FILTER
    info: FilterInfo


class GetMapConfig(Action):
    """Action payload sent with `get_map_config` calls"""

    type: ActionType = ActionType.GET_MAP_CONFIG


class SetMapConfig(Action):
    """Action payload sent with `set_map_config` calls"""

    type: ActionType = ActionType.SET_MAP_CONFIG
    map_config: MapConfig


class SetSplitMode(Action):
    """Action payload sent with `set_split_mode` calls"""

    type: ActionType = ActionType.SET_SPLIT_MODE
    mode: Literal["single", "dual", "swipe"]
    layers: Optional[List[List[str]]]
