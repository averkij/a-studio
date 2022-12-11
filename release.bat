REM sentence-transformers-v2 (50+ langs)

xcopy /y %~dp0\release\st.config.py %~dp0\release\config.py
xcopy /y %~dp0\release\st.dockerignore %~dp0\.dockerignore

docker build . -t aligner
docker tag aligner lingtrain/studio:v8.4
docker push lingtrain/studio:v8.4

REM LABSE (105+ langs)

xcopy /y %~dp0\release\labse.config.py %~dp0\release\config.py
xcopy /y %~dp0\release\labse.dockerignore %~dp0\.dockerignore

docker build . -t aligner
docker tag aligner lingtrain/studio:v8.4-labse
docker push lingtrain/studio:v8.4-labse

REM rubert-tiny (ru-en)

xcopy /y %~dp0\release\tiny.config.py %~dp0\release\config.py
xcopy /y %~dp0\release\tiny.dockerignore %~dp0\.dockerignore

docker build . -t aligner
docker tag aligner lingtrain/studio:v8.4-tiny
docker push lingtrain/studio:v8.4-tiny