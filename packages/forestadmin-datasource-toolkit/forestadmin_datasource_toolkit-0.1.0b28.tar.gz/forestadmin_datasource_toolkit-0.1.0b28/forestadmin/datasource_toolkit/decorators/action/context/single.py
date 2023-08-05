from forestadmin.datasource_toolkit.decorators.action.context.base import ActionContext
from forestadmin.datasource_toolkit.interfaces.query.projections import Projection
from forestadmin.datasource_toolkit.interfaces.records import CompositeIdAlias, RecordsDataAlias
from forestadmin.datasource_toolkit.utils.records import RecordUtils


class ActionContextSingle(ActionContext):
    async def get_record_id(self) -> CompositeIdAlias:
        projection = Projection().with_pks(self.collection)
        records = await self.get_records(projection)
        return RecordUtils.get_primary_key(self.collection.schema, records[0])

    async def get_record(self, fields: Projection) -> RecordsDataAlias:
        records = await self.get_records(fields)
        return records[0]
