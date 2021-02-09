# Design Slack
## System design phases:
1. business/common sense
2. constraints
3. architecture
4. API design
5. DB choice
6. Data model

## Slack system requirement
1. Domain/group/individual chat/msg
2. link preview
3. multimedia msg
4. msg notification
5. highlight unread msg

* 面试时考虑缩减feature，找出mvp feature和bonus feature

## Features reorganized
* MVP features: direct msg, group chat, multimedia msg, link preview
* Goal: high available/reliability/consistency, real-time
* Bonus features: group membership, msg notification, highlight unread msg
* Non-goal: authentication, mobile/web client

## Calculation
* 假设DAU是10M, peak direct message: 5 * 10M * 100 / 86400 = 50k msg/s
* one msg: 100 bytes
* Throughput: 100 MB?
* Storage: 100Mb * 86400 = 10TB
* group chat: 1000 members in a group

## Architecture & database
* use SQL db (add cache):
  * account service: manage user account info
  * friends service: 不用graph model, 它适合friends of friends case
  * group service:
* CDN/S3
    * media service
* DAX（dynamo的cache)/REDIS -> amazon dynamoDB(支持horizontal scale)
    * msg storage service
    * 因为msg是时间序列，有一个cache非常必要
* messaging: Kafka
  * notification service
* message search service
  * Elastic search
* channel service -> redis
* Emoji response service -> redis

## API
Use RPC(such as Apache Thrift, JRPC， RestfulAPI)
### channel service(central service)
* GetChannels(user_id):
  * Store last viewed channel
  * store visible channels
  * show unread msg/last msg preview
* SendMsg(sender_id, receiver_id, msg_type, msg, media_id)
  * msg_type: direct/group msg
  * create_timestamp, update_timestamp, expired_time, state will be appended by channel service
  * STATE could be one of (received, sent, viewed, notification_sent, deleted)
    * Received: some multimedia msg may need to be pre-processed before sending
* updateMessage(msg_id, msg)
* uploadFile(...)
* lookupEntity(user_id)
* joinGroup(user_id, group_id)
* getDirectMessage(user_id, friend_id)
* getGroupMsg(user_id, group_id)
* CRUD for group/user info

### Media service
* processMedia(media_id)
  * replicate_media
  * post-processing
  * distributed to CDN

### Notification Service:
* notifyUser(user_id, sender_id, message_id, msg_preview)
  * Either used database or kafka
  * Exactly once if difficult, requiring two phase commit
