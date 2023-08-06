import json
import sys
import os

if (len(sys.argv)) < 4:
    print('no arguments passed')
    sys.exit()

folderName = sys.argv[2]
notebookName = sys.argv[1]
scriptLanguage = sys.argv[3]

body = {
    'name': os.path.basename(os.path.normpath(notebookName)),
    'properties': {
        'folder': {
            'name': folderName
        }
    }
}

f = open(notebookName + '.ipynb')
notebook_json = json.load(f)

for key in notebook_json:
    body['properties'][key] = notebook_json[key]

if scriptLanguage == 'scala':
    body['properties']['metadata']['kernelspec']['display_name'] = 'scala'
    body['properties']['metadata']['kernelspec']['language'] = 'scala'
    body['properties']['metadata']['kernelspec']['name'] = 'spark_scala'

    body['properties']['metadata']['language_info'] = {
        'name': 'scala'
    }

print(json.dumps(body))