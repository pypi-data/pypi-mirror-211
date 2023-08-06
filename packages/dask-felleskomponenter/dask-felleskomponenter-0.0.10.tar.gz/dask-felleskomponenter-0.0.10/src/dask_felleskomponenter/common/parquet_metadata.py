from dataclasses import dataclass, asdict
from typing import List, Optional
from pyproj import CRS


@dataclass
class ColumnMetadata:
    geometry_types: List[str]
    validering: Optional[str] = None
    encoding: str = "WKB"
    crs: str = CRS.from_epsg(25833).to_json()


@dataclass
class ParquetMetadata:
    primary_column: str
    columns: dict
    version: str = "0.0.4"

    def som_dict(self):
        return asdict(self)


def epsg_25833():
    """
    Definerer EPSG 25833/ETRS 89 (crs/coordinate reference system) som PROJJSON
    """

    return CRS.from_epsg(25833).to_json()


def column_metadata(geom_type: str) -> ColumnMetadata:
    return ColumnMetadata(
        geometry_types=[geom_type],
        validering="At geometri er gyldig i henhold til GEOS MakeValid-algoritme"
    )


def parquet_metadata(primary_column: str, geometry_type: str) -> ParquetMetadata:
    return ParquetMetadata(
        primary_column=primary_column,
        columns={primary_column: column_metadata(geometry_type)}
    )
