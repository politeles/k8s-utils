import argparse
import logging
import yaml
from subprocess import check_output

def getDeployment(helm,outName,index=0):
    try:
      if type(helm) is str:
        y = yaml.safe_load(helm)
      else:
        y = helm
      f = yaml.dump(y['items'][index])
    except yaml.YAMLError as exc:
      print(exc)
    with open(outName,'w') as file:
        try:
            file.write(f)
        except Exception as e:
            print(e)

"""
Reads a yaml file and returns the dict
"""
def readYaml(fileName):
    with open(fileName,"r") as file:
        try:
            y = yaml.safe_load(file)
            print(type(y))
            return y
        except Exception as e:
            print(e)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deployment generator')
    parser.add_argument('--component',help='Component or list of components to generate the deployment')
    parser.add_argument('--path',help='base path')
    parser.add_argument('--chart',help='path for charts')
    parser.add_argument('--values',help='path for values assuming is not path/values/values-env.yaml')
    parser.add_argument('--env',help='Environment: int, pre, prod')
    parser.add_argument('--deployment',help='Get the first element from the yaml file works in combination with component')



    args = parser.parse_args()
    components = args.component.split(',')
    values = args.values
    if values is None:
        values = 'values\\'
    # print(args.path)
    for comp in components:
        print("Working on component: " +comp)
        if args.deployment == 'True':
            y = readYaml(comp+".yaml")
            getDeployment(y,comp+"-deployment.yaml")

        else:
            helmPath = "\""+args.path+args.chart+"\\"+comp+"\""
            valuesPath = "\""+args.path + values+comp+'\\values-'+args.env+'.yaml'+"\""
            out = check_output(".\helm.exe template %s -f %s"%(helmPath,valuesPath ), shell=True)
            getDeployment(out,comp+'.yaml')

        #print(out)



