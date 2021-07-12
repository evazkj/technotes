# case-study-design-leetcode

https://docs.google.com/document/d/1MgoMz8McpZAmAq_hJfn1topocHqfmAhcbqq42zJEMsY/edit

### Business: 10 mins

*   User could view a list of problems
*   User could select language of his choice and submit code
*   User receive proper error code upon failures
*   User could define the input cases and expected outcomes.
*   User could view past submissions 
*   User could view runtime distribution
*   New! User could debug the code in the console.

### Constraints: 10 mins

*   Goal:High scalable in scale High available.
*   Constraints:Capped at 200ms / 200MB 
    *   CPU bounded system.100k daily users
    *   10 submission per user 1m submission / day -> 200,000s computing time per day = 3 dockers/VM. 
    *   Considering peak to normal ratio as 3 then, we need 6 - 9 dockers during peak time.

### Arch

[![img](https://lh4.googleusercontent.com/PthqD8-iCNtgG8l2hc3mjAXB5LrcEfdvH9gIkdzV12M940sHJICwhXS4LHxoRpt86o5MxxIOozAfo8YmZI0xpvO1uQHVnQc9POYLvKNLdSQug98qNc5qLz2_59kxULQQ8A)](https://app.lucidchart.com/documents/edit/35557445-0aeb-4e8f-8990-2b77a39a5ff3/0?callback=close&name=docs&callback_type=back&v=367&s=594)

*   No single point of failure, all modules have > 2 nodes. User service and Compute service are stateless. API gateway may contain active user token. If the API gateway is down, users may be forced to re login. Token lookup could be done as a look aside in-memory database as well(redis or memcache).
*   Online compile is just submitting complete code including wrapper code to a serverless node, like AWS lambda. However this could be done by webassembly and compute in the browser instead.
*   The data is very much smaller compared to other services we defined in the past, using a SQL with backup should address all the requirements.
*   Compute service is the heavy lifting part, using worker pool and async processing to decouple with work load bursts. Put a limit on code size and whole customized code could be put in the message(<20k max message size)
*   Security check is critical for the site. No file / database / network / socket access should be granted for any user submitted code. Output size should be capped at a certain threshold. Zip bomb?

### API

**getProblems(user_token, session_id)**Return a list of problems titles with markers done or not.
**submitCode(user_token, problem_id, code, language_id, session_id)**Once code submitted, a submission_id will be returned, the client will poll the result periodically to get the status.

### Datamodel

User table...

Session Table...

Submission Table:(**Sql row size is 8kb. Code can’t be store directly here**), Mongo document size is 16MB, better not store the state /runtime stats with the code.

![iShot2021-07-12 15.35.31](/Users/khang306/Documents/technotes/SystemDesign/images/iShot2021-07-12 15.35.31.png)

