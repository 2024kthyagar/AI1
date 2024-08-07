// Name:   
// Date:
 
import java.util.*;
import java.io.*;

/* Resource classes and interfaces
 * for use with Graphs3: EdgeList,
 *              Graphs4: DFS-BFS
 *          and Graphs5: EdgeListCities
 */

/**************** Graphs 3: EdgeList *****/
interface VertexInterface
{
   public String getName();
   public HashSet<Vertex> getAdjacencies();
   
   /*
     postcondition: if the set already contains a vertex with the same name, the vertex v is not added
                    this method should be O(1)
   */
   public void addAdjacent(Vertex v);
   /*
     postcondition:  returns as a string one vertex with its adjacencies, without commas.
                     for example, D [C A]
     */
   public String toString(); 
 
} 
 
/*************************************************************/
class Vertex implements VertexInterface, Comparable<Vertex> //2 vertexes are equal if and only if they have the same name
{
   private final String name;
   private HashSet<Vertex> adjacencies;
  /* enter your code here  */
   public Vertex(String n)
   {
      name = n;
      adjacencies = new HashSet<>();
   }
  
   public String getName()
   {
      return name;
   }
  
   public HashSet<Vertex> getAdjacencies()
   {
      return adjacencies;
   }
  
   public void addAdjacent(Vertex v)
   {
      adjacencies.add(v);
   }
  
   public String toString()
   {
      String toret = name + " [";
      for(Vertex v : adjacencies)
      {
         toret += v.getName() + " ";
      }
      if(adjacencies.size() > 0)
         toret = toret.substring(0, toret.length()-1);
      return toret + "]";
   }
   
   public int hashCode()
   {
      return name.hashCode();
   }
   
   public boolean equals(Object v)
   {
      if(v instanceof Vertex)
         return toString().equals(v.toString());
      return false;
   }
   
   public int compareTo(Vertex v)
   {
      return getName().compareTo(v.getName());
   }
  
}   

/*************************************************************/
interface AdjListInterface 
{
   public Set<Vertex> getVertices();
   public Vertex getVertex(String vName);
   public Map<String, Vertex> getVertexMap();  //this is just for codepost testing
   
   /*      
      postcondition: if a Vertex with the name v exists, then the map is unchanged.
                     addVertex should work in O(log n)
   */
   public void addVertex(String vName);
   
   /*
      precondition:  both Vertexes, source and target, are already stored in the graph.
      postcondition:  addEdge should work in O(1)
   */
   public void addEdge(String source, String target); 
   
   /*
       returns the whole graph as one string, e.g.:
       A [C]
       B [A]
       C [C D]
       D [C A]
     */
   public String toString(); 

}

  
/********************** Graphs 4: DFS and BFS *****/
interface DFS_BFS
{
   public List<Vertex> depthFirstSearch(String name);
   public List<Vertex> breadthFirstSearch(String name);
   /*   extra credit methods */
   public List<Vertex> depthFirstRecur(String name);
   public List<Vertex> depthFirstRecurHelper(Vertex v, ArrayList<Vertex> reachable);
}

/****************** Graphs 5: Edgelist with Cities *****/
interface EdgeListWithCities
{
   public void readData(String cities, String edges) throws FileNotFoundException;
   public int edgeCount();
   public int vertexCount();
   public boolean isReachable(String source, String target);
   public boolean isStronglyConnected(); //return true if every vertex is reachable from every 
                                          //other vertex, otherwise false 
}


/*************  start the Adjacency-List graph  *********/
public class AdjList implements AdjListInterface, DFS_BFS, EdgeListWithCities
{
   //we want our map to be ordered alphabetically by vertex name
   private Map<String, Vertex> vertexMap = new TreeMap<String, Vertex>();
      
   /* constructor is not needed because of the instantiation above */
  
   /* enter your code here  */
   public Set<Vertex> getVertices()
   {
      Set<Vertex> vertices = new HashSet<>();
      for(String s : vertexMap.keySet())
         vertices.add(vertexMap.get(s));
      return vertices;
   }
   public Vertex getVertex(String vName)
   {
      return vertexMap.get(vName);
   }
   public Map<String, Vertex> getVertexMap()  //this is just for codepost testing
   {
      return vertexMap;
   }
   
   /*      
      postcondition: if a Vertex with the name v exists, then the map is unchanged.
                     addVertex should work in O(log n)
   */
   public void addVertex(String vName)
   {
      if(!vertexMap.containsKey(vName))
         vertexMap.put(vName, new Vertex(vName));
   }
   
   /*
      precondition:  both Vertexes, source and target, are already stored in the graph.
      postcondition:  addEdge should work in O(1)
   */
   public void addEdge(String source, String target)
   {
      vertexMap.get(source).addAdjacent(vertexMap.get(target));
   }
   
   /*
       returns the whole graph as one string, e.g.:
       A [C]
       B [A]
       C [C D]
       D [C A]
     */
   public String toString()
   {
      String toret = "";
      for(String s : vertexMap.keySet())
      {
         toret += vertexMap.get(s).toString() + "\n";
      }
      return toret;
   }
 
   public List<Vertex> depthFirstSearch(String name)
   {
      List<Vertex> reachables = new ArrayList<>();
      Stack<Vertex> helper = new Stack<>();
      for(Vertex v : vertexMap.get(name).getAdjacencies())
         helper.add(v);
      while(!helper.isEmpty()) {
         Vertex vert = helper.pop();
         if(!reachables.contains(vert))
         {
            reachables.add(vert);
            for(Vertex v : vert.getAdjacencies())
               helper.push(v);
         }
      }
      return reachables;
   }
   public List<Vertex> breadthFirstSearch(String name)
   {
      List<Vertex> reachables = new ArrayList<>();
      Queue<Vertex> helper = new LinkedList<>();
      for(Vertex v : vertexMap.get(name).getAdjacencies())
         helper.add(v);
      while(!helper.isEmpty()) {
         Vertex vert = helper.remove();
         if(!reachables.contains(vert))
         {
            reachables.add(vert);
            for(Vertex v : vert.getAdjacencies())
               helper.add(v);
         }
      }
      return reachables;
   }
   
   /*   extra credit methods */
   public List<Vertex> depthFirstRecur(String name)
   {
      ArrayList<Vertex> copy = new ArrayList<>();
      ArrayList<Vertex> reachable = new ArrayList<>();
      for(Vertex v : vertexMap.get(name).getAdjacencies())
         copy.add(v);
      for(int i=copy.size()-1; i>=0; i--)
         reachable = depthFirstRecurHelper(copy.get(i), reachable);
      
      return reachable;
   }
   
   public ArrayList<Vertex> depthFirstRecurHelper(Vertex v, ArrayList<Vertex> reachable)
   {
      if(!reachable.contains(v))
      {
         reachable.add(v);
         ArrayList<Vertex> copy = new ArrayList<>();
         for(Vertex temp : v.getAdjacencies())
            copy.add(temp);
         for(int i=copy.size()-1; i>=0; i--)
            reachable = depthFirstRecurHelper(copy.get(i), reachable);
      }
      return reachable;
   } 
   
   public List<Vertex> breadthFirstRecur(String name)
   {
      ArrayList<Vertex> reachable = new ArrayList<>();
      for(Vertex v : vertexMap.get(name).getAdjacencies())
         reachable = breadthFirstRecurHelper(v, reachable);   
      return reachable;
   }
   
   public ArrayList<Vertex> breadthFirstRecurHelper(Vertex v, ArrayList<Vertex> reachable)
   {
      if(!reachable.contains(v))
      {
         reachable.add(v);
         for(Vertex temp : v.getAdjacencies())
            reachable = breadthFirstRecurHelper(temp, reachable);
      }
      return reachable;
   } 
   
   public void readData(String cities, String edges) throws FileNotFoundException
   {
      Scanner infile = null;
      Scanner edgefile = null;
      try
      {
         infile = new Scanner(new File(cities));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      try
      {
         edgefile = new Scanner(new File(edges));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      while(infile.hasNext())
      {
         String name = infile.next();
         addVertex(name);
      }
      while(edgefile.hasNextLine())
      {
         String[] edge = edgefile.nextLine().strip().split(" ");
         addEdge(edge[0], edge[1]);
      }
   }
 
   public int edgeCount()
   {
      int sum = 0;
      for(Vertex v : getVertices())
         sum += v.getAdjacencies().size();
      return sum;
   }
   public int vertexCount()
   {
      return getVertices().size();
   }
   public boolean isReachable(String source, String target)
   {
      return breadthFirstSearch(source).contains(getVertex(target));
   }
   public boolean isStronglyConnected() //return true if every vertex is reachable from every 
                                        //other vertex, otherwise false 
   {
      for(Vertex v : getVertices())
      {
         for(Vertex e : getVertices())
         {
            if(!isReachable(v.getName(), e.getName()))
               return false;
         }
      }   
      return true;             
   }
 
 
}


