from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction
import base64
from contract import approval_program, clear_state_program

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
creator_mnemonic = "amount hour sugar trend carbon fun very adapt hint avoid cube blossom limit vibrant chair elegant page crush egg unhappy comic food save about file"
# buyer wallet

# helper function to compile program source


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

# helper function that converts a mnemonic passphrase into a private signing key


def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key

# helper function that waits for a given txid to be confirmed by the network


def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

# helper function that formats global state for printing


def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        formatted_key = base64.b64decode(key).decode('utf-8')
        if value['type'] == 1:
            # byte string
            if formatted_key == 'voted':
                formatted_value = base64.b64decode(
                    value['bytes']).decode('utf-8')
            else:
                formatted_value = value['bytes']
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted

# helper function to read app global state


def read_global_state(client, app_id):
    app = client.application_info(app_id)
    print(app, "global sttate")
    global_state = app['params']['global-state'] if "global-state" in app['params'] else []
    return format_state(global_state)


def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):
    sender = account.address_from_private_key(private_key)
    on_complete = transaction.OnComplete.NoOpOC.real
    params = client.suggested_params()
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete,
                                           approval_program, clear_program,
                                           global_schema, local_schema)
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    client.send_transactions([signed_txn])

    wait_for_confirmation(client, tx_id, 5)

    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id

# call application
def call_app(client, private_key, application_id, app_args) :
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, application_id, app_args)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id, 5)

    print("Application called")

def main() :
    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1
    global_bytes = 0
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # compile program to TEAL assembly
    with open("./approval.teal", "w") as f:
        approval_program_teal = approval_program()
        f.write(approval_program_teal)

    # compile program to TEAL assembly
    with open("./clear.teal", "w") as f:
        clear_state_program_teal = clear_state_program()
        f.write(clear_state_program_teal)

    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying Counter application......")

    # create new application
    app_id = create_app(algod_client, creator_private_key, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    # read global state of application
    print("Global state:", read_global_state(algod_client, app_id))

    print("--------------------------------------------")
    print("Calling Counter application......")
    app_args = ["Add"]
    call_app(algod_client, creator_private_key, app_id, app_args)

    # read global state of application
    print("Global state:", read_global_state(algod_client, app_id))


main()