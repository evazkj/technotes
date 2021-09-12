# Design Craiglist

 Problem description: 

*   design craigslist
*   User could post record in a particular region, of particular category
    *   Video game selling
    *   San Francisco Bay area, South Beach.
*   An email sent to the user to publish the record.
*   After certain time (usually 1 - 2 hours), the post is released
*   Other user could scan through the list
*   Bonus: User could search the records dddd

 

## Solution

*   Business use case:

    *   Search items
    *   posting
    *   Send an email after posting, generate a token for modification

*   Capacity estimation and constraints:

    *   46k zipcode, 10 categories, 200 posts per day
    *   46k x 10 x 200 / 24 / 3600 = ~1000qps peak 5k qps (write)
    *   read is about 100x write, ~500k read
    *   1 SQL server(10k qps), then 50 Database read, 1 DB write
    *   valid for 7 days
    *   Storage:
        *   DB: 2k *1000 * 24 * 3600 * 7 = 1.4T
            *   About 3 SQL primary DB, 6 replicas
        *   S3: 100k * 1000 * 24 * 3600 * 7 = 70T ---- S3

*   Architecture

    *   Client -> https request -> LB -> app servers (stateless, elastic) -> databases

*   API

    *   createPost(postAsJson, email, )

    *   modifyPost(postAsJson, email,)

    *   PostAsJson:

        *   location

        *   description

        *   title

        *   imageURLs

            