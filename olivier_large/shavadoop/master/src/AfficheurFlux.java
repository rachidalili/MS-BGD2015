import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class AfficheurFlux implements Runnable {

	public static String lignefin;
    public static String getLignefin() {
		return lignefin;
	}

	public final InputStream inputStream;
    AfficheurFlux(InputStream inputStream) {
        this.inputStream = inputStream;
    }

    public BufferedReader getBufferedReader(InputStream is) {
        return new BufferedReader(new InputStreamReader(is));
    }

    @Override
    public void run() {
        BufferedReader br = getBufferedReader(inputStream);
        String ligne = "";
        try {
            while ((ligne = br.readLine()) != null) {
                //System.out.println(ligne);
                lignefin = ligne;
                
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
}