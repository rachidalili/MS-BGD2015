package pagerank;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mrunit.mapreduce.MapDriver;
import org.apache.hadoop.mrunit.mapreduce.ReduceDriver;

/**
 * This class contains the public test cases for the project. The public tests
 * are distributed with the project description, and students can run the public
 * tests themselves against their own implementation.
 * 
 * Any changes to this file will be ignored when testing your project.
 * 
 */
public class PublicTests extends BaseTests {
	static Configuration conf;
	// directories for graph to matrix
	static final String graph = "data/graph";
	static final String stochasticMatrix = "data/stochasticMatrix";
	static {

		conf = new Configuration();
		conf.set("processedGraphPath", graph);
		conf.set("stochasticMatrixPath", stochasticMatrix);

	}


	public void testJobConstructionStochasticMatrix(){
		try {

			FileUtils.deleteQuietly(new File(stochasticMatrix));
			GraphToMatrix.job(conf);

			File directory = new File(stochasticMatrix);
			if(!directory.exists())
				fail("Output directory  doesn't exist");

			File[] contents = directory.listFiles();
			File outputFile = null;

			for (int i = 0; i < contents.length; ++i)
				if (!contents[i].getName().equals("_SUCCESS")
						&& !contents[i].getName().startsWith("."))
					outputFile = contents[i].getAbsoluteFile();

			if (outputFile == null)
				fail("Output file  doesn't exist");

			HashMap<Integer, Double> sumColumns = new HashMap<Integer, Double>();
			BufferedReader r = new BufferedReader(new FileReader(outputFile));

			String line;
			while ((line = r.readLine()) != null) {
				String[] parts = line.split("\\s+");
				if(parts.length < 3)
					continue;

				if(sumColumns.get(Integer.valueOf(parts[1])) == null)
					sumColumns.put(Integer.valueOf(parts[1]), Double.valueOf((parts[2])));
				else
					sumColumns.put(Integer.valueOf(parts[1]), sumColumns.get(Integer.valueOf(parts[1])) + Double.valueOf(parts[2]));
			}

			r.close();
			if(sumColumns.isEmpty())
				fail("no output");
			for(int k:sumColumns.keySet())
				if(Math.abs(sumColumns.get(k) - 1) > 0.001)
					fail("Output matrix is not correct. Please read again the exercise.");

		} catch (IOException | ClassNotFoundException | InterruptedException e) {
			System.out.println(e.toString());
			fail(e.toString());
		}
	}
}

