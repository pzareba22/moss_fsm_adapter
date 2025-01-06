import java.io.File
import java.io.FileWriter
import scala.io.Source
println("converting...")

val inputFilePath = "./moleculenet/delaney-processed.csv"
val outputFilePath = "./moleculenet/processed.csv"

val lines = Source.fromFile(inputFilePath).getLines.toVector
val fileWriter = new FileWriter(new File(outputFilePath))

lines.drop(1).zipWithIndex.foreach { case (line, index) => 
  val smile = line.split(",").last
  val newLine = "a" + "," + index.toString() + "," + smile + "\n"
  fileWriter.write(newLine)
}

fileWriter.close()
println("conversion done!")
