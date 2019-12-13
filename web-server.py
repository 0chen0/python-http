 
import flask
import os
import sys
import json
from flask import request
from flask import Response
 
 
interface_path = os.path.dirname(__file__)
sys.path.insert(0, interface_path)  # 将当前文件的父目录加入临时系统变量
 
 
app = flask.Flask(__name__)
 
 
def file_iterator(file_path, chunk_size=512):
    """
        文件读取迭代器
    :param file_path:文件路径
    :param chunk_size: 每次读取流大小
    :return:
    """
    with open(file_path, 'rb') as target_file:
        while True:
            chunk = target_file.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break
 
 
def to_json(obj):
    """
        放置
    :return:
    """
    return json.dumps(obj, ensure_ascii=False)
 
 
# 下载
@app.route('/download', methods=['GET'])
def download():
    """
        文件下载
    :return:
    """
    file_path = request.values.get('filepath')
    if file_path is None:
        return to_json({'success': 0, 'message': '请输入参数'})
    else:
        if file_path == '':
            return to_json({'success': 0, 'message': '请输入正确路径'})
        else:
            if not os.path.isfile(file_path):
                return to_json({'success': 0, 'message': '文件路径不存在'})
            else:
                filename = os.path.basename(file_path)
                response = Response(file_iterator(file_path))
                response.headers['Content-Type'] = 'application/octet-stream'
                response.headers["Content-Disposition"] = 'attachment;filename="{}"'.format(filename)
                return response
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)