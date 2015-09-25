import world.*;

public class MyRobotClass extends Robot{
  
  @Override
  public void travelToDestination(){
//    super.pingMap(new Point(5,3));
//    super.move(new Point(3,7));
  }

  public static void main(String args[]) throws java.lang.Exception{
    World myWorld = new World("myInputFile.txt", false);
    myWorld.createGUI(1,2,3);
    MyRobotClass myRobot = new MyRobotClass();
    myRobot.addToWorld(myWorld);
    
    
    myRobot.travelToDestination();
    
  }
  
}