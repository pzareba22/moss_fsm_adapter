import java.io.File
import java.io.FileWriter
import scala.io.Source
println("converting...")

val inputFilePath = "./moleculenet/delaney-processed.csv"
val outputFilePath = "./moleculenet/processed.smi"

val lines = Source.fromFile(inputFilePath)("UTF-8").getLines.toVector
val fileWriter = new FileWriter(new File(outputFilePath))


fileWriter.write("id,value,description\n")
lines.drop(1).zipWithIndex.foreach { case (line, index) => 
  val data = line.split(",")
  val smile = data.last
  val identifier = data.head
  println(identifier)
  println()
  val newLine = identifier + "," + "0" + "," + smile + "\n"
  fileWriter.write(newLine)
}

fileWriter.close()
println("conversion done!")
