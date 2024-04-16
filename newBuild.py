# flake8: noqa: E501
# create a new build for the project
import os
import re


def updated_version(old_version):
    # old_version = old_version.split('.')

    major_release, minor_release, revision = (int(i) for i in old_version.split("."))
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

    return f"{major_release}.{minor_release}.{revision}"


# update the version in the setup.py file
with open("setup.py", "r") as f:
    data = f.read()
    # read the version number from the setup.py file
    VERSION = re.search(r'VERSION = "(.*?)"', data).group(1)
    print("[info]", "old version", VERSION)

    FOLDER_NAME = re.search(r'name="(.*?)"', data).group(1)
    print("[info]", "FOLDER_NAME ", FOLDER_NAME)
    # update the version number
    NEW_VERSION = updated_version(VERSION)
    print("[info]", "new version", NEW_VERSION)
    data = data.replace(f'VERSION = "{VERSION}"', f'VERSION = "{NEW_VERSION}"')
    isUpdated = re.search(r'VERSION = "(.*?)"', data).group(1)
    print("[info]", "updated version", isUpdated)

    # update the package list
    all_packages_old = re.search(r"install_requires=\[([\s\S]*?)\]", data).group(1)
    # print(all_packages_old)
    install_requires = [
        i.replace("\n", "").replace("==", ">=")
        for i in open("requirements.txt", "r").readlines()
    ]
    data = data.replace(
        f"install_requires=[{all_packages_old}]", f"install_requires={install_requires}"
    )

with open("setup.py", "w") as f:
    f.write(data)

# remove the old build from the dist folder
print(
    "[info]", "deleting old build", f"{os.getcwd()}/dist/{FOLDER_NAME}-{VERSION}.tar.gz"
)
os.system(f"rm {os.getcwd()}/dist/{FOLDER_NAME}-{VERSION}.tar.gz")


# convert the README.md to README.rst
print("[info]", "converting README.md to README.rst")
os.system("pandoc --from=markdown --to=rst --output=README.rst README.md")


# create a new build
print("[info]", "creating new build")
os.system(f"python3 setup.py sdist")

# upload to test pypi using twine
print("[info]", "uploading to test pypi")
# os.system(f'twine upload --repository testpypi dist/{FOLDER_NAME}-{NEW_VERSION}.tar.gz')
# os.system(f"twine upload dist/{FOLDER_NAME}-{NEW_VERSION}.tar.gz --verbose")
os.system(f"twine upload dist/{FOLDER_NAME}-{NEW_VERSION}.tar.gz ")
