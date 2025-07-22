from app.main import app # app/__init__의 app 객체를 가져온다 / FastAPI 앱 자체를 이 파일에서 실행하려고 임포트

if __name__ == "__main__": # 이 파일이 직접 실행 될 때만 아래 코드를 실행
    import uvicorn # uvicorn은 asgi 서버이다. FastAPI 앱을 실제로 실행할 수 있도록 도와주는 서버

    uvicorn.run(app, host="0.0.0.0", port=8000) # FastAPI를 실행하는 실제 명령