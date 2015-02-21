import json, os, re, subprocess

def resolve(stringToResolve):
    output = subprocess.Popen("MAVEN_OPTS='-Xmx2g' mvn exec:java -Dexec.mainClass='com.bericotech.clavin.Resolve' -DstringForClavin='" + stringToResolve + "'", cwd=os.path.dirname(os.path.realpath(__file__)) + "/clavin-java", shell=True, stdout=subprocess.PIPE).stdout.read()
    try:
        return json.loads(re.search("{\"locations.*}]}", output).group(0))
    except:
        return None
