import argparse
import logging
import yaml

"""
Reads a yaml file and returns the dict
"""
def readYaml(fileName):
    with open(fileName,"r") as file:
        try:
            y = yaml.safe_load(file)
            return y
        except Exception as e:
            print(e)

def recursiveCompare(orig,new,path="",diffs=None):
    if diffs is None:
        diffs = []
    
    if type(orig) != type(new):
        diffs.append(f"Diferencia de tipos en la ruta '{path}': {type(orig).__name__ } != {type(new).__name__}")
    
    if isinstance(orig,dict):
        if not isinstance(new,dict):
            diffs.append(f"Diferencia de tipos en la ruta '{path}'")
        else:    
            for key in orig:              
                if key not in new:
                    diffs.append(f"Key '{key}' no se encuentra en el nuevo objeto en la ruta '{path}'")
                else:
                    recursiveCompare(orig[key],new[key],path+"."+key,diffs)
            for key in new:
                if key not in orig:
                    diffs.append(f"Key '{key}' no se encuentra en el original en la ruta '{path}'")
    elif isinstance(orig,list):
        if not isinstance(new,list):
            diffs.append(f"Diferencia de tipos en la ruta '{path}'")
        
        elif len(orig) != len(new):
            diffs.append(f"La longitud de la lista no encaja en la ruta '{path}': {len(orig)} != {len(new)}")
        for i,(item1,item2) in enumerate(zip(orig,new)):
            recursiveCompare(item1,item2,path+f".[{i}]",diffs)

    else:
        if orig!=new:
            diffs.append(f"Diferencia de valores en la ruta '{path}': {orig} != {new}")
    if not diffs:
        return None
    return diffs



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='diff Yaml')
    parser.add_argument('--orig',help='original file')
    parser.add_argument('--new',help='new file')

    args = parser.parse_args()
    orig = readYaml(args.orig)
    new = readYaml(args.new)

    result = recursiveCompare(orig,new)
    if result:
        for diff in result:
            print(diff)
    else:
        print("Los archivos son idénticos")


    