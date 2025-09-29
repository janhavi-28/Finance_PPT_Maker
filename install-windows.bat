@echo off
echo Installing FinancePPT AI dependencies for Windows...
echo.

REM Uninstall problematic packages first
pip uninstall -y google-generativeai grpcio grpcio-status protobuf

REM Install grpc first with specific version
pip install grpcio==1.59.0 grpcio-status==1.59.0 protobuf==4.24.4

REM Install google-generativeai with older compatible version
pip install google-generativeai==0.2.2

REM Install remaining requirements
pip install -r requirements-windows-safe.txt

echo.
echo Installation complete! You can now run: streamlit run app.py
pause
