package ttr.model.player;

import ttr.model.destinationCards.DestinationTicket;
import ttr.model.destinationCards.Route;
import ttr.model.destinationCards.Routes;
import ttr.model.trainCards.TrainCard;
import ttr.model.trainCards.TrainCardColor;
import java.util.*;

/**
 * A very stupid player that simply draws train cards only. Shown as an example of implemented a player.
 * */

class DummyPlayer {

    public DummyPlayer(){

    }

    public DummyPlayer(StupidPlayer p, String name, ArrayList<TrainCard> list) {
        hand = p.getHand();
        points = p.getPoints();
        tickets = p.getDestinationTickets();
        numTrainPieces = p.getNumTrainPieces();
        claimedRoutes = p.getPlayerClaimedRoutes();
        faceUp=list;
    }

    public void addCard(TrainCard t){
        hand.add(t);
        faceUp.remove(t);
    }

    public void claimRoute(Route r){
        claimedRoutes.add(r);
        points+=r.getPoints();
        numTrainPieces-=r.getCost();

    }

    ArrayList <TrainCard> faceUp;


    ArrayList<TrainCard> hand = new ArrayList<TrainCard>();
    /* The hand of cards the player has */

    /* The destination tickets this player currently holds, and another list for the completed tickets */
    ArrayList<DestinationTicket> tickets;
    ArrayList<DestinationTicket> completed;

    int points = 0;

    /* Number of total train pieces the player has left, starting with 45 */
    int numTrainPieces = 45;

    /* All of the routes this player has claimed */
    ArrayList<Route> claimedRoutes;

    public ArrayList<Route> getAvailableRoutes(){
        ArrayList<Route> availableRoutes = Routes.getInstance().getAllRoutes();
        ArrayList<Route> out = new ArrayList<Route>();
        for(Route r : claimedRoutes){
            availableRoutes.remove(r);
        }
        return availableRoutes;
    }

    public boolean canClaimRoute(Route r){
        return this.getNumTrainCardsByColor(r.getColor()) >= r.getCost() && !Routes.getInstance().isRouteClaimed(r);
    }

    public int getNumTrainCardsByColor(TrainCardColor color){
        int count = 0;
        for(TrainCard card : this.hand){
            if(card.getColor() == color) count++;
        }
        return count;
    }
}

class State {
    DummyPlayer us;
    DummyPlayer them;

    public State (DummyPlayer us, DummyPlayer them) {
        this.us = us;
        this.them = them;
    }
}

class StateNode {
    boolean min = false;
    int value;
    State state;
    ArrayList<StateNode> children;

    public StateNode (StateNode stateNode){
        this.state = stateNode.state;
    }

    public StateNode (State st) {
        this.state = st;
    }

    public void setState (State st){
        this.state = st;
    }

    public static ArrayList<StateNode> generateChildNodes(StateNode currentNode) {

        if (currentNode.state.us.numTrainPieces<=3)
            return new ArrayList<StateNode>();

        ArrayList<StateNode> children = new ArrayList<StateNode>();
        ArrayList<TrainCard> faceUp= (ArrayList<TrainCard>)currentNode.state.us.faceUp.clone();
        for (TrainCard t: faceUp) {
            StateNode newNode = new StateNode(currentNode);
            newNode.state.us.addCard(t);
            newNode.min = !currentNode.min;
            children.add(newNode);
        }

        for (Route r: currentNode.state.us.getAvailableRoutes()){
            StateNode newNode = new StateNode(currentNode);
            newNode.state.us.claimRoute(r);
            newNode.min = !currentNode.min;
            children.add(newNode);
        }


        return children;
    }

}

public class StupidPlayer extends Player{



	/**
	 * Need to have this constructor so the player has a name, you can use no parameters and pass the name of your player
	 * to the super constructor, or just take in the name as a parameter. Both options are shown here.
	 * */
	public StupidPlayer(String name) {
		super(name);
	}

    StateNode initial;
	/**
	 * MUST override the makeMove() method and implement it.
	 * */
	@Override
	public void makeMove(){
        if (initial==null) {
            initial = new StateNode(new State(new DummyPlayer(this, "us", this.getFaceUpCards()), new DummyPlayer()));
            initial.children = StateNode.generateChildNodes(initial);
            for (int i = 0; i<initial.children.size(); i++){
                StateNode c = initial.children.get(i);
                c.children=StateNode.generateChildNodes(c);
                initial.children.set(i,c);
            }

        }
    }

    public ArrayList<Route> getAvailableRoutes(){
        ArrayList<Route> out = new ArrayList<Route>();
        for(Route r : Routes.getInstance().getAllRoutes()){
            if(this.canClaimRoute(r)){
                out.add(r);
            }
        }
        return out;
    }

    public boolean canClaimRoute(Route r){
        return this.getNumTrainCardsByColor(r.getColor()) >= r.getCost() && !Routes.getInstance().isRouteClaimed(r);
    }


}
