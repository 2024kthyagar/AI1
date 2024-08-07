// Name:
// Date:

import java.util.*;
import java.io.*;

public class Josephus
{
   private static String WINNER = "Jophesus";
   
   public static void main(String[] args) throws FileNotFoundException
   {
      ListNode p = null;
      p = insert(p, "B");
      p = insert(p, "C");
      p = insert(p, "D");
      p = insert(p, "E");
      p = insert(p, "F");
      print(p);
        
      /* run numberCircle first with J_numbers.txt  */
      Scanner sc = new Scanner(System.in);
      System.out.print("How many names (2-20)? ");
      int n = Integer.parseInt(sc.next());
      System.out.print("How many names to count off each time?"  );
      int countOff = Integer.parseInt(sc.next());
      ListNode winningPos = numberCircle(n, countOff, "J_numbers.txt");
      System.out.println(winningPos.getValue() + " wins!");  
     
      /* run josephusCircle next with J_names.txt  */
      System.out.println("\n ****  Now start all over. **** \n");
      System.out.print("Where should "+WINNER+" stand?  ");
      int winPos = Integer.parseInt(sc.next());        
      ListNode theWinner = josephusCircle(n, countOff, "J_names.txt", winPos);
      System.out.println(theWinner.getValue() + " wins!");  
   }
   
   public static ListNode numberCircle(int n, int countOff, String filename) throws FileNotFoundException
   {
      ListNode p = null;
      p = readNLinesOfFile(n, new File(filename));
      p = countingOff(p, countOff, n);
      return p;
   }
   
   public static ListNode josephusCircle(int n, int countOff, String filename, int winPos) throws FileNotFoundException
   {
      ListNode p = null;
      p = readNLinesOfFile(n, new File(filename));
      replaceAt(p, WINNER, winPos);
      p = countingOff(p, countOff, n);
      return p;
   }

   /* reads the names, calls insert(), builds the linked list.
	 */
   public static ListNode readNLinesOfFile(int n, File f) throws FileNotFoundException
   {
      ListNode listy = null;
      Scanner infile = null;
      try
      {
         infile = new Scanner(f);  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
   	//process each word in each line
      for(int i=0; i<n; i++)
      {
         listy = insert(listy, infile.next());
      }
      infile.close();
      return listy;
   }
   
   /* helper method to build the list.  Creates the node, then
      inserts it in the circular linked list.
	 */
   public static ListNode insert(ListNode p, Object obj)
   {
      if(p == null)
      {
         p = new ListNode(obj, null);
         p.setNext(p);
      }
      else
      {
         p.setNext(new ListNode(obj, p.getNext()));
         p = p.getNext();
         
      }
      return p;
   }
   
   /* Runs a Josephus game, counting off and removing each name. Prints after each removal.
      Ends with one remaining name, who is the winner. 
	 */
   public static ListNode countingOff(ListNode p, int count, int n)
   {
      print(p);
      for(int i=0; i<n-1; i++)
      {
         p = remove(p, count);
         print(p);  
      }
      return p;
   }
   
   /* removes the node after counting off count-1 nodes.
	 */
   public static ListNode remove(ListNode p, int count)
   {
      ListNode iter = p;
      for(int i=0; i<count-1; i++)
         iter = iter.getNext();
      iter.setNext(iter.getNext().getNext());
      return iter;
   }
   
   /* prints the circular linked list.
	 */
   public static void print(ListNode p)
   {
      for(ListNode iter = p.getNext(); iter != p && iter != null; iter = iter.getNext())
      {
         System.out.print(iter.getValue() + " ");
      } 
      System.out.print(p.getValue());
      System.out.println();
   }
	
   /* replaces the value (the String) at the winning node.
	 */
   public static void replaceAt(ListNode p, Object obj, int pos)
   {
      p = p.getNext();
      ListNode iter = p;
      for(int i=0; i<pos-1; i++)
      {
         iter = iter.getNext();
      }
      iter.setValue(obj);
   }
}
/**********************************************************
     
 B C D E F
 How many names (2-20)? 5
 How many names to count off each time? 2
 1 2 3 4 5
 3 4 5 1
 5 1 3
 3 5
 3
 3 wins!
 
  ****  Now start all over. **** 
 
 Where should Josephus stand?  3
 Michael Hannah Josephus Ruth Matthew
 Josephus Ruth Matthew Michael
 Matthew Michael Josephus
 Josephus Matthew
 Josephus
 Josephus wins!
 
  ----jGRASP: operation complete.
  
  **************************************************/

