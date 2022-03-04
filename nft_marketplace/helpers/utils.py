from abc import ABC, abstractmethod
from pyteal import *
from algosdk.future import transaction

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
        escrow_address = Bytes("ESCROW_ADDRESS") #byteslice (addr)
        asa_id = Bytes("ASA_ID") #unit64
        asa_price = Bytes("ASA_PRICE") #unit64
        asa_owner = Bytes("ASA_OWNER") #byteslice (addr)
        app_state = Bytes("APP_STATE") #unit64
        app_admin = Bytes("APP_ADMIN") #byteslice

    class AppMethods:
        initialize_escrow = Bytes("initializeEscrow")
        make_sell_offer = Bytes("makeSellOffer")
        buy = Bytes("buy")
        stop_sell_offer = Bytes("stopSellOffer")

    class AppState:
        not_initialized = Int(0)
        active = Int(1)
        selling_in_progress = Int(2)

    def initialize_escrow(self, escrow_address):
        pass

    def make_sell_offer(self, sellprice):
        pass

    def buy(sell):
        pass

    def stop_sell_offer(sell):
        pass

    @property
    def global_schema(self):
        return transaction.StateSchema(num_units=3, num_byte_slices=3)

    @property
    def local_schema(self):
        return transaction.StateSchema(num_units=0, num_byte_slices=0)

    def app_initialization(self):
        # app deployment
        return Seq(
            [
                Assert(Txn.application_args.length() == Int(0)),
                App.globalPut(self.GlobalVar.app_admin, Txn.sender()),
                App.globalPut(self.GlobalVar.app_state, Txn.application_args[1]),
                App.globalPut(self.GlobalVar.asa_id, Txn.assets[0]),
                App.globalPut(self.GlobalVar.asa_owner, Txn.application_args[0]),
            ]
        )


