import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map.Entry;


public class main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String dicosend = "";
		try {
			dicosend = InetAddress.getLocalHost().getHostName();
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		String newline = null;
		HashMap<String, Integer> map = new HashMap<>();
		
       for(int i = 0; i < args.length; i++) {
            newline = args[0];
        }
       /*try {
		Thread.sleep(10000);
	} catch (InterruptedException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}*/
       for(String el : newline.split(" ")){
    	   if(!map.containsKey(el)){
    		   map.put(el, 1);
    		   dicosend += " " + el;
    	   } else{
    		   map.put(el, map.get(el) +1);
    	   }
       }
       System.out.println(dicosend);
       //System.out.println(map);
		
	}

}
