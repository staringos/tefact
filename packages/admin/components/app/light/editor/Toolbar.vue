<template>
  <div class="editor-toolbar">
    <i class="el-icon-arrow-left"></i>
    <div class="page-title">
      {{page.title}}
      <i class="el-icon-edit"></i>
    </div>

    <div class="right-button">
      <el-button-group>
        <el-button v-for="device in deviceList" :type="editorSetting.device === device.value ? 'primary' : 'default'" size="small" @click="handleSelectDevices(device)">
          <i :class="`tefact-icon ${device.icon}`"></i>
        </el-button>
      </el-button-group>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script lang="ts">
  import { Vue, Component, Prop } from 'nuxt-property-decorator'

  @Component
  export default class Toolbar extends Vue {
      @Prop([Object]) page
      @Prop([Object]) editorSetting

      deviceList = [
        { icon: 'tf-icon-pc', name: 'PC', value: 'pc' },
        { icon: 'tf-icon-mobile-phone', name: 'h5', value: 'h5' },
      ]

      handleSelectDevices(device) {
        this.$emit('editorSettingChange', { ...this.editorSetting, device: device.value })
      }
  }
</script>
<style lang="scss">
  @import "../../../../assets/styles/variables";

  .editor-toolbar {
    display: flex;
    align-items: center;

    .page-title {
      margin: 0 10px;
      cursor: pointer;
      flex: 1;

      &:hover {
        color: $editor-main-color;
      }
    }

    .right-button {
      float: right;
    }
  }

  .editor-toolbar {
    height: 32px;
    padding: 10px;
    background-color: white;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);
  }
</style>
