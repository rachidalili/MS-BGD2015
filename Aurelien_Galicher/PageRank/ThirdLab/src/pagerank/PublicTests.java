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
 * Any changes to this file will be ignored when testing your project on the submission server.
 * 
 */
public class PublicTests extends BaseTests {
	static Configuration conf;
	static {  
		conf = new Configuration();
		//MatrixVectorMultiplication
		conf.set("graphPath", "data/graph");
		conf.set("graphNoDeadendsPath", "data/graphNoDeadends");
		conf.set("processedGraphPath", "data/processedGraph");
		conf.set("initialVectorPath", "data/initialRankVector");
		conf.set("currentVectorPath", "data/currentRankVector");
		conf.set("stochasticMatrixPath", "data/stochasticMatrix");
		conf.set("finalVectorPath", "data/finalRankVector");
		conf.set("intermediaryResultPath", "data/intermediaryDirectory");
		conf.set("inputMatrixPath", "data/stochasticMatrix");
		
		
	}
	
	public void testFinalVector() {
		try {
		
		conf.setDouble("epsilon", 0.1);
		conf.setDouble("beta", 0.8);
		FileUtils.deleteQuietly(new File(conf.get("intermediaryResultPath")));
		FileUtils.deleteQuietly(new File(conf.get("finalVectorPath")));
		FileUtils.deleteQuietly(new File(conf.get("processedGraphPath")));

		FileUtils.deleteQuietly(new File(conf.get("stochasticMatrixPath")));
		
		//needed for when we exclude remove deadends from the pagerank algorithm
		FileUtils.copyDirectory(new File(conf.get("graphNoDeadendsPath")), new File(conf.get("processedGraphPath")));
		conf.setLong("numNodes", 7);
		
		PageRank.iterativePageRank(conf);
		File directory = new File(conf.get("finalVectorPath"));
		if(!directory.exists())
			fail("Output directory doesn't exist");
		
		File[] contents = directory.listFiles();
		File outputFile = null;
	
		for (int i = 0; i < contents.length; ++i)
			if (!contents[i].getName().equals("_SUCCESS")
					&& !contents[i].getName().startsWith("."))
				outputFile = contents[i].getAbsoluteFile();
	
		if (outputFile == null)
			fail("Output file doesn't exist");
	
		BufferedReader r;
		
		r = new BufferedReader(new FileReader(outputFile));
		
		double sum = 0.;
		double value = 0.;
		String line;
		while ((line = r.readLine()) != null) {
			String[] parts = line.split("\\s+");
			if(Integer.valueOf(parts[0]) == 2)
				value = Double.valueOf(parts[1]);
			sum += Double.valueOf(parts[1]);
		}
	
		r.close();
		assertEquals("Node 2 has not the right rank.", 0.091, value, 0.01);
		assertEquals("The sum of ranks does not equal 1.", 1.0, sum, 0.01);
	
		} catch (IOException | ClassNotFoundException | InterruptedException e) {
			System.out.println(e.toString());
			fail(e.toString());
		}
	}
	public void testRemoveDeadendsJob(){
	try {
		FileUtils.deleteQuietly(new File(conf.get("intermediaryResultPath")));
		FileUtils.deleteQuietly(new File(conf.get("finalVectorPath")));
		FileUtils.deleteQuietly(new File(conf.get("processedGraphPath")));
		
		FileUtils.copyDirectory(new File(conf.get("graphPath")), new File(conf.get("processedGraphPath")));
		
		conf.setLong("numNodes", 9);
		RemoveDeadends.job(conf);

		File directory = new File(conf.get("processedGraphPath"));
		if(!directory.exists())
			fail("Output directory processedGraphPath doesn't exist");
		
		File[] contents = directory.listFiles();
		File outputFile = null;
	
		for (int i = 0; i < contents.length; ++i)
			if (!contents[i].getName().equals("_SUCCESS")
					&& !contents[i].getName().startsWith("."))
				outputFile = contents[i].getAbsoluteFile();
	
		if (outputFile == null)
			fail("Output file doesn't exist");
	
		BufferedReader r = new BufferedReader(new FileReader(outputFile));
		int noLines = 0;
		String line;
		while ((line = r.readLine()) != null) {
			String[] parts = line.split("\\s+");
			noLines ++;
			if(Integer.valueOf(parts[0]) == 7 && Integer.valueOf(parts[1]) == 8)
				fail("Deadend was not removed.");
		}
	
		r.close();
		assertEquals("The number of edges outputed is not correct.", 9, noLines);
		assertEquals("The value of numNodes in conf was not updated.",7, conf.getLong("numNodes", 0));
		
	} catch (IOException | ClassNotFoundException | InterruptedException e) {
		System.out.println(e.toString());
		fail(e.toString());
	}
	}
}

