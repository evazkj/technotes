# Design recommendation system

Create a recommendation system similar to toutiao, recommend personal news to individual users:

*   Support news publishing from selected users
*   Ingesting news from other news websites 
*   Classify the news 
*   Analysis user behavior
*   Recommend the related news to the right user based on user behavior

Key discussion points:

1.   Where to store raw news: key-value store, like DynamoDB
2.   Timeliness
3.   Recommendation
4.   Deduplication
5.   Online-offline
6.   Words processing



### Dimensions for recommendation

1.   Item-based
     1.   News popularity
     2.   Publisher's credibility
     3.   Timeliness Decay
2.   Content-based filtering:
     1.   User's engagement with publisher
     2.   relevance with user's preferred topics
3.   Collaborative filtering
     1.   similar user