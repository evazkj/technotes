* read-modify-write conflicts: use read/write lock. inclusive write + exclusive write (2-phase-locking).
* Relational database is used to guarantee a strong transaction
* Database have to be sharded in order to handle the traffic, the normal shard key is trainID-traveltime

## Main Idea
1. Isolate booking and seat allocation
2. Admin determin how many seats are availabe for G1234
3. The database uses snapshot isolation concurrent control, so read not blocking write and vice versa.
4. ![](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-02-11 11.54.26.png)
5. state[empty, booked, cancelled]
6. Booking table indexed on passenger_id, requerst_id, and route. Primary key is auto increment_id
7. Each book = append one row in the booking table. R/W ratio = 10:1, then 100k QPS can be handled easily by one shard sql.
8. Use a background process to decide who claimed the seats, who is in waitlist, who's out
9. Book canceling: