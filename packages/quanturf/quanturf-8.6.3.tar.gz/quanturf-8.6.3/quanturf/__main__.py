import os
import typer
import requests
import maskpass
import json
import site
import os
import shutil
from . import quanturf_logo
import fnmatch

app=typer.Typer()

env_dir = site.getsitepackages()[0] + '/' + 'quanturf'
os.environ['JUPYTER_APP_LAUNCHER_PATH'] = env_dir

def get_js_file(site_package_dir, logo_code):
    os.chdir(site_package_dir)
    os.chdir("../")
    os.chdir("../")
    os.chdir("../")
    env_dir = os.getcwd()
    src_files = []

    for file in os.listdir(os.path.join(env_dir, "share", "jupyter", "labextensions", "jupyterlab_templates", "static")):
        if fnmatch.fnmatch(file, '568.*.js'):
            src_files.append(file)

    if src_files:
        src_file_path = os.path.join(env_dir, "share", "jupyter", "labextensions", "jupyterlab_templates", "static", src_files[0])
        src_file_path = src_file_path.replace(os.sep, '/')
        src_file = open(src_file_path, "w")
        src_file.write(logo_code)
        src_file.close()        
        print("Logo code updated successfully.")
    else:
        print("No matching file found.")
    return

@app.command()
def deploy():   
    AUTH_URL="https://quanturf.com/api/auth/"
    URL="https://quanturf.com/api/files/"

    path=os.getcwd()
    dir_list = os.listdir(path)
    files=[]
    for file in dir_list:
        if file != '__pycache__':
            files.append(('file',open(path+'/'+str(file),"rb")))
    
    print("Enter your Quanturf username and password...")
    username=input("Enter Username: ")
    password=maskpass.askpass(mask="*")
    user_auth={'username':username,'password':password}
    user_auth=json.dumps(user_auth)
    headers = {'Content-type': 'application/json'}
    auth_request=requests.post(url=AUTH_URL,data=user_auth,headers=headers)
    auth_response=auth_request.json()
    print(auth_response['message'])

    if auth_response['message'] == 'Authentication Successful!':
        file_upload_request=requests.post(url=URL,files=files)
        file_upload_response=file_upload_request.json()
        print(file_upload_response['message'])

@app.command()
def jupyterlab():

    ## packages
        # jupyterlab_templates --> dropdown menu list of jupyter notebooks
        # jupyter_app_launcher --> jupyter notebook shortcut
    os.system("pip install jupyterlab_templates jupyter_app_launcher")
    os.system("jupyter labextension install jupyterlab_templates")
    os.system("jupyter serverextension enable --py jupyterlab_templates")

    
    print("Running Jupyter platform!")
    out = site.getsitepackages()

    if len(out) == 1:
        str_out = out
        str_out = ' '.join(str_out)

        logo_code=quanturf_logo.logo_js()
        get_js_file(str_out,logo_code)

        jupyterlab_templates=['quanturf.ipynb','download_data.ipynb']
        blankly_templates=['golden_cross.ipynb','MACD.ipynb','mlp_model.ipynb','RSI.ipynb']
        backtrader_alpaca_templates=['BarraFactorModel_FactorBased.ipynb','RelativeStrengthIndex(RSI)_Indicator.ipynb']

        filename = os.path.join(str_out, "quanturf","jupyter_notebook_config.py")
        filename2 = filename.replace(os.sep, '/')

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/jupyterlab_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in  jupyterlab_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path,dst_path)


        try:
            os.remove(dst_path+"Sample.ipynb") 
        except Exception as e:
            print(str(e))

        blankly_template_path=os.path.join(str_out,'jupyterlab_templates/templates/blankly_templates')
        try:
            os.mkdir(blankly_template_path)
        except Exception as e:
            print(str(e))

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/blankly_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in blankly_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path,dst_path)     

        backtrader_alpaca_templates_path=os.path.join(str_out, 'jupyterlab_templates/templates/backtrader_alpaca_templates')
        try:
            os.mkdir(backtrader_alpaca_templates_path)
        except Exception as e:
            print(str(e))

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/backtrader_alpaca_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in backtrader_alpaca_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path, dst_path) 

        os.system("jupyter lab --config=" + filename2)

    if len(out) >= 2:
        str_out = out[1]

        logo_code=quanturf_logo.logo_js()
        get_js_file(str_out,logo_code)

        jupyterlab_templates=['quanturf.ipynb','download_data.ipynb']
        blankly_templates=['golden_cross.ipynb','MACD.ipynb','mlp_model.ipynb','RSI.ipynb']
        backtrader_alpaca_templates=['BarraFactorModel_FactorBased.ipynb','RelativeStrengthIndex(RSI)_Indicator.ipynb']

        filename = os.path.join(str_out, "quanturf","jupyter_notebook_config.py")
        filename2 = filename.replace(os.sep, '/')

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/jupyterlab_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in  jupyterlab_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path,dst_path)


        try:
            os.remove(dst_path+"Sample.ipynb")
        except:
            pass

        blankly_template_path=os.path.join(str_out,'jupyterlab_templates/templates/blankly_templates')
        try:
            os.mkdir(blankly_template_path)
        except:
            pass

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/blankly_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in blankly_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path,dst_path)     
        
        backtrader_alpaca_templates_path=os.path.join(str_out, 'jupyterlab_templates/templates/backtrader_alpaca_templates')
        try:
            os.mkdir(backtrader_alpaca_templates_path)
        except Exception as e:
            print(str(e))

        filename3 = os.path.join(str_out, "jupyterlab_templates/templates/backtrader_alpaca_templates/")
        dst_path = filename3.replace(os.sep, '/')

        for temp in backtrader_alpaca_templates:
            src_path = os.path.join(str_out, "quanturf", temp)
            shutil.copy(src_path, dst_path)

        os.system("jupyter lab --config=" + filename2)
    

if __name__ == "__main__":
    app()
