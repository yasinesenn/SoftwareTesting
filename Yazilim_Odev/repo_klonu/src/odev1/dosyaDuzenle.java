/* 
*
* @author Yasin Emin Esen yasin.esen2@ogr.sakarya.edu.tr
* @since 25/03/22
* <p>
* Okunacak dosyayi yorumlardan ve string ifadelerden ayirip duzenleyen sinif.
* </p>
*/
package odev1;

import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class dosyaDuzenle {

	public static StringBuilder DosyadanOku(String file) throws IOException {
		
		BufferedReader bReader;
		StringBuilder received_data = new StringBuilder();
		bReader = new BufferedReader(new FileReader(file));
		String str = "";
		str = bReader.readLine();

		while (str != null) { // Dosyayi okur ve okudugu ifadeleri received_data'ya ekler.
			received_data.append(str);
			received_data.append("\n");
			str = bReader.readLine();

		}

		return received_data;
		
	}

	public static String tirnakAralariniSil(String file) { // okunacak dosya icerisindeki string ifadeleri temizlememizi
															// saglar.

		String str = yorumlariSil(file);

		final String regex = "(\\\"(.*?)\\\")(\\+?\\*?)";
		final String subst = "\"\"";

		final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
		final Matcher matcher = pattern.matcher(str);

		str = matcher.replaceAll(subst); // eslesen degerleri "" karakterleri ile degistirir.

		final String regex1 = "\\<\\w*?\\s*?\\w*?\\s*?(\\,?)\\w*?\\s*?\\w*?\\s*?(\\,?)\\w*?\\s*?\\w*?\\s*?\\>";
		// arraylist<> gibi durumlarda buyuktur ve kucuktur isaretleri kullanildiginda
		// bunlari operator olarak saymamasi icin <> ve arasini temizler.
		final Pattern pattern1 = Pattern.compile(regex1, Pattern.MULTILINE);
		final Matcher matcher1 = pattern1.matcher(str);

		str = matcher1.replaceAll("\"\"");

		return str;

	}

	public static String yorumlariSil(String file) { // okunacak dosya icerisindeki yorum satirlarini temizler.
		final String regex = "(\\/)([\\*])+(.|\\n)+?(\\2\\1)|((\\/)([\\*][\\*]?)(.|\\n)*?\\3\\2)|(\\/\\/.*)\n";
		final String subst = "";

		String str = null;

		try {
			str = DosyadanOku(file).toString(); // dosyadan okunan strBuilder ifadeyi stringe cevirir.

			final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
			final Matcher matcher = pattern.matcher(str);

			str = matcher.replaceAll(subst);
			// System.out.println(str);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return str;
	}

	public static String duzenlenmisDosya(String file) throws IOException { // okunan dosyayi yorumlardan ve string
																			// ifadelerden temizlemis bicimde geri
																			// dondurur.
		String str = DosyadanOku(file).toString();
		str = dosyaDuzenle.yorumlariSil(file);
		str = dosyaDuzenle.tirnakAralariniSil(file);

		return str;
	}

	public static void print() { // bulunan sonuclari ekrana yazdirir.
		
		System.out.println("Operator Bilgisi:");
		System.out.println("--------------------------------");
		System.out.println("	tekli operator sayisi     : " + Lexical.tekli_op);
		System.out.println("	ikili operator sayisi     : " + Lexical.ikili_op);
		System.out.println("	sayisal operator sayisi   : " + Lexical.sayisal_op);
		System.out.println("	iliskisel operator sayisi : " + Lexical.iliskisel_op);
		System.out.println("	mantiksal operator sayisi : " + Lexical.mantiksal_op);
		System.out.println("--------------------------------");
		System.out.println("Operand Bilgisi:");
		System.out.println("--------------------------------");
		System.out.println("	operand sayisi            : " + Lexical.operandSayisiBul());
	}

}
