/**
*
* @author Yasin Emin Esen yasin.esen2@ogr.sakarya.edu.tr
* @since 25/03/22
* <p>
* tum islemler yapıldiktan sonra calistirilabilir sinif.
* </p>
*/
package odev1;

import java.io.*;


public class program {

	public static void main(String[] args) throws IOException {

		if (args.length > 0) {
			// System.out.println(dosyaDuzenle.duzenlenmisDosya("read.java"));
			Lexical.operator_Sayaci(args[0]);

		} else {
			// System.out.println(dosyaDuzenle.duzenlenmisDosya("read.java"));
			Lexical.operator_Sayaci("Ogrenci.java");
		}

		//System.out.println(dosyaDuzenle.duzenlenmisDosya("Deneme.txt"));
	
	}
}