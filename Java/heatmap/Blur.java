
public class Blur implements Manipulator {

	public void manipulate(ImageBase ib) {
		Picture picture = ib.getPicture();
	    int imageWidth = picture.getWidth();
	    int imageHeight = picture.getHeight();
	    Pixel pix, pixL, pixR, pixT, pixB;
	    double avgR, avgG, avgB;
		Picture pict = new Picture(imageWidth, imageHeight);

	    for (int x = 0; x < imageWidth; x++) {
	      for (int y = 0; y < imageHeight; y++) {
	        pix = pixL = pixR = pixT = pixB = picture.getPixel(x, y);
	        if (x != 0)
	        	pixL = picture.getPixel(x-1, y);
	        if (x != imageWidth-1)
	        	pixR = picture.getPixel(x+1,y);
	        if (y != 0)
	        	pixT = picture.getPixel(x, y-1);
	        if (y != imageHeight-1)
	        	pixB = picture.getPixel(x, y+1); 
	        avgR = pix.getRed()*0.6 + pixL.getRed()*0.1 + pixR.getRed()*0.1 + 
	        	pixT.getRed()*0.1 + pixB.getRed()*0.1;
	        avgG = pix.getGreen()*0.6 + pixL.getGreen()*0.1 + pixR.getGreen()*0.1 + 
        		pixT.getGreen()*0.1 + pixB.getGreen()*0.1;
	        avgB = pix.getBlue()*0.6 + pixL.getBlue()*0.1 + pixR.getBlue()*0.1 + 
        		pixT.getBlue()*0.1 + pixB.getBlue()*0.1;
	        pict.setPixel(x, y, new Pixel((int)avgR, (int)avgG, (int)avgB));
	      }
	    }
	    // tells the ImageBase object to display the new Picture. 
	    ib.setPicture(pict);
	    ib.refresh();
	}

	public String getManipulationName() {
		return "Blur";
	}

}
