from typing import Any, List

from forestadmin.datasource_toolkit.decorators.action.context.base import ActionContext
from forestadmin.datasource_toolkit.interfaces.query.projections import Projection
from forestadmin.datasource_toolkit.interfaces.records import CompositeIdAlias
from forestadmin.datasource_toolkit.utils.records import RecordUtils


class ActionContextBulk(ActionContext):
    async def get_records_ids(self) -> List[CompositeIdAlias]:
        projection = Projection().with_pks(self.collection)
        records = await self.get_records(projection)
        return [RecordUtils.get_primary_key(self.collection.schema, record) for record in records]

    async def get_records(self, fields: Projection) -> Any:
        return await super(ActionContextBulk, self).get_records(fields)
