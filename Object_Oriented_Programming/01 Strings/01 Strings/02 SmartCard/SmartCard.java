//name:    date:

import java.text.DecimalFormat;
public class SmartCard 
{
   public final static DecimalFormat df = new DecimalFormat("$0.00");
   public final static double MIN_FARE = 0.5;
   /* enter the private fields */
   private double balance;
   private Station station;
   private boolean onboard;
   
   /* the one-arg constructor  */
   public SmartCard(double initBalance)
   {
      balance = initBalance;
      station = null;
      onboard = false;
   }

   //these three getter methods only return your private data
   //they do not make any changes to your data
   public boolean getIsBoarded() 
   { 
      return onboard;
   }
   
   public double getBalance()
   {
      return balance;
   }
         
   public String getFormattedBalance()
   {
      return df.format(balance);
   }
   
   public Station getBoardedAt()
   {
      return station;
   }
    
   /* write the instance methods  */
   public void board(Station s)
   {
      if (onboard)
         System.out.println("Error: already boarded?!");
      else if (balance < MIN_FARE)
         System.out.println("Insufficient funds to board. Please add more money.");
      else
      {
         station = s;
         onboard = true;
      }
   }
   
   public double cost(Station s)
   {
      return ( 0.50 + Math.abs( station.getZone() - s.getZone() ) * 0.75 );
   }
    
   public void exit(Station s)
   {
      if (!onboard)
         System.out.println("Error: Did not board?!");
      else if (cost(s) > balance)
         System.out.println("Insufficient funds to exit. Please add more money.");
      else
      {
         double c = cost(s);
         balance -= c;
         onboard = false;
         System.out.println("From " + station.getName() + " to " + s.getName() + " costs " + df.format(c) + ". SmartCard has " + getFormattedBalance() );
         station = null;
      }
   
   }
   
   public void addMoney (double d)
   {
      balance += d;
   }

}
   
// ***********  start a new class.  The new class does NOT have public or private.  ***/
class Station
{
      
   private int zone;
   private String name;

   public Station()
   {
      zone = 1;
      name = "Downtown";
   }

   public Station(String n, int z)
   {
      name = n;
      zone = z;
   }

   public String getName()
   {
      return name;
   }

   public int getZone()
   {
      return zone;
   }
}

