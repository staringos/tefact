from arrplat.app import app
from arrplat.config import DEBUG
import sys
from arrplat.common.utils import json_response


# 全局异常捕获
# @app.errorhandler(Exception)
# def framework_error(e):
#     print(e)
#     return json_response(data={}, message=str(e), status=500)


if __name__ == '__main__':
    port = 5500
    if len(sys.argv) == 2:
        port = sys.argv[1]
        print(f"端口启动: {port}")
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
