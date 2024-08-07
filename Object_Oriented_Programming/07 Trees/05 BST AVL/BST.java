// Name: 
// Date: 

interface BSTinterface
{
   public int size();
   public boolean contains(String obj);
   public void add(String obj);   //does not balance
   public void addBalanced(String obj);
   public void remove(String obj);
   public String min();
   public String max();
   public String display();
   public String toString();
}

public class BST implements BSTinterface
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





   /*  precondition:  target must be in the tree.
                      implies that tree cannot be null.
   */
   public void remove(String target)
   {
      root = remove(root, target);
      size--;
   }
   private TreeNode remove(TreeNode current, String target)
   {
      TreeNode store = current;
      if(current==null)
         return null;
      if(target.compareTo(current.getValue()+"") == 0)
      {
         if(current.getLeft() == null && current.getRight() == null)
            return null;
         else if(current.getRight() == null)
            return current.getLeft();
         else if(current.getLeft() == null)
            return current.getRight();
         else
         {
            String max = max(current.getLeft());
            current = remove(current, max);
            current.setValue(max);
            return current;
         }
      }
      TreeNode parent = current;
      while(target.compareTo(current.getValue()+"") != 0)
      {
         if(target.compareTo(current.getValue()+"") < 0)
         {
            parent = current;
            current = current.getLeft();
         }
         else if(target.compareTo(current.getValue()+"") > 0)
         {
            parent = current;
            current = current.getRight();
         }
      }
      boolean left = parent.getLeft() == current;
      boolean right = parent.getRight() == current;
      // replacing leaves
      if(current.getLeft()==null && current.getRight()==null)
      { 
         if(left)
            parent.setLeft(null);
         else if(right)
            parent.setRight(null);
         return store;
      }
      // one child
      if(current.getRight()==null)
      {
         if(left)
            parent.setLeft(current.getLeft());
         else if(right)
            parent.setRight(current.getLeft());
         return store;
      }
      if(current.getLeft()==null)
      {
         if(left)
            parent.setLeft(current.getRight());
         else if(right)
            parent.setRight(current.getRight());
         return store;
      }
      // two children
      
      String max = max(current.getLeft());
      current.setLeft(remove(current.getLeft(), max));
      current.setValue(max);
      return store;
   }


   /*  start the addBalanced methods */
   private int calcBalance(TreeNode t) //height to right minus 
   {                                    //height to left
      if(t == null)
         return 0;
      return height(t.getRight()) - height(t.getLeft());
   }

   private int height(TreeNode t)   //from TreeLab
   {
      if(t == null)
         return -1;
      int heightL = 0;
      int heightR = 0;
      heightL += height(t.getLeft());
      heightR += height(t.getRight());
      return 1 + Math.max(heightL, heightR);
   }

   public void addBalanced(String value)  
   {
      add(value);
      root = balanceTree(root);   // for an AVL tree. Put in the arguments you want.
   }
   
   public void removeBalanced(String value)
   {
      remove(value);
      root = balanceTree(root);
   }
   
   private TreeNode balanceTree(TreeNode t)  //recursive.  Whatever makes sense.
   {
      //TreeNode store = t;
      if(t == null)
         return null;
      t.setLeft(balanceTree(t.getLeft()));
      t.setRight(balanceTree(t.getRight()));
      int balance = calcBalance(t);
      if(Math.abs(balance) <= 1)
         return t;
      if(balance < 0)
      {
         int leftbal = calcBalance(t.getLeft());
         if(leftbal < 0)
            t = LL(t);
         else if(leftbal > 0)
            t = LR(t);
      }
      else if(balance > 0)
      {
         int rightbal = calcBalance(t.getRight());
         if(rightbal < 0)
            t = RL(t);
         else if(rightbal > 0)
            t = RR(t);
      }
   /*
      if(t.getRight() == root || t.getLeft() == root)
         root = t;
   
      */
      
      return t;
   }
   // 4 rotation methods
   private TreeNode LL(TreeNode t)
   {
      TreeNode left = t.getLeft();
      TreeNode leftright = left.getRight();
      left.setRight(t);
      t.setLeft(leftright);
      return left;
   }
   
   private TreeNode RR(TreeNode t)
   {
      TreeNode right = t.getRight();
      TreeNode rightleft = right.getLeft();
      right.setLeft(t);
      t.setRight(rightleft);
      return right;
   }
   
   private TreeNode LR(TreeNode t)
   {
      t.setLeft(RR(t.getLeft()));
      t = LL(t);
      return t;
   }
   
   private TreeNode RL(TreeNode t)
   {
      t.setRight(LL(t.getRight()));
      t = RR(t);
      return t;
   }
   
}