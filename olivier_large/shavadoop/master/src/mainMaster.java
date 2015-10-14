import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;


public class mainMaster {
	public static ArrayList<String> ipreachables = new ArrayList<>();
	public static ArrayList<String> ipvalides = new ArrayList<>();
	public static HashMap<Integer, String> dicoUmxMachine = new HashMap<>();
	public static HashMap<String, String> dicoCleUmx = new HashMap<>();
	public static HashMap<String, String> dicoRmxMachine = new HashMap<>();
	/**
	 * @param args
	 */
	public static void main(String[] args) {
        System.out.println("Début du programme local");
        
        
        
        //Récupérer la liste des hotes reachables du 0
        
        int timeout=10;
       // for (int i=1;i<255;i++){
        for (int j=1;j<25;j++){
            String host="137.194" + "." + "35" + "." + j;
            try {
				if (InetAddress.getByName(host).isReachable(timeout)){
				    //System.out.println(host + " is reachable");
				    ipreachables.add(host);
				}
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        }
        //}
        System.out.println(ipreachables.size() + " machines pingables");
        //Récupérer liste des hotes actifs
        for (String ip_test : ipreachables){
	        try{
	        	//System.out.println(ip_test);
	        	String[] commandetest = {"ssh",ip_test, "echo a"};
	            //Process p = Runtime.getRuntime().exec(commandetest);
	        	Process p = new ProcessBuilder(commandetest).start();
	            AfficheurFlux fluxSortie = new AfficheurFlux(p.getInputStream());
	            AfficheurFlux fluxErreur = new AfficheurFlux(p.getErrorStream());
	            
	            new Thread(fluxSortie).start();
	            new Thread(fluxErreur).start();
	            p.waitFor();
	            
	            //System.out.println();
	            if(fluxSortie.getLignefin().equals("a")){
	            	ipvalides.add(ip_test);
	            }
	           
	            //System.out.println(fluxSortie);
	        } catch (IOException e) {
	            e.printStackTrace();
	        } catch (InterruptedException e) {
	            e.printStackTrace();
	        }
	        
        }
        System.out.println(ipvalides.size() + " machines disponibles");
        //Input fichier
       ByteArrayOutputStream baos = new ByteArrayOutputStream();
       System.setOut(new PrintStream(baos));
        map("/cal/homes/olarge/fichiertestMR");
        try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out)));
        for(String line : baos.toString().split("\n")){
        	String valDicoCleUmx = line.split(" ")[0];
        	
        	System.out.println();
        }
        //System.out.println(baos.toString());
        //Separe en fonction des lignes
        
        //Envoie chaque ligne dans chaque mapper
        
        
        
        System.out.println("Fin du programme local");
    }
	
	
	
    private static BufferedReader getBufferedReader(InputStream is) {
        return new BufferedReader(new InputStreamReader(is));
    }



	public static int map(String fileName) {
	    try {
	        Scanner e = new Scanner(new FileReader(fileName));
	        String ligne = null;
	        int cnt_ipvalide = 0;
	        int lineNumber = 1;
	        //For each line in file, we launch a command on a machine. 
	        while(e.hasNextLine()) {
	            ligne = e.nextLine();
	            try {
	                String[] commande = {"ssh",ipvalides.get(cnt_ipvalide), "java -jar Exec.jar \"" + ligne + "\""};
	                //Process p = Runtime.getRuntime().exec(commande);
	                Process p = new ProcessBuilder(commande).start();
	                AfficheurFlux fluxSortie = new AfficheurFlux(p.getInputStream());
	                AfficheurFlux fluxErreur = new AfficheurFlux(p.getErrorStream());

	                new Thread(fluxSortie).start();
	                new Thread(fluxErreur).start();

	                p.waitFor();
	                System.out.println(fluxSortie.getLignefin());
	            } catch (IOException e1) {
	                e1.printStackTrace();
	            } catch (InterruptedException e1) {
	                e1.printStackTrace();
	            }
	            //we add the line to our dicoUmxMachine where key is the number of line 
	            dicoUmxMachine.put(lineNumber, ipvalides.get(cnt_ipvalide));
	            cnt_ipvalide++;
	            lineNumber++;
	            //if there is no machine anymore, we send another command to the firsts machine.
	            if(cnt_ipvalide>=ipvalides.size()){
	            	cnt_ipvalide=0;
	            }
	        }

	    } catch (Exception a) {
	        a.printStackTrace();
	    }

	    return 1;
	}
}

