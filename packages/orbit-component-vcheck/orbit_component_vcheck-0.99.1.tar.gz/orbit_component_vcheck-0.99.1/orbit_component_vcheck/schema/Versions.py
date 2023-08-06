from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType, Doc
from orbit_component_vcheck.schema.Sessions import SessionsCollection, SessionsTable
from orbit_component_vcheck.schema.Users import UsersTable
from datetime import datetime
from loguru import logger as log


class VersionsTable (BaseTable):

    norm_table_name = 'versions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_product', 'func': '{product}'},
    ]

    @property
    def last_seen (self):
        return datetime.utcfromtimestamp(self._when).strftime('%Y-%m-%d %H:%M:%S')

    def from_product (self, product, transaction=None):
        self.set(self.norm_tb.seek_one('by_product', Doc({'product': product}), txn=transaction))
        return self


class VersionsCollection (BaseCollection):

    table_class = VersionsTable
    table_methods = ['get_ids']

    async def get_version (self, product, version):
        log.error(f"get_version: {product} => {version}")
        doc = VersionsTable().from_product(product)
        if doc.isValid:
            doc = SessionsTable().from_sid(self._sid)
            if not doc.isValid:
                log.error(f'SESSION IS INVALID: {self._sid}')
                return {'ok': False, 'error': 'invalid session' }
            else:
                doc.update({'product': product, 'version': version}).save()
            doc = UsersTable().from_key(self._session.get('host_id'))
            if not doc.isValid:
                log.error(f'USER IS INVALID: {self._session.get("host_id")}')
            else:
                doc.update({'version': version}).save()
            return {'ok': True, 'version': doc._version}
        return {'ok': False, 'error': 'Failed to find product in version table'}

