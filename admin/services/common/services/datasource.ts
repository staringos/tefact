export default (request) => {
  return {
    getDataSource: (appId) => request({
      url: `/app/light/${appId}/data-source`,
      method: 'get',
    }),
  }
}
