import environ
env = environ.Env()
env.read_env(env.str('ENV_PATH', '.env'))
TOKEN = env('TOKEN')
ID = env('ID')
SERVER_KEY = env('SERVER_KEY')
environ.Env.read_env()
from django.core.files.storage import FileSystemStorage
def index(request):
    return render(request, 'translator/capch.html')

from django.shortcuts import render
from googletrans import Translator
import base64
'''def home_page(request):
    # POST - обязательный метод
    if request.method == 'POST' and request.FILES:
        # получаем загруженный файл
        file = request.FILES['myfile1']
        #fs = FileSystemStorage()
        # сохраняем на файловой системе
        filename = fs.save(file.name, file)
        # получение адреса по которому лежит файл
        file_url = fs.url(filename)
        return render(request, 'home_page.html', {
            'file_url': file_url
        })
    return render(request, 'home_page.html')'''


def encode_file(file_path):
  with open(file_path, "rb") as fid:
      file_content = fid.read()
  return base64.b64encode(file_content).decode("utf-8")
def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'translator/upload.html', {'file_url': file_url})
    return render(request, 'translator/upload.html')



def transfer(mytext,lang):
   IAM_TOKEN = TOKEN
   folder_id = ID
   target_language = lang
   texts = mytext

   body = {
    "targetLanguageCode": target_language,
    "texts": texts,
    "folderId": folder_id,
    }

    headers = {
     "Content-Type": "application/json",
     "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    r = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
    json = body,
    headers = headers
    )
    if r['code'] == 200:
        return r['text'][0]
    else:
        return 'error'



def translate_app(request):
 try:
    if request.method == "POST":
        lang = request.POST.get("lang", None)

        txt = request.POST.get("txt", None)


        tr = transfer(txt,lang)
        translator = Translator()
        tr = translator.translate(txt, dest=lang)
        return render(request, 'translator/menu.html', {"result":tr.text})

    return render(request, 'translator/menu.html')
 except Exception as e:
     return render(request, 'translator/menu.html',{"result":"ОШИБКА: Возможно, Вы забыли указать язык!"})

 import requests
 import sys
 import json

 SMARTCAPTCHA_SERVER_KEY =SERVER_KEY
 def get_ip(request):

     ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
     return ip or request.META.get('REMOTE_ADDR')

 def check_captcha(token):
     resp = requests.post(
         "https://smartcaptcha.yandexcloud.net/validate",
         data={
             "secret": SMARTCAPTCHA_SERVER_KEY,
             "token": token,
             "ip": get_ip(request)

         },
         timeout=1
     )
     server_output = resp.content.decode()
     if resp.status_code != 200:
         print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
         return True
     return json.loads(server_output)["status"] == "ok"

 token = request.form["smart-token"]
 if check_captcha(token):
     print("Passed")
 else:
     print("Robot")
