"""Models related to measurement data."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Union

from bson.objectid import ObjectId
from mongoengine import DateTimeField, Document, EnumField, ReferenceField, StringField, signals


@dataclass
class Setting:
    """Setting model.

    A Setting represents a single setting in a Settings document.

    Attributes:
        value (str | float): The value of the setting
        unit (str): Optionally contains the unit of the setting.
    """

    value: str | float
    unit: str | None = None


class Settings(Document):
    """Settings database model.

    The settings document has a fairly dynamic schema. Each settings
    document contains a test case name and a time. Documents also
    contain other keys, which are names of settings. These keys have
    values of type ``Setting``.

    The dynamic schema requires a workaround to make usable. MongoEngine
    does not support unknown keys having values of a known type. The
    ``post_init`` method is used to initialize these.

    Attributes:
        test_case (str): The name of the test case.
        time (datetime): The time the test was run.
        settings (dict[str, Setting]): The settings associated with the
            test.
    """

    meta = {"strict": False, "db_alias": "data"}

    test_case: str = StringField(required=True)
    time: datetime = DateTimeField(required=True)
    settings: dict[str, Setting]

    @staticmethod
    def post_init(sender: type, document: "Settings", **kwargs: Any) -> None:
        """Initialize dynamic settings."""
        document.settings = {}

        for name, setting in document._data.items():
            try:
                document.settings[name] = Setting(**setting)
            except TypeError:
                pass


# Enable the post_init callback for Settings objects
signals.post_init.connect(Settings.post_init, sender=Settings)


class DataType(Enum):
    """Data type enum."""

    NUMERIC = "numeric"
    XY_PLOT = "xy_plot"
    ARRAY = "array"


# TODO: to polars df
class Data(Document):
    """Database model for the data document.

    The data document has three sub types: numeric, array and xy-plot.
    The ``resolve`` method is used to get the specialized model, with
    relevant fields for the specific document type.

    One way to implement this would be to use subclasses. Unfortunately
    MongoEngine support for this is not quite flexible enough to fit
    the existing db schema. MongoEngine internally uses a ``_cls``
    attribute to discriminate subclasses stored in the same collection.
    The schema stores this information in the ``type`` attribute. Since
    MongoEngine lacks support for using a different discriminator field,
    a custome ``resolve`` method is needed to do this.

    MongoEngine also defaults to using the ``_cls`` attribute in
    queries, which made Data.objects return an empty query set.

    This is solved by using data classes for the specialized data models
    which are not subclasses of this class. Doing this avoid the issues
    with MongoEngine subclasses.

    Attributes:
        settings (Settings): Settings document model.
        name (str): Name of data document
        type (DataType): One of ``numeric``, ``array``, ``xy_plot``.

    Examples:
        Resolving a Data object:

        >>> Data.objects.get(type="xy_plot").resolve()
        XyPlot(x=[...], y=[...])
    """

    meta = {"strict": False, "db_alias": "data"}

    settings: Settings = ReferenceField(Settings, required=True, db_field="settings_id")
    name: str = StringField(required=True)
    type: DataType = EnumField(DataType, required=True)

    def resolve(self) -> Union["NumericData", "ArrayData", "XyData"]:
        """Resolve to one of NumericData, XyData, ArrayData."""
        props = {k: self[k] for k in self} | self._data

        match self.type:
            case DataType.NUMERIC:
                return NumericData(data=self, **props)
            case DataType.XY_PLOT:
                return XyData(data=self, **props)
            case DataType.ARRAY:
                return ArrayData(data=self, **props)
            case _:
                raise TypeError(f"Could not resolve data, unknown data type: {self.type}")


@dataclass(kw_only=True)
class BaseData:
    """Base class for data specializations.

    Attributes:
        data (Data): a reference to the ODM object.
        id (ObjectId): the id of the data document.
        settings (Settings): the settings document associated with the
            data instance.
        name (str): the name of the data document.
        type (DataType): One of ``numeric``, ``array``, ``xy_plot``.
    """

    data: Data
    id: ObjectId
    settings: Settings
    name: str
    type: DataType


@dataclass(kw_only=True)
class NumericData(BaseData):
    """Numeric data model.

    Attributes:
        value (float): the value of the data point.
        unit (str | None): optionally, the unit of the data.
    """

    value: float
    unit: str | None = None


@dataclass(kw_only=True)
class ArrayData(BaseData):
    """Array data model.

    Attributes:
        value (list[float]): the list of values.
        unit (str | None): optionally, the unit of the data.
    """

    value: list[float]
    unit: str | None = None


@dataclass
class Marker:
    """Plot marker.

    Attributes:
        text (str): Marker description.
        x (float): x coordinate of marker.
        y (float): y coordinate of marker.
    """

    text: str
    x: float
    y: float


@dataclass(kw_only=True)
class XyData(BaseData):
    """XY plot data model.

    Attributes:
        x (list[float]): x sequence.
        y (list[float]): y sequence.
        x_unit (str | None): Optional unit of x axis.
        y_unit (str | None): Optional unit of y axis.
        markers (list[Marker]): List of markers
    """

    x: list[float]
    y: list[float]
    x_unit: str | None = None
    y_unit: str | None = None
    markers: list[Marker] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Post initialize xy data.

        Convert marker dicts to Marker objects.
        """
        # Before post_init self.markers is a list of marker dicts.
        self.markers = [Marker(**marker) for marker in self.markers]  # type: ignore
