package pagerank;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import org.apache.commons.io.FileUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;


public class MatrixVectorMult {
	
	static class FirstMap extends Mapper<LongWritable, Text, IntWritable, Text> {
		private IntWritable row = new IntWritable();
		private IntWritable column = new IntWritable();
		private Text element = new Text();
		protected void map(LongWritable key, Text value, Context context) 
			throws IOException, InterruptedException
			{
				
			    String[] splits  = value.toString().split("\\s+");
				if(splits.length == 2)
				{
					row.set(Integer.parseInt(splits[0]));
					element.set (splits[1]);
					context.write(row, element);
				}
				else if(splits.length == 3)
				{
					element.set (splits[0]);
					column.set (Integer.parseInt(splits[1]));
					element.set(element + " " + splits[2]);
					context.write(column, element);
				}
			
			}
		}
	

	static class FirstReduce extends Reducer<IntWritable, Text, IntWritable, DoubleWritable> {
		private DoubleWritable partialResult = new DoubleWritable ();
		protected void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
			
			HashMap<Integer,Double> matrixColumn = new HashMap<Integer,Double> ();
			double vectorValue = 0.;
			
			for (Text value : values)
			{
				String[] splits  = value.toString().split("\\s+");
				if(splits.length == 1)
				{
					vectorValue = Double.valueOf(splits[0]);
				}
				else if(splits.length == 2)
				{
					matrixColumn.put(Integer.valueOf(splits[0]),
					                 Double.valueOf(splits[1]));
				}
			}
			
			for (Integer row:matrixColumn.keySet())
			{
				partialResult = new DoubleWritable(matrixColumn.get(row)* vectorValue);
				context.write(new IntWritable(row), partialResult);
			}
		}
	}
static class SecondMap extends Mapper<Text, Text, IntWritable, DoubleWritable> {
		
		protected void map(Text key, Text value, Context context) 
			throws IOException, InterruptedException
			{
				
				context.write(new IntWritable(Integer.parseInt(key.toString())),new DoubleWritable(Double.parseDouble(value.toString())));
			
			}
		}

static class CombinerForSecondMap extends Reducer<IntWritable, DoubleWritable, IntWritable, DoubleWritable> {
	private DoubleWritable partialResult = new DoubleWritable();
	protected void reduce(IntWritable key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException{
		
		Double vectorValue = 0.;
		
		for (DoubleWritable value : values)
		{
			vectorValue += value.get();
		}
		partialResult.set(vectorValue);
		context.write(key, partialResult);
	}
}

static class SecondReduce extends Reducer<IntWritable, DoubleWritable, IntWritable, DoubleWritable> {
	private DoubleWritable finalResult = new DoubleWritable();
	protected void reduce(IntWritable key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException{
		
		Double vectorValue = 0.;
		
		for (DoubleWritable value : values)
		{
			vectorValue += value.get();
		}
		finalResult.set(vectorValue);
		context.write(key, finalResult);
	}
}
	
	public static void job(Configuration conf)
			throws IOException, ClassNotFoundException, InterruptedException {
		// First job
		Job job1 = Job.getInstance(conf);
		job1.setMapOutputKeyClass(IntWritable.class);
		job1.setMapOutputValueClass(Text.class);

		job1.setMapperClass(FirstMap.class);
		job1.setReducerClass(FirstReduce.class);

		job1.setInputFormatClass(TextInputFormat.class);
		job1.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.setInputPaths(job1, new Path[]{new Path(conf.get("initialVectorPath")), new Path(conf.get("inputMatrixPath"))});
		FileOutputFormat.setOutputPath(job1, new Path(conf.get("intermediaryResultPath")));

		job1.waitForCompletion(true);
		
		// Second job
		Job job2 = Job.getInstance(conf);
		job2.setMapOutputKeyClass(IntWritable.class);
		job2.setMapOutputValueClass(DoubleWritable.class);

		job2.setMapperClass(SecondMap.class);
		job2.setReducerClass(SecondReduce.class);
		
		// If your implementation of the combiner passed the unit test, uncomment the following line
		job2.setCombinerClass(CombinerForSecondMap.class);
		
		job2.setInputFormatClass(KeyValueTextInputFormat.class);
		job2.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.setInputPaths(job2, new Path(conf.get("intermediaryResultPath")));
		FileOutputFormat.setOutputPath(job2, new Path(conf.get("currentVectorPath")));
		
		job2.waitForCompletion(true);
		
		FileUtils.deleteQuietly(new File(conf.get("intermediaryResultPath")));
	}
	
}

