# Ascertainment

Obligations and acceptances are bilateral relations between two counterparties
that need to be agreed to by each counterparty. I can't just declare that you owe
me without your consent. We call this consent *ascertainment*. For an obligation
or acceptance to be valid, it must be *doubly ascertained*, that is, ascertained
by both parties. In practice, ascertainment amounts to a cryptographic signature
over the relevant data. 

Either a debtor or creditor can create an obligation or acceptance, and
ascertain it themselves. But to be valid, the other counterparty must asertain
as well. 

Liquidity Nodes are special nodes in the graph that allow obligations to be
created from them, and acceptances to be created to them, without double
ascertainment. A user can unilaterally create an obligation from a whitelisted liquidity node
to themselves by tendering funds from the shielded pool - effectively moving their funds from the pool to the graph. 
A user can also unilaterally create an acceptance to a liquidity node, allowing
themselves to get paid in that currency in the graph.
