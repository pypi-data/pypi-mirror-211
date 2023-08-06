from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType, Doc
from loguru import logger as log


class SessionsTable (BaseTable):

    norm_table_name = 'sessions'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    norm_ensure = [
        {'index_name': 'by_when'   , 'duplicates': True , 'func': '{when:14.6f}'},
        {'index_name': 'by_sid'    , 'duplicates': False, 'func': '{sid}'},
        {'index_name': 'by_ns'     , 'duplicates': True,  'func': '{ns}'},
    ]

    def from_sid (self, sid, transaction=None):
        self.set(self.norm_tb.seek_one('by_sid', Doc({'sid': sid}), txn=transaction))
        return self


class SessionsCollection (BaseCollection):

    table_class = SessionsTable
    table_strip = ['address', 'sid', 'user_id']

    def flush (self, nsp):
        limit = Doc({'ns': nsp})
        for result in self.filter(index_name='by_ns', lower=limit, upper=limit):
            result.doc.delete()
        return self
