// Name:   
// Date:
 
import java.util.*;
import java.io.*;

/* Resource classes and interfaces for 
 *              Graphs6: Dijkstra
 *              Graphs7: Dijkstra with Cities
 */

class Neighbor implements Comparable<Neighbor>
{
   //2 Neighbors are equal if and only if they have the same name
   //implement all methods needed for a HashSet and TreeSet to work with Neighbor objects
   private final wVertex target;
   private final double edgeDistance;
   
   public Neighbor(wVertex t, double d) {
      target = t;
      edgeDistance = d;
   }
   
   public wVertex getTarget()
   {
      return target;
   }
   
   
   public double getDistance()
   {
      return edgeDistance;
   }
   
   //add all methods needed for a HashSet and TreeSet to function with Neighbor objects
   //use only target, not distances, since a vertex can't have 2 neighbors that have the same target
   //.........
   public int hashCode()
   {
      return target.hashCode();
   }
   
   public boolean equals(Object other)
   {
      if(other instanceof Neighbor)
      {
         Neighbor temp = (Neighbor) other;
         return target.getName().equals(temp.getTarget().getName());
      }
      return false;
   }
   
   public int compareTo(Neighbor n)
   {
      return target.getName().compareTo(n.getTarget().getName());
   }
   
   public String toString()
   {
      return target.getName() + " " + edgeDistance;  
   }
}

 /**************************************************************/
class PQelement implements Comparable<PQelement> { 
//used just for a PQ, contains a wVertex and a distance, also previous that is used for Dijksra 7
//compareTo is using the distanceToVertex to order them such that the PriorityQueue works
//will be used by the priority queue to order by distance
 
   private wVertex vertex;
   private Double distanceToVertex; 
   private wVertex previous; //for Dijkstra 7
      
   public PQelement(wVertex v, double d) {
      vertex = v;
      distanceToVertex = d;
   }
   
   //getter and setter methods provided
   public wVertex getVertex() {
      return this.vertex;
   }
   
   public Double getDistanceToVertex() {
      return this.distanceToVertex;
   }
   
   public void setVertex(wVertex v) {
      this.vertex = v;
   }
   
   public void setDistanceToVertex(Double d) {
      this.distanceToVertex = d;
   }   
   
   public int compareTo(PQelement other) {
      //we assume no overflow will happen since distances will not go over the range of int
      return (int)(distanceToVertex - other.distanceToVertex);
   }
   
   public wVertex getPrevious()  //Dijkstra 7
   {
      return this.previous;
   }
   public void setPrevious(wVertex v) //Dijkstra 7
   {
      this.previous = v;
   } 
   
   //implement toString to match the sample output   
   public String toString()
   { 
      String toReturn = "";
      //your code here...
      if(previous == null)
         toReturn += vertex.getName() + " " + distanceToVertex + " Previous: null";
      else if(previous != null)
         toReturn += vertex.getName() + " " + distanceToVertex + " Previous: " + previous.getName();
      return toReturn;
   }
}

/********************* wVertexInterface ************************/
interface wVertexInterface 
{
   public String getName(); 
      
    //returns an arraylist of PQelements that store distanceToVertex to another wVertex
   public ArrayList<PQelement> getAlDistanceToVertex();
   
   //returns the PQelement that has the vertex equal to v
   public PQelement getPQelement(wVertex v);
      
   /*
   postcondition: returns null if wVertex v is not in the alDistanceToVertex
                  or the distance associated with that wVertex in case there is a PQelement that has v as wVertex
   */
   public Double getDistanceToVertex(wVertex v);
   
   /*
   precondition:  v is not null
   postcondition: - if the alDistanceToVertex has a PQelement that has the wVertex component equal to v
                  it updates the distanceToVertex component to d
                  - if the alDistanceToVertex has no PQelement that has the wVertex component equal to v,
                  then a new PQelement is added to the alDistanceToVertex using v and d   
   */
   public void setDistanceToVertex(wVertex v, double m);
   public Set<Neighbor> getNeighbors(); 
   public void addAdjacent(wVertex v, double d);  
   public String toString(); 
}

class wVertex implements Comparable<wVertex>, wVertexInterface 
{ 
   public static final double NODISTANCE = Double.POSITIVE_INFINITY; //constant to be used in class
   private final String name;
   private Set<Neighbor> neighbors;  
   private ArrayList<PQelement> alDistanceToVertex; //should have no duplicates, enforced by the getter/setter methods
  
   /* constructor, accessors, modifiers  */ 
   public wVertex(String n)
   {
      name = n;
      neighbors = new TreeSet<>();
      alDistanceToVertex = new ArrayList<>();
   }
   
   public String getName()
   {
      return name;
   } 
      
    //returns an arraylist of PQelements that store distanceToVertex to another wVertex
   public ArrayList<PQelement> getAlDistanceToVertex()
   {
      return alDistanceToVertex;
   }
   
   //returns the PQelement that has the vertex equal to v
   public PQelement getPQelement(wVertex v)
   {
      for(PQelement p : alDistanceToVertex)
         if(p.getVertex().equals(v))
            return p;
      return null;
   }
      
   /*
   postcondition: returns null if wVertex v is not in the alDistanceToVertex
                  or the distance associated with that wVertex in case there is a PQelement that has v as wVertex
   */
   public Double getDistanceToVertex(wVertex v)
   {
      PQelement p = getPQelement(v);
      if(p == null)
         return NODISTANCE;
      return p.getDistanceToVertex();
   }
   
   /*
   precondition:  v is not null
   postcondition: - if the alDistanceToVertex has a PQelement that has the wVertex component equal to v
                  it updates the distanceToVertex component to d
                  - if the alDistanceToVertex has no PQelement that has the wVertex component equal to v,
                  then a new PQelement is added to the alDistanceToVertex using v and d   
   */
   public void setDistanceToVertex(wVertex v, double m)
   {
      PQelement p = getPQelement(v);
      if(p != null)
         p.setDistanceToVertex((Double) m);
      else
         alDistanceToVertex.add(new PQelement(v, m));
   }
   public Set<Neighbor> getNeighbors()
   {
      return neighbors;
   }
   public void addAdjacent(wVertex v, double d)
   {
      neighbors.add(new Neighbor(v, d));
   }
   
   /* 2 vertexes are equal if and only if they have the same name
      add all methods needed for a HashSet and TreeSet to function with Neighbor objects
      use only target, not distances, since a vertex can't have 2 neighbors that have the same target   
   */
   public int hashCode()
   {
      return name.hashCode();
   }
   
   public boolean equals(Object other)
   {
      if(other instanceof wVertex)
      {
         wVertex temp = (wVertex) other;
         return name.equals(temp.getName());
      }
      return false;
   }
   
   public int compareTo(wVertex w)
   {
      return name.compareTo(w.getName());
   }
   
   public String toString()
   { 
      String toReturn = name;
      toReturn += " "+ neighbors;
      toReturn += " List: " + alDistanceToVertex; 
      return toReturn;
   }
}

/*********************   Interface for Graphs 6:  Dijkstra ****************/
interface AdjListWeightedInterface 
{
   public Set<wVertex> getVertices();  
   public Map<String, wVertex> getVertexMap();  //this is just for codepost testing
   public wVertex getVertex(String vName);
   /* 
      postcondition: if a Vertex with the name v exists, then the map is unchanged.
                     addVertex should work in O(logn)
   */
   public void addVertex(String vName);
   /*
      precondition:  both Vertexes, source and target, are already stored in the graph.
                     addEdge should work in O(1)
   */   
   public void addEdge(String source, String target, double d);
   public void minimumWeightPath(String vertexName); // Dijstra's algorithm
   public String toString();  
}  

 /***********************  Interface for Graphs 7:  Dijkstra with Cities   */
interface AdjListWeightedInterfaceWithCities 
{       
   public List<String> getShortestPathTo(wVertex source, wVertex target);
   public void readData(String vertexNames, String edgeListData) ;
}
 
/****************************************************************/ 
/**************** this is the graph  ****************************/
public class AdjListWeighted implements AdjListWeightedInterface,AdjListWeightedInterfaceWithCities
{
   //we want our map to be ordered alphabetically by vertex name
   private Map<String, wVertex> vertexMap = new TreeMap<String, wVertex>();
   
   /* default constructor -- not needed!  */
  
   /* similar to AdjList, but handles distances (weights) and wVertex*/ 
   
   public Set<wVertex> getVertices()
   {
      Set<wVertex> store = new HashSet<>();
      for(String s : vertexMap.keySet())
         store.add(vertexMap.get(s));
      return store;
   }
   public Map<String, wVertex> getVertexMap()  //this is just for codepost testing
   {
      return vertexMap;
   }
   public wVertex getVertex(String vName)
   {
      return vertexMap.get(vName);
   }
   /* 
      postcondition: if a Vertex with the name v exists, then the map is unchanged.
                     addVertex should work in O(logn)
   */
   public void addVertex(String vName)
   {
      if(!vertexMap.containsKey(vName))
         vertexMap.put(vName, new wVertex(vName));
   }
   /*
      precondition:  both Vertexes, source and target, are already stored in the graph.
                     addEdge should work in O(1)
   */   
   public void addEdge(String source, String target, double d)
   {
      vertexMap.get(source).addAdjacent(vertexMap.get(target), d);
   }
   
   public void minimumWeightPath(String vertexName) // Dijstra's algorithm
   {
      PriorityQueue<PQelement> pq = new PriorityQueue<>();
      wVertex vert = getVertex(vertexName);
      for(wVertex w : getVertices())
         vert.setDistanceToVertex(w, vert.NODISTANCE);
      vert.setDistanceToVertex(vert, 0);
      pq.add(new PQelement(vert, 0));
      while(!pq.isEmpty())
      {
         PQelement nearest = pq.remove();
         for(Neighbor n : nearest.getVertex().getNeighbors())
         {
            double newdist = n.getDistance() + nearest.getDistanceToVertex();
            double olddist = vert.getDistanceToVertex(n.getTarget());
            wVertex nVert = n.getTarget();
            if(newdist < olddist)
            {
               vert.setDistanceToVertex(nVert, newdist);
               vert.getPQelement(nVert).setPrevious(nearest.getVertex());
               pq.add(vert.getPQelement(nVert));
            }
            
         }
      }
   }
      
   public String toString()
   {
      String strResult = "";
      for(String vName: vertexMap.keySet())
      {
         strResult += vertexMap.get(vName) + "\n"; 
      }
      return strResult;
   }
   
   /*  Graphs 7 has two more methods */
   public List<String> getShortestPathTo(wVertex source, wVertex target) 
   {
      List<String> path = new ArrayList<>(); 
      wVertex prev = source.getPQelement(target).getPrevious();
      path.add(0, target.getName());
      while(prev != null)
      {
         path.add(0, prev.getName());
         prev = source.getPQelement(prev).getPrevious();
      }
      return path;
   }  
     
   public void readData(String vertexNames, String edgeListData) 
   {
     /* use a try-catch  */
      Scanner infile = null;
      Scanner edgefile = null;
      try
      {
         infile = new Scanner(new File(vertexNames));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      try
      {
         edgefile = new Scanner(new File(edgeListData));  
      }
      catch(IOException e)
      {
         System.out.println("oops");
         System.exit(0);   
      }
      int size = infile.nextInt();
      for(int i=0; i<size; i++)
      {
         addVertex(infile.next());
      }
      while(edgefile.hasNextLine())
      {
         String[] edge = edgefile.nextLine().split(" ");
         addEdge(edge[0], edge[1], Double.parseDouble(edge[2]));
      }
   }
}