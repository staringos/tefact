import os
import importlib


if not os.path.isfile('pid.txt'):
    raise Exception('没有找到pid文件')
with open('pid.txt', 'r') as f:
    pid = f.read()
print('====kill flask process====')
kill_process = os.system('kill -9 {}'.format(pid))
if int(kill_process) != 0:
    print('kill error')
print('====loading web config====')
init_web = os.system(f'./bin/startup.ts')
print(f'====>{init_web}')
if init_web != 0:
    print('init web error')
print('====init data====')
os.system('python manage.py init-data')
print('====start flask====')
main_process = importlib.machinery.SourceFileLoader('app','main.py').load_module()
main_process.app.run()
