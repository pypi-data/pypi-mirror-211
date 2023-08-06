from Pytheas22 import Python_Port_Scanner

data = Python_Port_Scanner.PythonPortScannerList(port_range="22-22")
data = data.make_lst()

scaning = Python_Port_Scanner.PythonPortScanner(data)
scaning.scan_ip_cameras()
