// Name:   
// Date: 
import java.util.*;
import java.io.*;
public class PigLatin
{
   public static void main(String[] args) 
   {
      //part_1_using_pig();
      part_2_using_piglatenizeFile();
      
      /*  extension only    */
      // String pigLatin = pig("What!?");
      // System.out.print(pigLatin + "\t\t" + pigReverse(pigLatin));   //Yahwta!?
      // pigLatin = pig("{(Hello!)}");
      // System.out.print("\n" + pigLatin + "\t\t" + pigReverse(pigLatin)); //{(Yaholle!)}
      // pigLatin = pig("\"McDonald???\"");
      // System.out.println("\n" + pigLatin + "  " + pigReverse(pigLatin));//"YaDcmdlano???"
   }

   public static void part_1_using_pig()
   {
      Scanner sc = new Scanner(System.in);
      while(true)
      {
         System.out.print("\nWhat word? ");
         String s = sc.next();
         if(s.equals("-1"))
         {
            System.out.println("Goodbye!"); 
            System.exit(0);
         }
         String p = pig(s);
         System.out.println( p );
      }		
   }

   public static final String punct = ",./;:'\"?<>[]{}|`~!@#$%^&*()";
   public static final String letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
   public static final String vowels = "AEIOUaeiou";
   public static String pig(String s)
   {
      if(s.length() == 0)
         return "";
   
      String igpay = "";
   
      //remove and store the beginning punctuation 
      String firstPunct = "";
      
      for (int i=0; i<s.length(); i++)
      {
         if(!Character.isLetterOrDigit(s.charAt(i)))
         {
            continue;
         }
         else
         {
            firstPunct = s.substring(0, i);
            char temp[] = s.toCharArray();
            s = "";
            for(int j=i; j<temp.length; j++)
            {
               s += temp[j];
            }
            break;
         }
      }
      
     
     
     
      //remove and store the ending punctuation 
      String lastPunct = "";
      for (int i=s.length()-1; i>=0; i--)
      {
         if(!Character.isLetterOrDigit(s.charAt(i)))
         {
            continue;
         }
         else
         {
            lastPunct = s.substring(i+1, s.length());
            char temp[] = s.toCharArray();
            s = "";
            for(int j=0; j<=i; j++)
            {
               s += temp[j];
            }
            break;
         }
      }
      
      //System.out.println("After punct removal: " + s);
      
      
      //START HERE with the basic case:
      //     find the index of the first vowel
      //     y is a vowel if it is not the first letter
      //     qu
      
      int vowindex = 0;
      boolean firstvow = false;
      boolean firstupper = false;
      boolean vowfound = false;
      boolean novow = false;
      int startsearch = 1;
      
      for(int n=0; n<vowels.length(); n++)
      {
         if (s.charAt(0) == vowels.charAt(n))
         {
            firstvow = true;
            vowfound = true;
         }
      }
      
      
      
      if (!firstvow)
      {
         if((s.substring(0, 2).toLowerCase()).equals("qu") && vowels.contains("" + s.charAt(2)))
            startsearch = 2;
         for(int m=startsearch; m<s.length(); m++)
         {
            if(vowfound)
               break;
            if(m < s.length()-2)
            {
               if ((s.substring(m, m+2).toLowerCase()).equals("qu") && vowels.contains("" + s.charAt(m+2)))
               {
                  m++;
                  continue;
               }
            }
            
            if (vowels.contains("" + s.charAt(m)) || Character.toLowerCase(s.charAt(m)) == 'y')
            {
               vowindex = m;
               vowfound = true;
               break;
            }
            
            
         }
      }
      
      if(!vowfound) //if no vowel has been found
         novow = true;
      
      
      //is the first letter capitalized?
      if(Character.isUpperCase(s.charAt(0)))
         firstupper = true;
      
      //return the piglatinized word 
      if(novow)
      {
         return "**** NO VOWEL ****";
      }
      else
      {
         if(firstupper) //if the first letter is capitalized
         {
            char[] divide = s.toCharArray();
            String replaced = "";
            String convert = "";
            divide[0] = Character.toLowerCase(s.charAt(0));
            for(char c : divide)
            {
               replaced += c;
            }
            
            if(firstvow) //if starts with vowel
            {
               convert = replaced + "way";
            }
            else
            {
               convert = replaced.substring(vowindex) + replaced.substring(0, vowindex) + "ay";
            }
            char[] divide2 = convert.toCharArray();
            divide2[0] = Character.toUpperCase(convert.charAt(0));
            for(char c : divide2)
            {
               igpay += c;
            }
         }
         else
         {
            if(firstvow) //if starts with vowel
            {
               igpay = s + "way";
            }
            else
            {
               igpay = s.substring(vowindex) + s.substring(0, vowindex) + "ay";
            }
         }
         
         return firstPunct + igpay + lastPunct;
      }
   }


   public static void part_2_using_piglatenizeFile() 
   {
      Scanner sc = new Scanner(System.in);
      System.out.print("input filename including .txt: ");
      String fileNameIn = sc.next();
      System.out.print("output filename including .txt: ");
      String fileNameOut = sc.next();
      piglatenizeFile( fileNameIn, fileNameOut );
      System.out.println("Piglatin done!");
   }

/****************************** 
*  piglatinizes each word in each line of the input file
*    precondition:  both fileNames include .txt
*    postcondition:  output a piglatinized .txt file 
******************************/
   public static void piglatenizeFile(String fileNameIn, String fileNameOut) 
   {
      Scanner infile = null;
      try
      {
         infile = new Scanner(new File(fileNameIn));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
   
      PrintWriter outfile = null;
      try
      {
         outfile = new PrintWriter(new FileWriter(fileNameOut));
      }
      catch(IOException e)
      {
         System.out.println("File not created");
         System.exit(0);
      }
   	//process each word in each line
      while(infile.hasNextLine())
      {
         String lines = infile.nextLine();
         String[] splitlines = lines.split(" ");
         for(String str : splitlines)
         {
            outfile.print(pig(str) + " ");
         }
         outfile.print("\n");
      }
      
      
   
      outfile.close();
      infile.close();
   }
   
   /** EXTENSION: Output each PigLatin word in reverse, preserving before-and-after 
       punctuation.  
   */
   public static String pigReverse(String s)
   {
      if(s.length() == 0)
         return "";
         
      boolean firstupper = false;
      
      String firstPunct = "";
      
      for (int i=0; i<s.length(); i++)
      {
         if(!Character.isLetterOrDigit(s.charAt(i)))
         {
            continue;
         }
         else
         {
            firstPunct = s.substring(0, i);
            char temp[] = s.toCharArray();
            s = "";
            for(int j=i; j<temp.length; j++)
            {
               s += temp[j];
            }
            break;
         }
      }
      
     
     
     
      //remove and store the ending punctuation 
      String lastPunct = "";
      for (int i=s.length()-1; i>=0; i--)
      {
         if(!Character.isLetterOrDigit(s.charAt(i)))
         {
            continue;
         }
         else
         {
            lastPunct = s.substring(i+1, s.length());
            char temp[] = s.toCharArray();
            s = "";
            for(int j=0; j<=i; j++)
            {
               s += temp[j];
            }
            break;
         }
      }
   
      if(Character.isUpperCase(s.charAt(0)))
      {
         firstupper = true;
      }
      char[] sArray = s.toCharArray();
      s = "";
      
      
      
      if(firstupper)
      {
         
         sArray[sArray.length-1] = Character.toUpperCase(sArray[sArray.length-1]);
         sArray[0] = Character.toLowerCase(sArray[0]);
      }
      
      for(int i=sArray.length-1; i>=0; i--)
      {
         s += sArray[i];
         /*
         System.out.println();
         System.out.println(i + "\t" + sArray[i]);
         System.out.println(s);
         */
      }
      
      return firstPunct + s + lastPunct;     
   }
}
