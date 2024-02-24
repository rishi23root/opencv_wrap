# create a new build for the project
import os
from constants import VERSION,FOLDER_NAME

def updated_version(old_version):
    # old_version = old_version.split('.')

    major_release, minor_release, revision = (int(i) for i in old_version.split('.'))
    # if revision < 30:
    #     revision += 1
    # else:
    #     revision = 0
    #     if minor_release < 30:
    #         minor_release += 1
    #     else:
    #         minor_release = 0
    #         major_release += 1
    revision += 1

    return f'{major_release}.{minor_release}.{revision}'

    

# remove the old build from the dist folder
print('[info]', 'deleting old build',f'{os.getcwd()}/dist/{FOLDER_NAME}-{VERSION}.tar.gz')
os.system(f'rm {os.getcwd()}/dist/{FOLDER_NAME}-{VERSION}.tar.gz')

# update the version in the constants.py file
with open('./constants.py','r') as f:
    data = f.read()
    # update the version number
    NEW_VERSION = updated_version(VERSION)
    print('[info]', 'new version', NEW_VERSION)

    data = data.replace(f"VERSION='{VERSION}'",f"VERSION='{NEW_VERSION}'")

with open('constants.py','w') as f:
    f.write(data)


# convert the README.md to README.rst
print('[info]', 'converting README.md to README.rst')
os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')



# create a new build
print('[info]', 'creating new build')
os.system(f'python3 setup.py sdist')

# upload to test pypi using twine
print('[info]', 'uploading to test pypi')
os.system(f'twine upload --repository testpypi dist/{FOLDER_NAME}-{NEW_VERSION}.tar.gz')