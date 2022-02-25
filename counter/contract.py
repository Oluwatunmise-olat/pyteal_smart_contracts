from ast import If
from ensurepip import version
from pyteal import *


def approval_program():
    # Txn -> trabsaction that invoked the smartContract (used to inspect transaction fields)
    # Gtxn[n] -> for griuped transacctions

    scratchCount = ScratchVar()

    add=Seq(
        scratchCount.store(App.globalGet(Bytes("count"))),
        App.globalPut(Bytes("count"), scratchCount.load()+Int(1)),
        Approve()
    )
    deduct=Seq(
        scratchCount.store(App.globalGet(Bytes("count"))),
        If(scratchCount.load() > Int(0), App.globalPut(Bytes("count"), scratchCount.load()-Int(1))
),
        Approve()

    )

    handle_creation=Seq(
        App.globalPut(Bytes("count"), Int(0)),
        Approve()
    )

    handle_op=Seq(
        Assert(Global.group_size()==Int(1)),
        Cond(
            [Txn.application_args[0] == Bytes("Add"), add], 
            [Txn.application_args[0] == Bytes("Deduct"), deduct]
    )
    )
    

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.NoOp, handle_op]

    )

    return compileTeal(program, Mode.Application, version=5)

def clear_state_program():
    return compileTeal(Approve(), Mode.Application, version=5)

# print(approval_program())
# print(clear_state_program())