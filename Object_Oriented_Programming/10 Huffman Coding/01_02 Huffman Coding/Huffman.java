// name:        date: 
import java.util.*;
import java.io.*;
public class Huffman
{
   public static Scanner keyboard = new Scanner(System.in);
   public static void main(String[] args) throws IOException
   {
      //Prompt for two strings 
      System.out.print("Encoding using Huffman codes");
      System.out.print("\nWhat message? ");
      String message = keyboard.nextLine();
   
      System.out.print("\nEnter middle part of filename:  ");
      String middlePart = keyboard.next();
   
      huffmanize( message, middlePart );
   }
   public static void huffmanize(String message, String middlePart) throws IOException
   {
         //Make a frequency table of the letters
      	//Put each letter-frequency pair into a HuffmanTreeNode. Put each 
   		//        node into a priority queue (or a min-heap).     
      	//Use the priority queue of nodes to build the Huffman tree
      	//Process the string letter-by-letter and search the tree for the 
   		//       letter. It's recursive. As you recur, build the path through the tree, 
   		//       where going left is 0 and going right is 1.
         //System.out.println the binary message 
      	//Write the binary message to the hard drive using the file name ("message." + middlePart + ".txt")
         //System.out.println the scheme from the tree--needs a recursive helper method
      	//Write the scheme to the hard drive using the file name ("scheme." + middlePart + ".txt")
      HashMap<String, Integer> freqmap = new HashMap<>();
      for(String s : message.split(""))
      {
         if(freqmap.containsKey(s))
            freqmap.put(s, freqmap.get(s) + 1);
         else
            freqmap.put(s, 1);
      }
      PriorityQueue<HuffmanTreeNode> pq = new PriorityQueue<>();
      for(String s : freqmap.keySet())
         pq.add(new HuffmanTreeNode(s, freqmap.get(s)));
      while(pq.size() > 1)
      {
         HuffmanTreeNode one = pq.remove();
         HuffmanTreeNode two = pq.remove();
         pq.add(new HuffmanTreeNode("*", one.getFreq() + two.getFreq(), one, two));
      }
         
            
   }


   public String treeTravel(HuffmanTreeNode t, String goal)
   {
      return "blah";
   }

   public String schemer(HuffmanTreeNode t, String goal)
   {
      return "bleh";
   }

}
	/*
	  * This tree node stores two values.  Look at TreeNode's API for some help.
	  * The compareTo method must ensure that the lowest frequency has the highest priority.
	  */
class HuffmanTreeNode implements Comparable<HuffmanTreeNode>
{
   private String letter;
   private int freq;
   private HuffmanTreeNode left;
   private HuffmanTreeNode right;
 
   public HuffmanTreeNode(String first, int second)
   {
      letter = first;
      freq = second;
      left = null;
      right = null;
   }
   
   public HuffmanTreeNode(String first, int second, HuffmanTreeNode l, HuffmanTreeNode r)
   {
      letter = first;
      freq = second;
      left = l;
      right = r;
   }
   
   public String getLetter()
   {
      return letter;
   }
   
   public int getFreq()
   {
      return freq;
   }
   
   public void setLetter(String o)
   {
      letter = o;
   }
   
   public void setFreq(int o)
   {
      freq = o;
   }
   
   public HuffmanTreeNode getLeft()
   {
      return left;
   }
   
   public HuffmanTreeNode getRight()
   {
      return right;
   }
   
   public void setLeft(HuffmanTreeNode h)
   {
      left = h;
   }
   
   public void setRight(HuffmanTreeNode h)
   {
      right = h;
   }
   
   public int compareTo(HuffmanTreeNode arg)
   {
      return freq - arg.getFreq();
   }


}
