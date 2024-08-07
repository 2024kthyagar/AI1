// Name:
// Date:
//uses PostfixEval

import java.util.*;
public class Infix_Extension
{
   public static final String LEFT  = "([{<";
   public static final String RIGHT = ")]}>";
   public static final String operators = "+ - * / % ^ !";
   
   public static void main(String[] args) throws Exception
   {
      System.out.println("Infix  \t-->\tPostfix\t\t-->\tEvaluate");
      /*build your list of Infix expressions here  */
      List<String> infixExp = new ArrayList<>();
      // System.out.println(isStrictlyLower("+", "/"));      
      // infixExp.add("3 + 4 * 5");
      // infixExp.add("3 * 4 + 5");
      // infixExp.add("1.3 + 2.7 + -6 * 6");
      // infixExp.add("( 33 + -43 ) * ( -55 + 65 )");
      // infixExp.add("3 * 4 + 5 / 2 - 5");
      // infixExp.add("8 + 1 * 2 - 9 / 3");
      // infixExp.add("3 * ( 4 * 5 + 6 )");
      // infixExp.add("3 + ( 4 - 5 - 6 * 2 )");
      // infixExp.add("2 + 7 % 3");
      // infixExp.add("( 2 + 7 ) % 3");
      infixExp.add("( 3.0 + -1.0 ) ^ 3.0");
      infixExp.add("2 ^ 3 + 3");
      infixExp.add("3 * 2 ^ 3");
      infixExp.add("( 1 + 3 ) !");
      infixExp.add("1 + 3 !");
      infixExp.add("1 * 3 !");
      infixExp.add("3 * ( 4 ^ 2 ! ) + 1 - 2");
      // infixExp.add("3 ? 2");
      // infixExp.add("3 @ 2");
      // infixExp.add("( 3 + 2");
      infixExp.add("3 + 2 ]");
      // infixExp.add("( 3 + 2 ]");
         
         
      for( String infix : infixExp )
      {
         String pf = infixToPostfix(infix);  //get the conversion to work first
         // System.out.println(infix + "\t\t\t" + pf );  
         System.out.println(infix + "\t\t\t" + pf + "\t\t\t" + PostfixEval.eval(pf));  //PostfixEval must work!
      }
   }
   
   public static String infixToPostfix(String infix) throws Exception
   {
      if(!ParenMatch.checkParen(infix))
         throw new Exception(infix + " ERROR in parentheses");
      List<String> nums = new ArrayList<String>(Arrays.asList(infix.split(" ")));
            /* enter your code here  */
      String finalstr = "";
      Stack<String> symbols = new Stack<>();
      for(String str : nums)
      {
         if(ParenMatch.isLeftParen(str) >= 0)
            symbols.push(str);
         else if(ParenMatch.isRightParen(str) >= 0)
         {
            while(ParenMatch.isRightParen(str) != ParenMatch.isLeftParen(symbols.peek()))
            {
               finalstr += symbols.pop() + " ";
            }
            symbols.pop();
         }
         else if(PostfixEval.isOperator(str))
         {
            if(symbols.isEmpty())
               symbols.push(str);
            else
            {
               while(!symbols.isEmpty() && isHigherOrEqual(symbols.peek(), str))
               {
                  finalstr += symbols.pop() + " ";
               }
               symbols.push(str);
            }
         }
         else
         {
            try {
               double d = Double.parseDouble(str);
            } catch (NumberFormatException nfe) {
               throw new Exception(infix + " ERROR non-algebraic symbol");
            }
            finalstr += str + " ";
         }
      }
      while(!symbols.isEmpty())
         finalstr += symbols.pop() + " ";
      return finalstr.strip();
   }
   
   
   //enter your precedence method below
   public static boolean isHigherOrEqual(String top, String next) // true if top >= next
   {
      if(getLevel(top) >= getLevel(next))
         return true;
      return false;
   }
   
   public static int getLevel(String operator)
   {
      if(operator.equals("+") || operator.equals("-"))
         return 0;
      else if(operator.equals("*") || operator.equals("/") || operator.equals("%"))
         return 1;  
      else if(operator.equals("^"))
         return 2;
      else if(operator.equals("!"))
         return 3;
      return -1;
   }
   
}


/********************************************

Infix  	-->	Postfix		-->	Evaluate
 5 - 1 - 1			5 1 - 1 -			3.0
 5 - 1 + 1			5 1 - 1 +			5.0
 12 / 6 / 2			12 6 / 2 /			1.0
 3 + 4 * 5			3 4 5 * +			23.0
 3 * 4 + 5			3 4 * 5 +			17.0
 1.3 + 2.7 + -6 * 6			1.3 2.7 + -6 6 * +			-32.0
 ( 33 + -43 ) * ( -55 + 65 )			33 -43 + -55 65 + *			-100.0
 8 + 1 * 2 - 9 / 3			8 1 2 * + 9 3 / -			7.0
 3 * ( 4 * 5 + 6 )			3 4 5 * 6 + *			78.0
 3 + ( 4 - 5 - 6 * 2 )			3 4 5 - 6 2 * - +			-10.0
 2 + 7 % 3			2 7 3 % +			3.0
 ( 2 + 7 ) % 3			2 7 + 3 %			0.0
      
***********************************************/
