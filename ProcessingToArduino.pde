import processing.serial.*;
import osteele.processing.SerialRecord.*;
// initializing variables
Serial serialPort; // name for serial port
String distraction = "1"; // distraction = 1 if you're looking toward screen and 2 if you are looking away
void setup(){  
    String serialPortName = SerialUtils.findArduinoPort(); // find which serial port arduino is connected to
    serialPort = new Serial(this, serialPortName, 9600); // set serialPort to found port
}
void draw(){
    String[] file = loadStrings("C:/Users/airha/OneDrive/Productivity-Project/input.txt"); //path directory to text file. Must be exact path file may need to update
    // checks if there is a change to whether you are looking away and tells arduino
    if(distraction != file[0]){      
      distraction = file[0];
      serialPort.write(distraction);
      delay(2000); // some buffer delay so you don't overwhelm arduino
    }   
} 
