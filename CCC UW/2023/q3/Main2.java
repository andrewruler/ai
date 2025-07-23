import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int N = sc.nextInt();
        int M = sc.nextInt();
        int R = sc.nextInt();
        int C = sc.nextInt();
        sc.close();
        
        // Check for impossible case
        if (R > N || C > M || (C==M && R!=N) || (C!=M && R==N)){
            System.out.println("IMPOSSIBLE");
            return;
        }
        
        // Initialize grid with 'a'
        char[][] grid = new char[N][M];
        for (int i = 0; i < N; i++) {
            Arrays.fill(grid[i], 'b');
        }

        for(int i = 0; i<N; i++){
            for(int j = 0; j<C;j++){
                grid[i][j] = 'a';
            }
        }

        for(int i = 0; i<M; i++){
            for(int j = 0; j<R;j++){
                grid[j][i] = 'a';
            }
        }

        for (char[] row : grid) {
            System.out.println(new String(row)); // Converts row to String
        }
        
    }
}