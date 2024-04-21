/**
*
* @author Yasin Emin Esen yasin.esen2@ogr.sakarya.edu.tr
* @since 25/03/22
* <p>
* operand ve operator bilgilerini bulup bunların sonuclarını donduren sinif.
* </p>
*/
package odev1;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.sound.midi.Receiver;

public class Lexical {
	public static int tekli_op = 0;
	public static int ikili_op = 0;
	public static int sayisal_op = 0;
	public static int iliskisel_op = 0;
	public static int mantiksal_op = 0;
	public static int unlemSayac = 0; // mantiksal op de operand sayisini +2 olarak aldigindan dolayi son durumda
										// operand sayisini dogru bulmamizda yardimci olur.

	public static void tekli_opIkiArti_Eksi(String str, String file) throws IOException { // tekli operator olan ++ ve
																							// -- yi ayirmamizi saglar.
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String regex = "\\w*\\+\\+\\w*|\\w*\\-\\-\\w*";

		final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
		final Matcher matcher = pattern.matcher(str);

		while (matcher.find()) { // eslesen ifade oldukca iceriye girip ilgili operator sayisini artirir.
			tekli_op++;
			sayisal_op++;
		}
	}

	public static void ikili_opCarpma_Bolme_Mod(String str, String file) throws IOException {// carpma bolme mod
																								// operatorlerini
																								// ayirir.
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String ikili_opCarpma_Bolme_Mod = "(\\*(?!\\=)(?!\\;))|(\\/(?!\\=)(?!\\;))|(\\%(?!\\=)(?!\\;))";
		final Pattern pattern = Pattern.compile(ikili_opCarpma_Bolme_Mod, Pattern.MULTILINE);
		final Matcher matcher = pattern.matcher(str);

		while (matcher.find()) {
			ikili_op++;
			sayisal_op++;
		}
	}

	public static void Mantiksal_op(String str, String file) throws IOException {
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String regex = "\\w*\\&\\&\\w*|\\w*(\\|)(\\|)\\w*"; // || ve && operatorlerini ayirmamizda yardimci olur.
		final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
		final Matcher matcher = pattern.matcher(str);

		final String regexUnlem = "(\\!(?!\\=))"; // sadece unlem operatorunu ayirmamizda yardimci olur.
		final Pattern pattern2 = Pattern.compile(regexUnlem, Pattern.MULTILINE);
		final Matcher matcher2 = pattern2.matcher(str);

		while (matcher.find()) {
			mantiksal_op++;
		}
		while (matcher2.find()) {
			tekli_op++;
			unlemSayac++;
			mantiksal_op++;
		}
	}

	public static void IkiliSayisal_op(String str, String file) throws IOException {
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String ikiliSayisal = "(\\*\\=)|(\\+\\=)|(\\-\\=)|(\\/\\=)|(\\%\\=)|(\\&\\=)|(\\|\\=)|(\\^\\=)"; // atama
																												// operatorlerini
																												// ayirirken
																												// kullanilir.
		final Pattern pattern = Pattern.compile(ikiliSayisal, Pattern.MULTILINE);
		final Matcher matcher = pattern.matcher(str);

		while (matcher.find()) {
			ikili_op++;
			sayisal_op++;
		}
	}

	public static void Iliskisel_op(String str, String file) throws IOException { // iliskisel operatorleri ayirip
																					// bunlarin sayisini bulmamizi
																					// saglar
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String iliskisel = "(\\>\\=)|(\\<\\=)|(\\=\\=)|(\\!\\=)";

		final Pattern pattern1 = Pattern.compile(iliskisel, Pattern.MULTILINE);
		final Matcher matcher1 = pattern1.matcher(str);

		while (matcher1.find()) {
			iliskisel_op++;
		}

		final String buyukKucuk = "\\<(?!\\=)(?!\\<)|(?<!\\-)\\>(?!\\=)(?!\\>)";

		final Pattern pattern2 = Pattern.compile(buyukKucuk, Pattern.MULTILINE);
		final Matcher matcher2 = pattern2.matcher(str);

		while (matcher2.find()) {
			iliskisel_op++;
		}

	}

	public static void tekKarakter_Op_Say(String str, String file) throws IOException {
		str = dosyaDuzenle.duzenlenmisDosya(file);

		final String toplama_cikarma_us = "((?<!\\+)\\+(?!\\+|\\=))|((?<!\\-)\\-(?!\\>)(?!\\-|\\=))|(\\^(?!\\=))";
		final Pattern pattern1 = Pattern.compile(toplama_cikarma_us, Pattern.MULTILINE);
		final Matcher matcher1 = pattern1.matcher(str);

		while (matcher1.find()) {
			ikili_op++;
			sayisal_op++;
		}
		final String sayisal_opEsittir = "(?<!\\*)(?<!\\-)(?<!\\+)(?<!\\/)(?<!\\<)(?<!\\>)(?<!\\=)(?<!\\!)(?<!\\&)(?<!\\|)(?<!\\%)(?<!\\^)\\=(?!\\=)";
		// yalnizca esittir operatorunu ayirmamizi saglar.
		final Pattern pattern2 = Pattern.compile(sayisal_opEsittir, Pattern.MULTILINE);
		final Matcher matcher2 = pattern2.matcher(str);

		while (matcher2.find()) {
			ikili_op++;
			sayisal_op++;
		}

		final String sayisal_opVeVeya = "(?<!\\&)\\&(?!\\&)(?!\\=)|(?<!\\|)\\|(?!\\|)(?!\\=)";
		final Pattern pattern3 = Pattern.compile(sayisal_opVeVeya, Pattern.MULTILINE);
		final Matcher matcher3 = pattern3.matcher(str);

		while (matcher3.find()) {
			ikili_op++;
			sayisal_op++;
		}

	}

	public static void operator_Sayaci(String file) throws IOException { // okunan dosyadaki operand ve operator
																			// sayilarini bulur ve sonucu ekrana
																			// yazdirir.
		String str = null;

		tekli_opIkiArti_Eksi(str, file);
		ikili_opCarpma_Bolme_Mod(str, file);
		Iliskisel_op(str, file);
		Mantiksal_op(str, file);
		IkiliSayisal_op(str, file);
		tekKarakter_Op_Say(str, file);
		operandSayisiBul();

		dosyaDuzenle.print();
	}

	public static int operandSayisiBul() { // buldugumuz operator sayilarini kullanarak operand sayisini hesaplar ve
											// dondurur.

		int operandSayisi = tekli_op + ikili_op * 2 + iliskisel_op * 2 + mantiksal_op * 2 - unlemSayac * 2;

		return operandSayisi;
	}

}
