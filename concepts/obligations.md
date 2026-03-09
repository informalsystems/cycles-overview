# Obligations

In the Cycles Shielded Graph, the basic objects are not coins but 
rather commitments to liabilities in the past and the future. 
We call a commitment to a liability in
the past an **obligation** and a commitment to a liability in the future an
**acceptance**. Sometimes we will refer to obligations and acceptances jointly as
**graph notes**. Let's start with obligations.

An obligation has a creditor, a debtor, and an amount. It is an asset to
its creditor and a liability to its debtor. We can think of it as an arrow,
representing an amount owed from debtor to credit. 

Fulfillment of an obligation is called **settlement**. 
When an obligation is settled we say that it has been **discharged** - it's
value has been reduced. Discharge can be full or partial.

The foundational insight of Cycles is that obligations that form a closed loop
can be discharged up to the smallest obligation in the cycle, reducing the gross
amount of money actually needed to fully settle them:

![Obligations](../imgs/obligations.png)

Note that the smallest obligation was fully discharged, while the other two were
partially discharged. This is a simple example of size 3, but closed loops like this can come in any size.
We call this kind of settlement **clearing** because the obligations are reduced
("cleared") without the use of any money.

While this is powerful already, we can make Cycles much more powerful by
incorporating a second basic primitive, **acceptances**.





