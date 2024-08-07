// Name:
// Date: 
import java.util.*;

interface BSTinterface<E>
{
   public int size();
   public boolean contains(E element);
   public E add(E element);
   public E addBalanced(E element);
   public E remove(E element);
   public E min();
   public E max();
   public String display();
   public String toString();
   public List<E> toList();  //returns an in-order list of E
}

/*******************
  Copy your BST code.  Implement generics.
**********************/
public class BST_Generic<E extends Comparable<E>> implements BSTinterface<E>
{
   private TreeNode<E> root;
   private int size;
   public BST_Generic()
   {
      root = null;
      size = 0;
   }
   public int size()
   {
      return size;
   }
   public TreeNode<E> getRoot()   //for Grade-It
   {
      return root;
   }
   /***************************************
   @param s -- one string to be inserted
   ****************************************/
   public E add(E s) 
   {
      root = add(root, s);
      size++;
      return s;
   }
   private TreeNode<E> add(TreeNode<E> t, E s) //recursive helper method
   {      
      if(t==null)
      {
         t = new TreeNode<E>(s);
         return t;
      }
      else if(s.compareTo(t.getValue()) <= 0)
         t.setLeft(add(t.getLeft(), s));
      else if(s.compareTo(t.getValue()) > 0)
         t.setRight(add(t.getRight(), s));
      return t;
   }
   
   public String display()
   {
      return display(root, 0);
   }
   private String display(TreeNode<E> t, int level) //recursive helper method
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
   
   public boolean contains( E obj)
   {
      return contains(root, obj);
   }
   private boolean contains(TreeNode<E> t, E x) //recursive helper method
   {
      if(t==null)
         return false;
      else if(x.compareTo(t.getValue()) == 0)
         return true;
      else if(x.compareTo(t.getValue()) < 0)
         return contains(t.getLeft(), x);
      else if(x.compareTo(t.getValue()) > 0)
         return contains(t.getRight(), x);
      return false;
   }
   
   public E min()
   {
      return min(root);
   }
   private E min(TreeNode<E> t)  //use iteration
   {
      if(t==null)
         return null;
      while(t.getLeft() != null)
         t = t.getLeft();
      return t.getValue();
   }
   
   public E max()
   {
      return max(root);
   }
   private E max(TreeNode<E> t)  //recursive helper method
   {
      if(t==null)
         return null;
      else if(t.getRight()==null)
         return t.getValue();
      return max(t.getRight());
   }
   
   public String toString()
   {
      return toString(root);
   }
   private String toString(TreeNode<E> t)  //an in-order traversal.  Use recursion.
   {
      String toReturn = "";
      if(t == null)
         return "";
      toReturn += toString(t.getLeft());   
      toReturn += t.getValue() + " ";   
      toReturn += toString(t.getRight());  
      return toReturn;
   }   

   public List<E> toList()
   {
      List<E> list = new ArrayList<>();
      toList(root, list);
      return list;
   }
   
   public void toList(TreeNode<E> t, List<E> list)
   {
      if(t==null)
         return;
      toList(t.getLeft(), list);
      list.add(t.getValue());
      toList(t.getRight(), list);
   }




   /*  precondition:  target must be in the tree.
                      implies that tree cannot be null.
   */
   public E remove(E target)
   {
      root = remove(root, target);
      size--;
      return target;
   }
   private TreeNode remove(TreeNode<E> current, E target)
   {
      TreeNode<E> store = current;
      if(current==null)
         return null;
      if(target.compareTo(current.getValue()) == 0)
      {
         if(current.getLeft() == null && current.getRight() == null)
            return null;
         else if(current.getRight() == null)
            return current.getLeft();
         else if(current.getLeft() == null)
            return current.getRight();
         else
         {
            E max = max(current.getLeft());
            current = remove(current, max);
            current.setValue(max);
            return current;
         }
      }
      TreeNode<E> parent = current;
      while(target.compareTo(current.getValue()) != 0)
      {
         if(target.compareTo(current.getValue()) < 0)
         {
            parent = current;
            current = current.getLeft();
         }
         else if(target.compareTo(current.getValue()) > 0)
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
      
      E max = max(current.getLeft());
      current.setLeft(remove(current.getLeft(), max));
      current.setValue(max);
      return store;
   }


   /*  start the addBalanced methods */
   private int calcBalance(TreeNode<E> t) //height to right minus 
   {                                    //height to left
      if(t == null)
         return 0;
      return height(t.getRight()) - height(t.getLeft());
   }

   private int height(TreeNode<E> t)   //from TreeLab
   {
      if(t == null)
         return -1;
      int heightL = 0;
      int heightR = 0;
      heightL += height(t.getLeft());
      heightR += height(t.getRight());
      return 1 + Math.max(heightL, heightR);
   }

   public E addBalanced(E value)  
   {
      E added = add(value);
      root = balanceTree(root);   // for an AVL tree. Put in the arguments you want.
      return added;
   }
   
   public E removeBalanced(E value)
   {
      E removed  = remove(value);
      root = balanceTree(root);
      return removed;
   }
   
   private TreeNode<E> balanceTree(TreeNode<E> t)  //recursive.  Whatever makes sense.
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
      return t;
   }
   // 4 rotation methods
   private TreeNode<E> LL(TreeNode<E> t)
   {
      TreeNode<E> left = t.getLeft();
      TreeNode<E> leftright = left.getRight();
      left.setRight(t);
      t.setLeft(leftright);
      return left;
   }
   
   private TreeNode<E> RR(TreeNode<E> t)
   {
      TreeNode<E> right = t.getRight();
      TreeNode<E> rightleft = right.getLeft();
      right.setLeft(t);
      t.setRight(rightleft);
      return right;
   }
   
   private TreeNode<E> LR(TreeNode<E> t)
   {
      t.setLeft(RR(t.getLeft()));
      t = LL(t);
      return t;
   }
   
   private TreeNode<E> RL(TreeNode<E> t)
   {
      t.setRight(LL(t.getRight()));
      t = RR(t);
      return t;
   }
   

}

/*******************
  Copy your TreeNode code.  Implement generics.
**********************/
class TreeNode<E>
{
   private E value; 
   private TreeNode<E> left, right;
   
   public TreeNode(E initValue)
   { 
      value = initValue; 
      left = null; 
      right = null; 
   }
   
   public TreeNode(E initValue, TreeNode<E> initLeft, TreeNode<E> initRight)
   { 
      value = initValue; 
      left = initLeft; 
      right = initRight; 
   }
   
   public E getValue()
   { 
      return value; 
   }
   
   public TreeNode<E> getLeft() 
   { 
      return left; 
   }
   
   public TreeNode<E> getRight() 
   { 
      return right; 
   }
   
   public void setValue(E theNewValue) 
   { 
      value = theNewValue; 
   }
   
   public void setLeft(TreeNode<E> theNewLeft) 
   { 
      left = theNewLeft;
   }
   
   public void setRight(TreeNode<E> theNewRight)
   { 
      right = theNewRight;
   }
}