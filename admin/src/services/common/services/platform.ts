export default (request) => {
  return {
    reConfigAndRestart: () => request({
      url: '/platform/config',
      method: 'post',
    }),
    getPlatformConfig: () => request({
      url: '/platform/config',
      method: 'get',
    }),
    savePlatformConfig: (key, config) => request({
      url: '/platform/config',
      method: 'put',
      data: {
        key,
        config_json: config,
      },
    }),
  }
}
