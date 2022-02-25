from deploy import call_app, get_private_key_from_mnemonic, creator_mnemonic, algod, algod_address, algod_token


algod_client = algod.AlgodClient(algod_token, algod_address)
creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
app_id = "75149535"
app_args = ["Add"]
call_app(algod_client, creator_private_key, app_id, app_args)
