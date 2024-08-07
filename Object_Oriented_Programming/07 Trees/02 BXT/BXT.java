// Name: 
// Date:  
/*  Represents a binary expression tree.
 *  The BXT builds itself from postorder expressions. It can
 *  evaluate and print itself.  Also prints inorder and postorder strings. 
 */
 
import java.util.*;

public class BXT
{
   public static final String operators = "+ - * / % ^ !";
   private TreeNode root;   
   
   public BXT()
   {
      root = null;
   }
   public TreeNode getRoot()   //for Codepost
   {
      return root;
   }
    
   public void buildTree(String str)
   {
      Stack<TreeNode> exp = new Stack<>();
      String[] split = str.split(" ");
      for(String s : split)
      {
         if(!isOperator(s))
            exp.push(new TreeNode(s));
         else
         {
            TreeNode oper = new TreeNode(s);
            if(s.equals("!"))
               oper.setLeft(exp.pop());
            else {
               oper.setRight(exp.pop());
               oper.setLeft(exp.pop());
            }
            exp.push(oper);
         }
      }
      root = exp.pop();
         
   }
   
   public double evaluateTree()
   {
      return evaluateNode(root);
   }
   
   private double evaluateNode(TreeNode t)  //recursive
   {
      if(t.getLeft()==null && t.getRight()==null)
         return Double.parseDouble(t.getValue() + "");
      double left = 0;
      double right = 0;
      if(t.getLeft()!=null && isOperator(t.getLeft().getValue() + ""))
         left = evaluateNode(t.getLeft());
      else if(t.getLeft()!=null)
         left = Double.parseDouble(t.getLeft().getValue() + "");
      if(t.getRight()!=null && isOperator(t.getRight().getValue() + ""))
         right = evaluateNode(t.getRight());
      else if(t.getRight()!=null)
         right = Double.parseDouble(t.getRight().getValue() + "");
         
      return computeTerm(t.getValue() + "", left, right);
      
   }
   
   private double computeTerm(String s, double a, double b)
   {
      if(s.equals("+"))
         return a + b;
      else if(s.equals("-"))
         return a-b;
      else if(s.equals("*"))
         return a*b;
      else if(s.equals("/"))
         return a/b;
      else if(s.equals("%"))
         return a%b;
      else if(s.equals("^"))
         return Math.pow(a,b);
      else if(s.equals("!"))
         return fact((int) b);
      return -1;
   }
   
   private int fact(int a)
   {
      int val = 1;
      for(int i=1; i<=a; i++)
         val *= i;
      return val;
   }
   
   private boolean isOperator(String s)
   {
      return operators.contains(s);
   }
   
   public String display()
   {
      return display(root, 0);
   }
   
   private String display(TreeNode t, int level)
   {
      String toRet = "";
      if(t == null)
         return "";
      toRet += display(t.getRight(), level + 1); //recurse right
      for(int k = 0; k < level; k++)
         toRet += "\t";
      toRet += t.getValue() + "\n";
      toRet += display(t.getLeft(), level + 1); //recurse left
      return toRet;
   }
    
   public String inorderTraverse()
   {
      return inorderTraverse(root);
   }
   
   private  String inorderTraverse(TreeNode t)
   {
      String toReturn = "";
      if(t == null)
         return "";
      toReturn += inorderTraverse(t.getLeft());   
      toReturn += t.getValue() + " ";   
      toReturn += inorderTraverse(t.getRight());  
      return toReturn;
   }
   
   public String preorderTraverse()
   {
      return preorderTraverse(root);
   }
   
   private String preorderTraverse(TreeNode root)
   {
      String toReturn = "";
      if(root == null)
         return "";
      toReturn += root.getValue() + " ";              //process root
      toReturn += preorderTraverse(root.getLeft());   //recurse left
      toReturn += preorderTraverse(root.getRight());  //recurse right
      return toReturn;
   }
   
  /* extension */
   public String inorderTraverseWithParentheses()
   {
      return inorderTraverseWithParentheses(root);
   }
   
   private String inorderTraverseWithParentheses(TreeNode t)
   {
      String toReturn = "";
      if(t == null)
         return "";
      // check if each side is an operator, its child is an operator, and if it's greater than the child
      boolean leftmatch = isOperator(t.getValue()+"") && isOperator(t.getLeft().getValue()+"") && getLevel(t.getLeft().getValue()+"") < getLevel(t.getValue()+"");
      boolean rightmatch = isOperator(t.getValue()+"") && isOperator(t.getRight().getValue()+"") && getLevel(t.getRight().getValue()+"") < getLevel(t.getValue()+"");
      // add parens
      if(leftmatch)
         toReturn += "( ";
      toReturn += inorderTraverseWithParentheses(t.getLeft()); 
      if(leftmatch)
         toReturn += ") "; 
      toReturn += t.getValue() + " ";  
      if(rightmatch)
         toReturn += "( "; 
      toReturn += inorderTraverseWithParentheses(t.getRight()); 
      if(rightmatch)
         toReturn += ") ";  
      return toReturn;
   }
   
   private int getLevel(String s)
   {
      if(s==null)
         return -1;
      else if(s.equals("+") || s.equals("-"))
         return 0;
      else if(s.equals("*") || s.equals("/") || s.equals("%"))
         return 1;
      else if(s.equals("^"))
         return 2;
      else if(s.equals("!"))
         return 3;
      else 
         return -1;
   }
}