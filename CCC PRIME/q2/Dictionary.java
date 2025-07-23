import java.io.BufferedReader; 
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashSet;
import java.util.Scanner;


public class Dictionary {
   public static void main(String[] args) throws Exception {
       BufferedReader inputStream = null;
       String line = "";
       HashSet<String> dictionary = new HashSet<>();


       try {
           inputStream = new BufferedReader(new FileReader("dictionary.txt"));
           while ((line = inputStream.readLine()) != null) {
               line = line.trim();
               if (!line.isEmpty()) {
                   dictionary.add(line);
               }
           }
       } catch (FileNotFoundException exception) {
           System.out.println("dictionary.txt not found.");
           return;
       } catch (IOException exception) {
           System.out.println("Error reading dictionary.txt");
           return;
       } finally {
           if (inputStream != null) {
               inputStream.close();
           }
       }


       Scanner keyboard = new Scanner(System.in);
       System.out.println("Enter a sentence in English:");
       String sentence = keyboard.nextLine();
       keyboard.close();


       String[] words = sentence.split("\\s+");


       for (String word : words) {
           String cleanWord = word.toLowerCase().replaceAll("[^a-z]", "");


           if (cleanWord.isEmpty())
               continue;


           if (dictionary.contains(cleanWord)) {
               System.out.println(word + " <valid>");


           } else {
               System.out.println(word + " <invalid>");


           }
       }
   }
}



