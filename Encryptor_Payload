using System;
using System.IO;
using System.Security.Cryptography;

public class EncryptDecrypt
{
    public static void Main(string[] args)
    {
        // AES Encryption Key
        byte[] key = { 0x13, 0x37, 0x13, 0x37, 0x03, 0x07, 0x05, 0x0a, 0x2d, 0xa5, 0x5a, 0x1c, 0x3c, 0x4a, 0xab, 0x13 };

        // ENCRYPT DATA
        try
        {
            File.WriteAllText(@"C:\encrypted.txt", "Encrypted Text");

            // create file stream
            using FileStream myStream = new FileStream(@"C:\encrypted.txt", FileMode.OpenOrCreate);

            // configure encryption key.  
            using Aes aes = Aes.Create();
            aes.Key = key;

            // store IV
            byte[] iv = aes.IV;
            myStream.Write(iv, 0, iv.Length);
            using CryptoStream cryptStream = new CryptoStream(
                myStream,
                aes.CreateEncryptor(),
                CryptoStreamMode.Write);

            // write to filestream
            using StreamWriter sWriter = new StreamWriter(cryptStream);

            Console.WriteLine("[+] Encrypted the Data in File encrypted.txt\n");

        }
        catch
        {
            // error  
            Console.WriteLine("[+] Encryption Failed!");
            throw;
        }

        // SHOW ENCRYPTED DATA
        try
        {
            string text = System.IO.File.ReadAllText(@"C:\encrypted.txt");

            // encrypted data
            Console.WriteLine("Encrypted Data: {0}\n", text);

        }
        catch
        {
            throw;
        }
        // DECRYPT DATA
        try
        {
            using FileStream myStream = new FileStream(@"c:\encrypted.txt", FileMode.Open);
            using Aes aes = Aes.Create();
            byte[] iv = new byte[aes.IV.Length];
            myStream.Read(iv, 0, iv.Length);

            // decrypt data
            using CryptoStream cryptStream = new CryptoStream(
               myStream,
               aes.CreateDecryptor(key, iv),
               CryptoStreamMode.Read);
            using StreamReader sReader = new StreamReader(cryptStream);

            // display stream
            Console.WriteLine("\n[+] The File c:\encrypted.txt Has Been Decrypted.\n");
            Console.WriteLine("Decrypted data: {0}", sReader.ReadToEnd());
            Console.ReadKey();
        }
        catch
        {
            // error
            Console.WriteLine("[+] Decryption Failed!\n");
            throw;
        }
    }
}
