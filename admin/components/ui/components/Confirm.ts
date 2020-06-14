export default {
  deleteConfirm: (ctx: any, entityName: string, request: Function, actionName = '移除') => {
    return new Promise((resolve) => {
      ctx.$confirm(`确定要${actionName}该${entityName}吗？`, `${actionName}${entityName}`, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const res = await request()

        if (res.status === 200) {
          resolve()
          return ctx.$message({ type: 'success', message: `${actionName}成功!` })
        }
      }).catch((e: any) => {
        if (e.response) {
          ctx.$message({ message: e.response.data.message, type: 'error' })
        }
      })
    })
  }
}
