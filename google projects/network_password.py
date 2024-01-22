import os
import glob


def Get_Name(file):
    wifi_name = (os.path.basename(file).split(".")[0])
    return wifi_name


def GetPasswords(content):
    start = content.find("<keyMaterial>")
    end = content.find("</keyMaterial>")
    wifi_passwords = (content[(start + 13):end])
    return wifi_passwords


def main():
    try:
        x = os.getcwd()
        os.system("netsh wlan export profile folder=" + x + " key=clear ")
        with open("name&passwords.txt", "w+") as f:
            f.write("operation- shalom balahot")
            wifi_files = []
            for file in glob.glob("*.xml"):
                wifi_files.append(file)

            for file in wifi_files:
                with open(file) as xmlfile:
                    content = xmlfile.read()
                    if "keyMaterial" in content:
                        name = Get_Name(file)
                        password = GetPasswords(content)
                        f.write("\n" + "\n" + str(name) + ":\t" + str(password))
            f.seek(0)  # Move the file pointer to the beginning of the file
            content = f.read()
            f.close()
    except Exception as e:
        print("An error occurred:", e)
if __name__ == '__main__':
    main()