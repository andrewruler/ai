public class TestPets {
    public static void main(String[] args) {
        try {
            // Test Pet
            Pet pet = new Pet("Generic", 3);
            System.out.println("--- Testing Pet ---");
            System.out.println(pet.describe());
            System.out.println(pet.eat());
            System.out.println(pet.sleep());

            // Test Cat
            Cat cat = new Cat("Whiskers", 5, "Siamese");
            System.out.println("\n--- Testing Cat ---");
            System.out.println(cat.describe());
            System.out.println(cat.meow());
            System.out.println(cat.scratch());

            // Test Dog
            Dog dog = new Dog("Buddy", 4, "Golden Retriever");
            System.out.println("\n--- Testing Dog ---");
            System.out.println(dog.describe());
            System.out.println(dog.bark());
            System.out.println(dog.fetch());
        } catch (Exception e) {
            System.out.println("Error creating pet: " + e.getMessage());
        }
    }
}