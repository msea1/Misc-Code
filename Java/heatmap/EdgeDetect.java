import java.lang.Math;

public class EdgeDetect implements Manipulator {
  
  public void manipulate(ImageBase ib) {
    Picture picture = ib.getPicture();
    int imageWidth = picture.getWidth();
    int imageHeight = picture.getHeight();
    double red, blue, green;
    Pixel pix, left, bottom;
    int lr = 0;
    int lb = 0;
    int lg = 0;
    int br = 0;
    int bb = 0;
    int bg = 0;
    Picture pict = new Picture(imageWidth, imageHeight);
    
    for (int x = 0; x < imageWidth; x++) {
      for (int y = 0; y < imageHeight; y++) {
        pix = left = bottom = picture.getPixel(x, y);
        if (x != 0) {
          left = picture.getPixel(x-1, y);
          lr = left.getRed() - pix.getRed();
          lb = left.getBlue() - pix.getBlue();
          lg = left.getGreen() - pix.getGreen();
        }
        if (y != imageHeight-1) {
          bottom = picture.getPixel(x, y+1);
          br = bottom.getRed() - pix.getRed();
          bb = bottom.getBlue() - pix.getBlue();
          bg = bottom.getGreen() - pix.getGreen();
        }
        red = Math.sqrt((lr*lr)+(br*br));
        blue = Math.sqrt((lb*lb)+(bb*bb));
        green = Math.sqrt((lg*lg)+(bg*bg));
        pix.setRed((int)red);
        pix.setGreen((int)green);
        pix.setBlue((int)blue);
        pict.setPixel(x, y, pix);
      }
    }
    // tells the ImageBase object to display the new Picture. 
    ib.setPicture(pict);
    ib.refresh();
  }
  
  public String getManipulationName() {
    return "Edge Detect";
  }
  
}
