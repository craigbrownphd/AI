import world.*;
import java.awt.Point;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.lang.NullPointerException;
import java.util.HashMap;

public class MyRobotClass extends Robot{

  // Meta class contains the parent as well as the gcost
  class Meta{
    Point parent;
    int gCost;
    int hCost;
    public Meta(Point parent, int gCost){this.parent=parent; this.gCost=gCost; this.hCost=-1;}
  }

  private World myWorld;
  
//  public class FComparator implements Comparator {
//    
//    public int compare(Point o1, Point o2) {
//      assert openListLookup.containsKey(o1);
//      assert openListLookup.containsKey(o2);
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
  
  
  
  private String[][] worldRep;
  // things we have seen but haven't stepped on
  HashMap<Point, Meta> openListLookup = new HashMap<Point, Meta>();
  HashSet<Point> openList = new HashSet<Point>();
    // compare function used to order treemap
//    public int compare(Point o1, Point o2) {
//      assert openListLookup.containsKey(o1);
//      assert openListLookup.containsKey(o2);
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
    


  // things we've stepped on
  HashMap<Point, Meta> closeList = new HashMap<Point, Meta>();
  Point dest;

  public String pingMap(Point p) {
    String pointVal = worldRep[((int) p.getY())] [(int)p.getX()];
    if (pointVal!="") {
      return pointVal;
    }
    else {
      return super.pingMap(p);
    }
  }

  public void travelCertain(){
    dest = this.getDest();
    Point start = this.getPosition();
    Point cur = start;
    // since we start here, put to start
    closeList.put(start, new Meta(null, 0));

    // while we haven't made it to the endgoal
    while(!cur.equals(dest)) {


      assert closeList.containsKey(cur);
      // for all adjacent points, update current
      for (Point p : this.adjacentPoints(cur)) {
        //put into list OR update it if it should be updated
        this.updateGCost(cur, p);
      }


      // the best point to move to next will have the best fcost

      Point best = (Point) openList.toArray()[0];
      int i = 0;
      for (Point p : openList) {
        Meta pMeta = openListLookup.get(p);
        Meta bestMeta = openListLookup.get(best);
        pMeta.hCost = hCost(p, dest);
        bestMeta.hCost = hCost(best, dest);
        if (pMeta.gCost + pMeta.hCost < bestMeta.gCost + bestMeta.hCost) {
          best = p;
        }
        i++;
      }


      assert openListLookup.containsKey(best);
      closeList.put(best, openListLookup.get(best));
      openListLookup.remove(best);
      openList.remove(best);
      cur = best;

    }

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

  public void travelUncertain(){

  }

  @Override
  public void travelToDestination(){
    if (this.myWorld.getUncertain()){
      travelUncertain();
    } else {
      travelCertain();
    }
  }


  // ping to determine where the destination is.
  public Point getDest(){
    return myWorld.getEndPos();
  }
  
  
  // if it's not in the closeList, can put on path
  public boolean canPutOnPath(Point p){
    if(!isValid(p)) return false;
    return !this.closeList.containsKey(p);
  }


  // ensures that a point is valid
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

  // adjacentPoints gets a list of points next to the current one
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
  
  // calculates total cost by adding gcost and hcost
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
    // retrieve cost for current node
    int curGCost = this.closeList.get(cur).gCost;
    int toAdd = 1;//diagonal(cur,p)? 14:10;

    // if already seen
    if(this.openListLookup.containsKey(p)){
      // compare new gcost with old, only update if less
      int gCostWithOldParent = this.openListLookup.get(p).gCost;
      if(curGCost+toAdd<gCostWithOldParent){
        this.openListLookup.put(p, new Meta(cur, curGCost+toAdd));
        this.openList.add(p);
      }
      
    } else {
      // if we haven't put this before, set the parent as where we are and the
      // gcost as the current cost plus one.
      this.openListLookup.put(p, new Meta(cur, curGCost+toAdd));
      this.openList.add(p);
    }
  }

  // retrieve the gCost from the openListLookup
  public int gCost(Point p){
    Meta m = this.openListLookup.get(p);
    return m.gCost;
    
  }
  @Override
  public void addToWorld(World world) {
    super.addToWorld(world);
    this.myWorld = world;
    this.worldRep = new String[this.myWorld.numRows()][this.myWorld.numCols()];
  }

  // heuristic between point and destination
  public int hCost(Point possible, Point dest){
    // hcost is initialized to -1. If changed, return what
    return manhattan(possible, dest);
  }

  // used to retrieve heuristic between points
  public int manhattan(Point from, Point dest){
    int m= Math.abs(from.x-dest.x) + Math.abs(from.y-dest.y);
    return m;
  }

  // check if moving to a point requires a diagnol
  public boolean diagonal(Point a, Point b){
    return this.manhattan(a,b) > 1;
  }
  
  public static void main(String args[]) throws java.lang.Exception{
    // MARIO'S
    World myWorld = new World("./hw2/TestCases/myInputFile4.txt", true);
    // HIMANSHU's
    // World myWorld = new World("TestCases/myInputFile3.txt", false);

    myWorld.createGUI(1000,1000,500);
    MyRobotClass myRobot = new MyRobotClass();
    myRobot.addToWorld(myWorld);
    myWorld.getUncertain();

    myRobot.travelToDestination();
    
  }
  
}