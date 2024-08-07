// Name:
// Date:

public class HeapSort
{
   public static int N;  //9 or 100
	
   public static void main(String[] args)
   {
      /* Part 1: Given a heap, sort it. Do this part first. */
      // N = 4;  
      // double heap[] = {-1,7.2, 3.4, 6.4, 9.9};  // size of array = N+1
   //    
      // display(heap);
      // makeHeap(heap, N);
      // display(heap);
      // sort(heap);
      // display(heap);
      // System.out.println(isSorted(heap));
      
      /* Part 2:  Generate 100 random numbers, make a heap, sort it.  */
      N = 100;
      double[] heap = new double[N + 1];  // size of array = N+1
      heap = createRandom(heap);
      display(heap);
      makeHeap(heap, N);
      display(heap); 
      sort(heap);
      display(heap);
      System.out.println(isSorted(heap));
   }
   
	//******* Part 1 ******************************************
   public static void display(double[] array)
   {
      for(int k = 1; k < array.length; k++)
         System.out.print(array[k] + "    ");
      System.out.println("\n");	
   }
   
   public static void sort(double[] array)
   {
      /* enter your code here */
      for(int i=N; i>0; i--)
      {
         swap(array, 1, i);
         heapDown(array, 1, i);
      }
      
   
      if(array[1] > array[2])   //just an extra swap, if needed.
         swap(array, 1, 2);
   }
  
   public static void swap(double[] array, int a, int b)
   {
      double temp = array[a];
      array[a] = array[b];
      array[b] = temp;
   }
   
   public static void heapDown(double[] array, int k, int last)
   {
      if(k < last/2.0)
      {
         int otherIndex = k;
         if(!(2*k+1 >= last))
         {
            if(array[2*k] >= array[otherIndex])
               otherIndex = 2*k;
            if(array[2*k+1] > array[otherIndex])
               otherIndex = 2*k+1;
         }
         else if(array[2*k] >= array[otherIndex])
            otherIndex = 2*k;
         
         swap(array, k, otherIndex);
         if(otherIndex != k)
            heapDown(array, otherIndex, last);
      }
   }
   
   public static boolean isSorted(double[] array)
   {
      for(int i=0; i<array.length-1; i++)
         if(array[i] > array[i+1])
            return false;
      return true;
   }
   
   //****** Part 2 *******************************************

   //Generate 100 random numbers (between 1 and 100, formatted to 2 decimal places) 
   public static double[] createRandom(double[] array)
   {  
      array[0] = -1;   //because it will become a heap
      for(int i=1; i<=N; i++)
         array[i] = Math.round(Math.random()*100*100)/100.0;
       
      return array;
   }
   
   //turn the random array into a heap
   public static void makeHeap(double[] array, int lastIndex)
   {
      for(int i=N/2; i>0; i--)
         heapDown(array, i, lastIndex+1);
   }
}

