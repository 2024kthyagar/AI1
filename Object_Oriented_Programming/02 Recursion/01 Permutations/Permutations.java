// Name:
// Date:
  
import java.util.*;
public class Permutations
{
   public static int count = 0;
    
   public static void main(String[] args)
   {
      Scanner sc = new Scanner(System.in);
      System.out.print("\nHow many digits? ");
      int n = sc.nextInt();
      //leftRight("", n);  
              
      //oddDigits("", n);
      
      superprime(n);
      if(count==0)
         System.out.println("no superprimes");
      else
         System.out.println("Count is "+count);
   }
   
    /**
     * Builds all the permutations of a string of length n containing Ls and Rs
     * @param s A string 
     * @param n An postive int representing the length of the string
     */
   public static void leftRight(String s, int n)
   {
      if(s.length() == n)
         System.out.println(s);
      else 
      {
         leftRight(s + "L", n);
         leftRight(s + "R", n);
      }
   }
   
    /**
     * Builds all the permutations of a string of length n containing odd digits
     * @param s A string 
     * @param n A postive int representing the length of the string
     */
   public static void oddDigits(String s, int n)
   {
   
      if(s.length() == n)
      {
         System.out.println(s);
      }
      
      else
      {
         oddDigits(s + "1", n);
         oddDigits(s + "3", n);
         oddDigits(s + "5", n);
         oddDigits(s + "7", n);
         oddDigits(s + "9", n);
      }
   }
      
    /**
     * Builds all combinations of a n-digit number whose value is a superprime
     * @param n A positive int representing the desired length of superprimes  
     */
   public static void superprime(int n)
   {
      recur(2, n); //try leading 2, 3, 5, 7, i.e. all the single-digit primes
      recur(3, n); 
      recur(5, n);
      recur(7, n);
   }

    /**
     * Recursive helper method for superprime
     * @param k The possible superprime
     * @param n A positive int representing the desired length of superprimes
     */
   private static void recur(int k, int n)
   {
      if(!isPrime(k))
      {
      }
      else if(Integer.toString(k).length() == n)
      {
         System.out.println(k);
         count++;
      }
      else
      {
         recur(Integer.parseInt(Integer.toString(k) + "1"), n);
         recur(Integer.parseInt(Integer.toString(k) + "3"), n);
         recur(Integer.parseInt(Integer.toString(k) + "5"), n);
         recur(Integer.parseInt(Integer.toString(k) + "7"), n);
         recur(Integer.parseInt(Integer.toString(k) + "9"), n);
      }
      
   }

    /**
     * Determines if the parameter is a prime number.
     * @param n An int.
     * @return true if prime, false otherwise.
     */
   public static boolean isPrime(int n)
   {
      int factor = 3;
      while(factor <= Math.sqrt(n))
      {
         if(n%factor == 0 || (n!=2 && n%2==0))
            return false;
         else
            factor += 2;
      }
      return true;
   }
}
