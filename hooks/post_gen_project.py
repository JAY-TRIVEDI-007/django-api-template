import json
import os
import shutil
import sys
import venv
import string
import random


try:
    random = random.SystemRandom()
except NotImplementedError:
    pass


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def generate_random_string(length, using_digits=False, using_ascii_letters=False, using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def remove_open_source_license_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        try:
            os.remove(file_name)
        except Exception:
            pass


def rename_example_secrets():
    """
    Rename example.secrets.json to .secrets.json
    """
    os.rename("example.secrets.json", ".secrets.json")
    os.rename("deployment/django/example.env", "deployment/django/.env")
    os.rename("deployment/database/mysql.env", "deployment/database/.env")
    print(f"{SUCCESS}Secret files renamed.{TERMINATOR}")


def setup_dev_environment():
    """
    Create virtual env
    Install requirements
    Make migrations
    """
    python_version = sys.version_info
    venv_path = os.path.join(os.getcwd(), "venv")

    print(f"{INFO}Python version: {python_version[0]}.{python_version[1]}.{python_version[2]}{TERMINATOR}")
    print(f"{INFO}Creating virtual env at '{venv_path}'{TERMINATOR}")
    venv.create(venv_path, with_pip=True)
    print(f"{INFO}Installing requirements{TERMINATOR}")
    os.system(f"{venv_path}/bin/pip install -r requirements.txt")
    os.system(f"{venv_path}/bin/pip install -r requirements_dev.txt")
    print(f"{SUCCESS}Requirements installed{TERMINATOR}")


def set_generated_secrets():
    db_password = generate_random_string(10, True, True)
    app_secret = generate_random_string(51, True, True, True)

    # Update .secrets.json file
    with open(".secrets.json", "r+") as fp:
        secrets_dict = json.load(fp)
        secrets_dict["DJANGO_SECRET_KEY"] = app_secret
        secrets_dict["DB"]["PASSWORD"] = db_password

        fp.seek(0)
        json.dump(secrets_dict, fp, indent=2)
        fp.truncate()

    # Update init.sql file
    with open(os.path.join(os.getcwd(), "deployment/database/init.sql"), "r+") as f:
        file_contents = f.read().replace("<APP_PASSWORD>", db_password)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    # Update django example.env file
    with open(os.path.join(os.getcwd(), "deployment/django/.env"), "r+") as f:
        file_contents = f.read().replace("<APP_PASSWORD>", db_password)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    print(f"{SUCCESS}Generated secrets updated to the secret file successfully.{TERMINATOR}")


def main():
    # Remove license file if not open source
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_license_files()

    rename_example_secrets()

    if "{{ cookiecutter.create_venv }}" == "y":
        setup_dev_environment()

    set_generated_secrets()

    if "{{ cookiecutter.use_nginx_proxy }}" == "n":
        shutil.rmtree(os.path.join(os.getcwd(), "deployment/nginx/"), ignore_errors=True)
        print(f"{INFO}nginx deployment removed.{TERMINATOR}")

    if "{{ cookiecutter.initialize_git }}" == "y":
        os.system(f"git init -q -b main {os.getcwd()}")
        print(f"{SUCCESS}Git init successful.{TERMINATOR}")

    if "{{ cookiecutter.first_commit }}" == "y":
        project_name = "{{ cookiecutter.project_name }}"
        os.system(f"git add {os.getcwd()}")
        os.system(f"git commit -m '{project_name} created.'")
        print(f"{SUCCESS}Initial commit successful.{TERMINATOR}")

    print(f"{SUCCESS}Project initialized, keep up the good work!{TERMINATOR}")


if __name__ == '__main__':
    main()
