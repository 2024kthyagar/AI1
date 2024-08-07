 // Name:    
 // Date: 

import java.util.*;

public class Polynomial_Driver
{
   public static void main(String[] args)
   {
      Polynomial poly = new Polynomial();    
      poly.makeTerm(3, 2);        // 2x^3
      poly.makeTerm(1, -4);       //  -4x
      poly.makeTerm(0, 2);        //    2
      System.out.println("Map:  " + poly.getMap());
      System.out.println("poly:  " + poly.toString());  // 2x^3 + -4x + 2
      double evaluateAt = 2.0;
      System.out.println("Evaluated at "+ evaluateAt +": " +poly.evaluateAt(evaluateAt));
      
      System.out.println("-----------");
      Polynomial poly2 = new Polynomial();  
      poly2.makeTerm(4, 2);      // 2x^4 
      poly2.makeTerm(1, 4);      //   4x
      poly2.makeTerm(0, -3);     //   -3
      System.out.println("Map:  " + poly2.getMap()); 
      System.out.println("poly2:  " +poly2.toString());  // 2x^4 + 4x + -3 
      evaluateAt = -10.5;
      System.out.println("Evaluated at "+ evaluateAt +": " +poly2.evaluateAt(evaluateAt));
      System.out.println("-----------");
      System.out.println("Sum: " + poly.add(poly2));
      System.out.println("Product:  " + poly.multiply(poly2));
      
      System.out.println("-----------");
      Polynomial poly3 = new Polynomial();   
      poly3.makeTerm(1, 1);      // x
      poly3.makeTerm(0, 1);      // 1
      System.out.println("poly3:  " + poly3.toString()); // x + 1
         
      Polynomial poly4 = new Polynomial();    
      poly4.makeTerm(1, 1);     //  x
      poly4.makeTerm(0, -1);    // -1
      System.out.println("poly4:  " + poly4.toString()); //  x + -1
      System.out.println("Sum:  " + poly4.add(poly3));   //  2x
      System.out.println("Product:  " + poly4.multiply(poly3));   // x^2 + -1 
      System.out.println("Product:  " + poly3.multiply(poly4));   // x^2 + -1
      
      System.out.println("-----------");
      Polynomial poly5 = new Polynomial();    
      poly5.makeTerm(1, -1);     // -x
      poly5.makeTerm(0, 1);      //  1
      System.out.println("poly5:  " + poly5.toString());  // -x + 1
      System.out.println("poly4:  " + poly4.toString());  //  x + -1
      System.out.println("Sum:  " + poly4.add(poly5));    //  0
      System.out.println("Product:  " + poly4.multiply(poly5));  // -x^2 + 2x + -1
   
      /*  extension:  constructor with a string argument  */
      // System.out.println("==========================="); 
      // Polynomial poly6 = new Polynomial("2x^3 + 4x^2 + 6x^1 + -3");
      // System.out.println("Map:  " + poly6.getMap());  
      // System.out.println(poly6);
   
   }
}
interface PolynomialInterface
{
   public void makeTerm(Integer exp, Integer coef);
   public Map<Integer, Integer> getMap();
   public double evaluateAt(double x);
   
   //precondition: both polynomials are in standard form
   //postcondition: terms with zero disappear. If all terms disappear (the size is zero), 
   //               add pair (0,0).
   public Polynomial add(Polynomial other);
   
   //precondition: both polynomials are in standard form
   //postcondition: terms with zero disappear. If all terms disappear (the size is zero), 
   //               add pair (0,0)
   public Polynomial multiply(Polynomial other);
   public String toString();
}

class Polynomial implements PolynomialInterface
{
   Map<Integer, Integer> poly;

   public Polynomial()
   {
      poly = new TreeMap<>();
   }
   
   public Polynomial(Map<Integer, Integer> m)
   {
      poly = m;
   }
   
   public void makeTerm(Integer exp, Integer coef)
   {
      poly.put(exp, coef);
   }
   
   public Map<Integer, Integer> getMap()
   {
      return poly;
   }
   
   public double evaluateAt(double x)
   {
      double end = 0.0;
      for(Integer i : poly.keySet())
         end += Math.pow(x, i) * poly.get(i);
      return end;
   }
   
   public Polynomial add(Polynomial other)
   {
      Map<Integer, Integer> output = new TreeMap<>();
      Map<Integer, Integer> othermap = other.getMap();
      for(Integer i : poly.keySet())
      {
         if(othermap.containsKey(i))
         {
            int sum = poly.get(i) + othermap.get(i);
            if(sum != 0)
               output.put(i, sum);
         }
         else
            output.put(i, poly.get(i));
      }
      for(Integer i : othermap.keySet())
      {
         if(poly.containsKey(i))
         {
            int sum = poly.get(i) + othermap.get(i);
            if(sum != 0)
               output.put(i, sum);
         }
         else
            output.put(i, othermap.get(i));
         
      }
      
      return new Polynomial(output);
   }
   
   public Polynomial multiply(Polynomial other)
   {
      Map<Integer, Integer> output = new TreeMap<>();
      Map<Integer, Integer> othermap = other.getMap();
      for(Integer i : poly.keySet())
      {
         for(Integer j : othermap.keySet())
         {
            int deg = i+j;
            int product = poly.get(i) * othermap.get(j);
            if(output.containsKey(deg))
            {
               int oldcoef = output.get(deg);
               output.put(deg, product + oldcoef);
               if(product + oldcoef == 0)
                  output.remove(deg);
            }
            else
               output.put(deg, product);
         
         }
      }
      return new Polynomial(output);
   }
   
   public String toString()
   {
      if(poly.size() == 0)
         return "0";
      String ret = "";
      for(Integer i : poly.keySet())
      {
         String term = "";
         if(poly.get(i) == -1 && i > 0)
            term += "-";
         else if(poly.get(i) != 1 || i==0)
            term += poly.get(i);
         if(i > 0)
         {
            term += "x";
            if(i != 1)
               term += "^" + i;
         }
         ret = term + " + " + ret;
      }
      return ret.substring(0, ret.length()-3);
   }

}


/***************************************  
 
 Map:  {0=2, 1=-4, 3=2}
 poly:  2x^3 + -4x + 2
 Evaluated at 2.0: 10.0
 -----------
 Map:  {0=-3, 1=4, 4=2}
 poly2:  2x^4 + 4x + -3
 Evaluated at -10.5: 24265.125
 -----------
 Sum: 2x^4 + 2x^3 + -1
 Product:  4x^7 + -8x^5 + 12x^4 + -6x^3 + -16x^2 + 20x + -6
 -----------
 poly3:  x + 1
 poly4:  x + -1
 Sum:  2x
 Product:  x^2 + -1
 Product:  x^2 + -1
 -----------
 poly5:  -1x + 1
 poly4:  x + -1
 Sum:  0
 Product:  -x^2 + 2x + -1    
 
 ********************************************/