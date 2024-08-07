// Name:
// Date:

import java.util.*;

public class PostfixEval
{
   public static final String operators = "+ - * / % ^ !";
   
   public static void main(String[] args)
   {
      System.out.println("Postfix  -->  Evaluate");
      ArrayList<String> postfixExp = new ArrayList<String>();
      /*  build your list of expressions here  */
      postfixExp.add("3 4 5 * +");
      postfixExp.add("3 4 * 5 +");
      postfixExp.add("1.3 2.7 + -6 6 * +");
      postfixExp.add("33 -43 + -55 65 + *");
      postfixExp.add("3 4 * 5 2 / + 5 -");
      postfixExp.add("8 1 2 * + 9 3 / -");
      postfixExp.add("3 4 5 * 6 + *");
      postfixExp.add("3 4 5 - 6 2 * - +");
      postfixExp.add("2 7 3 % +");
      postfixExp.add("2 7 + 3 %");
      postfixExp.add("2 3 ^");
      postfixExp.add("2 -2 ^");
      postfixExp.add("5 !");
      postfixExp.add("1 1 1 1 1 + + + + !");
   
      
   
      
      for( String pf : postfixExp )
      {
         System.out.println(pf + "\t\t" + eval(pf));
      }
   }
   
   public static double eval(String pf)
   {
      List<String> postfixParts = new ArrayList<String>(Arrays.asList(pf.split(" ")));
      /*  enter your code here  */
      double result = 0;
      Stack<Double> nums = new Stack<>();
      for(String str : postfixParts)
      {
         if(!isOperator(str))
            nums.push(Double.parseDouble(str));
         else if(str.equals("!"))
         {
            result = eval(0, nums.pop(), str);
            nums.push(result);
         }
         else if(nums.size() > 1)
         {
            result = eval(nums.pop(), nums.pop(), str);
            nums.push(result);
         }
      }
      
      return result;
   }
   
   public static double eval(double a, double b, String ch)
   {
      if(ch.equals("+"))
         return b+a;
      else if(ch.equals("-"))
         return b-a;
      else if(ch.equals("*"))
         return b*a;
      else if(ch.equals("/"))
         return b/a;
      else if(ch.equals("%"))
         return b%a;
      else if(ch.equals("^"))
         return Math.pow(b, a);
      else if(ch.equals("!"))
      {
         for(double i=b-1; i>0; i--)
            b *= i;
         return b;
      }    
      else 
         return -1;
   }
   
   public static boolean isOperator(String op)
   {
      if(operators.contains(op))
         return true;
      return false;
   }
}

/**********************************************
Postfix  -->  Evaluate
 3 4 5 * +		23
 3 4 * 5 +		17
 10 20 + -6 6 * +		-6
 3 4 + 5 6 + *		77
 3 4 5 + * 2 - 5 /		5
 8 1 2 * + 9 3 / -		7
 2 3 ^		8
 20 3 %		2
 21 3 %		0
 22 3 %		1
 23 3 %		2
 5 !		120
 1 1 1 1 1 + + + + !		120
 
 
 *************************************/