import world.*;
import java.awt.Point;
import java.util.ArrayList;
import java.util.List;
import java.lang.NullPointerException;
import java.util.HashMap;
import java.util.TreeMap;
import java.util.Comparator;

public class MyRobotClass extends Robot{
  
  
  class Meta{
    Point parent;
    int gCost;
    public Meta(Point parent, int gCost){this.parent=parent; this.gCost=gCost;}
  }
  
//  public class FComparator implements Comparator {
//    
//    public int compare(Point o1, Point o2) {
//      assert openList.containsKey(o1);
//      assert openList.containsKey(o2);
//      
//      if(o1==o2) return 0;
//      if(o1.equals(o2)) return 0;
//      
//      int o1f = fCost(o1, dest);
//      int o2f = fCost(o2, dest);
//      if(o1f<o2f) return -1;
//      if(o1f>o2f) return 1;
//      return 0;
//    
//    }
//  }
//  
  
  
  
  
  
  TreeMap<Point, Meta> openList = new TreeMap<Point, Meta>(new Comparator<Point>(){
    
    @Override
    public int compare(Point o1, Point o2) {
      assert openList.containsKey(o1);
      assert openList.containsKey(o2);
      
      if(o1==o2) return 0;
      if(o1.equals(o2)) return 0;
      
      int o1f = fCost(o1, dest);
      int o2f = fCost(o2, dest);
      if(o1f<o2f) return -1;
      if(o1f>o2f) return 1;
      return 0;
      
    }
    
  });
  HashMap<Point, Meta> closeList = new HashMap<Point, Meta>();
  Point dest;
  
  @Override
  public void travelToDestination(){
    
    dest = this.getDest();
    Point start = this.getPosition();
    Point cur = start;
    closeList.put(start, new Meta(null, 0));
    
    while(!cur.equals(dest)){
      
      assert closeList.containsKey(cur);
      for(Point p: this.adjacentPoints(cur)){
        //put into list OR update it if it should be updated
        this.updateGCost(cur, p);
      }
      
      
      
      Point best = this.openList.firstKey();
      
//      for(Point p: this.adjacentPoints(cur)){
//        this.updateGCost(cur, p);
//        int fcost = this.fCost(p, dest);
//        if(fcost < min) {
//          min = fcost;
//          best = p;
//        }
//      }
      
      assert openList.containsKey(best);
      closeList.put(best, openList.get(best));
      openList.remove(best);
      cur = best;
      
//      super.move(best);
      
      
      
      ArrayList<Point> path = new ArrayList<Point>();
      // cur is at dest at this point in code
      while(cur != start){
        path.add(0,cur);
        cur = this.closeList.get(cur).parent;
      }
      for(Point p : path){
        super.move(p);
      }
      
      
      
    }
  }
  
  public Point getDest(){
    for(int x=0;x<101;x++){
      for(int y=0;y<101;y++){
        try{
          Point p = new Point(x,y);
          if(super.pingMap(p).equals("F")) return p;
          
        }catch(NullPointerException e){
          //pass
        }
      }
    }
    return null;
  }
  
  
  
  public boolean canPutOnPath(Point p){
    if(!isValid(p)) return false;
    return !this.closeList.containsKey(p);
  }
  
  public boolean isValid(Point p){
    if(p==null) return false;
    if(p.getX() < 0 || p.getY()<0) return false;
    
    try{
      
      String val = super.pingMap(p);
      return val.equals("O") || val.equals("F");
      
    } catch (NullPointerException e){
      return false;
    }     
    
  }
  
  public List<Point> adjacentPoints(Point cur){
    assert this.closeList.containsKey(cur);
    List<Point> out = new ArrayList<Point>();
    
    Point [] possible = {
      new Point(cur.x+1, cur.y-1),
      new Point(cur.x+1, cur.y),
      new Point(cur.x+1, cur.y+1),
      
      new Point(cur.x, cur.y-1),
      new Point(cur.x, cur.y+1),
      
      new Point(cur.x-1, cur.y-1),
      new Point(cur.x-1, cur.y),
      new Point(cur.x-1, cur.y+1),
      
    };
    
    for(Point p: possible){
      if(canPutOnPath(p)) out.add(p);
    }
    return out;
  }
  
  
  public int fCost(Point possible, Point dest){
    //f = g + h
    
    return gCost(possible) + hCost(possible, dest);
  }
  
  public void updateGCost(Point cur, Point p){
    /* 
     * if p in OpenList:
     *     gCostWithOldParent = gCosts[p]
     *     if diagonal:
     *         gCostWithCur = gCosts[cur] + 14
     *     else:
     *         gCostWithCur = gCosts[cur] + 10
     *    
     *     if gCostWithCur < gCostWithOldParent:
     *         parents[p] = cur
     *         gCosts[p] = gCostWithCur
     * else:
     *     parents[p] = cur;
     *     if diagonal:
     *           pGCost =  gCosts[cur] + 14
     *     else:
     *           pGCost = gCosts[cur] + 10
     *     GCosts[p] = pGCost
     * 
     * 
     */
    assert this.closeList.containsKey(cur);
    
    int curGCost = this.closeList.get(cur).gCost;
    int toAdd = 1;//diagonal(cur,p)? 14:10;
    if(this.openList.containsKey(p)){
      int gCostWithOldParent = this.openList.get(p).gCost;
      if(curGCost+toAdd<gCostWithOldParent){
        this.openList.put(p, new Meta(cur, curGCost+toAdd));
      }
      
    } else {
      this.openList.put(p, new Meta(cur, curGCost+toAdd));
    }
  }
  
  public int gCost(Point p){
    
    return this.openList.get(p).gCost;
    
  }
  
  public int hCost(Point possible, Point dest){
    return manhattan(possible, dest);
  }
  
  public int manhattan(Point from, Point dest){
    int m= Math.abs(from.x-dest.x) + Math.abs(from.y-dest.y);
    return m;
  }
  
  public boolean diagonal(Point a, Point b){
    return this.manhattan(a,b) > 1;
  }
  
  public static void main(String args[]) throws java.lang.Exception{
    World myWorld = new World("TestCases/myInputFile2.txt", false);
    myWorld.createGUI(100,100,100);
    MyRobotClass myRobot = new MyRobotClass();
    myRobot.addToWorld(myWorld);
    
    
    myRobot.travelToDestination();
    
  }
  
}