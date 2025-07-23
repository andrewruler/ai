
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Read input
        int N = scanner.nextInt();
        int[] A = new int[N];
        int[] B = new int[N];

        for (int i = 0; i < N; i++) {
            A[i] = scanner.nextInt();
        }
        for (int i = 0; i < N; i++) {
            B[i] = scanner.nextInt();
        }
        
        // Check if A is already equal to B
        if (Arrays.equals(A,B)) {
            System.out.println("YES");
            System.out.println(0);
            return;
        }

        // List to store swipe operations
        List<String> operations = new ArrayList<>();
        List<int[]> segments = new ArrayList<>();

        int currentSegmentNum = B[0];

        int l = 0;
        int r = 0;
        
        for(int i = 0; i<N;i++){
          if(B[i]!=currentSegmentNum){
            r=i-1;
            segments.add(new int[]{l,r});
            l = i;
            currentSegmentNum = B[l];
          }
        }
        segments.add(new int[]{l,N-1});

        for(int i = 0; i<segments.size();i++){
          int[] seg = segments.get(i);
          l = seg[0];
          r = seg[1];
          // System.out.println("l+r:" + l + " " +r);
          int target = B[l];

          for(int j = l; j<N;j++){
            // System.out.println("A at "+j+" = "+ A[j] + " Target = " + target +". j = " + j + ". l = " + l);
            if(A[j]==target && j>l){
              operations.add("L " + j + " " + l);
              Arrays.fill(A,l,j,target);
              break;
            }
          }
        }
        // System.out.println(Arrays.toString(A) + Arrays.toString(B));

        for(int i = segments.size() - 1; i>=0;i--){
          int[] seg = segments.get(i);

          // System.out.println("segments "+(Arrays.toString(seg)));
         
          l = seg[0];
          r = seg[1];
           
          int target = B[l];
          // System.out.println("target: " + target);
          for(int j = N - 1; j>=0;j--){
            // System.out.println("l: " + l + "j: " + j);
            if(A[j]==target && j<r){
              operations.add("R " + j + " " + r);
              Arrays.fill(A,j,r+1,target);
              break;
            }
          }
        }

        // System.out.println(Arrays.toString(A) + Arrays.toString(B));

        if(Arrays.equals(A,B)){
          System.out.println("YES");
          System.out.println(operations.size());
          for(String op: operations){
            System.out.println(op);
          }
        } else {
          System.out.println("NO");
        }
    }
}