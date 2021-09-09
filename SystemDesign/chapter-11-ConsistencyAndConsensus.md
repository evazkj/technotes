# Consistency and Consensus

## Linearizability

*   Linearizability情况下，用户貌似只跟一个replica打交道，刚刚写入的值，现在肯定能读到。
*   将所有的用户的所有读写行为放到一个时间轴上，没有逻辑上的错误。
*   Behaves like there's only a single copy of the data and all operations on it are atomic

### Implementing linearizable systems

*   Single-leader replication: potentially linearizable if read from leader or syncly updated followers.
*   Consensus algorithm: linearizable
*   Multi-leader replication: not linearizable
*   Leaderless-replication: possibly not linearizable

## Orders

*   ​	The causal order is not a total order
    *   Linearizability: in a linearizable system, we have a total order of operations.
    *   Causality: Two events are ordered if they are causally related, but they are incomparable if they are concurrent. This means causality defines a partial order, not a total order. 

## Distributed Transactions in Practice

在现实中，有两种意义上的distributed transaction

1.   Database-internal distributed transaction： 比如mySQL，所有node都运行同样的software
2.   Heterogenous distributed transactions: 在多种不同的middleware中实现transaction

*   exact-once message processing
    *   比如有个message queue的side effect是发送一个email，同时写到db里一个log，并且commit一个offset。理想状态下，我们希望这两个operation是一个transaction
    *   但是“发email"这个动作并不支持2PC
*   综上， 我们可能需要一种跨系统的transaction protocol

## Consensus

state of the art algorithm: Raft https://raft.github.io/

