import java.util.*;

public class q2 {
    public static boolean checkAlternates(String str) {
        int[] alphabet = new int[26];  // Only track 'a' to 'z'
        
        // Count character occurrences
        for (int j = 0; j < str.length(); j++) {
            alphabet[str.charAt(j) - 'a']++;
        }

        // Determine if first character is heavy or light
        boolean isPrevHeavy = alphabet[str.charAt(0) - 'a'] > 1;

        // Iterate through the string to check alternating pattern
        for (int i = 1; i < str.length(); i++) {
            boolean currentHeavy = alphabet[str.charAt(i) - 'a'] > 1;

            // Heavy-Heavy or Light-Light in consecutive places → Invalid
            if (currentHeavy == isPrevHeavy) {
                return false;
            }

            // Toggle previous state
            isPrevHeavy = currentHeavy;
        }

        return true;  // Valid alternating pattern
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numStrings = sc.nextInt();
        int stringsLength = sc.nextInt();
        sc.nextLine(); // Consume newline after integer input

        for (int i = 0; i < numStrings; i++) {
            String string = sc.nextLine();
            System.out.println(checkAlternates(string) ? "T" : "F");
        }

        sc.close();
    }
}
