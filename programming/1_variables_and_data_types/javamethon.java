// Define the Person class (the blueprint)
public class Person {
    // Attributes (instance variables)
    String name;
    int age;
    float height;
    boolean isStudent;

    // Constructor to initialize objects
    public Person(String name, int age, float height, boolean isStudent) {
        this.name = name;       // 'this' refers to the current object's attribute
        this.age = age;
        this.height = height;
        this.isStudent = isStudent;
    }

    // Method to display a person's introduction
    public void introduce() {
        System.out.println(name + " is " + age + " years old, " + height + " feet tall, and is a student: " + isStudent);
    }

    // Main method to run the program
    public static void main(String[] args) {
        // Creating objects (instances) of the Person class
        Person person1 = new Person("Alice", 25, 5.9f, true);
        Person person2 = new Person("Bob", 30, 6.1f, false);

        // Calling the introduce method for each object
        person1.introduce();
        person2.introduce();
    }
}