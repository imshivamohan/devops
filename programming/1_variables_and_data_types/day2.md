Below, I’ll provide executable code examples for four common data types (integer, float, string, and boolean) in Java, Python, and Go. Each example demonstrates variable declaration, initialization, and basic usage, ensuring the code is executable and clear. I’ve chosen simple, practical examples to showcase each data type’s functionality.

---

### **1. Java**
Java is a statically typed language, so variables must be declared with their data types.

#### **Integer**
```java
public class IntegerExample {
    public static void main(String[] args) {
        int age = 25;
        int quantity = 100;
        int sum = age + quantity;
        System.out.println("Age: " + age);
        System.out.println("Quantity: " + quantity);
        System.out.println("Sum: " + sum);
        System.out.println("Is age greater than 20? " + (age > 20));
    }
}
```
**Explanation**: Declares `int` variables, performs addition, and checks a condition. Output shows variable values and a boolean result.

#### **Float**
```java
public class FloatExample {
    public static void main(String[] args) {
        float temperature = 36.6f;
        float price = 19.99f;
        float total = temperature + price;
        System.out.println("Temperature: " + temperature + "°C");
        System.out.println("Price: $" + price);
        System.out.println("Total (sum): " + total);
        System.out.println("Price rounded: " + Math.round(price));
    }
}
```
**Explanation**: Uses `float` for decimal numbers (note the `f` suffix). Demonstrates addition and rounding.

#### **String**
```java
public class StringExample {
    public static void main(String[] args) {
        String name = "Alice";
        String greeting = "Hello, " + name + "!";
        System.out.println("Name: " + name);
        System.out.println("Greeting: " + greeting);
        System.out.println("Name length: " + name.length());
        System.out.println("Uppercase name: " + name.toUpperCase());
    }
}
```
**Explanation**: Declares `String` variables, concatenates strings, and uses string methods like `length()` and `toUpperCase()`.

#### **Boolean**
```java
public class BooleanExample {
    public static void main(String[] args) {
        boolean isStudent = true;
        boolean isAdult = false;
        System.out.println("Is student? " + isStudent);
        System.out.println("Is adult? " + isAdult);
        System.out.println("Both true? " + (isStudent && isAdult));
        System.out.println("Either true? " + (isStudent || isAdult));
    }
}
```
**Explanation**: Uses `boolean` for true/false values and demonstrates logical operators (`&&`, `||`).

---

### **2. Python**
Python is dynamically typed, so variables don’t require explicit type declarations.

#### **Integer**
```python
# integer_example.py
age = 30
quantity = 50
sum_result = age + quantity
print(f"Age: {age}")
print(f"Quantity: {quantity}")
print(f"Sum: {sum_result}")
print(f"Is age greater than 25? {age > 25}")
```
**Explanation**: Declares integer variables, performs addition, and uses an f-string for output. The condition `age > 25` evaluates to a boolean.

#### **Float**
```python
# float_example.py
temperature = 98.6
price = 29.99
total = temperature + price
print(f"Temperature: {temperature}°F")
print(f"Price: ${price}")
print(f"Total (sum): {total}")
print(f"Price rounded: {round(price)}")
```
**Explanation**: Uses `float` for decimal numbers, performs addition, and rounds the price using the `round()` function.

#### **String**
```python
# string_example.py
name = "Bob"
greeting = f"Hello, {name}!"
print(f"Name: {name}")
print(f"Greeting: {greeting}")
print(f"Name length: {len(name)}")
print(f"Uppercase name: {name.upper()}")
```
**Explanation**: Declares string variables, uses f-string concatenation, and applies string methods `len()` and `upper()`.

#### **Boolean**
```python
# boolean_example.py
is_student = True
is_adult = False
print(f"Is student? {is_student}")
print(f"Is adult? {is_adult}")
print(f"Both true? {is_student and is_adult}")
print(f"Either true? {is_student or is_adult}")
```
**Explanation**: Uses boolean variables and demonstrates logical operators (`and`, `or`).

---

### **3. Go**
Go is statically typed, requiring explicit type declarations or type inference.

#### **Integer**
```go
package main

import "fmt"

func main() {
    var age int = 40
    quantity := 200 // Type inference
    sum := age + quantity
    fmt.Println("Age:", age)
    fmt.Println("Quantity:", quantity)
    fmt.Println("Sum:", sum)
    fmt.Println("Is age greater than 30?", age > 30)
}
```
**Explanation**: Declares `int` variables (using `var` and type inference with `:=`), performs addition, and checks a condition.

#### **Float**
```go
package main

import "fmt"

func main() {
    var temperature float32 = 37.2
    price := 49.99 // Type inference (float64 by default)
    total := float64(temperature) + price
    fmt.Println("Temperature:", temperature, "°C")
    fmt.Println("Price: $", price)
    fmt.Println("Total (sum):", total)
    fmt.Printf("Price rounded: %.0f\n", price)
}
```
**Explanation**: Uses `float32` and `float64` (Go’s default for floating-point literals), performs addition, and rounds using `fmt.Printf`.

#### **String**
```go
package main

import "fmt"

func main() {
    var name string = "Charlie"
    greeting := "Hello, " + name + "!"
    fmt.Println("Name:", name)
    fmt.Println("Greeting:", greeting)
    fmt.Println("Name length:", len(name))
    fmt.Println("First character:", string(name[0]))
}
```
**Explanation**: Declares `string` variables, concatenates strings, and uses `len()` for string length. Accesses the first character as a byte.

#### **Boolean**
```go
package main

import "fmt"

func main() {
    var isStudent bool = true
    isAdult := false // Type inference
    fmt.Println("Is student?", isStudent)
    fmt.Println("Is adult?", isAdult)
    fmt.Println("Both true?", isStudent && isAdult)
    fmt.Println("Either true?", isStudent || isAdult)
}
```
**Explanation**: Uses `bool` for true/false values and demonstrates logical operators (`&&`, `||`).

---

### **How to Execute**

#### **Java**
1. Save each example in a `.java` file (e.g., `IntegerExample.java`).
2. Compile: `javac IntegerExample.java`
3. Run: `java IntegerExample`

#### **Python**
1. Save each example in a `.py` file (e.g., `integer_example.py`).
2. Run: `python integer_example.py`

#### **Go**
1. Save each example in a `.go` file (e.g., `integer_example.go`).
2. Run: `go run integer_example.go`
   - Ensure Go is installed (`go` command available).

---

### **Notes**
- Each example is self-contained and executable, producing clear output to demonstrate the data type’s usage.
- I avoided overly complex examples to keep them beginner-friendly while showing practical operations (arithmetic, string manipulation, logical operations).
- If you need more specific examples (e.g., arrays, structs, or advanced operations) or have issues running the code, let me know!



I’ll provide executable code examples for four common data types (integer, float, string, and boolean) in Java, Python, and Go, focusing on key operations for each data type. Each example will include operations specific to the data type, such as arithmetic for integers and floats, string manipulation for strings, and logical operations for booleans. The code will be concise, executable, and demonstrate practical use cases.

---

### **1. Java**
Java is statically typed, requiring explicit type declarations. Each example includes operations relevant to the data type.

#### **Integer (Arithmetic Operations)**
```java
public class IntegerOperations {
    public static void main(String[] args) {
        int num1 = 50;
        int num2 = 10;
        int sum = num1 + num2;        // Addition
        int difference = num1 - num2; // Subtraction
        int product = num1 * num2;    // Multiplication
        int quotient = num1 / num2;   // Division
        System.out.println("Number 1: " + num1);
        System.out.println("Number 2: " + num2);
        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
        System.out.println("Product: " + product);
        System.out.println("Quotient: " + quotient);
    }
}
```
**Operations**: Addition, subtraction, multiplication, division.

#### **Float (Arithmetic and Comparison Operations)**
```java
public class FloatOperations {
    public static void main(String[] args) {
        float num1 = 25.5f;
        float num2 = 10.2f;
        float sum = num1 + num2;      // Addition
        float difference = num1 - num2; // Subtraction
        float product = num1 * num2;  // Multiplication
        float quotient = num1 / num2; // Division
        System.out.println("Number 1: " + num1);
        System.out.println("Number 2: " + num2);
        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
        System.out.println("Product: " + product);
        System.out.println("Quotient: " + quotient);
    }
}
```
**Operations**: Addition, subtraction, multiplication, division (floating-point precision).

#### **String (Manipulation Operations)**
```java
public class StringOperations {
    public static void main(String[] args) {
        String text = "Hello, World!";
        String name = "Alice";
        String concatenated = text + " " + name; // Concatenation
        String uppercase = text.toUpperCase();   // Convert to uppercase
        String substring = text.substring(0, 5); // Extract substring
        boolean contains = text.contains("World"); // Check for substring
        System.out.println("Original: " + text);
        System.out.println("Concatenated: " + concatenated);
        System.out.println("Uppercase: " + uppercase);
        System.out.println("Substring (0-5): " + substring);
        System.out.println("Contains 'World': " + contains);
    }
}
```
**Operations**: Concatenation, uppercase conversion, substring extraction, substring check.

#### **Boolean (Logical Operations)**
```java
public class BooleanOperations {
    public static void main(String[] args) {
        boolean isSunny = true;
        boolean isWarm = false;
        boolean andResult = isSunny && isWarm; // Logical AND
        boolean orResult = isSunny || isWarm;  // Logical OR
        boolean notSunny = !isSunny;           // Logical NOT
        boolean xorResult = isSunny ^ isWarm;  // Logical XOR
        System.out.println("Is sunny? " + isSunny);
        System.out.println("Is warm? " + isWarm);
        System.out.println("AND result: " + andResult);
        System.out.println("OR result: " + orResult);
        System.out.println("NOT sunny: " + notSunny);
        System.out.println("XOR result: " + xorResult);
    }
}
```
**Operations**: Logical AND, OR, NOT, and XOR.

---

### **2. Python**
Python is dynamically typed, so no explicit type declarations are needed. Each example includes operations specific to the data type.

#### **Integer (Arithmetic Operations)**
```python
# integer_operations.py
num1 = 100
num2 = 25
sum_result = num1 + num2      # Addition
difference = num1 - num2      # Subtraction
product = num1 * num2         # Multiplication
quotient = num1 // num2       # Integer division
print(f"Number 1: {num1}")
print(f"Number 2: {num2}")
print(f"Sum: {sum_result}")
print(f"Difference: {difference}")
print(f"Product: {product}")
print(f"Quotient: {quotient}")
```
**Operations**: Addition, subtraction, multiplication, integer division (using `//` for integer results).

#### **Float (Arithmetic and Comparison Operations)**
```python
# float_operations.py
num1 = 50.75
num2 = 12.25
sum_result = num1 + num2      # Addition
difference = num1 - num2      # Subtraction
product = num1 * num2         # Multiplication
quotient = num1 / num2        # Division
print(f"Number 1: {num1}")
print(f"Number 2: {num2}")
print(f"Sum: {sum_result}")
print(f"Difference: {difference}")
print(f"Product: {product}")
print(f"Quotient: {quotient}")
```
**Operations**: Addition, subtraction, multiplication, division (floating-point results).

#### **String (Manipulation Operations)**
```python
# string_operations.py
text = "Python Programming"
name = "Bob"
concatenated = text + " with " + name  # Concatenation
uppercase = text.upper()               # Convert to uppercase
substring = text[0:6]                 # Extract substring
contains = "Python" in text           # Check for substring
print(f"Original: {text}")
print(f"Concatenated: {concatenated}")
print(f"Uppercase: {uppercase}")
print(f"Substring (0-6): {substring}")
print(f"Contains 'Python': {contains}")
```
**Operations**: Concatenation, uppercase conversion, substring slicing, substring check.

#### **Boolean (Logical Operations)**
```python
# boolean_operations.py
is_raining = False
is_cold = True
and_result = is_raining and is_cold  # Logical AND
or_result = is_raining or is_cold    # Logical OR
not_raining = not is_raining         # Logical NOT
xor_result = (is_raining != is_cold) # Logical XOR (using inequality)
print(f"Is raining? {is_raining}")
print(f"Is cold? {is_cold}")
print(f"AND result: {and_result}")
print(f"OR result: {or_result}")
print(f"NOT raining: {not_raining}")
print(f"XOR result: {xor_result}")
```
**Operations**: Logical AND, OR, NOT, and XOR (implemented via inequality).

---

### **3. Go**
Go is statically typed, with explicit type declarations or type inference. Each example includes operations relevant to the data type.

#### **Integer (Arithmetic Operations)**
```go
package main

import "fmt"

func main() {
    var num1 int = 75
    num2 := 15                // Type inference
    sum := num1 + num2        // Addition
    difference := num1 - num2 // Subtraction
    product := num1 * num2    // Multiplication
    quotient := num1 / num2   // Division
    fmt.Println("Number 1:", num1)
    fmt.Println("Number 2:", num2)
    fmt.Println("Sum:", sum)
    fmt.Println("Difference:", difference)
    fmt.Println("Product:", product)
    fmt.Println("Quotient:", quotient)
}
```
**Operations**: Addition, subtraction, multiplication, division (integer results).

#### **Float (Arithmetic and Comparison Operations)**
```go
package main

import "fmt"

func main() {
    var num1 float64 = 45.67
    num2 := 10.33            // Type inference (float64)
    sum := num1 + num2       // Addition
    difference := num1 - num2 // Subtraction
    product := num1 * num2   // Multiplication
    quotient := num1 / num2  // Division
    fmt.Println("Number 1:", num1)
    fmt.Println("Number 2:", num2)
    fmt.Println("Sum:", sum)
    fmt.Println("Difference:", difference)
    fmt.Println("Product:", product)
    fmt.Println("Quotient:", quotient)
}
```
**Operations**: Addition, subtraction, multiplication, division (floating-point results).

#### **String (Manipulation Operations)**
```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    var text string = "Go Language"
    name := "Charlie"
    concatenated := text + " and " + name // Concatenation
    uppercase := strings.ToUpper(text)    // Convert to uppercase
    substring := text[0:2]               // Extract substring
    contains := strings.Contains(text, "Go") // Check for substring
    fmt.Println("Original:", text)
    fmt.Println("Concatenated:", concatenated)
    fmt.Println("Uppercase:", uppercase)
    fmt.Println("Substring (0-2):", substring)
    fmt.Println("Contains 'Go':", contains)
}
```
**Operations**: Concatenation, uppercase conversion (using `strings` package), substring slicing, substring check.

#### **Boolean (Logical Operations)**
```go
package main

import "fmt"

func main() {
    var isMorning bool = true
    isWeekend := false          // Type inference
    andResult := isMorning && isWeekend // Logical AND
    orResult := isMorning || isWeekend  // Logical OR
    notMorning := !isMorning           // Logical NOT
    xorResult := isMorning != isWeekend // Logical XOR (using inequality)
    fmt.Println("Is morning?", isMorning)
    fmt.Println("Is weekend?", isWeekend)
    fmt.Println("AND result:", andResult)
    fmt.Println("OR result:", orResult)
    fmt.Println("NOT morning:", notMorning)
    fmt.Println("XOR result:", xorResult)
}
```
**Operations**: Logical AND, OR, NOT, and XOR (using inequality).

---

### **How to Execute**

#### **Java**
1. Save each example in a `.java` file (e.g., `IntegerOperations.java`).
2. Compile: `javac IntegerOperations.java`
3. Run: `java IntegerOperations`

#### **Python**
1. Save each example in a `.py` file (e.g., `integer_operations.py`).
2. Run: `python integer_operations.py`

#### **Go**
1. Save each example in a `.go` file (e.g., `integer_operations.go`).
2. Run: `go run integer_operations.go`
   - Ensure Go is installed (`go` command available).
   - For the string example, the `strings` package is used, which is part of Go’s standard library.

---

### **Notes**
- Each example is executable and focuses on operations specific to the data type: arithmetic for integers and floats, string manipulation for strings, and logical operations for booleans.
- I used consistent operations across languages where possible to highlight similarities and differences (e.g., Python’s `//` for integer division vs. Go’s `/` for integers).
- Go requires the `strings` package for some string operations, which is standard and doesn’t need external dependencies.
- If you need additional operations (e.g., modulus for integers, formatting for strings) or encounter issues running the code, let me know!
