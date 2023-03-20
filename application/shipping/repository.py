from oscar.apps.shipping.repository import Repository as RepositoryCore
from .methods import GLS, DPD, ConsultationRequired


class Repository(RepositoryCore):
    methods = (GLS(), DPD(), ConsultationRequired())
