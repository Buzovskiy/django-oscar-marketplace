from oscar.apps.shipping.repository import Repository as RepositoryCore
from .methods import CORREOS, MRW


class Repository(RepositoryCore):
    methods = (CORREOS(), MRW())
