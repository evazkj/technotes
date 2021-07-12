# Design Youtube

## High level components:

---

 1.    Videal updload, processing, view

 2.    Metadata management (include.user, # of views, likes, watching history, comment, channel, follow)

 3.    Streaming

 4.    Video recommendation

       ![iShot2021-07-08 11.28.41](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-07-08 11.28.41.png) 

       *   Video is chopped into 2-sec clips

       *   stores the video clips into S3 along with metadata
       *   return True after upload, compress, stored, metadata processes
       *   Then video with be processes, generate thumbnail, index the video to make it searchable

## API

---

### Public

*   `uploadVideo(api_dev_key, video_title, video_description, tags[], category_id, default_language, recording_details, video_contents)`
    *   Api_dev_key is per registered account, used to limit quota
    *   Video_contents: location of the video, it will build a socket for file transfering
*   `SearchVideo(search_query, user_location, maximum_videos_to_return, page_token)`
*   `getVideo(user_id, user_context, video_id, offset)`

### Private

*   `generateThumbnail(video_id)`
*   `storeThumbnail(video_id, image)`
*   `indexVideo(video_id)`

## Data Model

---

*   Video storage SQL +  S3 table
    *   Primary key = (video_id + clip_id + resolution)

![iShot2021-07-08 11.53.57](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-07-08 11.53.57.png)

*   Elastic Search Index

    *   each video is processed as a bag of words, similar to articles or webpages, use inverted index to index the video and BM25 to search the relevant videos. give terms and criteria, the elastic search will return the highly relevant video and then filter based on the other criterias like video length, upload time etc

*   Video metadata SQL table:![iShot2021-07-08 12.12.00](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-07-08 12.12.00.png)

    State could be one of the following {NEW, UPLOADED, AVAILABLE, DELETED_PENDING, DELETED, STREAMING*}, new is when the user starts uploading a video. When the video is uploaded, compressed, broken down and stored, the service changes the state into UPLOADED, async triggered the video post processing. When the video is indexed in the search engine and passed all other checks(e.g. safety check), the service changed the state back to the AVAILABLE. When the user deletes the video, the state will be changed to DELETED_PENDING, the search engine will un-index the video and then change it to DELETED. STREAMING will be explained in the stream section.

## Community

---

[![img](https://lh3.googleusercontent.com/avf74-Anf0dIK5fwGmQPmDT2rjltfFvarCNdsHpHTrcXnOFiSCgZ8jPn8oMCRv4iLE9qsSqmf-5J3-TV-6dJdha_7s46OaUh34q2tsfdpgAAl3q0w07YNvceZgskW_Drnw)](https://app.lucidchart.com/documents/edit/7ba6cf67-b348-4dbe-bdad-cb49bfe5b11c/0?callback=close&name=docs&callback_type=back&v=440&s=593)



*   Popularity service in charge of the views, likes, dislikes of the video, likes and dislikes of the comments. The popularity service will periodically read all user activity logs and update the likes/views etc.
*   Popularity has massive read / write but ok with small chance of data loss, therefore use redis to store the data and async write back to DB.
*   All light weight(small data loss OK) activity go to the user activity logs kafka, that includes, view video clips, leave video pages, like a video etc.The view of video will update view history and popularity separately.
    *   One caveat is read after write could be inconsistent, either cached in the client side or read also from the last few seconds logs.
*   主要观点就是把activity放进kafka topic，创建多个async的service来处理，比如history(写进用户的history里), popularity(统计video被观看数), 这样带来的一个问题就是因为是async，后续操作的完成有可能有延迟，比如用户看了视频，但是在history中看不到，有一个方法就是在client端cache

## Comment

---

*   Comment:AddComment(video_id, user, parent_comment_id, reply_to_user, comment)Create timestamp will be added by the server
*   UpdateComment(video_id, user, comment_id, comment)Edit timestamp will be added by the server.

![iShot2021-07-12 11.46.38](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-07-12 11.46.38.png)

## Recommendation system

---

[![img](https://lh6.googleusercontent.com/hj4LaH7gVY6CgIBrtdVrY50xFVfWuWPKujLW1Ly_nS_uVfDCtCbyRIGakP7105OcMyuPKosBQ79qFy0RPnvbVG_21Uigj1k_-oy3VwlaQ7t_JULw4hycH2NsRwE_nVC8lA)](https://app.lucidchart.com/documents/edit/795bca23-8c30-42a5-81cf-f7676c03205d/0?callback=close&name=docs&callback_type=back&v=465&s=595.4399999999999)

*   Every video is labeled with several tags, it could be done automatically or manuallySystem design, news, stock, yu qian, classical music, civ 6, food etc.Some less popular page could be classified badly (bridge)
*   User preference profile could be built on top of user view/like/dislike of video ids. Then based on weight, an user profile could be built
    *   Scott: food:5.4, civ 6: 1.3, yu qian: 0.9, system design:2.8 
*   A separate service could rank video by popularity from the popular service. Based on tags and the most popular video, a list of recommendations could be generated.
*   Collaborative filtering could be also used to do video recommendations.
*   The generated personal recommendations will be stored and saved in the database. When user login to the youtube page, the recommendations will render the page then.

## Streaming

Features: Trending video / topics / streaming / live chat. 

Trending Video / Topics could be done by adding a flink, realtime stateful computation on top of data stream(user activities) to calculate.

Streaming requires prefill the metadata, thumbnail (if wanted), to make the stream searchable. the data is piped through the websocket to the server and then the server broadcasts **the video clip bundled with the pointer to the next video clip**.

Users fresh open the page will get the current clips and then subsequent reads will be based on the next video clip pointer, no need to request it from the server.If a connection is lost, reconnect to get the current clip url. 

Sending of live chat will be temp stored, bundled with video clip id.When the streamer streams the video, the live chat within a certain time threshold (< 5 seconds) will be displayed back asap. Viewers will watch the stream with a few seconds latency, therefore the live chat will be precisely displayed when the other user sends it.

