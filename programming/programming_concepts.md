# Core Programming Concepts in Python, Java, and Go

This document explains fundamental programming concepts in a language-agnostic way, followed by implementations in Python, Java, and Go. Each concept includes a brief explanation, why it matters, and a code example for the task described. The examples are simple and consistent to help beginners understand syntax differences across these languages.

## Part 1: Basic Programming Concepts

### 1. Variables and Data Types
- **What It Is**: Variables store data (e.g., numbers, text) with a name. Data types (e.g., integer, string, boolean) define the kind of data.
- **Why It Matters**: Variables are essential for storing and manipulating data. Types ensure correct operations (e.g., adding numbers, not text).
- **Task**: Store a person’s age (25) and name ("Alice"), then print "Alice is 25 years old."

### 2. Control Structures
- **What It Is**: Conditionals (`if`, `else`) make decisions; loops (`for`, `while`) repeat actions.
- **Why It Matters**: They enable dynamic behavior, like checking conditions or processing multiple items.
- **Task**: Check if a number (10) is positive, negative, or zero.

### 3. Functions
- **What It Is**: Functions are reusable code blocks that perform a task, often with inputs and outputs.
- **Why It Matters**: They improve code organization and reduce repetition.
- **Task**: Create a function to return the square of a number (5).

### 4. Arrays/Lists
- **What It Is**: Arrays/lists store multiple values (e.g., numbers, names) accessed by index (starting at 0).
- **Why It Matters**: They handle collections of data, like lists of scores.
- **Task**: Store 5 numbers (1, 2, 3, 4, 5) and calculate their sum.

### 5. Strings and Text Processing
- **What It Is**: Strings are character sequences. Operations include concatenation, reversal, or substring extraction.
- **Why It Matters**: Strings are key for user input/output and text manipulation.
- **Task**: Reverse the string "hello".

### 6. Stacks (Basic Data Structure)
- **What It Is**: A stack is a Last-In-First-Out (LIFO) structure where items are added (pushed) and removed (popped) from the top.
- **Why It Matters**: Useful for tasks like undoing actions or parsing.
- **Task**: Push three numbers (1, 2, 3) onto a stack and pop one, printing the popped value.

### 7. File Input/Output
- **What It Is**: File I/O reads from or writes to files for data persistence.
- **Why It Matters**: Enables saving/loading data, like user settings.
- **Task**: Write "Hello" to a file and read it back to print.

### 8. Object-Oriented Programming (OOP)
- **What It Is**: OOP uses classes (blueprints) and objects (instances) to organize code with attributes and methods.
- **Why It Matters**: Promotes modular, reusable, and scalable code.
- **Task**: Create a `Person` class with a name attribute and an introduce method.

### 9. Error Handling
- **What It Is**: Error handling manages runtime errors (e.g., division by zero) to prevent crashes.
- **Why It Matters**: Ensures robust, user-friendly programs.
- **Task**: Handle division by zero and print an error message.

## Part 2: Implementations
# Programming Basics: A Beginner-Friendly Guide

# Programming Basics: A Beginner-Friendly Guide

Welcome! This guide is designed for **students who have no prior experience** with programming. It will help you understand the **core programming concepts** in a **simple and beginner-friendly way**, using multiple languages like **Python**, **Java**, and **Go**. Each topic includes clear explanations and **at least two examples per concept**, with **line-by-line descriptions**.

---

## 1. Variables and Data Types

Variables are containers for storing data values. Data types define the type of data (e.g., number, text).

### Python Examples

```python
age = 25                # Store an integer value in variable 'age'
name = "Alice"           # Store a string in variable 'name'
print(f"{name} is {age} years old")  # Print formatted string with variable values

height = 5.9            # Float (decimal number)
is_student = True       # Boolean value (True or False)
print(height, is_student)  # Print multiple variables
```

### Java Examples

```java
int age = 25;                      // Declare integer variable
String name = "Alice";             // Declare string variable
System.out.println(name + " is " + age + " years old");  // Concatenate and print

float height = 5.9f;               // Float value with 'f'
boolean isStudent = true;         // Boolean variable
System.out.println(height + ", " + isStudent);  // Print both values
```

### Go Examples

```go
age := 25              // Declare integer using shorthand
name := "Alice"         // Declare string
fmt.Printf("%s is %d years old\n", name, age)  // Format and print

height := 5.9          // Float value
isStudent := true      // Boolean value
fmt.Println(height, isStudent)  // Print both variables
```

---

## 2. Control Structures (Conditions)

Control structures make decisions using `if`, `else if`, and `else`.

### Python Examples

```python
num = 10               # Assign number to variable
if num > 0:            # Check if number is positive
    print("Positive")
else:                  # Executes if condition is false
    print("Zero or Negative")

score = 70             # Example grade logic
if score >= 90:
    print("A grade")    # If score 90 or more
elif score >= 60:
    print("Pass")       # If score between 60-89
else:
    print("Fail")       # If score below 60
```

### Java Examples

```java
int num = 10;                      // Initialize variable
if (num > 0) {
    System.out.println("Positive");
} else {
    System.out.println("Zero or Negative");
}

int score = 70;                    // Grade logic
if (score >= 90) {
    System.out.println("A grade");
} else if (score >= 60) {
    System.out.println("Pass");
} else {
    System.out.println("Fail");
}
```

### Go Examples

```go
num := 10                         // Initialize variable
if num > 0 {
    fmt.Println("Positive")       // Print if condition is true
} else {
    fmt.Println("Zero or Negative")
}

score := 70                       // Grade logic
if score >= 90 {
    fmt.Println("A grade")
} else if score >= 60 {
    fmt.Println("Pass")
} else {
    fmt.Println("Fail")
}
```

---

## 3. Loops

Loops repeat a set of instructions.

### Python Examples

```python
for i in range(3):                # Repeat 3 times
    print("Hello")

count = 0                         # Start at 0
while count < 3:                  # Repeat while count < 3
    print("Count is", count)
    count += 1                    # Increment count
```

### Java Examples

```java
for (int i = 0; i < 3; i++) {
    System.out.println("Hello");  // Print 3 times
}

int count = 0;
while (count < 3) {
    System.out.println("Count is " + count);
    count++;
}
```

### Go Examples

```go
for i := 0; i < 3; i++ {          // Repeat 3 times
    fmt.Println("Hello")
}

count := 0
for count < 3 {
    fmt.Println("Count is", count)
    count++
}
```

---

## 4. Functions

Functions let you reuse code by calling them with or without inputs.

### Python Examples

```python
def greet():                       # Define function
    print("Hello")
greet()                            # Call function

def square(x):                     # Function with parameter
    return x * x                   # Return square value
print(square(4))
```

### Java Examples

```java
public static void greet() {
    System.out.println("Hello");
}
greet();

public static int square(int x) {
    return x * x;
}
System.out.println(square(4));
```

### Go Examples

```go
func greet() {
    fmt.Println("Hello")
}
greet()

func square(x int) int {
    return x * x
}
fmt.Println(square(4))
```

---

## 5. Lists/Arrays

Lists (Python) or Arrays (Java/Go) store collections of data.

### Python

```python
numbers = [1, 2, 3, 4, 5]          # Create a list of integers
total = sum(numbers)              # Calculate sum of elements
print(total)                      # Output: 15

print(numbers[2])                 # Access 3rd item (index starts at 0)
numbers.append(6)                # Add a new number to the list
print(numbers)
```

### Java

```java
int[] numbers = {1, 2, 3, 4, 5};   // Declare an array
int total = 0;
for (int num : numbers) {
    total += num;                 // Add each number to total
}
System.out.println(total);        // Output: 15

System.out.println(numbers[2]);   // Access index 2 (3rd item)
```

### Go

```go
numbers := []int{1, 2, 3, 4, 5}    // Declare a slice (dynamic array)
total := 0
for _, num := range numbers {     // Loop through each number
    total += num
}
fmt.Println(total)                // Output: 15

fmt.Println(numbers[2])           // Access 3rd element
```

---

## 6. Strings and Text Processing

Strings are sequences of characters. They can be manipulated using indexing, slicing, and built-in functions.

### Python

```python
text = "hello"
print(text[::-1])                 # Reverse the string
print(text.upper())               # Convert to uppercase
```

### Java

```java
String text = "hello";
StringBuilder reversed = new StringBuilder(text).reverse();
System.out.println(reversed);     // Reverse string
System.out.println(text.toUpperCase());  // Uppercase
```

### Go

```go
text := "hello"
runes := []rune(text)              // Convert string to runes for reverse
for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
    runes[i], runes[j] = runes[j], runes[i]
}
fmt.Println(string(runes))         // Print reversed
fmt.Println(strings.ToUpper(text)) // Convert to uppercase
```

---

## 7. File Input/Output

Programs can read from and write to files.

### Python

```python
with open("output.txt", "w") as f:
    f.write("Hello")              # Write to file
with open("output.txt", "r") as f:
    print(f.read())               # Read and print file content
```

### Java

```java
Files.writeString(Path.of("output.txt"), "Hello"); // Write to file
System.out.println(Files.readString(Path.of("output.txt"))); // Read file
```

### Go

```go
os.WriteFile("output.txt", []byte("Hello"), 0644) // Write to file
data, _ := os.ReadFile("output.txt")              // Read file
fmt.Println(string(data))                          // Print content
```

---

## 8. Object-Oriented Programming

OOP is a programming style where you model concepts as classes and objects.

### Python

```python
class Person:
    def __init__(self, name):     # Constructor with name
        self.name = name

    def introduce(self):
        return f"Hi, I'm {self.name}"

p = Person("Alice")
print(p.introduce())              # Call method
```

### Java

```java
public class Person {
    String name;
    Person(String name) {
        this.name = name;
    }
    String introduce() {
        return "Hi, I'm " + name;
    }
    public static void main(String[] args) {
        Person p = new Person("Alice");
        System.out.println(p.introduce());
    }
}
```

### Go

```go
type Person struct {
    name string
}
func (p Person) introduce() string {
    return "Hi, I'm " + p.name
}
func main() {
    p := Person{name: "Alice"}
    fmt.Println(p.introduce())
}
```

---

## 9. Error Handling

Errors should be handled gracefully using exception or error checks.

### Python

```python
try:
    x = 10 / 0                     # Division by zero
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Java

```java
try {
    int x = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
}
```

### Go

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil
}

_, err := divide(10, 0)
if err != nil {
    fmt.Println(err)
}
```

...

---

## 10. Recursion

Recursion is when a function calls itself to solve a smaller part of a problem.

### Python

```python
def factorial(n):                    # Define a function to calculate factorial
    if n == 0:
        return 1                    # Base case: factorial(0) is 1
    else:
        return n * factorial(n - 1) # Recursive call

print(factorial(5))                 # Output: 120 (5 * 4 * 3 * 2 * 1)
```

```python
def countdown(n):                    # Print numbers from n to 1
    if n == 0:
        print("Blastoff!")
    else:
        print(n)
        countdown(n - 1)            # Recursive call with n - 1

countdown(5)
```

---

## 11. Sorting Algorithms

Sorting helps organize data in ascending or descending order.

### Python (Bubble Sort)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):              # Outer loop
        for j in range(0, n - i - 1):  # Inner loop
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap

arr = [5, 3, 1, 4, 2]
bubble_sort(arr)
print(arr)                          # Output: [1, 2, 3, 4, 5]
```

### Java (Using Arrays.sort)

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] arr = {5, 3, 1, 4, 2};
        Arrays.sort(arr);              // Sort using built-in method
        System.out.println(Arrays.toString(arr));
    }
}
```

---

## 12. Data Structures

### Stacks

A stack follows Last-In-First-Out (LIFO) behavior.

#### Python

```python
stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print(stack.pop())                  # Output: 3 (last pushed, first out)
```

#### Java

```java
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.push(2);
stack.push(3);
System.out.println(stack.pop());    // Output: 3
```

### Queues

A queue follows First-In-First-Out (FIFO) behavior.

#### Python

```python
from collections import deque
queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
print(queue.popleft())              # Output: 1 (first in, first out)
```

#### Java

```java
Queue<Integer> queue = new LinkedList<>();
queue.add(1);
queue.add(2);
queue.add(3);
System.out.println(queue.remove()); // Output: 1
```

### Trees (Binary Tree Node in Python)

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

root = Node(10)
root.left = Node(5)
root.right = Node(20)
print(root.left.data)               # Output: 5
```

---

## 13. Input Validation and User Input

Validating input ensures the program receives correct and safe data.

### Python

```python
user_input = input("Enter a number: ")
if user_input.isdigit():
    print("You entered:", int(user_input))
else:
    print("Invalid input! Please enter a number.")
```

### Java

```java
Scanner scanner = new Scanner(System.in);
System.out.print("Enter a number: ");
if (scanner.hasNextInt()) {
    int num = scanner.nextInt();
    System.out.println("You entered: " + num);
} else {
    System.out.println("Invalid input!");
}
```

### Go

```go
var input string
fmt.Print("Enter a number: ")
fmt.Scanln(&input)
num, err := strconv.Atoi(input)
if err != nil {
    fmt.Println("Invalid input!")
} else {
    fmt.Println("You entered:", num)
}
```

...

---

## 14. File Parsing (JSON and CSV)

### Python (JSON)

```python
import json  # Import the json module

# Sample dictionary to be converted to JSON
data = {"name": "Alice", "age": 25}

# Write JSON to file
with open("data.json", "w") as f:  # Open file in write mode
    json.dump(data, f)  # Convert dictionary to JSON and write it to the file

# Read JSON from file
with open("data.json", "r") as f:  # Open file in read mode
    result = json.load(f)  # Load JSON content from file into a dictionary
    print(result)  # Print the dictionary
```

### Python (CSV)

```python
import csv  # Import the csv module

# Write to CSV file
with open("data.csv", "w", newline="") as f:  # Open file in write mode
    writer = csv.writer(f)  # Create a CSV writer object
    writer.writerow(["name", "age"])  # Write header row
    writer.writerow(["Alice", 25])  # Write data row

# Read from CSV file
with open("data.csv", "r") as f:  # Open file in read mode
    reader = csv.reader(f)  # Create a CSV reader object
    for row in reader:  # Iterate through each row
        print(row)  # Print the row
```

### Java (JSON using org.json library)

```java
import org.json.JSONObject;  // Import JSON object class
import java.io.*;  // Import Java IO classes

public class JsonExample {
    public static void main(String[] args) throws IOException {
        JSONObject obj = new JSONObject();  // Create a new JSON object
        obj.put("name", "Alice");  // Add name field
        obj.put("age", 25);  // Add age field

        // Write JSON to file
        FileWriter file = new FileWriter("data.json");  // Create file writer
        file.write(obj.toString());  // Write JSON string to file
        file.flush();  // Flush writer to ensure data is written

        // Read JSON from file
        BufferedReader reader = new BufferedReader(new FileReader("data.json"));  // Read file line-by-line
        String line = reader.readLine();  // Read a single line
        JSONObject result = new JSONObject(line);  // Convert line into JSON object
        System.out.println(result);  // Print the JSON object
    }
}
```

### Java (CSV using OpenCSV)

```java
import com.opencsv.*;  // Import OpenCSV classes
import java.io.*;  // Import Java IO classes

public class CsvExample {
    public static void main(String[] args) throws IOException {
        // Write to CSV
        CSVWriter writer = new CSVWriter(new FileWriter("data.csv"));  // Create CSV writer
        String[] header = {"name", "age"};  // Define header
        String[] row = {"Alice", "25"};  // Define a data row
        writer.writeNext(header);  // Write header row
        writer.writeNext(row);  // Write data row
        writer.close();  // Close the writer

        // Read from CSV
        CSVReader reader = new CSVReader(new FileReader("data.csv"));  // Create CSV reader
        String[] nextLine;  // Temporary array for rows
        while ((nextLine = reader.readNext()) != null) {  // Read until end of file
            System.out.println(String.join(", ", nextLine));  // Print each row
        }
        reader.close();  // Close the reader
    }
}
```

### Go (JSON)

```go
package main
import (
    "encoding/json"  // JSON library
    "fmt"             // For formatted I/O
    "os"              // File operations
)

func main() {
    data := map[string]interface{}{"name": "Alice", "age": 25}  // Create a map

    // Write JSON
    file, _ := os.Create("data.json")  // Create file
    json.NewEncoder(file).Encode(data)  // Encode and write JSON to file
    file.Close()  // Close file

    // Read JSON
    file, _ = os.Open("data.json")  // Open file
    var result map[string]interface{}  // Create map to store JSON
    json.NewDecoder(file).Decode(&result)  // Decode JSON from file
    fmt.Println(result)  // Print result
}
```

### Go (CSV)

```go
package main
import (
    "encoding/csv"  // CSV library
    "fmt"           // For printing
    "os"            // File handling
)

func main() {
    // Write CSV
    file, _ := os.Create("data.csv")  // Create CSV file
    writer := csv.NewWriter(file)  // Create writer
    writer.Write([]string{"name", "age"})  // Write header
    writer.Write([]string{"Alice", "25"})  // Write data row
    writer.Flush()  // Flush the data to file
    file.Close()  // Close file

    // Read CSV
    file, _ = os.Open("data.csv")  // Open file
    reader := csv.NewReader(file)  // Create reader
    records, _ := reader.ReadAll()  // Read all lines
    for _, row := range records {  // Iterate over rows
        fmt.Println(row)  // Print row
    }
}
```
...

---

## 15. Regular Expressions (Regex)

### Python

```python
import re  # Import the regular expressions module

text = "Email: hello@example.com"  # Input text
pattern = r"\S+@\S+\.\S+"  # Regex pattern to match an email address
match = re.search(pattern, text)  # Search for the pattern in the text
if match:
    print("Match found:", match.group())  # Print the matched string if found
else:
    print("No match found")  # Inform if no match is found
```

```python
input_str = "12345"  # Input string of digits
if re.fullmatch(r"\d+", input_str):  # Check if the string contains only digits
    print("All digits")  # If yes, print confirmation
else:
    print("Contains non-digit characters")  # Else, indicate it's not all digits
```

### Java

```java
import java.util.regex.*;  // Import regex classes

public class RegexExample {
    public static void main(String[] args) {
        String text = "Email: hello@example.com";  // Input text
        Pattern pattern = Pattern.compile("\\S+@\\S+\\.\\S+");  // Regex for email
        Matcher matcher = pattern.matcher(text);  // Create matcher to apply regex

        if (matcher.find()) {
            System.out.println("Match found: " + matcher.group());  // Output match
        } else {
            System.out.println("No match found");
        }
    }
}
```

```java
public class DigitCheck {
    public static void main(String[] args) {
        String input = "12345";  // Input string
        boolean isDigits = input.matches("\\d+");  // Check if string contains only digits
        System.out.println("All digits? " + isDigits);  // Print result
    }
}
```

### Go

```go
package main
import (
    "fmt"
    "regexp"
)

func main() {
    text := "Email: hello@example.com"  // Input text
    re := regexp.MustCompile(`\S+@\S+\.\S+`)  // Compile regex for email
    match := re.FindString(text)  // Search for pattern
    if match != "" {
        fmt.Println("Match found:", match)  // Print match
    } else {
        fmt.Println("No match found")
    }
}
```

```go
package main
import (
    "fmt"
    "regexp"
)

func main() {
    input := "12345"  // Input string
    matched, _ := regexp.MatchString(`^\d+$`, input)  // Check if only digits
    fmt.Println("All digits?", matched)  // Print result
}
```
...

---

## 16. Web API Calls

### Python

```python
import requests  # Import the requests library to handle HTTP requests

response = requests.get("https://api.github.com")  # Send a GET request to GitHub API
print(response.status_code)  # Print HTTP status code (e.g., 200 for success)
print(response.text)  # Print the full response content as a string
```

```python
import requests  # Import the requests library

response = requests.get("https://api.github.com/repos/python/cpython")  # GET specific repo details
if response.status_code == 200:
    data = response.json()  # Convert response to Python dictionary
    print("Repository name:", data["name"])  # Print the repository name
else:
    print("Request failed with status code", response.status_code)  # Handle failure
```

### Java (using HttpURLConnection)

```java
import java.io.*;
import java.net.*;

public class HttpExample {
    public static void main(String[] args) throws Exception {
        URL url = new URL("https://api.github.com");  // Define the URL
        HttpURLConnection con = (HttpURLConnection) url.openConnection();  // Open connection
        con.setRequestMethod("GET");  // Set HTTP method to GET

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));  // Reader to read response
        String inputLine;
        StringBuffer response = new StringBuffer();  // Store response text
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);  // Append each line of the response
        }
        in.close();  // Close the reader

        System.out.println(response.toString());  // Print the full response
    }
}
```

```java
import java.io.*;
import java.net.*;

public class RepoExample {
    public static void main(String[] args) throws Exception {
        URL url = new URL("https://api.github.com/repos/python/cpython");  // Target specific GitHub repo
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");  // Send GET request

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String line;
        StringBuilder content = new StringBuilder();
        while ((line = in.readLine()) != null) {
            content.append(line);  // Read line-by-line
        }
        in.close();

        System.out.println(content.toString());  // Print raw JSON response
    }
}
```

### Go

```go
package main
import (
    "fmt"
    "io/ioutil"
    "net/http"
)

func main() {
    resp, err := http.Get("https://api.github.com")  // Send GET request
    if err != nil {
        fmt.Println("Error:", err)  // Print error if any
        return
    }
    defer resp.Body.Close()  // Close the response body when done

    body, _ := ioutil.ReadAll(resp.Body)  // Read entire response body
    fmt.Println(string(body))  // Print as string
}
```

```go
package main
import (
    "encoding/json"
    "fmt"
    "net/http"
    "io/ioutil"
)

func main() {
    resp, err := http.Get("https://api.github.com/repos/python/cpython")  // Fetch repo details
    if err != nil {
        fmt.Println("Request failed:", err)
        return
    }
    defer resp.Body.Close()

    body, _ := ioutil.ReadAll(resp.Body)  // Read body
    var data map[string]interface{}  // Prepare map to store parsed JSON
    json.Unmarshal(body, &data)  // Parse JSON into map
    fmt.Println("Repository name:", data["name"])  // Access a specific field
}
```
...

---

## 17. SQLite / Embedded Database

### Python (sqlite3)

```python
import sqlite3  # Import sqlite3 module

# Connect to database (or create one if it doesn’t exist)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()  # Create a cursor to execute SQL commands

# Create a table
cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)")

# Insert data into the table
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))

# Query the table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()  # Fetch all rows
for row in rows:
    print(row)  # Print each row

conn.commit()  # Save changes
conn.close()  # Close the database connection
```

```python
import sqlite3

conn = sqlite3.connect("example.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO products (name) VALUES (?)", ("Laptop",))

cursor.execute("SELECT * FROM products")
print(cursor.fetchall())

conn.commit()
conn.close()
```

### Java (JDBC with SQLite)

```java
import java.sql.*;

public class SQLiteExample {
    public static void main(String[] args) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:sqlite:test.db");  // Connect to SQLite
        Statement stmt = conn.createStatement();
        stmt.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)");
        stmt.execute("INSERT INTO users VALUES ('Alice', 25)");

        ResultSet rs = stmt.executeQuery("SELECT * FROM users");
        while (rs.next()) {
            System.out.println(rs.getString("name") + ", " + rs.getInt("age"));
        }
        conn.close();
    }
}
```

```java
import java.sql.*;

public class ProductDB {
    public static void main(String[] args) throws Exception {
        Connection conn = DriverManager.getConnection("jdbc:sqlite:example.db");
        Statement stmt = conn.createStatement();
        stmt.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)");
        stmt.execute("INSERT INTO products (name) VALUES ('Laptop')");

        ResultSet rs = stmt.executeQuery("SELECT * FROM products");
        while (rs.next()) {
            System.out.println(rs.getInt("id") + ": " + rs.getString("name"));
        }
        conn.close();
    }
}
```

### Go (sqlite3)

```go
package main
import (
    "database/sql"
    "fmt"
    _ "github.com/mattn/go-sqlite3"  // Import SQLite driver
)

func main() {
    db, _ := sql.Open("sqlite3", "test.db")  // Connect to SQLite database
    defer db.Close()

    db.Exec("CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)")
    db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Alice", 25)

    rows, _ := db.Query("SELECT name, age FROM users")
    defer rows.Close()

    var name string
    var age int
    for rows.Next() {
        rows.Scan(&name, &age)
        fmt.Println(name, age)
    }
}
```

```go
package main
import (
    "database/sql"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
)

func main() {
    db, _ := sql.Open("sqlite3", "example.db")
    defer db.Close()

    db.Exec("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)")
    db.Exec("INSERT INTO products (name) VALUES (?)", "Laptop")

    rows, _ := db.Query("SELECT id, name FROM products")
    var id int
    var name string
    for rows.Next() {
        rows.Scan(&id, &name)
        fmt.Println(id, name)
    }
}
```
...

---

## 18. Concurrency (Multithreading / Goroutines)

### Python (using threading)

```python
import threading  # Import the threading module

def print_numbers():
    for i in range(5):
        print("Thread 1 -", i)  # Print values from 0 to 4

def print_letters():
    for c in 'abcde':
        print("Thread 2 -", c)  # Print characters a to e

# Create two threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

thread1.start()  # Start the first thread
thread2.start()  # Start the second thread

thread1.join()  # Wait for thread1 to finish
thread2.join()  # Wait for thread2 to finish
```

```python
import threading

def task(name):
    for i in range(3):
        print(name, i)  # Print the name and index

# Launch multiple threads running the same function
threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(f"Worker-{i}",))  # Create thread with argument
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # Wait for each thread to complete
```

### Java (using Thread class)

```java
public class ThreadExample extends Thread {
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Thread - " + i);
        }
    }

    public static void main(String[] args) {
        ThreadExample t1 = new ThreadExample();
        ThreadExample t2 = new ThreadExample();
        t1.start();  // Start the first thread
        t2.start();  // Start the second thread
    }
}
```

```java
public class RunnableExample {
    public static void main(String[] args) {
        Runnable task = () -> {
            for (int i = 0; i < 3; i++) {
                System.out.println(Thread.currentThread().getName() + " - " + i);
            }
        };

        Thread t1 = new Thread(task, "Worker-1");
        Thread t2 = new Thread(task, "Worker-2");
        t1.start();
        t2.start();
    }
}
```

### Go (using goroutines)

```go
package main
import (
    "fmt"
    "time"
)

func printNumbers() {
    for i := 0; i < 5; i++ {
        fmt.Println("Goroutine 1 -", i)
        time.Sleep(100 * time.Millisecond)  // Delay for readability
    }
}

func printLetters() {
    for _, c := range "abcde" {
        fmt.Println("Goroutine 2 -", string(c))
        time.Sleep(100 * time.Millisecond)
    }
}

func main() {
    go printNumbers()  // Start printNumbers in a goroutine
    go printLetters()  // Start printLetters in a goroutine

    time.Sleep(1 * time.Second)  // Wait for goroutines to finish
    fmt.Println("Main function done")
}
```

```go
package main
import (
    "fmt"
    "sync"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()  // Notify WaitGroup when done
    for i := 0; i < 3; i++ {
        fmt.Printf("Worker %d - %d\n", id, i)
    }
}

func main() {
    var wg sync.WaitGroup  // WaitGroup to wait for all goroutines

    for i := 1; i <= 2; i++ {
        wg.Add(1)  // Increment counter
        go worker(i, &wg)  // Start worker goroutine
    }

    wg.Wait()  // Wait for all goroutines to finish
    fmt.Println("All workers done")
}
```
...

---

## 19. Unit Testing

### Python (using unittest)

```python
import unittest  # Import the unittest module

def add(a, b):
    return a + b  # Simple function to add two numbers

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)  # Test if 2 + 3 equals 5
        self.assertEqual(add(-1, 1), 0)  # Test with negative number

if __name__ == '__main__':
    unittest.main()  # Run the tests
```

```python
import unittest

def multiply(a, b):
    return a * b  # Simple multiplication function

class TestMultiply(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(0, 10), 0)

if __name__ == '__main__':
    unittest.main()
```

### Java (using JUnit)

```java
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class MathTest {
    public int add(int a, int b) {
        return a + b;
    }

    @Test
    public void testAdd() {
        assertEquals(5, add(2, 3));
        assertEquals(0, add(-1, 1));
    }
}
```

```java
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class MultiplyTest {
    public int multiply(int a, int b) {
        return a * b;
    }

    @Test
    public void testMultiply() {
        assertEquals(20, multiply(4, 5));
        assertEquals(0, multiply(0, 10));
    }
}
```

### Go (using testing package)

```go
package main

func add(a, b int) int {
    return a + b
}
```

```go
package main
import "testing"

func TestAdd(t *testing.T) {
    if add(2, 3) != 5 {
        t.Errorf("Expected 5, got %d", add(2, 3))
    }
    if add(-1, 1) != 0 {
        t.Errorf("Expected 0, got %d", add(-1, 1))
    }
}
```

```go
package main

func multiply(a, b int) int {
    return a * b
}
```

```go
package main
import "testing"

func TestMultiply(t *testing.T) {
    if multiply(4, 5) != 20 {
        t.Errorf("Expected 20, got %d", multiply(4, 5))
    }
    if multiply(0, 10) != 0 {
        t.Errorf("Expected 0, got %d", multiply(0, 10))
    }
}
```







