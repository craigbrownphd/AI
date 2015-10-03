import world.*;
import java.awt.Point;
public class MyTest extends Robot{
  

  @Override
  public void travelToDestination(){
    super.pingMap(new Point(5,3));
    super.move(new Point(3,7));
  }

  public static void main(String args[]) throws java.lang.Exception{
    World myWorld = new World("./TestCases/myInputFile1.txt", false);
    myWorld.createGUI(100,100,100);
    MyTest myRobot = new MyTest();
    myRobot.addToWorld(myWorld);
    
    
    myRobot.travelToDestination();
    
  }
  
}