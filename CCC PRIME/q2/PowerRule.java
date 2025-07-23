import java.util.Scanner;


public class PowerRule {


    public static void main(String[] args) throws Exception {
        Scanner keyboard = new Scanner(System.in);


        System.out.println("How many terms in your polynomial?");
        int terms = keyboard.nextInt();


        double[] coefficients = new double[terms];
        int[] degrees = new int[terms];


        System.out.println("Enter " + terms + " coefficients:");
        for (int i = 0; i < terms; i++) {
            coefficients[i] = keyboard.nextDouble();
        }


        System.out.println("Enter " + terms + " degrees:");
        for (int i = 0; i < terms; i++) {
            degrees[i] = keyboard.nextInt();
        }


        System.out.print("first derivative is: f'(x) = ");
        for (int i = 0; i < terms; i++) {
            double coeffPrime = coefficients[i] * degrees[i];
            int degreePrime = degrees[i] - 1;


            if (degreePrime != 0) {
                if (degreePrime == 1) {
                    System.out.print(coeffPrime + "x");
                } else {
                    System.out.print(coeffPrime + "x^" + degreePrime);
                }
            } else {
                System.out.print(coeffPrime);
            }


            if (i < terms - 1) {
                System.out.print(" + ");
            }
        }


        System.out.println();


        System.out.print("Second derivative is: f''(x) = ");
        for (int i = 0; i < terms; i++) {
            double coeffPrime = coefficients[i] * degrees[i]; // it's same as top "function", but it does it two times basically
            int degreePrime = degrees[i] - 1;


            if (degreePrime != 0) {
                double coeffPrimeTwo = coeffPrime * degreePrime;
                int degreePrimeTwo = degreePrime - 1;


                if (degreePrimeTwo != 0) {
                    if (degreePrime == 1) {
                        System.out.print(coeffPrimeTwo + "x");
                    } else {
                        System.out.print(coeffPrimeTwo + "x^" + degreePrime);
                    }
                } else {
                    System.out.print(coeffPrimeTwo);
                }


                if (i < terms - 1) {
                    System.out.print(" + ");
                }
            }
        }
    }
}



