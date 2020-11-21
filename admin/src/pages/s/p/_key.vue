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

@Component({
  layout: "Share",
  components: {
    RequestPasswordDialog, SharePage
  }
})
export default class AppItem extends Vue {
  key: string | null = null
  info: string | null = null
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

    this.info = res.data?.data
  }
}
</script>
