public class Dog extends Pet {
    private String breed;

    public Dog() throws Exception {
        super();
        this.breed = "Mixed Breed";
    }

    public Dog(String name, int age, String breed) throws Exception {
        super(name, age);
        this.breed = breed;
    }

    public String bark() {
        return getName() + " says: Woof!";
    }

    public String fetch() {
        return getName() + " fetched the ball!";
    }

    @Override
    public String describe() {
        return super.describe() + " Breed: " + breed;
    }
}


