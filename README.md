## 앱 RISE 의 서버 일부 기능

/isimage 엔드포인트로 REST API 통신 POST 형식의 통신을 해서 이미지를 받는다.

Flask를 사용했고 blip-image-captioning 모델을 사용하여 이미지의 설명 값을 도출했다.

그리고 설명값을 번역해서 다시 전달하는 기능이다.
