package ttr.model.player;

import ttr.model.destinationCards.Destination;
import ttr.model.destinationCards.DestinationTicket;
import ttr.model.destinationCards.Route;
import ttr.model.destinationCards.Routes;
import ttr.model.trainCards.TrainCard;
import ttr.model.trainCards.TrainCardColor;

import java.util.*;

/**
 * Created by mario on 10/30/15.
 */
public class NamelessPlayer extends Player {

    public NamelessPlayer(String name){
        super(name);
    }

    public boolean canClaimRoute(Route r){
        if (r.getColor()==TrainCardColor.rainbow) {
            for (TrainCardColor c : TrainCardColor.values()) {
                if (this.getNumTrainCardsByColor(c)>r.getCost() && !Routes.getInstance().isRouteClaimed(r))
                    return true;
            }
        }
        return (this.getNumTrainCardsByColor(r.getColor()) >= r.getCost()
                || this.getNumTrainCardsByColor(TrainCardColor.rainbow)>=r.getCost())
                && !Routes.getInstance().isRouteClaimed(r);
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

    public ArrayList<Route> getAvailableThresholdRoutes(){
        ArrayList<Route> out = new ArrayList<Route>();
        for(Route r : Routes.getInstance().getAllRoutes()){
            if(r.getCost()>=2.5*Math.log(this.getNumTrainPieces())-5.0 && this.canClaimRoute(r)){
                out.add(r);
            }
        }
        return out;

    }

    public ArrayList<Route> getOponentsRoutes(){
        ArrayList<Route> out = new ArrayList<Route>();
        for(Route r : Routes.getInstance().getAllRoutes()){
            if(r.getOwner()!=this && r.getOwner()!=null){
                out.add(r);
            }
        }
        return out;
    }

    public ArrayList<Route> getOponentsClaimableRoutes(){
        ArrayList<Route> out = new ArrayList<Route>();
        for(Route r : Routes.getInstance().getAllRoutes()){
            if(r.getOwner()!=this && r.getOwner()!=null && this.canClaimRoute(r)){
                out.add(r);
            }
        }
        return out;
    }

    public int pickFaceupCard(){
        //quantity for a routes - quantity for in hand
        //color -> quantity of color that is needed
        SortedMap<TrainCardColor, Integer> quantityWeNeed = new TreeMap<TrainCardColor, Integer>();
        for(Route r: getAvailableThresholdRoutes()){
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
                if(color == TrainCardColor.rainbow||k == color){
                    return i+1;
                }
            }
        }
        return 0;
    }

    public void makeMove (){
        ArrayList<DestinationTicket> destTickets= this.getDestinationTickets();
        boolean allClaimed = false;
        for (DestinationTicket d: destTickets){
            allClaimed = Routes.getInstance().hasCompletedRoute(this, d.getFrom(), d.getTo());
        }
        if (allClaimed && this.getNumTrainPieces()>20){
            this.drawDestinationTickets();
        }
        ArrayList<Route> available = this.getAvailableThresholdRoutes();
        if (available.size()>0) {
            Collections.shuffle(available);
            Route max = available.get(0);
            for (Route r : available) {
                if (r.getCost() > max.getCost())
                    max = r;
            }

            this.claimRoute(max, max.getColor());

        }
        this.drawTrainCard(this.pickFaceupCard());
    }

    public int findCostOfPath(ArrayList<Route> path){
        int cost = 0;
        for(Route r: path){
            assert Routes.getInstance().getOwner(r) == null ||  Routes.getInstance().getOwner(r) == this;
            //if you dont own it, then add to cost
            if(Routes.getInstance().getOwner(r) == null){
                cost += r.getCost();
            }
        }
        return cost;
    }
    public boolean routeClaimedByOther(Route r){
        Player owner = Routes.getInstance().getOwner(r);
        return owner != null && owner != this;
    }

    public ArrayList<ArrayList<Route>> getShortestPaths(Destination from, Destination to){
        // list from from to dest via all routes
        // no path in between is claimed by opponent
        // all colors

        ArrayList<Route> curpath = new ArrayList<Route>();
        ArrayList<ArrayList<Route>> minpaths = new ArrayList<ArrayList<Route>>();
        dfs(from, to, curpath, minpaths);
        for(ArrayList<Route> path: minpaths){
            System.out.println(path);
            System.out.println(findCostOfPath(path));
        }
        return minpaths;
    }

    /**
     *
     * @param from
     * @param to
     * @param curpath
     * @param minpaths: list of minimum paths from 'from' to 'to'
     */
    public void dfs(Destination from, Destination to, ArrayList<Route> curpath, ArrayList<ArrayList<Route>> minpaths){
        // list from from to dest via all routes
        // no path in between is claimed by opponent
        // all colors

//        System.out.println(curpath.toString() + from.toString() +"->"+ to.toString());

        if(from  == to){
            ArrayList completeCurPath = new ArrayList<Route>();
            completeCurPath.addAll(curpath);

            //find cost of curpath
            int curCost = findCostOfPath(completeCurPath);

            if(minpaths.size() ==0 ) {
                System.out.println("minpaths was empty, adding path of cost " +curCost + "to it");
                minpaths.add(completeCurPath);
            } else {
                int previousMinCost = findCostOfPath(minpaths.get(0));
                if(curCost < previousMinCost){
                    System.out.println("replace "+previousMinCost + " with " + curCost);
                    minpaths.clear();
                    minpaths.add(completeCurPath);
                    System.out.println("and the replaced thing is "+completeCurPath);
                } else if (curCost == previousMinCost){
                    System.out.println("adding to cost " + curCost);
                    minpaths.add(completeCurPath);
                } //else if curCost>previousMinCost then ignore curpath
            }

            return;
        }


        if( curpath.size()  >= 4 ) return;


        //get all routes from cur to adjacent cities
        ArrayList<Route> adjRoutes = new ArrayList<Route>();
        for(Destination adj: Routes.getInstance().getNeighbors(from)){
            adjRoutes.addAll(Routes.getInstance().getRoutes(from, adj));
        }


        //for all routes to adjacent cities
        for(Route r: adjRoutes){
            if(!curpath.contains(r) && !routeClaimedByOther(r)){
                curpath.add(r);


                Destination adjCity = r.getDest1() == from ? r.getDest2() : r.getDest1();

                dfs(adjCity, to, curpath, minpaths);
                curpath.remove(r);

            }
        }

    }

}
