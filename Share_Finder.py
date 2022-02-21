import argparse
import subprocess
from time import sleep

#Arg Parser
parser = argparse.ArgumentParser(description='Parse Shares for Sensitive Information')
parser.add_argument('--username', metavar='User', help='Username for Authentication.')
parser.add_argument('--password', metavar='Password', help='Password for Authentication.')
parser.add_argument('--domain', metavar='Domain', help='Domain for Authenticaiton.')
parser.add_argument('--ip', metavar='IP Address', help='IP Address for Shares.')
parser.add_argument('--list', metavar='List of IPs', help='List of IP Addresses to Parse.')
args = parser.parse_args()


#Arrays Utilized
mnt_pts = []


def cme_enum():
	if args.ip:
		command = str('crackmapexec smb %s -u %s -p %s -d %s --shares | anew cmeshares.out') % (args.ip,args.username,args.password,args.domain)
		print(command)
		cme_enum_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
		(cme_enum_results_stdout, cme_enum_results_stderr) = cme_enum_results.communicate()
		print(cme_enum_results_stdout)
	elif args.list:
		command = str('crackmapexec smb %s -u %s -p %s -d %s --shares | anew cmeshares.out') % (args.list,args.username,args.password,args.domain)
		print(command)
		cme_enum_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
		(cme_enum_results_stdout, cme_enum_results_stderr) = cme_enum_results.communicate()
		print(cme_enum_results_stdout)
	else:
		print("\nA Single IP or List Needs to be Provided!")
cme_enum()


def parse_cme_output():
    command = str("""sudo sort -u -k5 cmeshares.out | grep -i 'read\|write' | grep -v 'IPC\|print' | awk '{print $2"/"$5}' | sed 's/\x1b\[[0-9;]*m//g' > sharessorted.txt""")
    cme_parse_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    (cme_parse_results_stdout, cme_parse_results_stderr) = cme_parse_results.communicate()
    print(cme_parse_results_stdout)
parse_cme_output()

def create_mountpoints():
	shares = open('sharessorted.txt', 'r')
	try:
		for share in shares:
			sleep(2)
			command = str('sudo mkdir -p /mnt/%s') % (share[:-1])
			print(command)
			create_mountpoint_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
			(create_mountpoint_results_stdout, create_mountpoint_results_stderr) = create_mountpoint_results.communicate()
			print(create_mountpoint_results_stdout)
	except Exception:
		print("Problem Creating Mountpoint Directories!")
		print(create_mountpoint_restults_stderr)
	shares.close()
create_mountpoints()

def mount_shares():
	shares = open('sharessorted.txt', 'r')
	try:
		for share in shares:
			command = str('sudo mount -t cifs -o username=%s,password=\'%s\',domain=%s //%s /mnt/%s')% (args.username,args.password,args.domain,share[:-1],share[:-1])
			print(command)
			mount_shares_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
			(mount_shares_results_stdout, mount_shares_results_stderr) = mount_shares_results.communicate()
			print(mount_shares_results_stdout)
	except Exception:
		print("Problem Mounting Share: " + share)
		print(mount_shares_results_stderr)
mount_shares()


def check_mounts():
	command = str('ls /mnt/')
	check_mnt_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
	(check_mnt_results_stdout, check_mnt_results_stderr) = check_mnt_results.communicate()
	mnts = check_mnt_results_stdout
	for mnt in mnts.split('\n')[:-1]:
		print("This Mount Was Found: /mnt/" +mnt)
		mnt_pts.append('/mnt/'+mnt +'\n')
check_mounts()

def search_mounts():
	for mnt in mnt_pts:
		mnt_filename = str(mnt[:-1].replace('/mnt/','') +'-results.txt')
		mnt_file = open(mnt_filename, 'w')
		command = str("""rg --type-add 'stratum:*.{config,conf,cnf,ini,php,py,pl,ps1,xml,txt,cs,html,log,myd,secrets,ovpn,pem,key,ppk,id_rsa,crt,cer,db,yml,yaml,tdb,vdb,passwd,vnc,cnt}' -tstratum 'password=|PASSWORD =|PASSWORD=|password =|Password=|apitoken|passwd|credentials|connectionString|cpassword|ftp://|api_token|apikey|APIKEY|API_KEY|API-KEY|api-key|api_key|Bearer |PRIVATE KEY|key=|AccountName=|AccountKey=|aws_access_key_id|aws_secret_access_key|AKIA|AWS_SECRET' """ + mnt)
		print(command)
		search_mnt_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
		(search_mnt_results_stdout, search_mnt_results_stderr) = search_mnt_results.communicate()
		mnt_file.write(str(search_mnt_results_stdout))
		mnt_file.close()
search_mounts()

