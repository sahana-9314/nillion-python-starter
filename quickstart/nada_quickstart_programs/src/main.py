from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    transaction1 = SecretInteger(Input(name="my_int1", party=party1))
    transaction2 = SecretInteger(Input(name="my_int2", party=party1))

    # Implementing the Proof of stake concept
    # Stacked amount is fix by the application
    # Both the parties pay agreed amount after the agreement is fulfilled
    # If any of the parties are found to be a counterfriet, the whole staked money is returned to the other person
    
    amount_to_be_staked = 510   #Example
    
    #transaction1 is the money staked by the Customer (to be returned once agreement is fulfiled)
    #transaction2 is the money staked by the Worker (also to be returned)

    total_stake_amount = transaction1 + transaction2


    return [Output(total_stake_amount, "Staked amount", party1)]
