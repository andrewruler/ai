import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String S = sc.nextLine();
        long c = sc.nextLong();
        long lengthOfPattern = 0;
        long currentNum = 0;

        if(S.length() > 1000000) {
            char currentChar;
            long remainder = c;
            for(int i = 1; i < S.length(); i+=2){
                currentChar = S.charAt(i-1);
                currentNum = S.charAt(i) - '0';
                while((i!= S.length()-1) && !(Character.isLetter(S.charAt(i+1))) ){
                    currentNum *= 10;
                    currentNum += S.charAt(i+1) - '0';
                    i++;
                }
                remainder -= currentNum;

                if(remainder < 0){
                    System.out.print(currentChar);
                    break;
                }
            }
        } else {
            for(int i = 1; i < S.length(); i+=2){
                currentNum = S.charAt(i) - '0';
                while((i!= S.length()-1) && !(Character.isLetter(S.charAt(i+1))) ){
                    currentNum *= 10;
                    currentNum += S.charAt(i+1) - '0';
                    i++;
                }
                lengthOfPattern += currentNum;
            }

            // System.out.println("length of Pattern " + lengthOfPattern);
            long modC = c % lengthOfPattern;
            long remainder = modC ;
            char currentChar;
            // System.out.println(remainder);
            
            if(remainder == 0){
                System.out.print(S.charAt(0));
            } else {
                for(int i = 1; i < S.length(); i+=2){
                    currentChar = S.charAt(i-1);
                    currentNum = S.charAt(i) - '0';
                    while((i!= S.length()-1) && !(Character.isLetter(S.charAt(i+1))) ){
                        currentNum *= 10;
                        currentNum += S.charAt(i+1) - '0';
                        i++;
                    }
                    remainder -= currentNum;
                    
                    if(remainder < 0){
                        System.out.print(currentChar);
                        break;
                    }
                }
            }
        }
        
    }
}