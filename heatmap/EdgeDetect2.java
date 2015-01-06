import java.lang.Math;

public class EdgeDetect2 implements Manipulator {
  
  public String getManipulationName() {
  return "ED 2";
 }

  
public void manipulate(ImageBase ib){

    Picture original = ib.getPicture();

    int imageWidth = original.getWidth();
    int imageHeight = original.getHeight();
        Picture picture = new Picture(imageWidth, imageHeight);
    double red, blue, green;
    Pixel pix, left, bottom;
    int lr = 0;
    int lb = 0;
    int lg = 0;
    int br = 0;
    int bb = 0;
    int bg = 0;

    for (int x = 0; x < imageWidth; x++) {
      for (int y = 0; y < imageHeight; y++) {
        pix = left = bottom = original.getPixel(x,y);
        if(x != 0){
          left = original.getPixel(x-1, y);
          lr = left.getRed() - pix.getRed();
          lb = left.getBlue() - pix.getBlue();
          lg = left.getGreen() - pix.getGreen();
        }

        if(y != imageHeight-1){
          bottom = original.getPixel(x, y+1);
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
        picture.setPixel(x, y, pix);
        ib.setPicture(picture);
      }
    }
    // tells the ImageBase object to display the new Picture.
    //ib.setPicture(picture);
    ib.refresh();
  }
}