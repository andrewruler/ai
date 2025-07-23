public class Cat extends Pet {
    private String breed;

    public Cat() throws Exception {
        super();
        this.breed = "Domestic Shorthair";
    }

    public Cat(String name, int age, String breed) throws Exception {
        super(name, age);
        this.breed = breed;
    }

    public String meow() {
        return getName() + " says: Meow!";
    }

    public String scratch() {
        return getName() + " is scratching the couch!";
    }

    @Override
    public String describe() {
        return super.describe() + " Breed: " + breed;
    }
}

