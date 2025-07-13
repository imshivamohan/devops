I’ll provide a clear and concise explanation of **functions** in programming, focusing on their core concepts, and give two simple examples for each in Go, Java, and Python. Each example will be wrapped in an appropriate `<xaiArtifact/>` tag with a unique UUID, title, and content type, as per the guidelines. I’ll keep the examples beginner-friendly and include brief explanations for clarity.

---

### 3. Functions

**Explanation**: Functions are reusable blocks of code that perform a specific task. They help organize code, reduce repetition, and improve maintainability. Functions typically take input (parameters), process it, and return an output (return value). In Go, Java, and Python, functions differ slightly in syntax but share this core purpose. Key aspects include:
- **Declaration**: Defining the function name, parameters, and return type (if any).
- **Calling**: Invoking the function with arguments to execute its logic.
- **Return**: Sending a result back to the caller (optional in some cases).

Below are two simple examples for each language, demonstrating function declaration, parameters, and return values.

#### Go
- **Syntax**: Go uses the `func` keyword, with parameters and return types explicitly declared. Multiple return values are supported, and curly braces `{}` are mandatory.
- **Example 1**: A function to calculate the square of a number.
```go
package main
import "fmt"

func square(num int) int {
    return num * num
}

func main() {
    result := square(5)
    fmt.Println("Square of 5 is:", result)
}
```
*Explanation*: The `square` function takes an integer `num`, multiplies it by itself, and returns the result. In `main`, calling `square(5)` returns 25, which is printed.

- **Example 2**: A function to add two numbers with multiple return values.
```go
package main
import "fmt"

func addNumbers(a int, b int) (int, string) {
    sum := a + b
    return sum, "Success"
}

func main() {
    result, message := addNumbers(3, 4)
    fmt.Println("Sum:", result, "Message:", message)
}
```
*Explanation*: The `addNumbers` function takes two integers, returns their sum and a string message. In `main`, it’s called with arguments 3 and 4, printing the sum (7) and message ("Success").

#### Java
- **Syntax**: Java uses methods (functions within classes) with explicit return types (or `void` for no return). Parameters are declared with types, and methods are defined inside a class.
- **Example 1**: A function to check if a number is even.
```java
public class Main {
    public static boolean isEven(int num) {
        return num % 2 == 0;
    }

    public static void main(String[] args) {
        boolean result = isEven(6);
        System.out.println("Is 6 even? " + result);
    }
}
```
*Explanation*: The `isEven` method takes an integer `num` and returns `true` if it’s even (divisible by 2), else `false`. In `main`, calling `isEven(6)` returns `true`, which is printed.

- **Example 2**: A function to find the maximum of two numbers.
```java
public class Main {
    public static int max(int a, int b) {
        if (a > b) {
            return a;
        }
        return b;
    }

    public static void main(String[] args) {
        int result = max(10, 7);
        System.out.println("Maximum is: " + result);
    }
}
```
*Explanation*: The `max` method compares two integers and returns the larger one. In `main`, calling `max(10, 7)` returns 10, which is printed.

#### Python
- **Syntax**: Python uses the `def` keyword, followed by the function name and parameters. Return types are not explicitly declared, and the `return` statement is optional. Indentation defines the function body.
- **Example 1**: A function to calculate the cube of a number.
```python
def cube(num):
    return num * num * num

result = cube(4)
print("Cube of 4 is:", result)
```
*Explanation*: The `cube` function takes a number `num` and returns its cube. Calling `cube(4)` returns 64, which is printed.

- **Example 2**: A function to greet a user with an optional parameter.
```python
def greet(name="Guest"):
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet())
```
*Explanation*: The `greet` function takes an optional parameter `name` with a default value of "Guest". It returns a greeting string. Calling `greet("Alice")` prints "Hello, Alice!", and `greet()` uses the default, printing "Hello, Guest!".

---

### Summary
- **Functions**: Reusable code blocks that take inputs (parameters), perform tasks, and optionally return outputs.
- **Go**: Uses `func`, supports multiple return values, explicit types.
- **Java**: Methods inside classes, explicit return types, `void` for no return.
- **Python**: Uses `def`, flexible with no explicit types, optional `return`.

Each example demonstrates a simple function with clear input/output behavior. Let me know if you need more examples or further clarification!
