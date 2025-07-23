import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int a = sc.nextInt() - 1;
        int b = sc.nextInt()- 1;
        int c = sc.nextInt()- 1;
        int d = sc.nextInt()- 1;
        int e = sc.nextInt()- 1;

        // Corrected character conversion
        System.out.println((char) a);
        System.out.println((char) b);
        System.out.println((char) c);
        System.out.println((char) d);
        System.out.println((char) e);

        sc.close(); // Best practice: Close the scanner when done
    }
}