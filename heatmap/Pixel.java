/**
 * Starting Point Code for Image Processing Project
 * @author Richard Wicentowski and Tia Newhall (2005)
 */
import javax.imageio.ImageIO;
import java.io.*;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import javax.swing.*;

public class Pixel {
  
  protected int[] component;

  /** creates a new black pixel */  
  Pixel() { this (0,0,0); }
 
  /** creates a new gray pixel of the specified intensity */ 
  Pixel(int gray) {
    component = new int[1];
    component[0] = gray;
  }
  
  /** creates a new color pixel with the specified color intensities
   * */
  Pixel(int r, int g, int b) {
    component = new int[3];
    component[0] = r;
    component[1] = g;
    component[2] = b;
  }
  
 /** creates a new pixel with the specified component intensities */ 
  Pixel(int[] c) {
    component = new int[c.length];
    for (int i = 0; i < c.length; i++) {
      component[i] = c[i];
    }
  }
 
 /** prints a tab-seperated list of components */ 
  public void info() {
    for (int i = 0; i < component.length; i++) {
      System.out.print(component[i] + "\t");
    }
    System.out.println();
  }
 
 /** sets this pixel to black */ 
  public void toBlack() {
    for (int i = 0; i < component.length; i++) { component[i] = 0; }
  }
 
 /** sets this pixel to white */ 
  public void toWhite() {
    for (int i = 0; i < component.length; i++) { component[i] = 255; }
  }
 
 /** gets the red component */ 
  public int getRed() { 
    return component[0];
  }
  
 /** gets the green component */ 
  public int getGreen() { 
    return component[1];
  }
  
 /** gets the blue component */ 
  public int getBlue() { 
    return component[2];
  }
 
 /** gets the gray component */ 
  public int getGray() {
    return component[0];
  }
 
 /** sets the red component */ 
  public void setRed(int red) { 
    if (red < 0) { red = 0; } else if (red > 255) { red = 255; }
    component[0] = red;
  }
  
 /** sets the green component */ 
  public void setGreen(int green) { 
    if (green < 0) { green = 0; } else if (green > 255) { green = 255; }
    component[1] = green;
  }
  
 /** sets the blue component */ 
  public void setBlue(int blue) { 
    if (blue < 0) { blue = 0; } else if (blue > 255) { blue = 255; }
    component[2] = blue;
  }
  
 /** sets the gray component */ 
  public void setGray(int gray) {
    component[0] = gray;
  }
 
 /** get the array of components */ 
  public int[] getComponents() {
    return component;
  }
 
 /** returns a String representation of this pixel. This is a
  * tab-seperated list of component values */ 
  public String toString() {
    String s = "";
    for (int k = 0; k < component.length; k++) {
      if (k != 0) { s += "\t"; }
      s += component[k];
    }
    return s;
  }
 
 /** checks whether this pixel has the same components as the given
  * Object.  If the object is not a Pixel, then this returns false */ 
  public boolean equals (Object other) {
    if (other instanceof Pixel) {
      Pixel o = (Pixel)other;
      if (o.component.length != component.length) {
        return false; 
      } else {
        for (int k = 0; k < component.length; k++) {
          if (o.component[k] != component[k]) {
            return false;
          }
        }
        return true;
      }
    } else {
      return false;
    }
  }
  
}
