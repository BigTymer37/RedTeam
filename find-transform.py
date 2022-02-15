import subprocess


ip_address = input("What IP address do you want to scan? ")

transforms = []

def create_transforms():
        encryptions = ["1","2","3","4","5","6","7/128","7/192","7/256","8"]
        hashes = ["1","2","3","4","5","6"]
        authentications = ["1","2","3","4","5","6","7","8","64221","64222","64223","64224","65001","65002","65003","65004","65005","65006","65006","65007","65008","65009","65010"]
        groups = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
        for encryption in encryptions:
            for hash in hashes:
                for authentication in authentications:
                    for group in groups:
                        print("--trans="+encryption+','+hash+','+authentication+','+group)
                        transform = ("--trans="+encryption+','+hash+','+authentication+','+group)
                        transforms.append(transform)
create_transforms()

def find_transforms():
        try:
            for transform in transforms:
                try:
                    command = str("""ike-scan -M -A %s %s -P hash.txt""") % (transform.strip(),ip_address)
                    print(command)
                    findtransform_results = subprocess.Popen((command),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                    (findtransform_results_stdout, findtransform_results_stderr) = findtransform_results.communicate()
                    print(findgroup_results_stdout)
                    print(findgroup_results_stderr)
                except:
                	pass
        except:
        	pass
find_transforms()
