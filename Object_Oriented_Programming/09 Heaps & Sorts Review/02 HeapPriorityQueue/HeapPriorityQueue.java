 //Name:   
 //Date:
 
import java.util.*;

/* implement the API for java.util.PriorityQueue
 *     a min-heap of objects in an ArrayList<E> in a resource class
 * test this class with HeapPriorityQueue_Driver.java.
 * test this class with LunchRoom.java.
 * add(E) and remove()  must work in O(log n) time
 */
public class HeapPriorityQueue<E extends Comparable<E>> 
{
   private ArrayList<E> myHeap;
   
   public HeapPriorityQueue()
   {
      myHeap = new ArrayList<E>();
      myHeap.add(null);
   }
   
   public ArrayList<E> getHeap()   //for Codepost
   {
      return myHeap;
   }
   
   public int lastIndex()
   {
      return myHeap.size()-1;
   }
   
   public boolean isEmpty()
   {
      return myHeap.size() <= 1;
   }
   
   public boolean add(E obj)
   {
      myHeap.add(obj);
      heapUp(lastIndex());
      return true;
   }
   
   public E remove()
   {
      if(isEmpty())
         return myHeap.get(0);
      if(myHeap.size() == 2)
         return myHeap.remove(1);
      E returnE = myHeap.set(1, myHeap.get(lastIndex()));
      myHeap.remove(lastIndex());
      heapDown(1, lastIndex());
      return returnE;
   }
   
   public E peek()
   {
      if(!isEmpty())
         return myHeap.get(1);
      return myHeap.get(0);
   }
   
   //  it's a min-heap of objects in an ArrayList<E> in a resource class
   public void heapUp(int k)
   {
      if(k/2.0 < 1)
         return;
      if(myHeap.get(k/2).compareTo(myHeap.get(k)) > 0)
      {
         swap(k/2, k);
         heapUp(k/2);
      }
         
   }
   
   private void swap(int a, int b)
   {
      E temp = myHeap.get(a);
      myHeap.set(a, myHeap.get(b));
      myHeap.set(b, temp);
   }
   
  //  it's a min-heap of objects in an ArrayList<E> in a resource class
   public void heapDown(int k, int last)
   {
      if(k < last/2.0)
      {
         int otherIndex = k;
         if(!(2*k+1 >= last))
         {
            if(myHeap.get(2*k).compareTo(myHeap.get(otherIndex)) < 0)
               otherIndex = 2*k;
            if(myHeap.get(2*k+1).compareTo(myHeap.get(otherIndex)) < 0)
               otherIndex = 2*k+1;
         }
         else if(myHeap.get(2*k).compareTo(myHeap.get(otherIndex)) < 0)
            otherIndex = 2*k;
         
         swap(k, otherIndex);
         if(otherIndex != k)
            heapDown(otherIndex, last);
      }
   }
   
   public String toString()
   {
      return myHeap.toString();
   }  
   
   public boolean isHeap()
   {
      for(int i=1; i<myHeap.size()/2; i++)
         if(myHeap.get(i).compareTo(myHeap.get(2*i)) > 0 || myHeap.get(i).compareTo(myHeap.get(2*i+1)) > 0)
            return false;
      return true;
   }
}
