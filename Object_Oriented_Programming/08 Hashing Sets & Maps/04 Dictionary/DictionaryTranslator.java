import java.io.*;
import java.util.*;
import javax.swing.*;

public class DictionaryTranslator
{
   public static void main(String[] args)
   {
      Scanner infile = null;
      PrintWriter outfile = null;
      try
      {
         infile = new Scanner(new File("dictionaryOutput.txt"));
      }
      catch(Exception e)
      {
      }
      Map<String, Set<String>> map = makeDictionary(infile);
      String password = "Lbad";
      while(true)
      {
         int option = 0;
         try
         {
            option = Integer.parseInt(JOptionPane.showInputDialog("Would you like to translate: \n1. English to Spanish \n2. Spanish to English \n3. Change Dictionary \n-1 to Cancel"));
         }
         catch (Exception e)
         {
         }
         
         if(option == -1)
            System.exit(0);
         if(option == 0)
            System.out.println("Please enter a valid option.");
         else if(option == 1)
         {
            String input = JOptionPane.showInputDialog("Enter the word you want to translate: ");
            System.out.println(getSpanish(map, input));
         }
         else if(option == 2)
         {
            String input = JOptionPane.showInputDialog("Enter the word you want to translate: ");
            System.out.println(getEnglish(map, input));
         }
         else if(option == 3)
         {
            for(int i=0; i<5; i++)
            {
               String passwd = JOptionPane.showInputDialog("Enter the password: ");
               if(!passwd.equals(password))
               {
                  System.out.println("Sorry, that is the wrong password.");
               }
               else
               {
                  String eng = JOptionPane.showInputDialog("Enter the English word: ");
                  String span = JOptionPane.showInputDialog("Enter the Spanish word: ");
                  changeDict(map, eng, span);
                  break;
               }
            }
         }
      }
      
   }
   
   public static Map<String, Set<String>> makeDictionary(Scanner infile)
   {
      Map<String, Set<String>> map = new TreeMap<>();
      while(infile.hasNextLine())
      {
         String type = infile.nextLine().strip();
         if(type.equals("ENGLISH TO SPANISH") || type.equals("SPANISH TO ENGLISH"))
            type = infile.nextLine().strip();
         String[] word = type.split(" ", 2);
         word[1] = word[1].substring(1,word[1].length()-1);
         String[] defs = word[1].split(", ");
         for(String s : defs)
            Dictionary.add(map, word[0], s);
      }
      return map;
   }
   
   public static String getSpanish(Map<String, Set<String>> map, String input)
   {
      if(!map.containsKey(input))
         return "Sorry, that word does not exist.";
      return input + " translates to " + map.get(input) + " in spanish.";
   }
   
   public static String getEnglish(Map<String, Set<String>> map, String input)
   {
      if(!map.containsKey(input))
         return "Sorry, that word does not exist.";
      return input + " translates to " + map.get(input) + " in english.";
   }
   
   public static void changeDict(Map<String, Set<String>> map, String word, String translation)
   {
      Dictionary.add(map, word, translation);
      Dictionary.add(map, translation, word);
      System.out.println("Added " + word + " and " + translation + " to dictionary.");
   }
}