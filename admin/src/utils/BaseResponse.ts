class BaseResponse {
  data: any = {}
  code = 200
  message = ''
}

function response(data: any, code=200, message='') {
  const base = new BaseResponse()
  base.data = data
  base.code = code
  base.message = message
  return JSON.stringify(base)
}

export default response


