import base64
import json
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, render_template
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests


app = Flask(__name__)


@app.route("/isimage/", methods=['POST'])
def isimage():
    if request.method == 'POST':
        dict_data = request.get_json()
        img_data = dict_data.get('image')
        if img_data:
            img = base64.b64decode(img_data)
            img = BytesIO(img)
            img = Image.open(img)
            #img = np.array(img) 오류나면 주석 풀기 아마 안풀어도 될듯!
            if img != None:
                #########################################

                # Blip1 모델과 프로세서 로드
                processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
                model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

                # 이미지를 텍스트로 변환
                inputs = processor(images=img, return_tensors="pt")
                outputs = model.generate(**inputs, max_new_tokens=50)

                # 'outputs'를 사용하여 텍스트 설명 얻기
                text_description = processor.decode(outputs[0], skip_special_tokens=True)
                print(text_description)
                result = text_description + "/" + enTOKo(text_description)
                return jsonify(result), 200
            else:
                print("no Img")
                return jsonify("no Img"), 200
        else:
            print("No image data provided")
            return jsonify("No image data provided"), 200

def enTOKo(text):
    client_id = "YOUR-ID"
    client_secret = "YOUR-SECRET"

    data = {'text': text,
            'source': 'en',
            'target': 'ko'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id": client_id,
              "X-Naver-Client-Secret": client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if (rescode == 200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        print(trans_data)
        return trans_data
    else:
        print("Error Code:", rescode)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


