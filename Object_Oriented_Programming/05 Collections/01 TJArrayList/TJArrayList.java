// Name: 
// Date:

/**
 * Implements the cheat sheet's List interface.  Implements generics.
 * The backing array is an array of (E[]) new Object[10];
 * @override toString()
 */ 
public class TJArrayList<E>
{
   private int size;							//stores the number of objects
   private E[] myArray;
   public TJArrayList()                
   {
      myArray = (E[]) new Object[10]; //default constructor instantiates a raw array with 10 cells
   
      size = 0;
   }
   public int size()
   {
      return size;
   }
 	/* appends obj to end of list; increases size;
      must be an O(1) operation when size < array.length, 
         and O(n) when it doubles the length of the array.
	  @return true  */
   public boolean add(E obj)
   {
      if(size >= myArray.length-1)
      {
         E[] temp = (E[]) new Object[myArray.length * 2];
         for(int i=0; i<size; i++)
            temp[i] = myArray[i];
         myArray = temp;
         
      }
      myArray[size] = obj;
      size++;
      return true;
   }
   /* inserts obj at position index.  increments size. 
		*/
   public void add(int index, E obj) throws IndexOutOfBoundsException  //this the way the real ArrayList is coded
   {
      if(index > size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      for(int i=size; i > index; i--)
         myArray[i] = myArray[i-1];
      myArray[index] = obj;
      size++;
   }

   /* return obj at position index.  
		*/
   public E get(int index) throws IndexOutOfBoundsException
   {
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      return myArray[index];
   
   }
   /**
    * Replaces obj at position index. 
    * @return the object is being replaced.
    */  
   public E set(int index, E obj) throws IndexOutOfBoundsException  
   { 
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      E temp = myArray[index];
      myArray[index] = obj;
      return temp;
   }
 /*  removes the node from position index. shifts elements 
     to the left.   Decrements size.
	  @return the object that used to be at position index.
	 */
   public E remove(int index) throws IndexOutOfBoundsException  
   {
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      E temp = myArray[index];
      for(int i=index; i<size; i++)
         myArray[i] = myArray[i+1];
      size--;
      return temp;
   }
	   /*
		   This method compares objects.
         Must use .equals(), not ==
     	*/
   public boolean contains(E obj)
   {
      for(E iter : myArray)
      {
         if(obj.equals(iter))
            return true;
      }
      return false;
   }
	 /*returns a String of E objects in the array with 
       square brackets and commas.
     	*/
   public String toString()
   {
      String endString = "[";
      for(int i=0; i<size-1; i++)
         endString += myArray[i] + ", ";
      return endString + myArray[size-1] + "]";
   }
}