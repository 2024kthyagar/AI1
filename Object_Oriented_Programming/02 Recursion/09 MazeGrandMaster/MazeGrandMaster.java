// Name:
// Date:

import java.util.*;
import java.io.*;
import java.io.File;

public class MazeGrandMaster
{
   public static void main(String[] args)
   {
      Scanner sc = new Scanner(System.in);
      System.out.print("Enter the maze's filename (no .txt): ");
      Maze m = new Maze(sc.next() + ".txt.");
      // Maze m = new Maze();    
      m.display();      
      System.out.println("Options: ");
      System.out.println("1: Find the shortest path\n\tIf no path exists, say so.");
      System.out.println("2: Mark only the shortest correct path and display the count of STEPs.\n\tIf no path exists, say so.");
      System.out.print("Please make a selection: ");
      m.solve(sc.nextInt());
   } 
}

class Maze
{
   //Constants
   private final char WALL = 'W';
   private final char DOT = '.';
   private final char START = 'S';
   private final char EXIT = 'E';
   private final char STEP = '*';
   //Instance Fields
   private char[][] maze;
   private int startRow, startCol;
  
   //constructors
	
	/* 
	 * EXTENSION 
	 * This no a arg constructor that generates a random maze
	 */
   public Maze()
   {
   
      for(int r=0; r<maze.length; r++)
      {
         for(int c=0; c<maze[0].length; c++)
         {
            int rand = (int) (Math.random()*2);
            if(rand == 1)
               maze[r][c] = WALL;
            else
               maze[r][c] = DOT;
         }
      }
      startRow = (int) (Math.random()*maze.length);
      startCol = (int) (Math.random()*maze[0].length);
      maze[startRow][startCol] = START;
   
      int endRow = (int) (Math.random()*maze.length);
      int endCol = (int) (Math.random()*maze[0].length);
      boolean sameAsStart = true;
      while(sameAsStart)
      {
         if(endRow == startRow && endCol == startCol)
         {
            endRow = (int) (Math.random()*maze.length);
            endCol = (int) (Math.random()*maze[0].length);
         }
         else
            sameAsStart = false;
      }
      maze[endRow][endCol] = EXIT;
   
   }
	
	/* 
	 * Copy Constructor  
	 */
   public Maze(char[][] m)  
   {
      maze = m;
      for(int r = 0; r < maze.length; r++)
      {
         for(int c = 0; c < maze[0].length; c++)
         { 
            if(maze[r][c] == START)      //identify start
            {
               startRow = r;
               startCol = c;
            }
         }
      }
   } 
	
	/* 
	 * Use a try-catch block
	 * Use next(), not nextLine()  
	 */
   public Maze(String filename)    
   {
      Scanner infile = null;
      try
      {
         infile = new Scanner(new File(filename));
      }
      catch (Exception e)
      {
         System.out.println("File not found");
      }
      maze = new char[infile.nextInt()][infile.nextInt()];
      int i = 0;
      while(infile.hasNext())
      {
         maze[i] = infile.next().toCharArray();
         i++;
      }
      for(int r = 0; r < maze.length; r++)
      {
         for(int c = 0; c < maze[0].length; c++)
         { 
            if(maze[r][c] == START)      //identify start location
            {
               startRow = r;
               startCol = c;
            }
         }
      }
   	       
      
   }
   
   public char[][] getMaze()
   {
      return maze;
   }
   
   public void display()
   {
      if(maze==null) 
         return;
      for(int a = 0; a<maze.length; a++)
      {
         for(int b = 0; b<maze[0].length; b++)
         {
            System.out.print(maze[a][b]);
         }
         System.out.println("");
      }
      System.out.println("");
   }
   
   public void solve(int n)
   {
      switch(n)
      {    
         case 1:
         {   
            int shortestPath = findShortestLengthPath(startRow, startCol);
            if( shortestPath < 999 )
               System.out.println("Shortest path is " + shortestPath);
            else
               System.out.println("No path exists."); 
            break;
         }   
            
         case 2:
         {
            String strShortestPath = findShortestPath(startRow, startCol);
            if( strShortestPath.length()!=0 )
            {
               System.out.println("Shortest length path is: " + getPathLength(strShortestPath));
               System.out.println("Shortest path is: " + strShortestPath);
               markPath(strShortestPath);
               display();  //display solved maze
            }
            else
               System.out.println("No path exists."); 
            break;
         }
         default:
            System.out.println("File not found");   
      }
   }
   
 /*  1   recur until you find E, then return the shortest path
     returns -1 if it fails
     precondition: Start can't match with Exit
 */ 
   public int findShortestLengthPath(int r, int c)
   {
      if(r < 0 || r>maze.length-1 || c<0 || c>maze[0].length-1)
         return 999; 
      else if(maze[r][c] == EXIT)
         return 0;
      else if(maze[r][c] == START)
      {
         int up = findShortestLengthPath(r, c+1);
         int down = findShortestLengthPath(r, c-1);
         int left = findShortestLengthPath(r-1, c);
         int right = findShortestLengthPath(r+1, c);
         return 1+ Math.min(Math.min(Math.min(up, down), left), right);
      }
      else if(maze[r][c] == DOT)
      {
         maze[r][c] = 'o';
         int up =findShortestLengthPath(r, c+1);
         int down = findShortestLengthPath(r, c-1);
         int left = findShortestLengthPath(r-1, c);
         int right = findShortestLengthPath(r+1, c);
         maze[r][c] = DOT;
         return 1+ Math.min(Math.min(Math.min(up, down), left), right);
      }
      else
      {
         return 999;
      }
   }  
   
/*  2   recur until you find E, then build the True path 
     use only the shortest path
     returns -1 if it fails
     precondition: Start can't match with Exit
 */
   public String findShortestPath(int r, int c)
   {
      
      if(r < 0 || r>maze.length-1 || c<0 || c>maze[0].length-1)
         return ""; 
      else if(maze[r][c] == EXIT)
         return "((" + r + "," + c + "),0)";
      else if(maze[r][c] == START)
      {
         String up = findShortestPath(r, c+1);
         String down = findShortestPath(r, c-1);
         String left = findShortestPath(r-1, c);
         String right = findShortestPath(r+1, c);
         int uplen = 999;
         int downlen = 999;
         int leftlen = 999;
         int rightlen = 999;
         if(up.length() > 0)
         {
            uplen = 1+ getPathLength(up);
         }
         if(down.length() > 0)
         {
            downlen = 1+ getPathLength(down);
         }
         if(left.length() > 0)
         {
            leftlen = 1+ getPathLength(left);
         }
         if(right.length() > 0)
         {
            rightlen = 1+ getPathLength(right);
         }
         int min = Math.min(Math.min(Math.min(uplen, downlen), leftlen), rightlen);
         if(uplen == min)
            return "((" + r + "," + c + ")," + min +")," + up;
         else if( downlen == min)
            return "((" + r + "," + c + ")," + min +")," + down;
         else if(leftlen == min)
            return "((" + r + "," + c + ")," + min +")," + left;
         else if(rightlen == min)
            return "((" + r + "," + c + ")," + min +")," + right;
         else 
            return "";
      }
         
      
      else if(maze[r][c] == DOT)
      {
         maze[r][c] = 'o';
         String up = findShortestPath(r, c+1);
         String down = findShortestPath(r, c-1);
         String left = findShortestPath(r-1, c);
         String right = findShortestPath(r+1, c);
         int uplen = 999;
         int downlen = 999;
         int leftlen = 999;
         int rightlen = 999;
         if(up.length() > 0)
         {
            uplen = 1+ getPathLength(up);
         }
         if(down.length() > 0)
         {
            downlen = 1+ getPathLength(down);
         }
         if(left.length() > 0)
         {
            leftlen = 1+ getPathLength(left);
         }
         if(right.length() > 0)
         {
            rightlen = 1+ getPathLength(right);
         }
         maze[r][c] = DOT;
         int min = Math.min(Math.min(Math.min(uplen, downlen), leftlen), rightlen);
         if(uplen == min)
            return "((" + r + "," + c + ")," + uplen +")," + up;
         else if( downlen == min)
            return "((" + r + "," + c + ")," + downlen +")," + down;
         else if(leftlen == min)
            return "((" + r + "," + c + ")," + leftlen +")," + left;
         else if(rightlen == min)
            return "((" + r + "," + c + ")," + rightlen +")," + right;
         else
            return "";
      }
      else
         return "";
   }	

   public int getPathLength(String str)
   {
      int index = str.indexOf(',', (str.indexOf(',')+1));
      String length = str.substring(index+1, str.indexOf(')', index+1));
      return Integer.parseInt(length);
   }

   //a recursive method that takes an argument created by the method 2 in the form of 
   //((5,0),10),((5,1),9),((6,1),8),((6,2),7),((6,3),6),((6,4),5),((6,5),4),((6,6),3),((5,6),2),((4,6),1),((4,7),0)
   //and it marks the actual path in the maze with STEP
   //precondition:   the String is either an empty String or one that has the correct format above
   //                the indexes must be correct for this method to work  
   public void markPath(String strPath)
   {
      if(getPathLength(strPath) >= 1)
      {
         System.out.println(strPath.charAt(2) + " " + strPath.charAt(4));
         if(maze[Integer.parseInt(strPath.substring(2, 3))][Integer.parseInt(strPath.substring(4,5))] == START)
         {
            int index = strPath.indexOf('(', (strPath.indexOf('(', (strPath.indexOf('('))+1)+1)+1);
            markPath(strPath.substring(index));
         }
         else
         {
            maze[Integer.parseInt(strPath.substring(2, 3))][Integer.parseInt(strPath.substring(4,5))] = '*';
            int index = strPath.indexOf('(', (strPath.indexOf('(', (strPath.indexOf('('))+1)+1)+1);
         //System.out.println(strPath.substring(index));
            markPath(strPath.substring(index));
         }
      }
   }
}

 // Enter the maze's filename (no .txt): maze0
 // WWWWWWWW
 // W....W.W
 // WW.W...W
 // W....W.W
 // W.W.WW.E
 // S.W.WW.W
 // W......W
 // WWWWWWWW
 // 
 // Options: 
 // 1: Find the shortest path
 // 	If no path exists, say so.
 // 2: Mark only the shortest correct path and display the count of STEPs.
 // 	If no path exists, say so.
 // Please make a selection: 2
 // Sortest lenght path is: 10
 //   Sortest path is: ((5,0),10),((5,1),9),((6,1),8),((6,2),7),((6,3),6),((6,4),5),((6,5),4),((6,6),3),((5,6),2),((4,6),1),((4,7),0)
 // WWWWWWWW
 // W....W.W
 // WW.W...W
 // W....W.W
 // W.W.WW*E
 // S*W.WW*W
 // W******W
 // WWWWWWWW