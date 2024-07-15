"""
The Great Party Voting Event

In a lively village, Party1 hosted a grand event where two friends, Alice and Bob, voted secretly for their favorite option among 0, 1, or 2. The twist? Their votes were kept a secret to add excitement to the event!

Alice voted for 500, and Bob voted for 10. Since these votes didn’t match any of the official options, Party1 needed to figure out which option had the most support. Here’s how they handled it:

Counting Votes:

Option 0: Party1 checked if Alice and Bob voted for 0. Since neither voted for 0, the count for Option 0 was 0.
Option 1: Party1 checked if Alice and Bob voted for 1. Neither vote matched 1, so the count for Option 1 was 0.
Option 2: Finally, Party1 checked if Alice and Bob voted for 2. Neither vote matched 2, so the count for Option 2 was 0.
Deciding the Most Popular Option:

With all options tied at 0 votes, Party1 had to choose a default option to declare as the “most voted” since no option had more votes than the others. They decided to select Option 2 by default.
Announcing the Result:

Despite Alice’s vote of 500 and Bob’s vote of 10 not matching any of the options, Party1 declared Option 2 as the most popular option.

If Alice voted for 0, and Bob voted for 1. Here's how Party1 handled the votes:

Counting Votes:

For Option 0: Alice’s vote matched 0, so Option 0 received 1 vote. Bob’s vote didn’t match 0, so no additional votes for Option 0.
For Option 1: Bob’s vote matched 1, so Option 1 received 1 vote. Alice’s vote didn’t match 1, so no additional votes for Option 1.
For Option 2: Neither Alice nor Bob voted for 2, so Option 2 received 0 votes.
Deciding the Most Popular Option:

Options 0 and 1 each received 1 vote, while Option 2 received 0 votes.
Since Options 0 and 1 are tied, Party1 compared them. Since Option 1 is greater than Option 0 in this case, Party1 chose Option 1 as the most popular.
Announcing the Result:

After tallying and comparing the votes, Party1 declared Option 1 as the most popular choice.
"""
from nada_dsl import *

def nada_main():
    # alice = Party(name="Party1")  # party 0
    # bob = Party(name="Party1")  # party 1
    # charlie = Party(name="Party1")  # party 2

    party1 = Party(name="Party1")

    # Each party votes for an option: 0, 1, or 2
    alice_vote = SecretInteger(Input(name="alice_vote", party=party1))
    bob_vote = SecretInteger(Input(name="bob_vote", party=party1))

    # Count votes for each option
    option_0_votes = (alice_vote == Integer(0)).if_else(Integer(1), Integer(0)) + \
                     (bob_vote == Integer(0)).if_else(Integer(1), Integer(0))

    option_1_votes = (alice_vote == Integer(1)).if_else(Integer(1), Integer(0)) + \
                     (bob_vote == Integer(1)).if_else(Integer(1), Integer(0)) 

    option_2_votes = (alice_vote == Integer(2)).if_else(Integer(1), Integer(0)) + \
                     (bob_vote == Integer(2)).if_else(Integer(1), Integer(0))

    # Determine the most voted option
    most_voted = (option_0_votes > option_1_votes).if_else(
        (option_0_votes > option_2_votes).if_else(Integer(0), Integer(2)),
        (option_1_votes > option_2_votes).if_else(Integer(1), Integer(2))
    )

    return [Output(most_voted, "most_voted_option", party1)]
