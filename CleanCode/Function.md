# Function

## 1. Small!

*   The first rule of functions is that they should be small.The second rule of functions is that *they should be smaller than that*.

### **Blocks and Indenting**

*    The blocks within `if` statements, `else` statements, `while` statements, and so on should be one line long. Probably that line should be a function call. Not only does this keep the enclosing function small, but it also adds documentary value because the function called within the block can have a nicely descriptive name.

*    **Functions should not be large enough to hold nested structures**:  Therefore, the indent level of a function **should not be greater than one or two.** This, of course, makes the functions easier to read and understand.

## 2. Do one thing

*   **FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL. THEY SHOULD DO IT ONLY.**
*   How do we know that a function is doing more than "one thing":
    *   you can extract another function from it with a name that is not merely a restatement of its implementation

## 3. ONE LEVEL OF ABSTRACTION PER FUNCTION

*   Mixing levels of abstraction within a function is always confusing. Readers may not be able to tell whether a particular expression is an essential concept or a detail. Worse, like broken windows, once details are mixed with essential concepts, more and more details tend to accrete within the function.
*   We want the code to read like a top-down narrative. We want every function to be followed by those at the next level of abstraction so that we can read the program. Descending one level of abstraction at a time as we read down the list of functions. I call this *The Step-down Rule*.
*   It turns out to be very difficult for programmers to learn to follow this rule and write functions that stay at a single level of abstraction. But learning this trick is also very important. It is the key to keeping functions short and making sure they do “one thing.”

*   Switch statement:

    ```java
    public Money calculatePay(Employee e) 
    
       throws InvalidEmployeeType {
    
           switch (e.type) {
    
             case COMMISSIONED:
    
               return calculateCommissionedPay(e);
    
             case HOURLY:
    
               return calculateHourlyPay(e);
    
             case SALARIED:
    
               return calculateSalariedPay(e);
    
             default:
    
               throw new InvalidEmployeeType(e.type);
    
           }
    
         }
    ```

    Problems with this code:

    *   It's large, when new employee types are added, it will grow.
    *   Second, it very clearly does more than one thing
    *   Third, it violates the Single Responsibility Principle
    *   Fourth, it violates the Open Closed Principle (OCP) because it must change whenever new types are added

**General rule for switch statements is that they can be tolerated if they appear only once, are used to create polymorphic objects,**

```java
public abstract class Employee {

     public abstract boolean isPayday();

     public abstract Money calculatePay();

     public abstract void deliverPay(Money pay);

   }

   -----------------

   public interface EmployeeFactory {

     public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;

   }

   -----------------

   public class EmployeeFactoryImpl implements EmployeeFactory {

     public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {

       switch (r.type) {

         case COMMISSIONED:

           return new CommissionedEmployee(r) ;

         case HOURLY:

           return new HourlyEmployee(r);

         case SALARIED:

           return new SalariedEmploye(r);

         default:

           throw new InvalidEmployeeType(r.type);

       }

     }

   }
```

## 4. USE DESCRIPTIVE NAMES

*   Don’t be afraid to make a name long. A long descriptive name is better than a short enigmatic name.
*   Don’t be afraid to spend time choosing a name. Indeed, you should try several different names and read the code with each in place. Modern IDEs like Eclipse or IntelliJ make it trivial to change names.
*   Choosing descriptive names will clarify the design of the module in your mind and help you to improve it
*   Be consistent in your names. Use the same phrases, nouns, and verbs in the function names you choose for your modules.

## 5. Function Arguments

*   The ideal number of arguments for a function is zero (niladic). Next comes one (monadic), followed closely by two (dyadic). Three arguments (triadic) should be avoided where possible
*   Arguments are hard. They take a lot of conceptual power. That’s why I got rid of almost all of them from the example.
*   Arguments are even harder from a testing point of view. Imagine the difficulty of writing all the test cases to ensure that all the various combinations of arguments work properly.
*   Output arguments are harder to understand than input arguments. When we read a function, we are used to the idea of information going *in* to the function through arguments and *out* through the return value.

### Common Monadic Forms:

*   Asking a question about that argument: e.g. `boolean fileExists("myFile")`
*   Operating on that argument, transforman argument: e.g.`InputStream fileOpen(“MyFile”)`

*   An event: e.g. `void passwordAttemptFailedNtimes(int attempts)`

*   **Try to avoid any monadic functions that don’t follow these forms**, such as:

    ```void includeSetupPageInto(StringBuffer pageText)```: Using an output argument instead of a return value for a transformation is confusing.

    If a function is going to transform its input argument, the transformation should appear as the return value. Indeed, `StringBuffer transform(StringBuffer in)` is better than `void transform(StringBuffer out)`, even if the implementation in the first case simply returns the input argument. At least it still follows the form of a transformation

### Flag Arguments

*   Flag arguments are ugly
    *   It loudly proclaiming that this function does more than one thing. It does one thing if the flag is true and another if the flag is false!

### Dyadic Functions

	* A function with two arguments is harder to understand than a monadic function 
	* Even obvious dyadic functions like `assertEquals(expected, actual)` are problematic. How many times have you put the `actual` where the `expected` should be? The two arguments have no natural ordering. The `expected,` `actual` ordering is a convention that requires practice to learn.

### Triads

*   Functions that take three arguments are significantly harder to understand than dyads. 

### Argument Objects

When a function seems to need more than two or three arguments, it is likely that some of those arguments ought to be wrapped into a class of their own. Consider, for example, the difference between the two following declarations:

```java
Circle makeCircle(double x, double y, double radius);

Circle makeCircle(Point center, double radius);
```

### Verbs and Keywords

*   Choosing good names for a function can go a long way toward explaining the intent of the function and the order and intent of the arguments. 
    *   For example, `write(name)` is very evocative. Whatever this “name” thing is, it is being “written.”
    *   For example, `assertEquals` might be better written as `assertExpectedEqualsActual(expected,` `actual)`

## 6. Have no side effects

*   Side effects are lies. Your function promises to do one thing, but it also does other *hidden* things

### Output arguments

*   Arguments are most naturally interpreted as *inputs* to a function.

*   For example:

    ```java
    appendFooter(s);
    ```

    Does this function append `s` as the footer to something? Or does it append some footer to `s`? 

    Consider:

    ```java
    public void appendFooter(StringBuffer report)
    ```

    This clarifies the issue, but only at the expense of checking the declaration of the function. Anything that forces you to check the function signature is equivalent to a double-take. It’s a cognitive break and should be avoided.

### Command Query Separation

*   Functions should either do something or answer something, but not both

*   For example:

    ```java
    public boolean set(String attribute, String value);
    ```

    This function sets the value of a named attribute and returns `true` if it is successful and `false` if no such attribute exists. This leads to odd statements like this:

    ```java
      if (set(”username”, ”unclebob”))…
    ```

    The author intended `set` to be a verb, but in the context of the `if` statement it *feels* like an adjective.

    The real solution is to separate the command from the query so that the ambiguity cannot occur

    ```java
    if (attributeExists(”username”)) {
    
         setAttribute(”username”, ”unclebob”);
    
         …
    
       }
    ```

### PREFER EXCEPTIONS TO RETURNING ERROR CODES

*   Returning error codes from command functions is a subtle violation of command query separation. It promotes commands being used as expressions in the predicates of `if` statements.

    ```java
    if (deletePage(page) == E_OK)
    ```

    This does not suffer from verb/adjective confusion but does lead to deeply nested structures

      

### Extract Try/Catch Blocks

*   `Try/catch` blocks are ugly in their own right. They confuse the structure of the code and mix error processing with normal processing. So it is better to extract the bodies of the `try` and `catch` blocks out into functions of their own.

```java
   public void delete(Page page) {

     try {

       deletePageAndAllReferences(page);

     }

     catch (Exception e) {

       logError(e);

     }

   }
```

