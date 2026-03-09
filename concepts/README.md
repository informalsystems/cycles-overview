# Cycles Conceptual Model

Cycles proposes a new conceptual model and application architecture for finance and settlement. 
The model proceeds from first principles by combining double-entry bookkeeping and graph theory 
in a novel but remarkably simple way. In Cycles, liquidity is a topological property of the graph. 
Cycles thus enables financial applications to be built with a new kind of generalized capital-efficiency - an ability to systematically do more with less. 

Here you will find more details on the core concepts in Cycles:

- [Obligations](./obligations.md)
- [Acceptances](./acceptances.md)
- [Tenders](./tenders.md)
- [Ascertainment](./ascertainment.md)
- [Settlement](./settlement.md)
- [Discharge](./discharge.md)

## Summary


The Cycles model comprises the following set of principles:

1. All agents and currencies are nodes in the graph
2. All nodes are balance sheets
3. All relations between nodes are directed edges in the graph
4. There are two types of edges:
    a. Obligation (from debtor to creditor) - commitment to a past liability
    b. Acceptance (from creditor to debtor) - commitment to a future liability
5. All settlements are cyclic flows in the graph.
6. Settlement of an acceptance spawns an obligation

This is the model motivated and described in the Design section of the Cycles Whitepaper. 
That section is structured around the idea of “4-ways to settle”), 
a fundamental observation about double-entry bookkeeping that seems to have gone largely unnoticed.

Of the six principles above, 1 and 5 represent deep insight into the nature of
the graph. 

*Respect the Graph*
