# Settlement

In a graph of obligations and acceptances, every settlement is a cycle in the
graph. We refer to these cycles as **settlement flows**. Any balanced (cyclic)
sub-graph is a valid settlement flow. Settlement flows are computed from the graph by running a flow
algorithm. Thus settlement becomes a graph flow optimization problem, 
and large, multilateral settlements become possible.

We refer to each edge in the settlement flow as a **set-off notice**.
The settlement flow (a balanced batch of set-off notices) can then be applied to the graph on-chain, causing the
relevant obligations and acceptances to be discharged by the specified amount.
For any acceptances discharged, new obligations are spawned in the other
direction. Individual set-off notices must be applied locally to each user's books
off-chain to account for the on-chain settlement of their existing obligations.

Settlement in Cycles is thus the execution of a multilateral settlement flow
against a graph of obligations and acceptances. Each obligation or acceptance
has a corresponding set-off notice that determines how much it was reduced by. 
These set-off notices are legally binding settlement records, just like any other blockchain
payment would be. 

In Cycles, the graph flow optimization algorithm runs off-chain in a *zk-TEE solver* authorized by the protocol.
Obligations and acceptances in the graph are encrypted such that they can be
read by the solver. The solver runs our Multilateral TradeCredit Setoff (MTCS)
algorithm to find an optimal settlement flow. The solver produces a zk-proof
that the flow is correct, encrypts the obligations and acceptances that result
after applying the settlement flow, and broadcasts everything on-chain.

With present cryptographic technology, practical private graph flow optimization
requires Trusted Execution Enclaves (TEEs). Using zk-proofs,
these devices do not need to be trusted for correctness or integrity, but only
for keeping data private to the enclave. Using a light client protocol we can
further restrict the surface area of the TEE as well. See our [Quartz
framework] for more.

[Quartz framework]: https://github.com/informalsystems/quartz

