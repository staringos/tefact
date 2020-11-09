export default ({ app: { router } }) => {
  router.afterEach(to => {
    /* 告诉增加一个PV */
    try {
      const win = (window as any)
      win._hmt = win._hmt || []
      win._hmt.push(['_trackPageview', to.fullPath])
    } catch (e) {}
  })
}
