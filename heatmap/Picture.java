/**
 * Starting Point Code for Image Processing Project
 * @author Richard Wicentowski and Tia Newhall (2005)
 * Modified by Fernando Pereira to accept URLs and other resource locators
 */
import javax.imageio.ImageIO;
import java.io.*;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import javax.swing.*;

public class Picture {

  /** The type representing a color image */  
  public static int COLOR = BufferedImage.TYPE_INT_RGB;
  /** The type representing a grayscale image */  
  public static int GRAY = BufferedImage.TYPE_BYTE_GRAY;
 
  /** The default image type (COLOR) */ 
  protected static int defaultImageType = BufferedImage.TYPE_INT_RGB;
  
  protected int imageType;
  protected BufferedImage bufferedImage;
  protected WritableRaster raster;
 
  /** crates a new Picture object with the default image type and no
   * image */
  Picture() { 
    imageType = defaultImageType;
    bufferedImage = null;
    raster = null;
  }
 
  /** behaves as Picture(width,height,Picture.defaultImageType)  */ 
  Picture(int width, int height) {
    this(width, height, defaultImageType);
  }
 
  /** creates a Picture object with an image of the specified size and
   * type */ 
  Picture(int width, int height, int type) {
    bufferedImage = new BufferedImage(width, height, type);
    raster = bufferedImage.getRaster();
    imageType = type;
  }
  
  /** identical to Picture(filename, Picture.defaultImageType) */
  Picture(String filename) {
    this(filename, defaultImageType);
  }
 
  /** creates a new Picture object of the specified type by reading in
   * the given file. 
   * @param filename the location of the image file to read */ 
  Picture(String filename, int type) {
    if ((type != COLOR) && (type != GRAY)) { type = defaultImageType; }
    imageType = type;
    load(filename);
  }
 
  /** get the type of the image */ 
  public int getImageType() { return imageType; }
  
  /** get the width of the image */ 
  public int getWidth() { return bufferedImage.getWidth(); }
  /** get the height of the image */ 
  public int getHeight() { return bufferedImage.getHeight(); }
  
  /** get the BufferedImage object associated with this picture */
  public BufferedImage getBufferedImage() { return bufferedImage; }
  /** get the WritableRaster object associated with this picture */
  public WritableRaster getRaster() { return raster; }
 
  /** load the image from the specified image into this Picture object */ 
  public void load(String filename) {
    ImageIcon icon;
    if ((new File(filename)).exists())
      icon = new ImageIcon(filename);
    else {
      java.net.URL u = Picture.class.getResource(filename);
      icon = new ImageIcon(u);
    }
    Image image = icon.getImage();
    bufferedImage = new BufferedImage(image.getWidth(null),
                                      image.getHeight(null),
                                      imageType);
    Graphics g = bufferedImage.getGraphics();
    g.drawImage(image, 0, 0, null);
    g.dispose();
    
    raster = bufferedImage.getRaster();
  }
 
 /** copy the image from the given picture onto this one 
  @param p the original picture */ 
    public void copy(Picture p) {
      imageType = p.getImageType();

      bufferedImage = new BufferedImage(p.getWidth(),
                                        p.getHeight(),
                                        imageType);
      
      raster = bufferedImage.getRaster();
      
      for (int x = 0; x < bufferedImage.getWidth(); x++) {
        for (int y = 0; y < bufferedImage.getHeight(); y++) {
          setPixel(x,y, p.getPixel(x, y));
        }
      }
    }
   
   /** get the Pixel at the specified position
    * @param x the x-coordinate
    * @param y the y-coordinate
    */ 
    public Pixel getPixel(int x, int y) {
      return new Pixel(raster.getPixel(x, y, (int [])null));
    }
    
   
   /** set the pixel at the specified coordinate 
    * @param x the x-coordinate
    * @param y the y-coordinate
    */ 
    public void setPixel(int x, int y, Pixel pixel) {
      int[] pixelArray = pixel.getComponents();
      raster.setPixel(x, y, pixelArray);
    }
    public double distance(Picture other) {
      int w = getWidth(), h = getHeight();
      if (w != other.getWidth() || h != other.getHeight() ||
          raster.getNumBands() != other.raster.getNumBands())
        return Double.POSITIVE_INFINITY;
      double dist = 0;
      int depth = raster.getNumBands();
      int[] pThis = new int[depth];
      int[] pOther = new int[depth];
      for (int i = 0; i < w; i++)
        for (int j = 0; j < h; j++) {
          raster.getPixel(i, j, pThis);
          other.raster.getPixel(i, j, pOther);
          for (int k = 0; k < depth; k++)
            dist += Math.abs(pThis[k]-pOther[k])/255.0;
        }
      return dist/(w*h*depth);
    }
}

