FROM unityci/editor:windows-2022.3.10f1
WORKDIR C:\app
COPY . C:\app
RUN powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; \
    choco install oculus-openxr -y"
CMD ["C:\\Program Files\\Unity\\Hub\\Editor\\2022.3.10f1\\Editor\\Unity.exe", "-batchmode", "-nographics", "-quit", "-projectPath", "C:\\app", "-runTests", "-testResults", "C:\\app\\TestResults.xml", "-logfile", "C:\\app\\test.log"]
