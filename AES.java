import java.util.*;

import java.nio.charset.Charset;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class AES
{

	/**
	 * @param args
	 */
	public static byte[] hexStringToByteArray(String s)
	{
		int len = s.length();
		byte[] data = new byte[len / 2];
		for (int i = 0; i < len; i += 2)
		{
			data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
				+ Character.digit(s.charAt(i + 1), 16));
		}
		return data;
	}

	public static byte[] increment(byte[] array) {
		byte[] r = array.clone();
		for ( int i = array.length - 1; i >= 0; i-- ) {
			byte x = array[ i ];
			if ( x == -1 )
				continue;
			r[ i ] = (byte) (x + 1);
			Arrays.fill( r, i + 1, array.length, (byte) 0 );
			return r;
		}
		throw new IllegalArgumentException( Arrays.toString( array ) );
	}
	
	static void aesECBcbc(String keyStr, String cipherStr, boolean cbc) throws Exception{
		// CipherText string
		// String ctStr = cipherStr.substring(32, cipherStr.length());
		// IV string
		// String ivStr = cipherStr.substring(0, 32);

		//My mode
		//Cipher
		// byte[] cipherBytes = hexStringToByteArray(cipherStr);
		//Key 16 bits 
		byte[] keyBytes = hexStringToByteArray(keyStr);
		//IV 16 bits
		// byte[] ivBytes = hexStringToByteArray(ivStr);
		//CipherText
		byte[]  cipherText = hexStringToByteArray(cipherStr);
		
		// Key
		SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
		// Cipher Mode
		Cipher cipher = Cipher.getInstance("AES/ECB/NoPadding");
		
		// Algorithm
		if (cbc == true) {
			String plaintext = new String();
			for (int i = 16; i < cipherText.length; i += 16) {
				byte[] ivByte = Arrays.copyOfRange(cipherText, (i-16), i);
				byte[] textByte = Arrays.copyOfRange(cipherText, i, (i+16));
				byte[] xored = new byte[16];
				// Part Decipher
				cipher.init(Cipher.DECRYPT_MODE, key);
				byte[] original = cipher.doFinal(textByte);
				// XORing
				int n = 0;
				for (byte b : original) {
					xored[n] = (byte)(b ^ ivByte[n++]);
				}
				String plainpart = new String(xored);
				plaintext += plainpart;
			}
			System.out.println(plaintext);
		} else {
			String plaintext = new String();
			byte[] ivByte = Arrays.copyOfRange(cipherText, 0, 16);
			for (int i = 16; i < cipherText.length; i += 16) {
				byte[] textByte = Arrays.copyOfRange(cipherText, i, (i+16));
				byte[] xored = new byte[16];
				// Part Decipher
				cipher.init(Cipher.ENCRYPT_MODE, key);
				byte[] original = cipher.doFinal(ivByte);
				// XORing
				int n = 0;
				for (byte b : textByte) {
					xored[n] = (byte)(b ^ original[n++]);
				}
				String plainpart = new String(xored);
				plaintext += plainpart;
				ivByte = increment(ivByte);
			}
			System.out.println(plaintext);
		}
	}
	
	static void aesCBC(String keyStr, String cipherStr) throws Exception{
		// CipherText string
		String ctStr = cipherStr.substring(32, cipherStr.length());
		// IV string
		String ivStr = cipherStr.substring(0, 32);

		//CBC mode
		//Cipher
		// byte[] cipherBytes = hexStringToByteArray(cipherStr);
		//Key 16 bits 
		byte[] keyBytes = hexStringToByteArray(keyStr);
		//IV 16 bits
		byte[] ivBytes = hexStringToByteArray(ivStr);
		//CipherText
		byte[]  cipherText = hexStringToByteArray(ctStr);

		//Initialisation
		SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
		IvParameterSpec ivSpec = new IvParameterSpec(ivBytes);

		//Mode
		Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");

		cipher.init(Cipher.DECRYPT_MODE, key, ivSpec);  
		byte [] original = cipher.doFinal(cipherText);
		String plaintext = new String(original);
		System.out.println(plaintext);
	}
	
	static void aesCTR(String keyStr, String cipherStr) throws Exception{
		// CipherText string
		String ctStr = cipherStr.substring(32, cipherStr.length());
		// IV string
		String ivStr = cipherStr.substring(0, 32);

		//CTR mode
		//Cipher
		// byte[] cipherBytes = hexStringToByteArray(cipherStr);
		//Key 16 bits 
		byte[] keyBytes = hexStringToByteArray(keyStr);
		//IV 16 bits
		byte[] ivBytes = hexStringToByteArray(ivStr);
		//CipherText
		byte[]  cipherText = hexStringToByteArray(ctStr);

		//Initialisation
		SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
		IvParameterSpec ivSpec = new IvParameterSpec(ivBytes);

		//Mode
		Cipher cipher = Cipher.getInstance("AES/CTR/NoPadding");

		cipher.init(Cipher.DECRYPT_MODE, key, ivSpec);  
		byte [] original = cipher.doFinal(cipherText);
		String plaintext = new String(original);
		System.out.println(plaintext);
	}
	
	public static void main(String[] args) throws Exception
	{
		// TODO Auto-generated method stub

		// CBC Cipher string 1
		String cipherCbc1 = new String("4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81");
		// CBC Cipher string 2
		String cipherCbc2 = new String("5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253");
		// CBC Key string
		String keyCbc = new String("140b41b22a29beb4061bda66b6747e14");
		// CTR Cipher string 1
		String cipherCtr1 = new String("69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329");
		// CTR Cipher string 2
		String cipherCtr2 = new String("770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451");
		// CTR Key string
		String keyCtr = new String("36f18357be4dbd77f050515c73fcf9f2");
        
		System.out.println("Library modes implementation:");
		
		aesCBC(keyCbc, cipherCbc1);
		aesCBC(keyCbc, cipherCbc2);
		
		aesCTR(keyCtr, cipherCtr1);
		aesCTR(keyCtr, cipherCtr2);
		
		System.out.println("My modes implementation:");
		
		aesECBcbc(keyCbc, cipherCbc1, true);
		aesECBcbc(keyCbc, cipherCbc2, true);
		
		aesECBcbc(keyCtr, cipherCtr1, false);
		aesECBcbc(keyCtr, cipherCtr2, false);
		
	}
}
