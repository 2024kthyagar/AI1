//Updated on 12.14.2020 v2

//Name:   Date:
import java.util.*;
import java.io.*;
public class McRonald3
{
   public static final int TIME = 1080;     //18 hrs * 60 min
   public static double CHANCE_OF_CUSTOMER = .2;
   public static int customers = 0;
   public static int totalMinutes = 0;
   public static int longestWaitTime = 0;
   public static int longestQueue = 0;
   public static int serviceWindow = 0;      // to serve the front of the queue
   //public static final int numberOfServiceWindows = 3;  //for McRonald 3
   public static int thisCustomersTime;
   public static PrintWriter outfile = null; // file to display the queue information
      
   public static int timeToOrderAndBeServed()
   {
      return (int)(Math.random() * 6 + 2);
   }
  
   public static void displayTimeAndQueue(Queue<Customer> q, int min)
   { 
      //Billington's
      outfile.println(min + ": " + q);	
      //Jurj's
      //outfile.println("Customer#" + intServiceAreas[i] + 
      //                            " leaves and his total wait time is " + (intMinute - intServiceAreas[i]));                     	
      
   }
   
   public static int getCustomers()
   {
      return customers;
   }
   public static double calculateAverage()
   {
      return (int)(1.0 * totalMinutes/customers * 10)/10.0;
   }
   public static int getLongestWaitTime()
   {
      return longestWaitTime;
   }
   public static int getLongestQueue()
   {
      return longestQueue;
   }
            
   public static void main(String[] args)
   {     
    //set up file      
      try
      {
         outfile = new PrintWriter(new FileWriter("McRonald 1 Queue 3 ServiceArea.txt"));
      }
      catch(IOException e)
      {
         System.out.println("File not created");
         System.exit(0);
      }
      
      mcRonald(TIME, outfile);   //run the simulation
      
      outfile.close();	
   }
   
   public static void mcRonald(int TIME, PrintWriter of)
   {
      /***************************************
           Write your code for the simulation   
      **********************************/
      Queue<Customer> hungry = new LinkedList<>();
   
      for(int min = 1; min < TIME; min++)
      {
         if(Math.random() <= CHANCE_OF_CUSTOMER)
         { 
            int servetime = (int) timeToOrderAndBeServed();
            totalMinutes += servetime;
            hungry.add(new Customer(min, servetime));
            customers++;
         }
         if(!hungry.isEmpty()) 
         {
            Customer current = hungry.peek();
            current.setOrder(current.getOrder()-1);
            if(current.getOrder() <= 0)
               hungry.remove();
         }
         int currentwait = 0;
         for(Customer c : hungry)
            currentwait += c.getOrder();
         if(currentwait > longestWaitTime)
            longestWaitTime = currentwait;
         if(hungry.size() > longestQueue)
            longestQueue = hungry.size();
         outfile.println(min + ": " + hungry);
         if(!hungry.isEmpty())
            outfile.println("\t" + hungry.peek() + " is now being served for " + hungry.peek().getOrder() + " minutes.");
      }
        
        
        
              
      /*   report the data to the screen    */  
      System.out.println("1 queue, 1 service window, probability of arrival = "+ CHANCE_OF_CUSTOMER);
      System.out.println("Total customers served = " + getCustomers());
      System.out.println("Average wait time = " + calculateAverage());
      System.out.println("Longest wait time = " + longestWaitTime);
      System.out.println("Longest queue = " + longestQueue);
   }
   
   static class Customer      
   {
      private int arrivedAt;
      private int orderAndBeServed;
      
    /**********************************
       Complete the Customer class with  
       constructor, accessor methods, toString.
    ***********************************/
      public Customer(int a, int o)
      {
         arrivedAt = a;
         orderAndBeServed = o;
      }
    
      public int getArrive()
      {
         return arrivedAt;
      }
      public int getOrder()
      {
         return orderAndBeServed;
      }
    
      public void setArrive(int a)
      {
         arrivedAt = a;
      }
      public void setOrder(int o)
      {
         orderAndBeServed = o;
      }
      public String toString()
      {
         return arrivedAt + "";
      }
   
    
    
   }
}