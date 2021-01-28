# System Design basics

### building blocks:
  * database, caches, search indexes, stream processing, batch processing
  * example:

![](images/iShot2021-01-28%2011.39.36.png)

  * request success应该在存进primary database的时候就返回
  * 一个team应该不能直接读取另外一个team的db，而是应该通过api，因为会有SLA(service level agreement)

### System design principles:
* reliablility
  * Netflix: chaos monkey
![](images/iShot2021-01-28%2012.12.36.png)
* scalability
* maintainability

## Design twitter:
![](images/iShot2021-01-28%2012.28.09.png)
* slow, 3 Table join

![](images/iShot2021-01-28%2012.29.20.png)

* fan-out mode, popular user cost high.

* hybrid: based on number of followers

