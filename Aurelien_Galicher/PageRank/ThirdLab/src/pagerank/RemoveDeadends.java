package pagerank;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.mapreduce.Counters;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import pagerank.MatrixVectorMult.FirstMap;
import pagerank.MatrixVectorMult.FirstReduce;

public class RemoveDeadends {

	enum myCounters{ 
		NUMNODES;
	}

	static class Map extends Mapper<LongWritable, Text, Text, Text> {
		private Integer j ;
		private Integer i;
		
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
			{
			    String[] splits  = value.toString().split("\\s+");
				j = Integer.parseInt(splits[0]);
				i = Integer.parseInt(splits[1]);
				context.write(new Text(i.toString()), new Text(j.toString()));
				//System.out.println("map key "+ i+ " value:  "+ j);
				context.write(new Text(j.toString()), new Text("X"));
				//System.out.println("map key "+ j+ " value: X");
			}
		}
	

	static class Reduce extends Reducer<Text, Text, Text, Text> {
		
		protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
			Integer i = Integer.parseInt(key.toString());
			ArrayList<Integer> jlist= new ArrayList<Integer>();
			boolean DeadEnd= true;
			for (Text value : values) {
				if (value.equals(new Text("X"))){
					DeadEnd = false;
				} else {
					Integer j = Integer.parseInt(value.toString());
					jlist.add(j);
				}
			}
			if (DeadEnd) {
				//System.out.println("Reduce found deadend: "+i);
			}
			if (!DeadEnd){
				//System.out.println("Reduce no dead end: key: "+i);
				for (Integer j:jlist){
					context.write(new Text(j.toString()), key);
					
					
				}
				
				Counter c = context.getCounter(myCounters.NUMNODES);
				c.increment(1);
				//System.out.println("Reduce Node "+key+ " NUMNODES "+c.getValue());
				
			}
		}
}

	public static void job(Configuration conf) throws IOException, ClassNotFoundException, InterruptedException{
		
		
		boolean existDeadends = true;
		
		/* You don't need to use or create other folders besides the two listed below.
		 * In the beginning, the initial graph is copied in the processedGraph. After this, the working directories are processedGraphPath and intermediaryResultPath.
		 * The final output should be in processedGraphPath. 
		 */
		
		FileUtils.copyDirectory(new File(conf.get("graphPath")), new File(conf.get("processedGraphPath")));
		String intermediaryDir = conf.get("intermediaryResultPath");
		String currentInput = conf.get("processedGraphPath");
		
		long nNodes = conf.getLong("numNodes", 0);
		int nb_iteration = 0;
		
		
		while(existDeadends)
		{
			nNodes = conf.getLong("numNodes", 0);
			//System.out.println("nNodes entrée de boucle: "+nNodes+ " iteration: "+nb_iteration);
			Job job = Job.getInstance(conf);
			job.setJobName("deadends job");
			
			/* TO DO : configure job and move in the best manner the output for each iteration
			 * you have to update the number of nodes in the graph after each iteration,
			 * use conf.setLong("numNodes", nNodes);
			*/
			
			job.setMapOutputKeyClass(Text.class);
			job.setMapOutputValueClass(Text.class);

			job.setMapperClass(Map.class);
			job.setReducerClass(Reduce.class);

			job.setInputFormatClass(TextInputFormat.class);
			job.setOutputFormatClass(TextOutputFormat.class);

			FileInputFormat.setInputPaths(job, new Path(currentInput));
			FileOutputFormat.setOutputPath(job, new Path(intermediaryDir));
				
			//System.out.println ("starting job n°: "+ nb_iteration);
						
			job.waitForCompletion(true);
			
			Counters counters = job.getCounters();
			Counter c= counters.findCounter(myCounters.NUMNODES);
			//System.out.println("NUMNODES "+ c.getValue());
			//System.out.println("nNodes " + nNodes);
			
			if (nNodes == 0){
				nNodes =   c.getValue();
			} else if (nNodes == c.getValue() ) {
				existDeadends = true;
				//System.out.println("exiting on iteration : " + nb_iteration + " NUMNODES "+ c.getValue());
				break;
			}
			conf.setLong("numNodes", c.getValue());
			nb_iteration +=1;
			//System.out.println("iteration: "+ nb_iteration + " nNodes: "+ nNodes);
			
			FileUtils.deleteDirectory(new File(currentInput));
			FileUtils.copyDirectory(new File(intermediaryDir), new File(currentInput));
			FileUtils.deleteDirectory(new File(intermediaryDir));
			
		}	
		FileUtils.deleteDirectory(new File(intermediaryDir));
		// when you finished implementing delete this line
		//throw new UnsupportedOperationException("Implementation missing");
		
		
	}
	
}