import java.io.*;
import java.util.*;
import gnu.io.*;

public class SerialReader implements SerialPortEventListener {

    private SerialPort serialPort;
    private InputStream input;
    private FileWriter writer;
    private boolean isWriting = false;

    public static void main(String[] args) throws Exception {
        String portName = "/dev/ttyACM0"; // change this to match your port name
        int baudRate = 9600; // change this to match your device's baud rate

        SerialReader reader = new SerialReader();
        reader.init(portName, baudRate);
        reader.startReading();

        // Wait for 10 seconds to receive data
        Thread.sleep(10000);

        reader.stopReading();
    }

    public void init(String portName, int baudRate) throws Exception {
        CommPortIdentifier portIdentifier = CommPortIdentifier.getPortIdentifier(portName);
        if (portIdentifier.isCurrentlyOwned()) {
            System.out.println("Error: Port is currently in use");
        } else {
            CommPort commPort = portIdentifier.open(this.getClass().getName(), 2000);
            if (commPort instanceof SerialPort) {
                serialPort = (SerialPort) commPort;
                serialPort.setSerialPortParams(baudRate, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);

                input = serialPort.getInputStream();
                writer = new FileWriter("serial_data.txt");
            } else {
                System.out.println("Error: Only serial ports are supported");
            }
        }
    }

    public void startReading() throws Exception {
        serialPort.addEventListener(this);
        serialPort.notifyOnDataAvailable(true);
    }

    public void stopReading() throws Exception {
        serialPort.removeEventListener();
        serialPort.close();
        writer.close();
        System.out.println("Serial communication stopped");
    }

    public void serialEvent(SerialPortEvent event) {
        if (event.getEventType() == SerialPortEvent.DATA_AVAILABLE) {
            try {
                if (!isWriting) {
                    isWriting = true;
                    Scanner scanner = new Scanner(input);
                    while (scanner.hasNextLine()) {
                        String line = scanner.nextLine();
                        System.out.println(line);
                        writer.write(line + "\n");
                        writer.flush();
                    }
                    scanner.close();
                    isWriting = false;
                }
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}
