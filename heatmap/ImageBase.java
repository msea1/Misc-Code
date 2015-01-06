import java.io.*;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import javax.swing.*;
import javax.imageio.*;

public class ImageBase {
  
  private JFrame menuFrame;
  private PictureFrame pictureFrame;
  //private SimpleButton[] buttons;
  //private JLabel photo;
  private static Picture picture;
  private static boolean closing = false;
  
    /** main method (for using this as a standalone application.  Creates
    * an ImageBase object and adds a FlipHorizontal button to it.  
    * @param args Should be a single-element array.  The value of the
    * element is the name of the file to read. */
  public static void main (String[] args) {
    ImageBase app; 
    if (args.length == 1) {
      File f = new File (args[0]);
      if (f.exists()) {
        try {
          process(args[0]);
        }
        catch (Exception e) {
        }
      } else {
        //System.out.println(args[0] + ": File not found.");
      }
    } else {
      //System.out.println("Image file required.");
    }
  }
  
  public ImageBase() {
    picture = new Picture();
  }
  
  ImageBase(String filename) {
    this();
  }
  
  private void shutdown() {
    if (!closing) {
      closing = true;
      if (menuFrame != null) {
        menuFrame.dispose();
        menuFrame = null;
      }
      if (pictureFrame != null) {
        pictureFrame.dispose();
        pictureFrame = null;
      }
    }
  }
  
  private static void save(String filename) {
    BufferedImage img = getPicture().getBufferedImage();
    File f = new File(filename);
    try {
      ImageIO.write(img, "JPEG", f);
    } 
    catch(IOException e) {
    }
  }
  
  private static void checkOpen() {
    if (closing)
      throw new UnsupportedOperationException("This ImageBase has been closed");
  }
  
  
  /** gets a reference to the current picture.  If you modify this
    * directly, then you need to call the refresh method to have the
    * results displayed. */ 
  public static Picture getPicture() {
    checkOpen();
    return picture;
  } 
  
  /** sets the current picture the the one provided and refreshes the
    * display. 
    * @param newPic the new picture
    */
  public void setPicture(Picture newPic) {
    checkOpen();
    picture=newPic;
  }
  
  public static void process (String path) {
    ImageBase app; 
    File f = new File (path);
    if (f.exists()) {
      try {
        app = new ImageBase();
        HeatMap hm = new HeatMap();
        BufferedReader buf = new BufferedReader(new FileReader(f));
        String car = buf.readLine();
        while (car != null) {
          hm.manipulate(app,car);
          String picSave = car.substring(0,car.indexOf("."));
          picSave += ".png";
          save(picSave);
          car = buf.readLine();
        }
        buf.close();
      }
      catch (Exception e) {
      }
    } 
    else {
      //System.out.println(args[0] + ": File not found.");
    }
  }  
}
