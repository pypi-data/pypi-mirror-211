from typing import Dict, List

from forestadmin.datasource_toolkit.exceptions import DatasourceToolkitException
from forestadmin.datasource_toolkit.interfaces.models.collections import BoundCollection
from forestadmin.datasource_toolkit.interfaces.models.collections import Datasource as DatasourceInterface


class DatasourceException(DatasourceToolkitException):
    pass


class Datasource(DatasourceInterface[BoundCollection]):
    def __init__(self) -> None:
        self._collections: Dict[str, BoundCollection] = {}

    @property
    def collections(self) -> List[BoundCollection]:
        return list(self._collections.values())

    def get_collection(self, name: str) -> BoundCollection:
        try:
            collection: BoundCollection = self._collections[name]
        except KeyError:
            raise DatasourceException(f"Collection '{name}' not found")
        else:
            return collection

    def add_collection(self, collection: BoundCollection) -> None:
        if collection.name in self._collections:
            raise DatasourceException(f"Collection '{collection.name}' already defined in datasource")
        self._collections[collection.name] = collection
