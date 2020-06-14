class BaseResponse {
  data: any = {}
  code: number = 200
  message: string = ''
}

function response(data: any, code=200, message:string='') {
  const base = new BaseResponse()
  base.data = data
  base.code = code
  base.message = message
  return JSON.stringify(base)
}

export default response


