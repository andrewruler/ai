/**
 * Description of Pet
 */
public class Pet {
    private String name;
    private int age;

    public Pet() throws Exception {
        this("Unknown", 0);
    }

    public Pet(String name, int age) throws Exception {
        this.name = name;
        this.age = age;
    }

    public String eat() {
        return name + " is eating.";
    }

    public String sleep() {
        return name + " is sleeping.";
    }

    public String describe() {
        return name + " is " + age + " years old.";
    }

    public String getName() {
        return name;
    }
}

