package ttr.model.player;

import ttr.model.destinationCards.Destination;
import ttr.model.destinationCards.Route;
import ttr.model.destinationCards.Routes;
import ttr.model.trainCards.TrainCard;
import ttr.model.trainCards.TrainCardColor;
import ttr.view.gameComponents.TrainCardDeckView;

import java.util.ArrayList;
import java.util.SortedMap;
import java.util.TreeMap;

/**
 * A very stupid player that simply draws train cards only. Shown as an example of implemented a player.
 * */
public class StupidPlayer extends Player{


	/**
	 * Need to have this constructor so the player has a name, you can use no parameters and pass the name of your player
	 * to the super constructor, or just take in the name as a parameter. Both options are shown here.
	 * */
	public StupidPlayer(String name) {
		super(name);
	}

	/**
	 * MUST override the makeMove() method and implement it.
	 * */
	@Override
	public void makeMove(){

		int i = (int)(Math.random() * 3);
		if(i==0){
			/* Always draw train cards (0 means we are drawing from the pile, not from the face-up cards) */
			super.drawTrainCard(0);
		} else if(i==1){
			/* This call would allow player to draw destination tickets*/
			super.drawDestinationTickets();
		} else {
			/* Something like this will allow an AI to attempt to buy a route on the board. The first param is the route they wish */
			/* ...to buy, the second param is the card color they wish to pay for the route with (some routes have options here) */
			super.claimRoute(new Route(Destination.Atlanta,  Destination.Miami, 6, TrainCardColor.blue), TrainCardColor.blue);
		}
		/* NOTE: This is just an example, a player cannot actually do all three of these things in one turn. The simulator won't allow it */
	}


    /*
    * CURRENT PLAN (basic):
    * 1) claim route if you can claim a route WITHOUT using locomotive cards
    * 2) if points attained by using locomotive card is > x, then claim route USING locomotive cards
    * 3) if some faceup card allows you to get points, then draw it.
    * 4) now have to pick between drawing 2 dest cards AND drawing 1 train card from facedown deck
    *       if cur_num_dest_cards_that_player_has < 5:
    *           2 dest cards
    *       else:
    *           facedown deck train card
    *
    *
    * THINGS TO DO:
    * 1) we need some way to determine what cities we can link to given the trains that we have placed.
    *       best to use a O(1) time, O(n^2) space matrix
    * 2) we need to store another matrix for ALL cities and ALL possible route patterns.
    *       going to use same data structure as
    * 3) to determine if we can claim route, we see if see
    *       if num trains of proper color needed for route is <= players num trains of proper color
    * 4) how to get all possible routes????
    *       Routes.isValidRoute(route)
    *       Routes.isValidRoute(dest1, dest2, color)
    *       Routes.isRouteClaimed(route)
    *       Routes.claimRoute(route, player)
    *****   Routes.getAllRoutes()
    *       Routes.getRoutes(dest1, dest2)
    *       Routes.getOwner(route)
    *       Routes.ownsRoute(player, route)
    *       Routes.shortestPathcost(dest1, dest2)
    *       Routes.hasCompletedRoute(player, dest1, dest2)
    *       Routes.getNeighbors(dest)
    *       Routes.getNeighborsByClaimedPlayer(player, dest)
    *       Routes.getInstance()
    * 5) how to get all cards that I have
    ****	Player.getNumTrainCardsByColor
    * 		Player.claimRoute
    * 		Player.getNumTrainCardsByColor
    *
    *
    *
    *
    * FOR SECOND TIME: can do same, but via prob.
    * */


	/*
	* Given specific route, do we have enough cards in the correct color for it
	* */
	public boolean canClaimRoute(Route r){
		return this.getNumTrainCardsByColor(r.getColor()) >= r.getCost() && !Routes.getInstance().isRouteClaimed(r);
	}


	/*
	* select a route to claim. Returns the route that we just claimed IF we can.
	* return null if no routes can be claimed
	* */
	public Route selectRouteToClaim() {
		for(Route r: getAvailableRoutes()){
            super.claimRoute(r, r.getColor());
            return r;
		}
		return null;
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


    public TrainCard pickFaceupCard(){
        //quantity for a routes - quantity for in hand
        //color  -> quantity of color that is needed
        SortedMap<TrainCardColor, Integer> quantityWeNeed = new TreeMap<TrainCardColor, Integer>();
        for(Route r: getAvailableRoutes()){
            int possibleNewQuantity = r.getCost() - this.getNumTrainCardsByColor(r.getColor());
            if(quantityWeNeed.containsKey(r.getColor())){
                if(possibleNewQuantity < quantityWeNeed.get(r.getColor())){
                    quantityWeNeed.put(r.getColor(), possibleNewQuantity);
                }
            }else {
                quantityWeNeed.put(r.getColor(), possibleNewQuantity);
            }
        }

        ArrayList<TrainCard> faceUpCards = this.getFaceUpCards();
        for(TrainCardColor k: quantityWeNeed.keySet()){

            for(int i=0; i<faceUpCards.size();i++){
                TrainCard c = faceUpCards.get(i);
                TrainCardColor color = c.getColor();
                if(k == color){
                    super.drawTrainCard(1+i); // ASSUMPTION: 0-deck, 1-first faceup card, 5-5th face up card
                    return c;
                }
            }

        }
        return null;

    }

    //controller that determines which of the 3 moves to make
    //if claim route, use rainbow card or not
    //class for nodes for markov decision chain
    //how to get


}
