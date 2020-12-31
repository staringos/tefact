<template>
  <el-popover
    placement="top"
    width="330"
    class="share-popover"
    v-model="visible">
    <h3>分享页面</h3>
    <div>
      <div class="share-block">
        <span class="share-title">分享权限</span>
        <div class="share-content">
          <el-radio v-model="form.type" label="free">无权限</el-radio>
          <el-radio v-model="form.type" label="password">密码</el-radio>
          <el-radio v-model="form.type" label="login">登录访问</el-radio>
        </div>
      </div>
      <div class="share-block" v-if="share">
        <span class="share-title">分享信息</span>
        <div class="share-content">
          <el-input class="address" size="mini" :value="address" @keydown="() => false" placeholder="地址"></el-input>
          <el-input v-if="form.type === 'password'" class="password" size="mini" v-model="share.password" @keydown="() => false" placeholder="密码"></el-input>
        </div>
      </div>
      <div class="share-block" v-if="share">
        <span class="share-title"></span>
        <div class="share-content">
          <el-button type="text" @click.stop="handleCopy">点击复制</el-button>
        </div>
      </div>
      <div style="text-align: right; margin: 0">
        <el-button size="mini" type="text" v-if="share" @click="visible = false">取消分享</el-button>
        <el-button type="primary" size="mini" @click="handleShare">分享</el-button>
      </div>
    </div>
    <slot slot="reference"></slot>
  </el-popover>
</template>
<script>
import { Vue, Component, namespace, Prop, Watch } from 'nuxt-property-decorator'
import { DefaultShare } from "@/services/common/entities/share.ts";
import cloneDeep from "lodash/cloneDeep";

const app = namespace('app')

@Component({
  components: {}
})
export default class SharePageEditor extends Vue {
  form = cloneDeep(DefaultShare)
  share = null
  visible = false

  @Prop() page
  @app.Action sharePage

  @Watch("page", { immediate: true })
  handlePageChange() {
    if (this.page.share) {
      this.share = this.page.share
      this.form = cloneDeep(this.page.share)
    }
  }

  get address() {
    if (!this.share) return '';
    const host = window.location.host;
    const protocol = window.location.protocol;
    return `${protocol}//${host}/s/p/${this.share.key}`;
  }

  async handleShare() {
    const res = await this.sharePage({ pageId: this.page.id, type: this.form.type });
    this.share = res.data;
  }

  async handleCopy() {
    let message = `链接：${this.address}`

    if(this.share.type === "password") {
      message += `密码：${this.share.password}`
    }

    this.$copyText(message).then(() => {
      this.$message.success('复制成功')
    }, () => {
      this.$message.error('复制失败，请手动复制')
    })
  }
}
</script>
<style lang="scss" scoped>
.share-block {
  display: flex;
  margin-top: 15px;
  margin-bottom: 15px;

  .share-title {
    width: 60px;
  }

  .share-content {
    flex: 1;
    display: flex;

    .address {
      flex: 1;
    }

    .password {
      width: 68px;
    }
  }
}
</style>
