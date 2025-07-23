import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numSeats = sc.nextInt();
        int [] hats = new int[numSeats];
        int hatCounter = 0;
        for(int i = 0; i<numSeats;i++){
            hats[i] = sc.nextInt();
        }

        for(int j = 0; j<numSeats/2;j++){
            // System.out.println(hats[j]);
            // System.out.println(hats[(numSeats/2)-1+j]);
            if(hats[j]==hats[(numSeats/2)+j]){
                hatCounter+=2;
            }
        }

        System.out.println(hatCounter);

    }
}