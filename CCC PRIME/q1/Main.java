import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int A = input.nextInt();
        int B = input.nextInt(); // height
        int X = input.nextInt();
        int Y = input.nextInt(); // height

        boolean useHeight = Math.min(B, Y) < Math.min(A, X);
        
        int result = 2* A + 2 * X + 2* B + 2 * Y;
        if (useHeight){
            if(A>X){
                result -= X*2;
            } else if (A<=X){
                result -= A*2;
            }
        } else {
            if(B>Y){
                result -= Y*2;
            } else if (B<=Y){
                result -= B*2;
            }
        }

        System.out.println(result);
    }
}