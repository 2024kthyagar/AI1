// Name:   
// Date:
 
import java.util.*;
import java.io.*;

/* Resource classes and interfaces
 * for use with Graph0 AdjMat_0_Driver,
 *              Graph1 WarshallDriver,
 *          and Graph2 FloydDriver
 */

interface AdjacencyMatrix
{
   public int[][] getGrid();
   public void addEdge(int source, int target);
   public void removeEdge(int source, int target);
   public boolean isEdge(int from, int to);
   public String toString();  //returns the grid as a String
   public int edgeCount();
   public List<Integer> getNeighbors(int source);
   //public List<String> getReachables(String from);  //Warshall extension
}

interface Warshall      //User-friendly functionality
{
   public boolean isEdge(String from, String to);
   public Map<String, Integer> getVertices();     
   public void readNames(String fileName) throws FileNotFoundException;
   public void readGrid(String fileName) throws FileNotFoundException;
   public void displayVertices();
   public void allPairsReachability();   // Warshall's Algorithm
   public List<String> getReachables(String from);  //Warshall extension
}

interface Floyd
{
   public int getCost(int from, int to);
   public int getCost(String from, String to);
   public void allPairsWeighted(); 
}

public class AdjMat implements AdjacencyMatrix,Warshall,Floyd 
{
   private int[][] grid = null;   //adjacency matrix representation
   private Map<String, Integer> vertices = null;   // name maps to index (for Warshall & Floyd)
   /*for Warshall's Extension*/  ArrayList<String> nameList = null;  //reverses the map, index-->name
	  
   /*  write constructor, accessor method, and instance methods here  */  
   public AdjMat(int numNodes)
   {
      grid = new int[numNodes][numNodes];
      vertices = new HashMap<>();
      nameList = new ArrayList<>();
   }
   public int[][] getGrid() 
   {
      return grid;
   }
   public Map<String, Integer> getVertices()
   {
      return vertices;
   }
   public void displayVertices()
   {
      for(int i=0; i<nameList.size(); i++)
      {
         System.out.println(i + "-" + nameList.get(i));
      }
   }
   public void readNames(String fileName) throws FileNotFoundException
   {
      Scanner infile = null;
      try
      {
         infile = new Scanner(new File(fileName));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      int size = infile.nextInt();
      for(int i=0; i<size; i++)
      {
         String name = infile.next();
         nameList.add(name);
         vertices.put(name, i);
      }
   }
   public void readGrid(String fileName) throws FileNotFoundException
   {
      Scanner infile = null;
      try
      {
         infile = new Scanner(new File(fileName));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      int size = infile.nextInt();
      for(int r=0; r<size; r++)
      {
         for(int c=0; c<size; c++)
         {
            grid[r][c] = infile.nextInt();
         }
      }
   }
   public void addEdge(int source, int target)
   {
      grid[source][target] = 1;
   }
   public void removeEdge(int source, int target)
   {
      grid[source][target] = 9999;
   }
   public boolean isEdge(String from, String to)
   {
      return isEdge(vertices.get(from), vertices.get(to));
   }
   public int getCost(int from, int to)
   {
      return grid[from][to];
   }
   public int getCost(String from, String to)
   {
      return getCost(vertices.get(from), vertices.get(to));
   }
   public boolean isEdge(int from, int to)
   {
      return grid[from][to] != 9999;
   }
   public String toString()  //returns the grid as a String
   {
      String ret = "";
      for(int r=0; r<grid.length; r++) {
         for(int c=0; c<grid[0].length; c++)
            ret += grid[r][c] + " ";
         ret += "\n";
      }
      return ret;
   }
   public int edgeCount()
   {
      int count = 0;
      for(int r=0; r<grid.length; r++)
         for(int c=0; c<grid[0].length; c++)
            if(grid[r][c] != 9999 && grid[r][c] > 0)
               count++;
      return count;           
   }
   public List<Integer> getNeighbors(int source)
   {
      List<Integer> neighbors = new ArrayList<>();
      for(int c = 0; c<grid[0].length; c++)
         if(grid[source][c] != 9999)
            neighbors.add(c);
      return neighbors;
   }
   public void allPairsReachability()
   {
      for(int r=0; r<grid.length; r++)
      {
         for(int v=0; v<grid[0].length; v++)
         {
            if(grid[r][v] == 1)
            {
               for(int c=0; c<grid.length; c++)
                  if(grid[v][c]==1)
                     addEdge(r, c);
            }
         }
      }
   }
   public void allPairsWeighted()
   {
      for(int i=0; i<2; i++) {
         for(int r=0; r<grid.length; r++)
         {
            for(int v=0; v<grid[0].length; v++)
            {
               for(int c=0; c<grid.length; c++)
               {
                  int value = grid[r][v] + grid[v][c];
                  if(grid[r][c] > value)
                     grid[r][c] = value;
               }
            }
         }
      }
   }
   public List<String> getReachables(String from)
   {
      List<String> reachable = new ArrayList<>();
      int index = vertices.get(from);
      for(int c=0; c<grid[0].length; c++)
      {
         if(grid[index][c] != 9999)
            reachable.add(nameList.get(c));
      }
      return reachable;
   }
}