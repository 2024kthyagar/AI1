//Name: 
//Date:

interface BSTinterface
{
   public int size();
   public boolean contains(String obj);
   public void add(String obj);
   //public void addBalanced(String obj);
   //public boolean remove(String obj);
   public String min();
   public String max();
   public String toString();
}

/*******************
Represents a binary search tree holding Strings. 
Implements (most of) BSTinterface, above. 
The recursive methods all have a public method calling a private helper method. 
Copy the display() method from TreeLab. 
**********************/
class BST implements BSTinterface
{
   private TreeNode root;
   private int size;
   public BST()
   {
      root = null;
      size = 0;
   }
   public int size()
   {
      return size;
   }
   public TreeNode getRoot()   //for Grade-It
   {
      return root;
   }
   /***************************************
   @param s -- one string to be inserted
   ****************************************/
   public void add(String s) 
   {
      root = add(root, s);
      size++;
   }
   private TreeNode add(TreeNode t, String s) //recursive helper method
   {      
      if(t==null)
      {
         t = new TreeNode(s);
         return t;
      }
      else if(s.compareTo(t.getValue()+"") <= 0)
         t.setLeft(add(t.getLeft(), s));
      else if(s.compareTo(t.getValue()+"") > 0)
         t.setRight(add(t.getRight(), s));
      return t;
   }
   
   public String display()
   {
      return display(root, 0);
   }
   private String display(TreeNode t, int level) //recursive helper method
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
   
   public boolean contains( String obj)
   {
      return contains(root, obj);
   }
   private boolean contains(TreeNode t, String x) //recursive helper method
   {
      if(t==null)
         return false;
      else if(x.compareTo(t.getValue() + "") == 0)
         return true;
      else if(x.compareTo(t.getValue() + "") < 0)
         return contains(t.getLeft(), x);
      else if(x.compareTo(t.getValue() + "") > 0)
         return contains(t.getRight(), x);
      return false;
   }
   
   public String min()
   {
      return min(root);
   }
   private String min(TreeNode t)  //use iteration
   {
      if(t==null)
         return null;
      while(t.getLeft() != null)
         t = t.getLeft();
      return t.getValue() + "";
   }
   
   public String max()
   {
      return max(root);
   }
   private String max(TreeNode t)  //recursive helper method
   {
      if(t==null)
         return null;
      else if(t.getRight()==null)
         return t.getValue()+"";
      return max(t.getRight());
   }
   
   public String toString()
   {
      return toString(root);
   }
   private String toString(TreeNode t)  //an in-order traversal.  Use recursion.
   {
      String toReturn = "";
      if(t == null)
         return "";
      toReturn += toString(t.getLeft());   
      toReturn += t.getValue() + " ";   
      toReturn += toString(t.getRight());  
      return toReturn;
   }
}
