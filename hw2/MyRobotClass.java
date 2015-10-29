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
    public Meta(Point parent, int gCost){
      this.parent=parent;
      this.gCost=gCost;
      this.hCost=-1;
    }
  }

  private World myWorld;


  /*
  "" -> havent seen yet
  "X" -> fire
  "O" -> open
  "x" -> maybe fire
  "o" -> maybe open
   */
  private String[][] worldRepresentation;

  // things we have seen but haven't stepped on
  HashMap<Point, Meta> openListLookup = new HashMap<Point, Meta>();
  HashSet<Point> openList = new HashSet<Point>();

  // things we've stepped on
  HashMap<Point, Meta> closeList = new HashMap<Point, Meta>();
  Point dest;
  ArrayList<Point> globalPath = new ArrayList<Point>();

  // can return either X or O or F or null
  // world representation will also include x or o to represent uncertainty
  public String pingMap(Point p){
    if (dest != null && p.x==dest.x && p.y==dest.y)
      return "F";
    String pointVal=null;
    if(pointInMap(p)){
      pointVal = worldRepresentation[p.x][p.y];
      if (pointVal != null) {
        return pointVal.toUpperCase();
      }
      worldRepresentation[p.x][p.y] = super.pingMap(p);
      pointVal= worldRepresentation[p.x][p.y];

//            super.makeGuess(p, pointVal.toUpperCase().equals("O"));
      updateMapView(p);

    }
    return pointVal;
  }

  public String guessVal (Point cur, Point p){
    int []numPings = {2,4};
    int distance = Math.max(Math.abs(cur.x-p.x), Math.abs(cur.y-p.y));
    HashMap<String, Integer> possible = new HashMap<String, Integer>();
    for (int i= 0; i<numPings[distance-1]; i++){
      String val = super.pingMap(p);
      if (possible.containsKey(val)) {
        possible.put(val, possible.get(val) + 1);
      }
      else {
        possible.put(val, 1);
      }
    }
    int max = Integer.MIN_VALUE;
    String maxString = "";
    for (String k: possible.keySet()) {
      if (possible.get(k)==max){
        return super.pingMap(p);
      }
      if (possible.get(k) > max) {
        maxString = k;
        max = possible.get(k);
      }
    }
    return maxString.toLowerCase();
  }

  public String pingMap(Point cur, Point p) {
    if (dest != null && p.x==dest.x && p.y==dest.y)
      return "F";
    String pointVal = null;
    if (pointInMap(p)){
      pointVal = worldRepresentation[p.x][p.y];
      if (pointVal != null) {
        return pointVal.toUpperCase();
      }
      worldRepresentation[p.x][p.y] =guessVal(cur, p);
      pointVal= worldRepresentation[p.x][p.y];
    }
    if (pointVal==null) {
      return pointVal;
    }
//        super.makeGuess(p, pointVal.toUpperCase().equals("O"));
    updateMapView(p);
    return pointVal.toUpperCase();
  }

  public void updateMapView(Point p){

    String val = worldRepresentation[p.x][p.y];

    if(val==null){
      return;
    }
    if(val.equals("o")) {
//            super.makeGuess(p, true);

    }
    if(val.equals("x")){
//            super.makeGuess(p, false);

    }




  }

  public boolean travelLocal(Point beginning, Point localDest) {
    openListLookup = new HashMap<Point, Meta>();
    openList = new HashSet<Point>();
    closeList = new HashMap<Point, Meta>();


    assert beginning.x==this.getPosition().x && beginning.y == this.getPosition().y;
    Point cur = beginning;
    // since we start here, put to start
    closeList.put(beginning, new Meta(null, 0));


    // while we haven't made it to the endgoal
    while(!cur.equals(localDest)) {
      if (!closeList.containsKey(cur)) {
        System.out.println("close list error");
        return false;
      }


      for (Point p : this.adjacentPoints(cur)) {
        //put into list OR update it if it should be updated
        this.updateGCost(cur, p);
      }


      // the best point to move to next will have the best fcost


      if(openList.size()==0) {

        System.out.printf("open list error: %s -> %s\n", beginning.toString(), localDest.toString());
        return false;
      }
      if (openListLookup.size() == 0) {
        System.out.println("openListLookup error");
        return false;
      }

      Point best = (Point) openList.toArray()[0];
      for (Point p : openList) {
        Meta pMeta = openListLookup.get(p);
        Meta bestMeta = openListLookup.get(best);
        pMeta.hCost = hCost(p, localDest);
        bestMeta.hCost = hCost(best, localDest);
        if (pMeta.gCost + pMeta.hCost < bestMeta.gCost + bestMeta.hCost) {
          if (!globalPath.contains(p))
            best = p;
        }
      }


      if (!openListLookup.containsKey(best)) {
        System.out.println("openListLookup contains error");
        return false;
      }

      closeList.put(best, openListLookup.get(best));
      openListLookup.remove(best);
      openList.remove(best);
      cur = best;
    }

    ArrayList<Point> path = new ArrayList<Point>();
    // cur is at dest at this point in code
    while(cur != beginning){
      path.add(0,cur);
      cur = this.closeList.get(cur).parent;
    }

    if(path.size()==0) return false;

    for(Point p : path){
      cur = this.move(p);
      globalPath.add(cur);
    }
    return true;
  }

  public Point move(Point p){
    Point ret = super.move(p);
    if(ret.x==p.x && ret.y==p.y){
      worldRepresentation[p.x][p.y] = "O";
    } else{
      worldRepresentation[p.x][p.y] = "X";
    }
    return ret;
  }

  public boolean travelCertain(Point dest) {
    return travelLocal(this.getPosition(), dest);
  }

  public void travelUncertain(){


    dest = this.getDest();


    ArrayList<Point> path = new ArrayList<Point>();
    HashSet<Point> seenPoints = new HashSet<Point>();

    //while robot not at dest:
    while(this.getPosition().x!=dest.x || this.getPosition().y!=dest.y) {


      path.add(this.getPosition());

      //ping spots two levels out to get their spots. store spots.
      pingSurroundings(this.getPosition(), 2);


      //using manhattan, find known spot closest to dest (MUST use our stored spots)
      //loop through all spots and have temp MIN and change it each time a manhattan(i)<manhattan(min)
      Point minPoint = new Point(200, 200);
      ArrayList<Point> feasible = new ArrayList<Point>();
      for (int i = 0; i < worldRepresentation.length; i++) {
        for (int j = 0; j < worldRepresentation[i].length; j++) {
          Point temp = new Point(i, j);
          if (worldRepresentation[i][j]!=null) {
            if (worldRepresentation[i][j].toUpperCase().equals("O") || worldRepresentation[i][j].toUpperCase().equals("F") ) {
              seenPoints.add(temp);
              feasible.add(temp);
            }
          }
        }
      }

      //before other checks, check to see if can go to final dest.
      this.travelLocal(this.getPosition(), this.getDest());


      while(feasible.size()>0){
        Point pointToCheck = getClosestPoint(feasible);
        //find best path to known spot using A*
        //if path exists: actualy move robot along path
        if (this.travelLocal(this.getPosition(), pointToCheck)) {
          if (globalPath.subList(0, globalPath.size()-2>=0?globalPath.size()-2:0).contains(pointToCheck)) {
            while (globalPath.size()!=0){
              Point lastVisited = globalPath.remove(globalPath.size() - 1);
              this.move(lastVisited);
              List<Point> adj= allAdjacent(this.getPosition());
              adj.remove(lastVisited);
              if (adj.size()==1){
                worldRepresentation[lastVisited.x][lastVisited.y]="X";
              }
              this.travelLocal(this.getPosition(), this.getDest());
            }
          }
          break;
        }
      }
      assert feasible.size() != 0;

    }
  }
  public Point getClosestPoint(ArrayList<Point> feasible){
    //run through, get min, remove min, return min
    //what if f
    Point min = feasible.get(0);
    for(Point p:feasible){
      if (manhattan(p, this.getDest()) < manhattan(min, this.getDest())) {
        if (!globalPath.contains(p))
          min = p;
      }
    }
    feasible.remove(min);
    return min;
  }

  public Point generateRandomNeighboringPoint(Point cur){
    List <Point> l = allAdjacent(cur);
    return l.get((int)((l.size()-1)*Math.random()));

  }
//
//  public boolean isSeeminglyOpen(Point p){
//    if(!pointInMap(p)) return false;
//    return worldRepresentation[p.x][p.y].equals("O") || worldRepresentation[p.x][p.y].equals("o");
//  }

  public void pingSurroundings(Point cur, int numLevels){
    //create special ping method that returns ping value if uncertain or actual value without pinging if certain

    //override special ping to have param that checks x num times and returns majority of them
    //O for openSURE, X for closeSURE, o for openMAYBE, x for closeMAYBE else unknown


    Point base = new Point(cur.x-numLevels, cur.y-numLevels);
    for (int i = 0; i<=numLevels*2; i++) {
      for (int j = 0; j <= numLevels * 2; j++) {
        Point temp =new Point (base.x+i, base.y+j);
        if (cur.x!=temp.x || cur.y != temp.y)
          pingMap(cur, temp);
      }
    }
  }


  public boolean pointInMap(Point p){
    return p.x >= 0 &&
            p.x < this.worldRepresentation.length &&
            p.y >= 0 &&
            p.y < this.worldRepresentation[0].length;
  }

  @Override
  public void travelToDestination(){
    if (this.myWorld.getUncertain()){
      travelUncertain();
    } else {

      if(!travelCertain(this.getDest())) System.out.println("ERROR");
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
  // TODO: Himanshu wishes to speak of this
  public boolean isValid(Point p){
    if(p==null) return false;
    if(!pointInMap(p)) return false;


    try{
      String val = "";
      if (myWorld.getUncertain()) {
        val = worldRepresentation[p.x][p.y].toUpperCase();
      } else {
        val = this.pingMap(p);
      }
      return val.equals("O") || val.equals("F");

    } catch (NullPointerException e){
      return false;
    }

  }


  public List<Point> allAdjacent(Point cur){
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

      String pingedVal = this.pingMap(p);

      if (pingedVal!=null && (pingedVal.equals("O")||pingedVal.equals("F"))) {
        out.add(p);
      }
    }
    return out;
  }
  // adjacentPoints gets a list of points next to the current one
  public List<Point> adjacentPoints(Point cur){
    assert this.closeList.containsKey(cur);
    assert cur.x == this.getPosition().x && cur.y == this.getPosition().y;
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
      if(p.equals(dest)){
        out = new ArrayList<Point>();
        out.add(p);
        return out;
      }
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
    this.worldRepresentation = new String[this.myWorld.numRows()][this.myWorld.numCols()];
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
        World myWorld = new World("TestCases/myInputFile1.txt", false);
    // HIMANSHU's
//    World myWorld = new World("TestCases/myInputFile4.txt", true);

    myWorld.createGUI(700,700,100);
    MyRobotClass myRobot = new MyRobotClass();
    myRobot.addToWorld(myWorld);
//        myWorld.getUncertain();

    myRobot.travelToDestination();

  }

}

//INSIGHTS:
//4)robot guesses wrong
//we thought open, but it is closed. ->  reevalute. DONE
//we thought closed, but it is open. ->
//6)we will change it so that we try next best point, and then next best after that...
//seenpoints is doing nothing