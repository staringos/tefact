export default {
  gotoAppIndex(app, router) {
    if (app.type === 'light')
      return router.push(`/light/${app.admin_route}`)

    router.push(`/plugins/${app.admin_route}`)
  },

  async loginStatus(scope, loginAction, params) {
    try {
      const res = await loginAction(params)

      if (res.status === 200) {
        scope.$message({ message: '登录成功，欢迎回来～', type: 'success' })
        return scope.$router.push('/admin')
      }

      return scope.$message({ message: res.message, type: 'error' })
    } catch (e) {
      if (e.data && e.data.message) {
        scope.$message({ message: e.data.message, type: 'error' })
        scope.refreshCode && scope.refreshCode()
        return
      }
      switch (e.status) {
        case 500:
          scope.$message({ message: '手机号或验证码格式错误', type: 'error' })
          break
        case 403:
          scope.$message({ message: '手机号或验证码错误', type: 'error' })
          break
        default:
          scope.$message({ message: e.data ? e.data.message : '登录失败', type: 'error' })
      }
      scope.refreshCode && scope.refreshCode()
    }
  },
  deepCopy(object, callback) {
    return Object.keys(object).reduce((output, key) => {
      output[key] = callback.call(this, object[key])
      return output
    }, {})
  },

  getRandomValues() {
    console.log('this is random')
    return 1
  },

  getCookie(cookies: string, name: string) {
    let arr, reg = new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if (!cookies) return null

    if (arr = cookies.match(reg)) {
      return unescape(arr[2])
    } else {
      return null
    }
  }
}
