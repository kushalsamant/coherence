"""
Enhanced Dataclass Patterns with Configuration-Driven Extraction
Inspired by SortDesk's dataclaster library
Provides JSONPath support and type-safe dataclass casting
"""
from dataclasses import dataclass, field, Field
from typing import Dict, Any, List, Optional, Type, TypeVar, Union
from datetime import datetime
import json

try:
    import jsonpath_rw
    JSONPATH_AVAILABLE = True
except ImportError:
    JSONPATH_AVAILABLE = False
    jsonpath_rw = None

from loguru import logger


T = TypeVar('T')


class DataExtractionError(Exception):
    """Exception raised during data extraction"""
    pass


@dataclass
class FieldConfig:
    """Configuration for field extraction"""
    path: str  # JSONPath or simple key path
    required: bool = True
    default: Any = None
    type_cast: Optional[Type] = None


def dcfield(config: FieldConfig = None, **kwargs):
    """
    Dataclass field with extraction configuration
    
    Args:
        config: FieldConfig for data extraction
        **kwargs: Standard dataclass field arguments
        
    Returns:
        Field with metadata for extraction
    """
    metadata = kwargs.get('metadata', {})
    if config:
        metadata['extraction_config'] = config
    kwargs['metadata'] = metadata
    return field(**kwargs)


class JSONCasting:
    """Base class for JSON to dataclass casting"""
    
    @classmethod
    def from_json(
        cls: Type[T],
        json_data: Union[str, dict],
        deserialize: bool = True
    ) -> T:
        """
        Create instance from JSON data
        
        Args:
            json_data: JSON string or dict
            deserialize: If True, deserialize JSON string
            
        Returns:
            Instance of dataclass
        """
        if isinstance(json_data, str):
            if deserialize:
                json_data = json.loads(json_data)
            else:
                raise ValueError("json_data is string but deserialize=False")
        
        if not isinstance(json_data, dict):
            raise ValueError(f"Expected dict, got {type(json_data)}")
        
        # Extract field values using config
        field_values = {}
        annotations = cls.__annotations__ if hasattr(cls, '__annotations__') else {}
        
        for field_name, field_type in annotations.items():
            if field_name.startswith('_'):
                continue
            
            # Get field object
            field_obj: Field = getattr(cls, field_name, None)
            if not isinstance(field_obj, Field):
                continue
            
            # Get extraction config from metadata
            metadata = field_obj.metadata or {}
            config: FieldConfig = metadata.get('extraction_config')
            
            if config:
                # Use configured path
                try:
                    value = cls._extract_value(json_data, config.path)
                    if value is None:
                        if config.required:
                            raise DataExtractionError(
                                f"Required field '{field_name}' not found at path '{config.path}'"
                            )
                        value = config.default
                    else:
                        # Type cast if specified
                        if config.type_cast:
                            value = cls._cast_value(value, config.type_cast)
                        elif field_type != type(value):
                            # Auto-cast based on field type
                            value = cls._cast_value(value, field_type)
                    
                    field_values[field_name] = value
                except Exception as e:
                    if config.required:
                        raise DataExtractionError(
                            f"Failed to extract field '{field_name}' from path '{config.path}': {e}"
                        ) from e
                    field_values[field_name] = config.default
            else:
                # Default: use field name as key
                if field_name in json_data:
                    value = json_data[field_name]
                    # Auto-cast
                    if field_type != type(value):
                        value = cls._cast_value(value, field_type)
                    field_values[field_name] = value
                else:
                    # Use default if available
                    default_value = field_obj.default
                    if default_value != field.MISSING:
                        field_values[field_name] = default_value() if callable(default_value) else default_value
        
        # Create instance
        try:
            return cls(**field_values)
        except TypeError as e:
            raise DataExtractionError(f"Failed to create {cls.__name__} instance: {e}") from e
    
    @classmethod
    def _extract_value(cls, data: Dict[str, Any], path: str) -> Any:
        """
        Extract value from data using path (JSONPath or simple key)
        
        Args:
            data: Dictionary to extract from
            path: JSONPath expression or simple key path (e.g., "key.nested" or "$.key.nested")
            
        Returns:
            Extracted value or None
        """
        if not path:
            return None
        
        # Simple key path (e.g., "key.nested")
        if not path.startswith('$') and '.' in path:
            keys = path.split('.')
            value = data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None
            return value
        
        # JSONPath (if available)
        if JSONPATH_AVAILABLE and path.startswith('$'):
            try:
                jsonpath_expr = jsonpath_rw.parse(path)
                matches = [match.value for match in jsonpath_expr.find(data)]
                if matches:
                    return matches[0] if len(matches) == 1 else matches
                return None
            except Exception as e:
                logger.warning(f"JSONPath extraction failed for '{path}': {e}")
                # Fallback to simple key lookup
                simple_path = path.replace('$', '').replace('.', '').strip('.')
                return cls._extract_value(data, simple_path)
        
        # Simple key lookup
        return data.get(path)
    
    @classmethod
    def _cast_value(cls, value: Any, target_type: Type) -> Any:
        """
        Cast value to target type
        
        Args:
            value: Value to cast
            target_type: Target type
            
        Returns:
            Cast value
        """
        if value is None:
            return None
        
        # Already correct type
        if isinstance(value, target_type):
            return value
        
        # Type is Optional[SomeType]
        if hasattr(target_type, '__origin__') and target_type.__origin__ is Union:
            # Extract non-None types
            args = [arg for arg in target_type.__args__ if arg is not type(None)]
            if args:
                return cls._cast_value(value, args[0])
        
        # String to type
        if target_type == str:
            return str(value)
        elif target_type == int:
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        elif target_type == float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        elif target_type == bool:
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif target_type == datetime:
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                try:
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    pass
            return None
        elif hasattr(target_type, '__origin__') and target_type.__origin__ is list:
            # List type
            if isinstance(value, list):
                # Get item type
                item_type = target_type.__args__[0] if target_type.__args__ else Any
                return [cls._cast_value(item, item_type) for item in value]
            return [value]
        
        # Default: return as-is
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary"""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert instance to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, default=str)


# Example usage classes for plan_data structures
@dataclass
class Room(JSONCasting):
    """Room data with extraction config"""
    id: int
    polygon: List[List[float]]
    room_type: Optional[str] = None
    area: Optional[float] = None
    name: Optional[str] = dcfield(
        config=FieldConfig(path="name", required=False),
        default=None
    )


@dataclass
class Wall(JSONCasting):
    """Wall data with extraction config"""
    id: int
    start_point: List[float]
    end_point: List[float]
    thickness: Optional[float] = None
    wall_type: Optional[str] = dcfield(
        config=FieldConfig(path="type", required=False),
        default=None
    )


@dataclass
class Path(JSONCasting):
    """Path/Pathway data for landscape plans"""
    id: int
    points: List[List[float]]  # Can be straight line or curved path
    path_type: Optional[str] = None  # pedestrian, bike, etc.
    width: Optional[float] = None


@dataclass
class Road(JSONCasting):
    """Road data for landscape/urban plans"""
    id: int
    points: List[List[float]]  # Road centerline or edges
    road_type: Optional[str] = None  # street, avenue, highway, etc.
    width: Optional[float] = None


@dataclass
class Zone(JSONCasting):
    """Zone data for landscape/urban plans (parks, plazas, districts)"""
    id: int
    polygon: List[List[float]]
    zone_type: Optional[str] = None  # park, plaza, district, etc.
    area: Optional[float] = None
    name: Optional[str] = None


@dataclass
class WaterFeature(JSONCasting):
    """Water feature data (ponds, fountains, pools)"""
    id: int
    polygon: List[List[float]]
    feature_type: Optional[str] = None  # pond, pool, fountain, etc.
    area: Optional[float] = None


@dataclass
class Parking(JSONCasting):
    """Parking area data"""
    id: int
    polygon: List[List[float]]  # Parking area boundary
    parking_type: Optional[str] = None  # surface, structured, etc.
    capacity: Optional[int] = None  # Number of spaces if detectable


@dataclass
class BuildingFootprint(JSONCasting):
    """Building footprint for urban plans"""
    id: int
    polygon: List[List[float]]
    building_type: Optional[str] = None
    area: Optional[float] = None


@dataclass
class PlanData(JSONCasting):
    """Plan data structure with extraction config"""
    rooms: List[Room] = dcfield(
        config=FieldConfig(path="rooms", required=False),
        default_factory=list
    )
    walls: List[Wall] = dcfield(
        config=FieldConfig(path="walls", required=False),
        default_factory=list
    )
    # Landscape/Urban elements
    paths: List[Path] = dcfield(
        config=FieldConfig(path="paths", required=False),
        default_factory=list
    )
    roads: List[Road] = dcfield(
        config=FieldConfig(path="roads", required=False),
        default_factory=list
    )
    zones: List[Zone] = dcfield(
        config=FieldConfig(path="zones", required=False),
        default_factory=list
    )
    water_features: List[WaterFeature] = dcfield(
        config=FieldConfig(path="water_features", required=False),
        default_factory=list
    )
    parking: List[Parking] = dcfield(
        config=FieldConfig(path="parking", required=False),
        default_factory=list
    )
    building_footprints: List[BuildingFootprint] = dcfield(
        config=FieldConfig(path="building_footprints", required=False),
        default_factory=list
    )
    scale_ratio: Optional[float] = dcfield(
        config=FieldConfig(path="scale_ratio", required=False),
        default=None
    )
    
    @classmethod
    def from_json(cls, json_data: Union[str, dict], deserialize: bool = True) -> 'PlanData':
        """Override to handle nested list extraction"""
        if isinstance(json_data, str):
            if deserialize:
                json_data = json.loads(json_data)
        
        # Extract top-level fields
        rooms_data = json_data.get('rooms', [])
        walls_data = json_data.get('walls', [])
        
        # Convert nested structures
        rooms = [Room.from_json(room) for room in rooms_data] if rooms_data else []
        walls = [Wall.from_json(wall) for wall in walls_data] if walls_data else []
        
        return cls(
            rooms=rooms,
            walls=walls,
            scale_ratio=json_data.get('scale_ratio')
        )


def parse_plan_data(json_data: Union[str, dict]) -> PlanData:
    """
    Convenience function to parse plan data
    
    Args:
        json_data: JSON string or dict
        
    Returns:
        PlanData instance
    """
    return PlanData.from_json(json_data)

