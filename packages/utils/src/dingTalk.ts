import * as request from 'request'

const ApplicationTypeHeader:string = "application/json;charset=utf-8";

export default class DingTalkBot {
  private readonly _webHookUrl:string;
  constructor(webHookUrl: string) {
    this._webHookUrl = webHookUrl;
  }

  public pushMsg (msg: string, atMobiles?: Array<string>): boolean {
    try {
      let options: request.CoreOptions = {
        headers: {
          "Content-Type": ApplicationTypeHeader
        },
        json: {
          "msgtype": "text",
          "text": {
            "content": msg
          },
          "at": {
            "atMobiles": atMobiles == null ? [] : atMobiles,
            "isAtAll": false
          }
        }
      };
      request.post(this._webHookUrl, options, function(error, response, body){
        console.log(`push msg ${msg}, response: ${JSON.stringify(body)}`);
      });

      return true
    } catch(err) {
      console.error(err);
      return false;
    }
  }
}
