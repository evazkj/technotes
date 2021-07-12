# Desing distributed-crawler

## Goal:
1. High scalability /flexibility in scale
2. Fault tolerant
   1. Idempotent
3. Schema flexible / extensible

## Strategy
* Given a list of whitlisted domains and seed URLs as its input and repeatedly execute the following steps
  * Pick a URL from the unvisited URL list
  * Async crawl the URL
  * Parse the document contents, store, index
  * look for new URLs in the whitelist

## Architecture
![](SystemDesign/images/iShot2021-02-10%2011.59.43.png)
* Scheduler: periodically or on demand trigger new crawling, insert seed URLs.
* Crawler: stateless crawler, async scalable worker.
* Parser: async stateless workder.

* Database choice:


## API
## Data model:
* Raw data:
  uuid, data, iteration
* clean data:
  * HASH(url, iteration) ...
* Record metadata (to guarantee idempotent)
  * id, URL, iteration, **state**, create_time
  * State(Queued, Crawled, Processed, Stuck)
* Iteration Progress:
  * schedule, iteration, start, urls found, stuck, crawled, processed
