<template>
  <el-button class="setting-btn" type="primary" icon="el-icon-setting" @click="handleClick"></el-button>
</template>
<style lang="scss" scoped>
.setting-btn {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  width: 40px;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  position: fixed;
  top: 50%;
  right: 0;
}
</style>
<script lang="ts">
import { Component, Vue, namespace } from 'nuxt-property-decorator'

const app = namespace('app')

@Component({
  components: {
  }
})
export default class SettingBtn extends Vue {
  @app.Getter currentApp

  handleClick() {
    this.$router.push(`/app/light/${this.currentApp.id}`)
  }

  created () {
  }
}
</script>
