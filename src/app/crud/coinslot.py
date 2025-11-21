from app.models import CoinSlot
from app.crud.base_crud import CRUDBase


class CoinSlotCrud(CRUDBase):
    """CRUD операции для модели CoinSlot."""


coinslot_crud = CoinSlotCrud(CoinSlot)
