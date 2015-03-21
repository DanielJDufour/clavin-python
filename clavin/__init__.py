import json, os, re, subprocess

# this is for high-memory machines that have more that 4.5G of memory free
# this essentially downloads geonames and then builds an index
def build():
    ## the code to run after install
    current_directory = os.path.dirname(os.path.realpath(__file__))
    if "clavin-java" in os.listdir(current_directory):
        print "it looks like you have already built the CLAVIN java engine"
    else:
        print "building CLAVIN Java engine. this can take a long time"
        subprocess.call(["curl", "-L", "https://github.com/DanielJDufour/CLAVIN/tarball/3.0", "-o", "clavin-java.tar.gz"], cwd=current_directory)
        subprocess.call(["tar", "-xvzf", "clavin-java.tar.gz"], cwd=current_directory)
        subprocess.call(["rm", "clavin-java.tar.gz"], cwd=current_directory)
        os.rename(d+next(f for f in os.listdir(current_directory) if "DanielJDufour-CLAVIN-" in f),current_directory+"clavin-java")
        subprocess.call("./script/ci/run_build.sh", cwd=current_directory+"clavin-java")

# download is for low-memory machines
# it basically downloads the CLAVIN java engine from an Amazon S3
def download():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    print "current directory is", current_directory
    if "clavin-java" in os.listdir(current_directory):
        print "it looks like you have already downloaded the CLAVIN java engine"
    else:
        urlOfClavinJavaEngine = "https://s3.amazonaws.com/clavinzip/CLAVIN.zip"
        print "downloading clavin from", urlOfClavinJavaEngine
        print "this could take 5 to 10 minutes, depending on your machine and internet connection"
        # try to download with urllib, if that throws an error, use wget
        try:
            import urllib
            urllib.urlretrieve(urlOfClavinJavaEngine,  current_directory + "/CLAVIN.zip")
        except:
            print "you don't have urllib installed, so we're going to use wget instead"
            subprocess.call(["wget", "https://s3.amazonaws.com/clavinzip/CLAVIN.zip"], cwd=current_directory)
        subprocess.call(["unzip", "CLAVIN.zip"], cwd=current_directory)
        subprocess.call(["rm", "CLAVIN.zip"], cwd=current_directory)
        os.rename(current_directory+"/CLAVIN",current_directory+"/clavin-java")
        print "you have successfully downloaded the pre-build CLAVIN java engine"
        

def resolve(stringToResolve):
    output = subprocess.Popen("MAVEN_OPTS='-Xmx2g' mvn exec:java -Dexec.mainClass='com.bericotech.clavin.Resolve' -DstringForClavin='" + stringToResolve + "'", cwd=os.path.dirname(os.path.realpath(__file__)) + "/clavin-java", shell=True, stdout=subprocess.PIPE).stdout.read()
    try:
        return json.loads(re.search("{\"locations.*}]}", output).group(0))
    except:
        return None
