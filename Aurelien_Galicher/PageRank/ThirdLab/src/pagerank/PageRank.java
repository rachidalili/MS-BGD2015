package pagerank;

import java.io.BufferedReader;
import java.io.File;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;

/*
 * VERY IMPORTANT 
 * 
 * Each time you need to read/write a file, retrieve the directory path with conf.get 
 * The paths will change during the release tests, so be very carefully, never write the actual path "data/..." 
 * CORRECT:
 * String initialVector = conf.get("initialRankVectorPath");
 * BufferedWriter output = new BufferedWriter(new FileWriter(initialVector + "/vector.txt"));
 * 
 * WRONG
 * BufferedWriter output = new BufferedWriter(new FileWriter(data/initialVector/vector.txt"));
 */

public class PageRank {
	
	public static void createInitialRankVector(String directoryPath, long n) throws IOException 
	{

		File dir = new File(directoryPath);
		if(! dir.exists())
			FileUtils.forceMkdir(dir);
		
		
		BufferedWriter output = new BufferedWriter(new FileWriter(dir + "/vector.txt"));
		for (int i=1; i <= n; i++){
			output.write(i+"\t"+1.0/n);
			output.newLine();
		}
		output.close();
		System.out.println("creating "+ dir +"/vector.txt "+" of size: "+n);
		//TO DO
		
	}
	
	public static boolean checkConvergence(String initialDirPath, String iterationDirPath, double epsilon) throws NumberFormatException, IOException
	{
		
		BufferedReader initbw = new BufferedReader(new FileReader(initialDirPath+"/vector.txt"));
		BufferedReader iterbw = new BufferedReader(new FileReader(iterationDirPath+"/part-r-00000"));
		
		String lineInit = null;
		String lineIter = null;
		Double result = new Double(0);
		while ( (lineInit = initbw.readLine()) != null){
			lineIter = iterbw.readLine();
			result+= Math.abs(Double.parseDouble(lineInit.split("\\s+")[1])-Double.parseDouble(lineIter.split("\\s+")[1]));
		}
		initbw.close();
		iterbw.close();
		
		System.out.println("checking convergence "+ initialDirPath + " " + iterationDirPath );
		System.out.println("epsilon "+ epsilon + " normL1 " + result);
		if (result < epsilon){
			return false;
		}
		return true;
		
	}
	
	public static void avoidSpiderTraps(String vectorDirPath, long nNodes, double beta) throws IOException 
	{
		
		File dir = new File(vectorDirPath);
		
		System.out.println("avoid SpiderTraps "+ vectorDirPath );
				
		BufferedWriter output = new BufferedWriter(new FileWriter(dir+ "/vector_nospider.txt"));
		BufferedReader input = new BufferedReader(new FileReader(dir + "/part-r-00000"));
		for (int i=1; i<= nNodes; i++){
			double value = Double.parseDouble(input.readLine().split("\\s+")[1]);
			output.write(i+"\t"+new Double(beta*value+(1.0-beta)/nNodes).toString());
			output.newLine();
		}
		output.close();
		input.close();
		System.out.println("end of reading: "+ vectorDirPath);
		
		FileUtils.deleteQuietly(new File(dir + "/part-r-00000"));
		System.out.println("deleted  "+ dir + "/part-r-00000");
		FileUtils.moveFile(new File(dir + "/vector_nospider.txt"), new File(dir + "/part-r-00000"));
		System.out.println("moving  "+ dir + "/part-r-00000" );
		FileUtils.deleteQuietly(new File(dir+ "/vector_nospider.txt"));
		System.out.println("deleted  "+ dir + "/vector_nospider.txt");				
	}
	
	public static void iterativePageRank(Configuration conf) 
			throws IOException, InterruptedException, ClassNotFoundException
	{
		
		
		String initialVector = conf.get("initialVectorPath");
		String currentVector = conf.get("currentVectorPath");
		
		String finalVector = conf.get("finalVectorPath"); 
		/*here the testing system will search for the final rank vector*/
		
		Double epsilon = conf.getDouble("epsilon", 0.1);
		Double beta = conf.getDouble("beta", 0.8);

 
		//TO DO
		RemoveDeadends.job(conf);
		GraphToMatrix.job(conf);
		// to retrieve the number of nodes use long nNodes = conf.getLong("numNodes", 0); 
		long nNodes = conf.getLong("numNodes", 0);
		createInitialRankVector(initialVector, nNodes);
		
		File currentVectorfile = new File(currentVector);
		if (currentVectorfile.exists()){
			FileUtils.deleteDirectory(currentVectorfile);
		}
		
		
		boolean ExitCondition = true ;
		while (ExitCondition){
			System.out.println("applying MatrixVectorMult");
			MatrixVectorMult.job(conf);
			System.out.println("avoid SpiderTrap");
			avoidSpiderTraps(currentVector, nNodes, beta);
			ExitCondition = checkConvergence(initialVector, currentVector, epsilon);
			
			FileUtils.deleteQuietly(new File(initialVector + "/vector.txt"));
			FileUtils.moveFile(new File(currentVector+"/part-r-00000"), new File(initialVector+"/vector.txt"));
			FileUtils.deleteDirectory(new File(currentVector));
			//System.out.println("deleted directory "+ currentVector);	
		}
		// finally manage finalVector
		//System.out.println("moving "+ initialVector+"/vector.txt" + " to "+ finalVector+"/vector.txt");	
		FileUtils.moveFile(new File(initialVector+"/vector.txt"), new File(finalVector+"/vector.txt"));
		
		// when you finished implementing delete this line
		//throw new UnsupportedOperationException("Implementation missing");
		
	}
}
