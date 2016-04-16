
public class ColorRotate implements Manipulator {

	public void manipulate(ImageBase ib) {
		Picture picture = ib.getPicture();

	    int imageWidth = picture.getWidth();
	    int imageHeight = picture.getHeight();
	    Pixel pix1;

	    for (int x = 0; x < imageWidth; x++) {
	      for (int y = 0; y < imageHeight; y++) {
	        pix1 = picture.getPixel(x, y);
	        picture.setPixel(x, y, new Pixel(pix1.getBlue(), pix1.getRed(), pix1.getGreen()));
	      }
	    }
	    // tells the ImageBase object to display the new Picture. 
	    ib.refresh();
	}

	public String getManipulationName() {
		return "Color Rotate";
	}

}
