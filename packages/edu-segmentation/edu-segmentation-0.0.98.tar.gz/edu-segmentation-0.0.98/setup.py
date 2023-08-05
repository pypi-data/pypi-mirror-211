from setuptools import setup
from setuptools.command.install import install
import os


# Download your models from a specific URL
def download_models():
    print("download models was being accessed")
    import requests
    # function is placed here because requirements.txt needs to be downloaded first to get requests
    def download_torch_models(model_folder, model_name):
        username = "patrialyx"
        repo_name = "edu-segmentation-models"
        tag = "v1.0.0"
        model_url = f"https://github.com/{username}/{repo_name}/releases/download/{tag}/{model_name}"
        model_path = os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies/{model_name}")

        response = requests.get(model_url)

        with open(model_path, "wb") as f:
            f.write(response.content)

    # just automatically download all models for the user

    # download bert-uncased
    try:
        model_name = "BERT_token_classification_final.pth"
        model_folder = "BERTTokenClassification"
        path_to_exist = os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies")
        if not os.path.exists(path_to_exist):
            os.makedirs(path_to_exist)
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies/{model_name}")):
            print(f"Segbot BERT-uncased Model has already been downloaded.")
            pass
        else:
            print("Downloading Segbot BERT-uncased Model...")
            download_torch_models(model_folder, model_name)
            print("Segbot BERT-uncased Model downloaded successfully.")
    except:
        print("Failed to download BERT-uncased Segbot Model.")
    
    # download bert-cased
    try:
        model_name = "BERT_token_classification_final_cased.pth"
        model_folder = "BERTTokenClassification"
        path_to_exist = os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies")
        if not os.path.exists(path_to_exist):
            os.makedirs(path_to_exist)
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies/{model_name}")):
            print(f"Segbot BERT-cased Model has already been downloaded.")
            pass
        else:
            print("Downloading Segbot BERT-cased Model...")
            download_torch_models(model_folder, model_name)
            print("Segbot BERT-cased Model downloaded successfully.")
    except:
        print("Failed to download BERT-cased Segbot Model.")
    
    # download original segbot model
    try:
        model_name = "model_segbot.torchsave"
        model_folder = "BARTTokenClassification"
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies/{model_name}")):
            # print(f"Original Segbot Model has already been downloaded.")
            pass
        else:
            # print("Downloading Original Segbot Model...")
            download_torch_models(model_folder, model_name)
            # print("Original Segbot Model downloaded successfully.")
    except:
        print("Failed to download Original Segbot Model.")

    # download bart model
    try:
        model_name = "model_segbot_bart.torchsave"
        model_folder = "BARTTokenClassification"
        if os.path.isfile(os.path.join(os.path.dirname(__file__), f"{model_folder}/model_dependencies/{model_name}")):
            print(f"Segbot BART Model has already been downloaded.")
        else:
            print("Downloading Segbot BART Model...")
            download_torch_models(model_folder, model_name)
            print("Segbot BART Model downloaded successfully.")
    except:
        print("Failed to download Segbot BART Model.")



class InstallCommand(install):
    def run(self):
        # Call the parent install command
        install.run(self)
        print("this command was being run")
        # Download your models from the GitHub release
        download_models()

print("setup.py was being run.")

setup(
    name='edu-segmentation',
    version='0.0.98',
    description='To improve EDU segmentation performance using Segbot.',
    author='Your Name',
    author_email='you@example.com',
    install_requires=[
        'attrs==23.1.0',
        'bleach==6.0.0',
        'build==0.10.0',
        'CacheControl==0.12.11',
        'certifi==2022.12.7',
        'charset-normalizer==3.1.0',
        'cleo==2.0.1',
        'click==8.1.3',
        'colorama==0.4.6',
        'crashtest==0.4.1',
        'distlib==0.3.6',
        'docutils==0.19',
        'dulwich==0.21.3',
        'filelock==3.12.0',
        'fsspec==2023.4.0',
        'html5lib==1.1',
        'huggingface-hub==0.14.1',
        'idna==3.4',
        'importlib-metadata==6.6.0',
        'installer==0.7.0',
        'jaraco.classes==3.2.3',
        'Jinja2==3.1.2',
        'joblib==1.2.0',
        'jsonschema==4.17.3',
        'keyring==23.13.1',
        'lockfile==0.12.2',
        'markdown-it-py==2.2.0',
        'MarkupSafe==2.1.2',
        'mdurl==0.1.2',
        'more-itertools==9.1.0',
        'mpmath==1.3.0',
        'msgpack==1.0.5',
        'networkx==3.1',
        'nltk==3.8.1',
        'numpy==1.24.3',
        'packaging==23.1',
        'pexpect==4.8.0',
        'pkginfo==1.9.6',
        'platformdirs==2.6.2',
        'poetry==1.4.2',
        'poetry-core==1.5.2',
        'poetry-plugin-export==1.3.1',
        'ptyprocess==0.7.0',
        'Pygments==2.15.1',
        'pyproject_hooks==1.0.0',
        'pyrsistent==0.19.3',
        'pywin32-ctypes==0.2.0',
        'PyYAML==6.0',
        'rapidfuzz==2.15.1',
        'readme-renderer==37.3',
        'regex==2023.3.23',
        'requests==2.29.0',
        'requests-toolbelt==0.10.1',
        'rfc3986==2.0.0',
        'rich==13.3.5',
        'shellingham==1.5.0.post1',
        'six==1.16.0',
        'sympy==1.11.1',
        'tokenizers==0.13.3',
        'tomlkit==0.11.8',
        'torch==2.0.0',
        'tqdm==4.65.0',
        'transformers==4.28.1',
        'trove-classifiers==2023.4.25',
        'twine==4.0.2',
        'typing_extensions==4.5.0',
        'urllib3==1.26.15',
        'virtualenv==20.21.1',
        'webencodings==0.5.1',
        'zipp==3.15.0',
    ],
    cmdclass={'install': InstallCommand}
)
