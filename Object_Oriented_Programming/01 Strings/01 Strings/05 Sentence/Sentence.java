class Sentence
{
   private String mySentence;
   private int myNumWords;
   
   //Precondition:  str is not empty.
   //               Words in str separated by exactly one blank.
   public Sentence( String str )
   { 
      mySentence = str;
      String splitstr[] = str.split(" ");
      for(String index : splitstr)
         myNumWords++;
   }
   
   public int getNumWords()
   {  
      return myNumWords;  
   }
   
   public String getSentence()
   {
      return mySentence; 
   }
   
   //Returns true if mySentence is a palindrome, false otherwise.
   public boolean isPalindrome()
   {
      String s = getSentence();
      s = removeBlanks(s);
      s = lowerCase(s);
      s = removePunctuation(s);
      return isPalindrome(s, 0, s.length()-1);
   }
   //Precondition: s has no blanks, no punctuation, and is in lower case.
   //Returns true if s is a palindrome, false otherwise.
   public static boolean isPalindrome( String s, int start, int end )
   {
      if(start == end)
         return true;
      else
      {
         if(s.charAt(start) == s.charAt(end))
         {
            if(end < start)
            {
               return true;
            }
            else
               return isPalindrome(s, start+1, end-1);
          
         }
         else
            return false;
      }
   }
   //Returns copy of String s with all blanks removed.
   //Postcondition:  Returned string contains just one word.
   public static String removeBlanks( String s )
   {  
      String noblanks = "";
      String[] splitstr = s.split(" ");
      for(String i : splitstr)
         noblanks += i;
      return noblanks;
   }
   
   //Returns copy of String s with all letters in lowercase.
   //Postcondition:  Number of words in returned string equals
   //						number of words in s.
   public static String lowerCase( String s )
   {  
      return s.toLowerCase();
   }
   
   //Returns copy of String s with all punctuation removed.
   //Postcondition:  Number of words in returned string equals
   //						number of words in s.
   public static String removePunctuation( String s )
   { 
      //String punct = ".,'?!:;\"(){}[]<>"; 
      String cleaned = "";
       
      for(int i=0; i<s.length(); i++)
      {
         if(Character.isLetterOrDigit(s.charAt(i)) || (s.charAt(i) == ' '))
            cleaned += s.charAt(i);
      }
      
      return cleaned;
   
   }
}
