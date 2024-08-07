// Name:              Date:
import java.util.*;
import java.io.*;
public class deHuffman
{
   public static void main(String[] args) throws IOException
   {
      Scanner keyboard = new Scanner(System.in);
      System.out.print("\nWhat binary message (middle part)? ");
      String middlePart = keyboard.next();
      Scanner sc = new Scanner(new File("message."+middlePart+".txt")); 
      String binaryCode = sc.next();
      Scanner huffLines = new Scanner(new File("scheme."+middlePart+".txt")); 
      	
      TreeNode root = huffmanTree(huffLines);
      String message = dehuff(binaryCode, root);
      System.out.println(message);
      	
      sc.close();
      huffLines.close();
   }
   public static TreeNode huffmanTree(Scanner huffLines)
   {
      TreeNode tree = new TreeNode("");
      TreeNode pointer = tree;
      while(huffLines.hasNextLine())
      {
         String line = huffLines.nextLine();
         String letter = line.substring(0, 1);
         line = line.substring(1);
         for(String s : line.split(""))
         {
            if(s.equals("0"))
            {
               if(pointer.getLeft() == null)
                  pointer.setLeft(new TreeNode(""));
               pointer = pointer.getLeft();
                  
            }
            if(s.equals("1"))
            {
               if(pointer.getRight() == null)
                  pointer.setRight(new TreeNode(""));
               pointer = pointer.getRight();
            }
         }
         pointer.setValue(letter);
         pointer = tree;
      }
      return tree;
   }
   public static String dehuff(String text, TreeNode root)
   {
      String toret = "";
      TreeNode pointer = root;
      for(String s : text.split(""))
      {
         if(s.equals("0"))
            pointer = pointer.getLeft();
         if(s.equals("1"))
            pointer = pointer.getRight();
         if(!pointer.getValue().equals(""))
         {
            toret += pointer.getValue();
            pointer = root;
         }
         
      }
      return toret;
   }
}

 /* TreeNode class for the AP Exams */
class TreeNode
{
   private Object value; 
   private TreeNode left, right;
   
   public TreeNode(Object initValue)
   { 
      value = initValue; 
      left = null; 
      right = null; 
   }
   
   public TreeNode(Object initValue, TreeNode initLeft, TreeNode initRight)
   { 
      value = initValue; 
      left = initLeft; 
      right = initRight; 
   }
   
   public Object getValue()
   { 
      return value; 
   }
   
   public TreeNode getLeft() 
   { 
      return left; 
   }
   
   public TreeNode getRight() 
   { 
      return right; 
   }
   
   public void setValue(Object theNewValue) 
   { 
      value = theNewValue; 
   }
   
   public void setLeft(TreeNode theNewLeft) 
   { 
      left = theNewLeft;
   }
   
   public void setRight(TreeNode theNewRight)
   { 
      right = theNewRight;
   }
}
