/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ocr;
import java.io.*;
import net.sourceforge.tess4j.*;

/**
 * The program takes in an input.tiff image and outputs and output.txt file
 * of text that is recognized on the image
 * @author pavelshering
 */
public class Ocr {
    /**
     * @param paths the command line arguments
     */
    public static void main(String[] paths) {
        // TODO code application logic here

//         for(int i=0; i< paths.length; i++){
//               System.out.println(paths[i]); // take as an argument for full path of img
//          }

        System.setProperty("jna.library.path", paths[0]); // look up how to pass
        File imageFile = new File(paths[1]);
            Tesseract instance = Tesseract.getInstance();  // JNA Interface Mapping
            //Tesseract1 instance = new Tesseract1(); // JNA Direct Mapping

        instance.setDatapath(paths[2]);
        String dirName = paths[3];
        instance.setLanguage("enm"); //eng

        if(imageFile.canRead() == true ) {
            try {
                String result = instance.doOCR(imageFile);
                System.out.println(result);
                Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(dirName + "/Output.txt"), "utf-8"));
                writer.write(result);
                writer.close();
            }
            catch (IOException | TesseractException e) {
                System.err.println(e.getMessage());
            }
        }
        else {
            System.out.println("Image can't be read");
        }
    }
}
