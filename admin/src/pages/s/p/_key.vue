<template>
  <el-container class="share-page-wrapper" v-loading="!info">
    <RequestPasswordDialog :info="info" :auth="auth" @authed="handleAuth" />
    <SharePage v-if="auth && pageData" :page="pageData" />
  </el-container>
</template>
<style lang="scss">
  .share-page-wrapper {
    min-height: 100%;
  }
</style>
<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator'
import { service } from '~/utils'

import RequestPasswordDialog from '~/components/share/RequestPasswordDialog.vue';
import SharePage from '~/components/share/SharePage.vue';
import { Page } from "~/services/common/entities/entities"
import { SharePageEntity } from "~/utils/entities/Share"

@Component({
  layout: "Share",
  components: {
    RequestPasswordDialog, SharePage
  }
})
export default class Share extends Vue {
  key: string | null = null
  info: SharePageEntity | null = null
  auth: boolean = false
  pageData: Page | null = null

  mounted() {
    this.refresh()
  }

  handleAuth(pageData) {
    this.auth = true;
    this.pageData = pageData;
    sessionStorage.setItem((this.key as any), JSON.stringify(this.pageData));
  }

  async refresh() {
    const loading = this.$loading({
      lock: true,
      text: '加载中...',
      spinner: 'el-icon-loading',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    const key = this.$route.params.key;
    this.key = key;
    if (!this.key) {
      location.href = "/s/404"
      return
    }

    const cache = sessionStorage.getItem(key)
    if (cache) {
      try {
        this.pageData = JSON.parse(cache)
        this.info = { key: this.key } as any
        this.auth = true

        loading.close();
        return;
      } catch(e) {
        sessionStorage.removeItem(key)
      }
    }

    const res = await service.app.getSharePageInfo(this.key);

    if (!res || !res.data) {
      location.href = "/s/404"
      return
    }

    this.info = res.data?.data as SharePageEntity

    if (this.info.type === "free") {
      this.auth = true
      const pageData = await service.app.getSharePageDetails(this.info.key)
      this.handleAuth(pageData.data.data)
      loading.close();
    }
  }
}
</script>
