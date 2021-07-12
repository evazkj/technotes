# Encoding and Evolution

*   In XML and CSV, you can not distinguish between a number and a string that happens to consist of digits
*   JSON and XML supports Unicode characters, but not binary strings.
*   There is optional schema support for XML and JSON
*   CSV doesn't have schema support

### Binary Encoding

*   Thrift, ProtoBuf, Avro
*   Thrift uses a specific `List` fields. In protobuf, use `repeated`. It's possible to change an `optional` to `repeated` 
*   Add an unnecessary required field is NOT OK.
*   Avro:
    *   Write schema can be different with Read schema, they just have to be compatible.
        *   If a field is in write schema but not in reader's schema, will be ignored
        *   If a field is in reader schema, but not in writer's schema, it will use default value
    *   To maintain compatibility, you may only add/remove a field that has a default value
*   Two different designs:
    *   `optional` (protobuf) vs `default value` (avro)
*   Avro is good for:
    *   Large file with lots of records:
    *   Database with individually written data
    *   Sending data over a network connection (Avro RPC)
    *   Avro(compared with Protobuf) doesn't contain any tag numbers, it is friendlier to dynamically generated schemas.
    *   Avro doesn't require code generation like ProtoBuf
*   Merits of binary encoding:
    *   More compact
    *   Schema is a valuable form of documentation
    *   Keeping a database of schemas allows you to check forward and backward comaptibility of schema changes
    *   For statically typed programming languages, the ability of generated code is useful, it enables type checking at compile time.

### Modes of dataflow

*   Via Database
    *   Wrong way to do it!
*   Via services: REST and RPC
    *   RPC flaws
        *   Not as predicatable as local function
        *   Local function either returns a result, or throws an exception or never returns. A network request has another possible outcome: it may return without a result due to a timeout.
        *   It's possible that the response is lost. If you retry, it may be bad unless it's idempotent.
        *   Latency is widely variable.
        *   Encoding/decoding cost.
*   Via message passing
    *   it acts as a buffer, improve system reliability.
    *   It automatically redeliver messages to process that has crashed.
    *   It avoids the sender needing to know the IP address. and port number of the recipient. 
    *   One to many sending.
    *   It logically decouples wht sender from the recipient.
    *   