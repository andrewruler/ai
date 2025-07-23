import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int N = input.nextInt();
        int M = input.nextInt();
        int K = input.nextInt();

        int diff = K - N;
        int[] output = new int[N];
        int current = 1;
        boolean alternate = false;
        int totalTracker = 0;

        for (int i = 0; i < N; i++) {
            alternate = diff > 0;
            if(alternate && i >0 ) {
                current = (current) % 2 + 1;
                totalTracker +=2;
                diff--;
            } else {
                totalTracker+=1;
            }
            output[i] = current;
        }
        //
        System.out.println("totalTracker: " + totalTracker);
        System.out.println(Arrays.toString(output));
        if(totalTracker == K) {
            for (int i = 0; i < N; i++) {
                System.out.print(output[i] + " ");
            }
        } else {
            System.out.println(-1);
        }
    }
}