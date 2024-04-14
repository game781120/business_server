#退出环境
deactivate
rm -rf runvenv
#删除当前目录下临时文件
find . -name '__pycache__' -type d -exec rm -rf {} +