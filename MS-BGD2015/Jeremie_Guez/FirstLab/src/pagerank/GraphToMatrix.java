package pagerank;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

/*
 * Write the map and reduce function. To test your code run PublicTests.java. 
 * On the site submit a zip archive of your src folder. 
 * Try also the release tests after your submission. You have 3 trials per hour for the release tests. 
 * A correct implementation will get the same number of points for both public and release tests.
 * Please take the time to understand the settings for a job, in the next lab your will need to configure it by yourself. 
 */

public class GraphToMatrix {

	static class Map extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{

			StringTokenizer itr = new StringTokenizer(value.toString());
			while (itr.hasMoreTokens())
			{
				int j = Integer.parseInt(itr.nextToken());
				int i = Integer.parseInt(itr.nextToken());
				context.write(new IntWritable(j), new IntWritable(i));
			}
			//			// On split value pour recuperer les valeurs
			//			String[] values  = value.toString().split("\\s+");
			//			
			//			// On stock dans des IntWritable la cle et la value
			//			IntWritable keyOutput  = new IntWritable (Integer.parseInt(values[0]));
			//			IntWritable valueOutput  = new IntWritable (Integer.parseInt(values[1]));
			//			
			//			// On ecrit dans le context
			//			context.write(keyOutput, valueOutput);
			//			
			//			System.out.println("Recuperation valeur : " + Integer.parseInt(values[0]) + " " + Integer.parseInt(values[1]));	
		}
	}

	static class Reduce extends Reducer<IntWritable, IntWritable, NullWritable, Text> {

		protected void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{

			NullWritable returnKey = null;
			// Creation de l arraylist de successeurs
			ArrayList<IntWritable> successeurs = new ArrayList<IntWritable> ();


			for (IntWritable value : values)
			{
				// On ajoute les successeur du meme cle dans l arraylist
				successeurs.add(new IntWritable(value.get()));
				System.out.println("Recuperation successeur : " + Integer.parseInt(value.toString()) + "   Pour la key : " + Integer.parseInt(key.toString()));	
			}

			// On parcours la liste des succesors pour construire la matrice
			for (IntWritable successeur : successeurs)
				// On ecrit dans le context
				// returnkey est un NullWritable 
				// Et on creer un objet Text qui contient le successeur, la cle et la probabilite
				context.write(returnKey, new Text(successeur.toString() + " " + key.toString() + " "+ Double.toString(1.0/successeurs.size())));
		}
	} 

	public static void job(Configuration conf) throws IOException, ClassNotFoundException, InterruptedException {
		Job job = Job.getInstance(conf);
		job.setMapOutputKeyClass(IntWritable.class);
		job.setMapOutputValueClass(IntWritable.class);

		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.setInputPaths(job, new Path(conf.get("processedGraphPath")));
		FileOutputFormat.setOutputPath(job, new Path(conf.get("stochasticMatrixPath")));
		job.waitForCompletion(true);
	}

}
