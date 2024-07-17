import asyncio
import py_nillion_client as nillion
import os
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

async def main():
    # 1. Initial setup
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

    seed = "my_seed"
    userkey = UserKey.from_seed(seed)
    nodekey = NodeKey.from_seed(seed)

    client = create_nillion_client(userkey, nodekey)

    party_id = client.party_id
    user_id = client.user_id

    # 2. Store the program
    program_name = "main"
    program_mir_path = f"../nada_quickstart_programs/target/{program_name}.nada.bin"

    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    receipt_store_program = await get_quote_and_pay(
        client,
        nillion.Operation.store_program(program_mir_path),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    action_id = await client.store_program(
        cluster_id, program_name, program_mir_path, receipt_store_program
    )

    program_id = f"{user_id}/{program_name}"
    print("Stored program. action_id:", action_id)
    print("Stored program_id:", program_id)

    # 3. User registration and verification
    print("Registering and verifying users...")
    def register_user(user_type, user_address):
        # Assuming a mapping of user_address to user_type
        users[user_address] = {
            "user_type": user_type,
            "is_verified": False
        }
        print(f"Registered {user_type} with address: {user_address}")

    def verify_user(user_address):
        if user_address in users:
            users[user_address]["is_verified"] = True
        print(f"Verified user with address: {user_address}")

    users = {}
    register_user("sex_worker", "0x8756456245576478678")
    register_user("client", "0x76463424637587577")
    verify_user("0x78567764687695749")
    verify_user("0x76453748579689875")

    # 4. Service listings
    print("Adding services...")
    services = {}

    def add_service(service_id, provider, description, price):
        services[service_id] = {
            "provider": provider,
            "description": description,
            "price": price,
            "is_available": True
        }
        print(f"Added service {service_id} by provider {provider}: {description} for {price} units")


    add_service(1, "0x56328276549493", "Service Description", 100)

    # 5. Booking services
    print("Booking services...")
    bookings = {}

    def book_service(service_id, client):
        service = services[service_id]
        if service["is_available"]:
            bookings[service_id] = {
                "client": client,
                "is_completed": False,
                "is_disputed": False
            }
            service["is_available"] = False
            print(f"Booked service {service_id} by client {client}")

    book_service(1, "0x74433413889799")

    # 6. Secure payments
    print("Completing service and handling payments...")
    def complete_service(service_id):
        booking = bookings[service_id]
        if not booking["is_completed"]:
            service = services[service_id]
            booking["is_completed"] = True
            service["provider"] = nillion.SecretInteger(service["price"])
        print(f"Service {service_id} completed. Payment of {service['price']} units to provider {service['provider']}")

    complete_service(1)

    # 7. Compute result using Nillion
    new_secret = nillion.NadaValues(
        {
            "my_int1": nillion.SecretInteger(90),
        }
    )

    party_name = "Party1"
    permissions = nillion.Permissions.default_for_user(client.user_id)
    permissions.add_compute_permissions({client.user_id: {program_id}})

    receipt_store = await get_quote_and_pay(
        client,
        nillion.Operation.store_values(new_secret, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    store_id = await client.store_values(
        cluster_id, new_secret, permissions, receipt_store
    )
    print(f"Computing using program {program_id}")
    print(f"Use secret store_id: {store_id}")

    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    computation_time_secrets = nillion.NadaValues({"my_int2": nillion.SecretInteger(10)})

    receipt_compute = await get_quote_and_pay(
        client,
        nillion.Operation.compute(program_id, computation_time_secrets),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        computation_time_secrets,
        receipt_compute,
    )

    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
          print(f"✅  Compute complete for compute_id {compute_event.uuid}")
          print(f"🖥️  The result is {compute_event.result.value}")
          #print(type(compute_event.result.value))
          if compute_event.result.value["Staked amount"] == 100:
            print("Amount staked. Please fulfil the agreement to get your staked amount back")
          else:
            print("Staked amount is incorrect. Checking for the details.")
          
          return compute_event.result.value

if __name__ == "__main__":
    asyncio.run(main())
