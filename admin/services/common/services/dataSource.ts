export default (request) => {
  return {
    getAllDataTable: dsId => request({
      url: `/data-source/${dsId}/connect/table`,
      method: 'get',
    }),
    getDataSourceList: (orgId) => request({
      url: `/data-source/org/${orgId}`,
      method: 'get',
    }),
    addDataSource: data => request({
      url: `/data-source/`,
      method: 'post',
      data: data
    }),
    modifyDataSource: (id, data) => request({
      url: `/data-source/${id}`,
      method: 'put',
      data: data
    }),
    deleteDataSource: id => request({
      url: `/data-source/${id}`,
      method: 'delete'
    }),
    testConnect: data => request({
      url: `/data-source/test/`,
      method: 'post',
      data
    }),
  }
}
