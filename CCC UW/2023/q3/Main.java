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
        if (R > N || C > M){
            System.out.println("IMPOSSIBLE");
            return;
        }
        
        // Initialize grid with 'a'
        char[][] grid = new char[N][M];
        for (int i = 0; i < N; i++) {
            Arrays.fill(grid[i], 'a');
        }
        if((C==M && )){

        } else if ((C!=M && R==N)){
        } else {

        for(int j = C;j<M;j++){ // cols
            System.out.println(j);
            int i = 0;
            for (i = 0; i < N-R; i++) { //rows
                grid[i][j] = (char)(j%25 + 'a');
            }
            // System.out.println(Arrays.deepToString(grid));
        } 

        for (char[] row : grid) {
            System.out.println(new String(row)); // Converts row to String
        }
    }
    }
}