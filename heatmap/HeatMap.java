import java.io.*;
import java.lang.Math;

public class HeatMap {
 public static int[][]chart;
 public static double max = 0.0;
 
 private void markOct(int x, int y) {
  int j = y-6;
  int i = 0;
  int vertLine = 0;
  while (j < 0) { j++; vertLine++; }
  for (;vertLine < 12; vertLine++) {
   if (vertLine == 0 || vertLine == 11) i = 7; 
   else if(vertLine == 1 || vertLine == 10) i = 9;
   else if(vertLine == 2 || vertLine == 9) i = 11;
   else i = 13;
   fillIn(i,j,x);
   j++;
  }
 }
 private void fillIn(int i, int j, int x) {
  if (j < 240) {
   int tX = x-(i/2);
   while (tX < 0) { tX++; i--;}
   for (;i > 0 && tX < 480; i--) {
    chart[j][tX]++;
	if (chart[j][tX] > max) {
		max+=1.0;
	}
    tX++;
   }
  }
 }
 public void manipulate(ImageBase ib, String filepath) {
	double n = 0.0;
	max = 0.0;
	try {
		chart = new int[240][480];
		BufferedReader buf = new BufferedReader(new FileReader(filepath));
		String line = buf.readLine();
		while (line != null) {
		    n++;
		    line = line.replace("\"","");
		    String[] xy = line.split(",");
			if (xy[0].indexOf("pfx") >= 0) {
				line = buf.readLine();
				continue;
			}
		    int xIndex = getXIndex(xy[0]);
		    int yIndex = getYIndex(xy[1]);
		    markOct(xIndex,yIndex);
		    line = buf.readLine();
		}
		Picture pict = new Picture(480, 240); //10' W 5'H, each pix = .25"
		if (n > 250) {
			//double step = (max/n)/12.5;
			double step = n/100;
			for (int x = 0; x < 480; x++) {
				for (int y = 0; y < 240; y++) {
					if (chart[y][x] > 0) {
						//double ratio = chart[y][x]/n;
						double ratio = chart[y][x];
						if (ratio < .2*step) {
							pict.setPixel(x, y, new Pixel(0,0,128)); //d blue
						}
						else if (ratio < .4*step) {
							pict.setPixel(x, y, new Pixel(0,20,255)); //blue
						} 
						else if (ratio < .6*step) {
							pict.setPixel(x, y, new Pixel(0,175,255)); //l blue
						} 
						else if (ratio < .8*step) {
							pict.setPixel(x, y, new Pixel(0,128,0)); //d green
						} 
						else if (ratio < 1.0*step) {
							pict.setPixel(x, y, new Pixel(0,255,0)); //green
						} 
						else if (ratio < 1.2*step) {
							pict.setPixel(x, y, new Pixel(127,255,0)); //l green
						} 
						else if (ratio < 1.4*step) {
							pict.setPixel(x, y, new Pixel(255,215,0)); //gold
						} 
						else if (ratio < 1.6*step) {
							pict.setPixel(x, y, new Pixel(255,140,0)); //d orange
						} 
						else if (ratio < 1.8*step) {
							pict.setPixel(x, y, new Pixel(255,70,0)); //orange red
						}
						else if (ratio < 2.0*step) {
							pict.setPixel(x, y, new Pixel(255,0,0)); //red
						} 
						else if (ratio < 2.2*step) {
							pict.setPixel(x, y, new Pixel(148,0,211)); //violet
						} 
						else {
							pict.setPixel(x, y, new Pixel(255,20,147)); //pink
						}
					}
					else {
						pict.setPixel(x,y,new Pixel(255,255,255));
					}
				}
			}
		}
		else {
			for (int x = 0; x < 480; x++) {
				for (int y = 0; y < 240; y++) {
					if (chart[y][x] > 0) {
						double num = chart[y][x]*200/n;
						if (num < 1) {
							pict.setPixel(x, y, new Pixel(0,0,128)); //d blue
						}
						else if (num < 2) {
							pict.setPixel(x, y, new Pixel(0,20,255)); //blue
						} 
						else if (num < 3) {
							pict.setPixel(x, y, new Pixel(0,175,255)); //l blue
						} 
						else if (num < 4) {
							pict.setPixel(x, y, new Pixel(0,128,0)); //d green
						} 
						else if (num < 5) {
							pict.setPixel(x, y, new Pixel(0,255,0)); //green
						} 
						else if (num < 6) {
							pict.setPixel(x, y, new Pixel(127,255,0)); //l green
						} 
						else if (num < 7) {
							pict.setPixel(x, y, new Pixel(255,215,0)); //gold
						} 
						else if (num < 8) {
							pict.setPixel(x, y, new Pixel(255,140,0)); //d orange
						} 
						else if (num < 9) {
							pict.setPixel(x, y, new Pixel(255,70,0)); //orange red
						}
						else if (num < 10) {
							pict.setPixel(x, y, new Pixel(255,0,0)); //red
						} 
						else if (num < 11) {
							pict.setPixel(x, y, new Pixel(148,0,211)); //violet
						} 
						else {
							pict.setPixel(x, y, new Pixel(255,20,147)); //pink
						}
					}
					else {
						pict.setPixel(x,y,new Pixel(255,255,255));
					}
				}
			}
		}
		markZone(pict);
		markGlossary(pict);
		//blur(pict,ib);
		ib.setPicture(pict);
	}
	catch (Exception e) { e.printStackTrace(); }
}

 private void markGlossary(Picture pict) {
	int j = 10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(0,0,128)); //d blue
		pict.setPixel(i, j+1, new Pixel(0,0,128)); //d blue
		pict.setPixel(i, j+2, new Pixel(0,0,128)); //d blue
		pict.setPixel(i, j+3, new Pixel(0,0,128)); //d blue
		pict.setPixel(i, j+4, new Pixel(0,0,128)); //d blue
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(0,20,255)); //blue
		pict.setPixel(i, j+1, new Pixel(0,20,255)); //blue
		pict.setPixel(i, j+2, new Pixel(0,20,255)); //blue
		pict.setPixel(i, j+3, new Pixel(0,20,255)); //blue
		pict.setPixel(i, j+4, new Pixel(0,20,255)); //blue
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(0,175,255)); //l blue
		pict.setPixel(i, j+1, new Pixel(0,175,255)); //l blue
		pict.setPixel(i, j+2, new Pixel(0,175,255)); //l blue
		pict.setPixel(i, j+3, new Pixel(0,175,255)); //l blue
		pict.setPixel(i, j+4, new Pixel(0,175,255)); //l blue
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(0,128,0)); //d green
		pict.setPixel(i, j+1, new Pixel(0,128,0)); //d green
		pict.setPixel(i, j+2, new Pixel(0,128,0)); //d green
		pict.setPixel(i, j+3, new Pixel(0,128,0)); //d green
		pict.setPixel(i, j+4, new Pixel(0,128,0)); //d green
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(0,255,0)); //green
		pict.setPixel(i, j+1, new Pixel(0,255,0)); //green
		pict.setPixel(i, j+2, new Pixel(0,255,0)); //green
		pict.setPixel(i, j+3, new Pixel(0,255,0)); //green
		pict.setPixel(i, j+4, new Pixel(0,255,0)); //green
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(127,255,0)); //l green
		pict.setPixel(i, j+1, new Pixel(127,255,0)); //l green
		pict.setPixel(i, j+2, new Pixel(127,255,0)); //l green
		pict.setPixel(i, j+3, new Pixel(127,255,0)); //l green
		pict.setPixel(i, j+4, new Pixel(127,255,0)); //l green
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(255,215,0)); //gold
		pict.setPixel(i, j+1, new Pixel(255,215,0)); //gold
		pict.setPixel(i, j+2, new Pixel(255,215,0)); //gold
		pict.setPixel(i, j+3, new Pixel(255,215,0)); //gold
		pict.setPixel(i, j+4, new Pixel(255,215,0)); //gold
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(255,140,0)); //d orange
		pict.setPixel(i, j+1, new Pixel(255,140,0)); //d orange
		pict.setPixel(i, j+2, new Pixel(255,140,0)); //d orange
		pict.setPixel(i, j+3, new Pixel(255,140,0)); //d orange
		pict.setPixel(i, j+4, new Pixel(255,140,0)); //d orange
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(255,70,0)); //orange red
		pict.setPixel(i, j+1, new Pixel(255,70,0)); //orange red
		pict.setPixel(i, j+2, new Pixel(255,70,0)); //orange red
		pict.setPixel(i, j+3, new Pixel(255,70,0)); //orange red
		pict.setPixel(i, j+4, new Pixel(255,70,0)); //orange red
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(255,0,0)); //red
		pict.setPixel(i, j+1, new Pixel(255,0,0)); //red
		pict.setPixel(i, j+2, new Pixel(255,0,0)); //red
		pict.setPixel(i, j+3, new Pixel(255,0,0)); //red
		pict.setPixel(i, j+4, new Pixel(255,0,0)); //red
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(148,0,211)); //violet
		pict.setPixel(i, j+1, new Pixel(148,0,211)); //violet
		pict.setPixel(i, j+2, new Pixel(148,0,211)); //violet
		pict.setPixel(i, j+3, new Pixel(148,0,211)); //violet
		pict.setPixel(i, j+4, new Pixel(148,0,211)); //violet
	}
	j+=10;
	for (int i = 5; i < 20; i++) {
		pict.setPixel(i, j, new Pixel(255,20,147)); //pink
		pict.setPixel(i, j+1, new Pixel(255,20,147)); //pink
		pict.setPixel(i, j+2, new Pixel(255,20,147)); //pink
		pict.setPixel(i, j+3, new Pixel(255,20,147)); //pink
		pict.setPixel(i, j+4, new Pixel(255,20,147)); //pink
	}
 }
 private void markZone(Picture pict) {
  for (int i = 204; i < 277; i++) {
   pict.setPixel(i, 75, new Pixel(0,0,0)); //black
   pict.setPixel(i, 76, new Pixel(0,0,0)); 
   pict.setPixel(i, 77, new Pixel(0,0,0)); 
   pict.setPixel(i, 165, new Pixel(0,0,0)); 
   pict.setPixel(i, 166, new Pixel(0,0,0)); 
   pict.setPixel(i, 167, new Pixel(0,0,0));
  }
  for (int i = 204; i < 277; i+=2) {
   pict.setPixel(i, 106, new Pixel(0,0,0)); //black
   pict.setPixel(i, 136, new Pixel(0,0,0)); 
  }
  for (int i = 77; i < 165; i++) {
   pict.setPixel(204, i, new Pixel(0,0,0)); //black
   pict.setPixel(205, i, new Pixel(0,0,0)); 
   pict.setPixel(206, i, new Pixel(0,0,0)); 
   pict.setPixel(274, i, new Pixel(0,0,0)); 
   pict.setPixel(275, i, new Pixel(0,0,0)); 
   pict.setPixel(276, i, new Pixel(0,0,0));
  }
  for (int i = 77; i < 165; i+=2) {
   pict.setPixel(229, i, new Pixel(0,0,0)); //black
   pict.setPixel(251, i, new Pixel(0,0,0)); 
  }
 }
 private int getYIndex(String coord) {
  int yP = (int)Math.round(Double.parseDouble(coord)*48);
  if (yP > 239) return 0;
  else if (yP < 0) return 239;
  else return 239 - yP;
 }
 private int getXIndex(String coord) {
  int xP = (int)Math.round((Double.parseDouble(coord)+5)*48);
  if (xP > 479) return 479;
  else if (xP < 0) return 0;
  else return xP;
 }
 public void blur(Picture picture, ImageBase ib) {
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
     //ib.refresh();
 }

 public String getManipulationName() {
  return "HeatMap";
 }

}