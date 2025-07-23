import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] A = new int[n];
        int[] B = new int[n];
        
        for (int i = 0; i < n; i++) {
            A[i] = scanner.nextInt();
        }
        for (int i = 0; i < n; i++) {
            B[i] = scanner.nextInt();
        }
        
        List<String> operations = new ArrayList<>();
        
        if (canTransform(A, B, operations)) {
            System.out.println("YES");
            System.out.println(operations.size());
            for (String op : operations) {
                System.out.println(op);
            }
        } else {
            System.out.println("NO");
        }
    }
    
    private static boolean canTransform(int[] A, int[] B, List<String> operations) {
        int n = A.length;
        
        // If already the same, no operations needed
        if (Arrays.equals(A, B)) {
            return true;
        }
        
        for (int i = 0; i < n; i++) {
            if (A[i] < B[i]) {
                return false; // Can't increase values, so impossible
            }
        }
        
        for (int i = n - 1; i >= 0; i--) {
            while (A[i] > B[i]) {
                int diff = A[i] - B[i];
                boolean moved = false;
                
                // Try swiping right first
                for (int j = 0; j < i; j++) {
                    if (A[j] >= diff) {
                        A[j] -= diff;
                        A[j + 1] += diff;
                        operations.add("R " + (j + 1) + " " + (j + 2));
                        moved = true;
                        break;
                    }
                }
                
                // If right swipe fails, try left swipe
                if (!moved) {
                    for (int j = i; j > 0; j--) {
                        if (A[j] >= diff) {
                            A[j] -= diff;
                            A[j - 1] += diff;
                            operations.add("L " + j + " " + (j + 1));
                            moved = true;
                            break;
                        }
                    }
                }
                
                // If neither worked, it's impossible
                if (!moved) {
                    return false;
                }
            }
        }
        return Arrays.equals(A, B);
    }
}
