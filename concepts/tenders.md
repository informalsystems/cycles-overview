# Tenders

The basic primitives in the Shielded Graph are Obligations and Acceptances.
There is no direct notion of coins. However coins can always be represented as
an obligation from the coin's "liquidity node". Thus for each coin type, we
create a special "liquidity node" in the graph specific to that coin. The
posession of some coins by a user is represented by an obligation from the
relevant liquidity node to that user's address. Users can also express their willingness
to accept a given coin in payment via an acceptance from their address to the
liquidity node. 

We already saw this in the previous figure about obligations and acceptances with bank
money. Here we have the same idea, but replace the Bank with a USDC liquidity
node and add some more participants:

![Tender](../imgs/tender.png)

In Cycles, the obligation from the USDC node to Alice is what we would call tendered funds,
since they are available for settlement. We also refer to it as a tendered
obligation. The tendered obligation, together with the acceptance, allow us to
form a cycle out of what would otherwise just be a chain. Thus Cycles can settle
all the obligations, and transfer Alice's funds to Carol, without Alice and
Carol having anything to do with one another. A small amount of tendered funds can thus help 
clear a much larger amount of debt in the network. 
Tenders and acceptances help dramatically in the creation of larger cycles. 

Coins from the Shielded Pool can be transferred into the Shielded Graph via 
a **Tender** action. Once tendered, the coin seizes to exist in the
shielded pool as a coin and instead exists in the shielded graph as an
obligation from the coin type's liquidity node to the user's address. 
Funds can be removed again from the graph back into the
pool via the **Untender** action.

Tendering funds thus makes them available to participate in clearing - they can
be used as part of a multilateral cycle to settle the user's obligations.
Tendering dramatically increases the potential liquidity saving for everyone. Ultimately,
users who tender funds should be rewarded for the additional liquidity saving
they make possible. Tendering funds is thus a major form of liquidity
provisioning in Cycles.
