import click
import os
import json

@click.command()
@click.option('--init', help='Creates a new Yugal Project', default='')
@click.option('--install', help='Installs a library in Yugal', default='')
@click.option('--remove', help='Deleted Library and Its files from Yugal Project', default='')
@click.option('--show', help='Show all libraries', default='')
@click.option('--dev', help='Toggles DEV_MODE, enter \'on\' to turn it on and \'off\' to turn production mode on.', default='')

def start(init, install, remove, show, dev):
    if init != "":
        init = init.lower()
        try:
            os.system('git clone https://github.com/sinhapaurush/yugal.git')
            os.system(f"mv yugal {init}")
            os.chdir(init)
            os.system("rm -rf .git")
            os.system("rm LICENSE")
            os.system("rm README.md")

            fh = open('string.php', 'r')
            nl = []
            data = fh.read()
            data = data.replace("--Yugal-Project--", init)
            fh.close()
            fh = open('string.php', 'w')
            fh.write(data)
            fh.close()
            conf = "You Are Good To Go!"
        except FileNotFoundError:
            print("Yugal Project can not be created due to unknown reason, please check your Internet connection")
        else:
            print("="*len(conf))
            print(conf)
            print("="*len(conf))
    if install != "":
        try:
            os.chdir('./lib/')
            os.system(f'git clone {install}')
            libname = install.split("/")
            libname = libname[len(libname) - 1]
            libname = libname.split(".")
            libname = libname[0]
            os.chdir(libname)
            os.system('rm *.md')
            fh = open("lib.json", "r")
            config = fh.read()
            fh.close()
            os.chdir('../')
            fh = open('config.json', 'r')
            uni = fh.read()
            fh.close()
            config = config.strip()
            config = json.loads(config)
            uni = uni.strip()
            uni = json.loads(uni)
            uni[libname] = config
            json_str = json.dumps(uni)
            fh = open('config.json', 'w')
            fh.write(json_str)
            fh.close()
        except:
            print("Unable to install Library")
        else:
            print("Library Installed!")
    if remove != "":
        try:
            os.chdir('./lib/')
            os.system(f'rm -rf {remove}')
            fh = open('config.json', 'r')
            data = fh.read()
            fh.close()
            data = data.strip()
            data = json.loads(data)
            del(data[remove])
            data = json.dumps(data)
            fh = open('config.json', 'w')
            fh.write(data)
            fh.close()
        except Exception:
            print('ERROR: Unable to delete this library.')
            print(Exception)
        else:
            print("Library Deleted!")
    if show != "":
        try:
            os.chdir('./lib/')
            fh = open('config.json', 'r')
            code = fh.read()
            fh.close()
            code = json.loads(code)
            for i in code:
                print(i, code[i]['github'], sep="\t")
        except:
            print("ERROR in fetching installed packages.")
    if dev != "":
        dev = dev.strip()
        try:
            fh = open('string.php', 'r')
            sphp = fh.read()
            fh.close()
            fh = open('string.php', 'w')
            if(dev == 'off'):
                sphp = sphp.replace("define('DEV_MODE', true);", "define('DEV_MODE', false);")
            elif(dev == 'on'):
                sphp = sphp.replace("define('DEV_MODE', false);", "define('DEV_MODE', true);")
            fh.write(sphp)
            fh = fh.close()
            if dev == 'off':
                os.system('chmod 644 *')
                os.system('chmod 755 modules')
                os.system('chmod 755 lib')
                os.system('chmod 755 src')
                os.chdir('modules')
                os.system('chmod 644 *')
            elif dev == 'on':
                os.system('chmod 777 *')
                os.system('chmod 777 modules')
                os.chdir('modules')
                os.system('chmod 777 *')
        except:
            print("ERROR IN TOGGLING MODE")
        else:
            if (dev == 'on'):
                print("DEVELOPER MODE TURNED ON")
            elif (dev == 'off'):
                print("PRODUCTION MODE TURNED ON")


if __name__ == '__main__':
    start()
