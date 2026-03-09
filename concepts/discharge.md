# Discharge

When an obligation or acceptance is reduced, we say it is discharged. 
The primary way to discharge obligations or acceptances is via settlement flows,
as described in the previous section.
However, Cycles allows obligations and acceptances to be discharged directly by users
under certain conditions.

For obligations that were doubly ascertained between two users, only the
creditor can directly discharge. This is equivalent to forgiving the debt, or recording
that it was paid off-chain. However a debtor can discharge the obligation if
they also simultaneously transfer assets in the shielded pool, thereby
paying the obligation without going through a multi-lateral settlement. This is
effectively a normal payment, but it defeats the purpose of having the
obligation in the graph. For tendered obligations (from a liquidity node to a user),
they can be safely discharged via untendering, returning the funds to the user
in the shielded pool. Note that users can technically destroy funds in the graph
by discharging tendered obligations without untendering them - but users always
have the power to burn their on-chain money by sending to inaccessible addresses. 

For acceptances between users, either party can discharge the acceptance (without thus spawning an obligation). 
This is effectively cancelling or reducing the amount of potential credit extended.
