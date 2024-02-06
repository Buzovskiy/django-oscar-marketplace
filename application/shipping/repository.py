from oscar.apps.shipping.repository import Repository as RepositoryCore
from .methods import CORREOS, MRW, ConsultationRequired


class Repository(RepositoryCore):
    methods = (CORREOS(), MRW(), ConsultationRequired())
