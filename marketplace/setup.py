import os
import sys
from xml.etree import ElementTree
from subprocess import Popen, PIPE
import shutil


print("Installing, please wait!...")

if getattr(sys, 'frozen', False):
	# frozen
	path = os.path.dirname(sys.executable) + "/"
else:
	# unfrozen
	path = os.path.dirname(os.path.realpath(__file__)) + "/"

user_dir = os.path.expanduser("~") + "/"

if os.path.isdir(user_dir + "RetroPie/"):
	retropie_dir = user_dir + "RetroPie/"
else:
	print("Could not found the RetroPie-Dir!")
	exit()

# GET FILE-PERMISSION:
if os.path.isfile(retropie_dir + "/marketplace/runcommand.sh"):
	file_permission = os.stat(retropie_dir + "/marketplace/runcommand.sh").st_mode
else:
	file_permission = None


# UPDATE SYSTEM-PACKAGES
update_system = Popen('sudo apt-get update', shell=True, stdin=PIPE )
out, err = update_system.communicate()
print(out)


# INSTALL PACKAGES:
from packages import install_packages
install_packages()

# INSTALL VENV:
from venv.install_venv import install_venv
if not install_venv(path + "/marketplace/core/venv/"):
	print("ERROR on install the virtual environment plus the requirement packages for python!")
	exit()

# DELETE OLD MARKETPLACE-FOLDER:
if os.path.isdir(retropie_dir + "/marketplace"):
	shutil.rmtree(retropie_dir + "/marketplace")

# COPY MARKETPLACE-FOLDER
shutil.copytree(path + "/marketplace", retropie_dir + "/marketplace")

# SET FILE-PERMISSIONS IF POSSIBLE:
if file_permission:
	for root, dirs, files in os.walk(retropie_dir + "/marketplace"):
		for file in files:
			os.chmod(root + "/" + file, file_permission)

# ADD MARKETPLACE AS A SYSTEM TO THE "es_systems.cfg"_FILE
es_systems_new_root = ElementTree.parse(path + "es_systems.cfg").getroot()
xml_path = es_systems_new_root.findall(".//path")[0]

xml_path.text = retropie_dir + "marketplace/menu"

xml_command = es_systems_new_root.findall(".//command")[0]
xml_command_text = xml_command.text
xml_command.text = retropie_dir + "marketplace/" + xml_command_text

es_systems_path = "/etc/emulationstation/es_systems.cfg"

es_systems = ElementTree.parse(es_systems_path)

es_systems_root = es_systems.getroot()

skip_es_systems = False
for name in es_systems_root.findall('.//name'):
	if name.text == "marketplace":
		skip_es_systems = True

if not skip_es_systems:
	xml_marketplace_system = es_systems_root.append(es_systems_new_root)

	es_systems.write(open(path + "es_systems_NEW.cfg", "w"), encoding='utf8')

	copy_es_systems = Popen("sudo sh " + path + "setup_helper.sh " + path + "es_systems_NEW.cfg " + es_systems_path, stdin=PIPE, stdout=PIPE, shell=True)  # THIS NEEDS ADMIN-RIGHTS!!!!

	copy_es_systems.wait()

	set_rights_to_files1 = Popen('find ' + retropie_dir + 'marketplace/ -type f -iname "*.sh" -exec chmod +x {} \\;', stdin=PIPE, stdout=PIPE, shell=True)	
	set_rights_to_files1.wait()
	set_rights_to_files2 = Popen('find ' + retropie_dir + 'marketplace/ -type f -iname "*.py" -exec chmod +x {} \\;', stdin=PIPE, stdout=PIPE, shell=True)
	set_rights_to_files2.wait()
	set_rights_to_files3 = Popen('find ' + retropie_dir + 'marketplace/ -type f -iname "python" -exec chmod +x {} \\;', stdin=PIPE, stdout=PIPE, shell=True)
	set_rights_to_files3.wait()
	set_rights_to_files4 = Popen('chmod +x ' + retropie_dir + 'marketplace/core/tools/*', stdin=PIPE, stdout=PIPE, shell=True)
	set_rights_to_files4.wait()

shutil.rmtree(path)

print("DONE!")
