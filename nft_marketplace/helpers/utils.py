from abc import ABC, abstractmethod
from pyteal import *


class InftMarketPlace(ABC):

    @abstractmethod
    def initialize_escrow(self, escrow_address):
        pass

    @abstractmethod
    def make_sell_offer(self, sellprice):
        pass

    @abstractmethod
    def buy(sell):
        pass

    @abstractmethod
    def stop_sell_offer(sell):
        pass


class NftAsc(InftMarketPlace):
    class GlobalVar:
        escrow_address = Bytes("ESCROW_ADDRESS")
        asa_id = Bytes("ASA_ID")
        asa_price = Bytes("ASA_PRICE")
        asa_owner = Bytes("ASA_OWNER")
        app_state = Bytes("APP_STATE")
        app_admin = Bytes("APP_ADMIN")

    def initialize_escrow(self, escrow_address):
        pass

    def make_sell_offer(self, sellprice):
        pass

    def buy(sell):
        pass

    def stop_sell_offer(sell):
        pass


