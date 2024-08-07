// Name:   
// Date:
 
import java.util.*;
import java.io.*;

/* For use with Graphs11: State Graphs,
   Heads-Tails-Heads
 */

class HTH_Driver
{
   public static void main(String[] args) throws FileNotFoundException
   {
      System.out.print("Enter the initial state, three H and/or T:  ");
      Scanner in = new Scanner(System.in);
      String initial = in.next().toUpperCase();
      Vertex v = makeGraph(initial);
      System.out.println("The state graph has been made.");
      
      while(true)
      {
         System.out.print("Enter the final state, three H and/or T:  ");
         String finalState = in.next().toUpperCase();;
         if( finalState.equals("-1") )
            break;
         v = findBreadth(v, finalState);
         System.out.println("The shortest path from "+initial+" to "+ finalState+ " is: ");
         System.out.println(initial);
         String s = "";
         while(v.previous != null)
         {
            s = v+"\n"+s;
            v = v.previous;
         }
         System.out.println(s);
      }
   }
   
   public static Vertex makeGraph(String s)
   {
   
      boolean[] state = new boolean[3];
      int i=0;
      for(char c : s.toCharArray())
      {
         if(c == 'H')
            state[i] = true;
         else state[i] = false;
         i++;
      }
      Vertex v = new Vertex(state, null);
      List<Vertex> allEdge = new ArrayList<>();
      allEdge.add(v);
      generateMap(v, allEdge);
      v.setEdges(allEdge);
      
      return v;
   }
   
   
   public static void generateMap(Vertex v, List<Vertex> allEdge)
   {
      System.out.println(v);
      boolean[] state = v.getState();
      boolean[] temp = new boolean[] {state[0], !state[1], state[2]};
      Vertex newV = new Vertex(temp, null);
      if(!allEdge.contains(newV))
      {
         allEdge.add(newV);
         generateMap(newV, allEdge);
      }
      
      if(state[0] == state[1]) {
         temp = new boolean[] {state[0], state[1], !state[2]};
         newV = new Vertex(temp, null);
         if(!allEdge.contains(newV))
         {
            allEdge.add(newV);
            generateMap(newV, allEdge);
         }
      }
      if(state[1] == state[2]) {
         temp = new boolean[] {!state[0], state[1], state[2]};
         newV = new Vertex(temp, null);
         if(!allEdge.contains(newV))
         {
            allEdge.add(newV);
            generateMap(newV, allEdge);
         }
      }
   }
   
   
   public static Vertex findBreadth(Vertex v, String goal)
   {
      for(int i=0; i<v.getEdges().size()-1; i++)
      {
         for(int j=i+1; j<v.getEdges().size(); j++)
         {
            makeEdge(v.getEdges().get(i), v.getEdges().get(j));
         }
      }
   
      for(Vertex temp : v.getEdges())
      {
         System.out.println(temp + " " + temp.getEdges());
      }
   
      for(Vertex next : v.getEdges())
      {
         if(next.toString().equals(goal))
            return next;
      }
      return v;
   
   }
   
   public static void makeEdge(Vertex source, Vertex target)
   {
      boolean[] state = source.getState();
      boolean[] temp = new boolean[] {state[0], !state[1], state[2]};
      if(areEqual(target.getState(), temp))
         source.addEdge(target);
   
      if(state[0] == state[1]) 
      {
         temp = new boolean[] {state[0], state[1], !state[2]};
         if(areEqual(target.getState(), temp))
            source.addEdge(target);
      }
   
      if(state[1] == state[2]) 
      {
         temp = new boolean[] {!state[0], state[1], state[2]};
         if(areEqual(target.getState(), temp))
            source.addEdge(target);
      }
   
   }
   
   private static boolean areEqual(boolean[] state, boolean[] temp)
   {
      boolean isEqual = true;
      for(int i=0; i<state.length; i++)
         if(state[i] != temp[i])
            isEqual = false;
      return isEqual;
   }
   
}

class Vertex
{
   private final boolean[] state;
   private List<Vertex> edges = new ArrayList<Vertex>();
   public Vertex previous;
   
   public Vertex(boolean[] s, Vertex p)
   {
      state = s;
      previous = p;
   
   }
   
   
   public boolean[] getState()
   {
      return state;
   }
   
   public List<Vertex> getEdges()
   {
      return edges;
   }
   
   public void setEdges(List<Vertex> e)
   {
      edges = e;
   }
   
   public void addEdge(Vertex v)
   {
      edges.add(v);
   }
   
   public boolean equals(Object other)
   {
      if(other instanceof Vertex)
         return toString().equals(other.toString());
      return false;
   }
   
   public String toString()
   {
      String toret = "";
      for(boolean b : state)
      {
         if(b)
            toret+="H";
         else
            toret+="T";
      }
      return toret;
   }
}

/************************
 Enter the initial state, three H and/or T:  HTH
 The state graph has been made.
 Enter the final state, three H and/or T:  THT
 The shortest path from HTH to THT is: 
 HTH
 HHH
 HHT
 HTT
 TTT
 THT
 
 Enter the final state, three H and/or T:  HHH
 The shortest path from HTH to HHH is: 
 HTH
 HHH
 
 Enter the final state, three H and/or T:  -1
 

 *************************************/