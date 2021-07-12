# Comments

Nothing can be quite so helpful as a well-placed comment. Nothing can clutter up a module more than frivolous dogmatic comments. Nothing can be quite so damaging as an old crufty comment that propagates lies and misinformation.

The proper use of comments is to compensate for our failure to express ourself in code. 

So when you find yourself in a position where you need to write a comment, think it through and see whether there isn’t some way to turn the tables and express yourself in code.

```JAVA
  // Check to see if the employee is eligible for full benefits
  if ((employee.flags & HOURLY_FLAG) &&
    (employee.age > 65))
```

Or this?

```java
  if (employee.isEligibleForFullBenefits())
```

## Good Comments:

*   Legal Comments

*   Informative comments

    ```java
    // Returns an instance of the Responder being tested.
    
       protected abstract Responder responderInstance();
    ```

    

    ```java
       // format matched kk:mm:ss EEE, MMM dd, yyyy
    
       Pattern timeMatcher = Pattern.compile(
    
         “\\d*:\\d*:\\d* \\w*, \\w* \\d*, \\d*”);
    ```

*   Explanation of intent

    ```java
       public void testConcurrentAddWidgets() throws Exception {
    
         WidgetBuilder widgetBuilder =
    
           new WidgetBuilder(new Class[]{BoldWidget.class});
    
           String text = ”’’’bold text’’’”;
    
           ParentWidget parent =
    
             new BoldWidget(new MockWidgetRoot(), ”’’’bold text’’’”);
    
           AtomicBoolean failFlag = new AtomicBoolean();
    
           failFlag.set(false);
    
       
    
           //This is our best attempt to get a race condition
    
           //by creating large number of threads.
    
           for (int i = 0; i < 25000; i++) {
    
             WidgetBuilderThread widgetBuilderThread =
    
               new WidgetBuilderThread(widgetBuilder, text, parent, failFlag);
    
             Thread thread = new Thread(widgetBuilderThread);
    
             thread.start();
    
           }
    
           assertEquals(false, failFlag.get());
    
         }
    ```

*   Clarification: Sometimes it is just helpful to translate the meaning of some obscure argument or return value into something that’s readable.

    ```java
         assertTrue(a.compareTo(a) == 0);    // a == a
    
         assertTrue(a.compareTo(b) != 0);    // a != b
    
         assertTrue(ab.compareTo(ab) == 0);  // ab == ab
    ```

*   Warning of consequences

    ```java
       public static SimpleDateFormat makeStandardHttpDateFormat()
    
       {
    
         //SimpleDateFormat is not thread safe,
    
         //so we need to create each instance independently.
    ```

*   TODO comments

*   Amplification: A comment may be used to amplify the importance of something that may otherwise seem inconsequential

## Bad Comments

*   Mumbling: hard to understand

*   Redundant Comments:

    ```java
       // Utility method that returns when this.closed is true. Throws an exception
    
       // if the timeout is reached.
    
       public synchronized void waitForClose(final long timeoutMillis) 
    ```

*   Misleading Comments

*   Mandated Comments: It is just plain silly to have a rule that says that every function must have a javadoc, or every variable must have a comment. Comments like this just clutter up the code, propagate lies, and lend to general confusion and disorganization.

*   Journal Comments: Sometimes people add a comment to the start of a module every time they edit it. These comments accumulate as a kind of journal, or log, of every change that has ever been made.

*   Noise Comments:

    ```java
       /**
    
        * Default constructor.
    
        */
    
       protected AnnualDateRule() {
    
       }
    ```

*   Position Marker

    ```java
     // Actions //////////////////////////////////
    ```

*   Closing Brace Comments

    Sometimes programmers will put special comments on closing braces, as in Listing 4-6. Although this might make sense for long functions with deeply nested structures, it serves only to clutter the kind of small and encapsulated functions that we prefer. So if you find yourself wanting to mark your closing braces, try to shorten your functions instead.

*   Attributions and Bylines

    ```java
     /* Added by Rick */
    ```

*   Commented-Out Code: Others who see that commented-out code won’t have the courage to delete it. They’ll think it is there for a reason and is too important to delete.

*   Nonlocal Information: If you must write a comment, then make sure it describes the code it appears near. Don’t offer systemwide information in the context of a local comment. 

    ```java
       /**
    
        * Port on which fitnesse would run. Defaults to 8082.
    
        *
    
        * @param fitnessePort
    
        */
    
       public void setFitnessePort(int fitnessePort)
    
       {
    
         this.fitnessePort = fitnessePort;
    
       }
    ```

*   Too much information: Don’t put interesting historical discussions or irrelevant descriptions of details into your comments

*   

