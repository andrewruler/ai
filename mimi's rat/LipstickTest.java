public class LipstickTest {
    public static void main(String[] args) {
        // Loop through each lipstick enum value and print its brand profile
        for (Lipstick lipstick : Lipstick.values()) {
            System.out.println(lipstick.getBrandProfile());
        }
    }
}



