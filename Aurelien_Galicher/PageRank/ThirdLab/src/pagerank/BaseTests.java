package pagerank;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Locale;




import junit.framework.TestCase;

public abstract class BaseTests extends TestCase {
	protected static String initializationError = null;
	protected static HashMap<Integer, Double> outputVector = null;

	static {
			Locale.setDefault(new Locale("en", "US"));
			
	}
	
	protected static HashMap<Integer, Double> readOutputVector(String output) throws IOException {
		File directory = new File(output);
		File[] contents = directory.listFiles();
		File outputFile = null;
	
		for (int i = 0; i < contents.length; ++i)
			if (!contents[i].getName().equals("_SUCCESS")
					&& !contents[i].getName().startsWith("."))
				outputFile = contents[i].getAbsoluteFile();
	
		if (outputFile == null)
			return null;
	
		HashMap<Integer, Double> outputVector = new HashMap<Integer, Double>();
	
		BufferedReader r = new BufferedReader(new FileReader(outputFile));
	
		String line;
		while ((line = r.readLine()) != null) {
			String[] parts = line.split("\\s+");
			outputVector.put(Integer.valueOf(parts[0]), Double.valueOf(parts[1]));
		}
	
		r.close();
		
		return outputVector;
	}

	public void testIndexBuiltWithNoError() {
		assertNull(initializationError);
	}
	
}