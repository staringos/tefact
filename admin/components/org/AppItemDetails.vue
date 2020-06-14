<template>
  <div class="app-item-details">
    <div class="section section-app-head">
      <div class="app-image-wrapper">
        <img class="app-image" :src="item.icon" />
      </div>
      <div class="app-details">
        <ArrTitle size="h2">{{item.title}}</ArrTitle>
        <AttributeList :attributes="attributes" />
      </div>
    </div>
    <div class="section">
      <ArrTitle size="h4">应用详情</ArrTitle>
      <div>
        {{item.description}}
      </div>
    </div>
    <div class="section">
      <ArrTitle size="h4" class="section-title">应用图册</ArrTitle>
      <div class="photo-gallery">
        <div class="item" v-for="(image, i) in item.images" :key="i">
          <img :src="image"/>
        </div>
      </div>
    </div>
    <AppToggleBtn :item="item" @onChange="handleDismissDialog"/>
  </div>
</template>
<style lang="scss">
  @import "../../components/ui/theme/variables";

  .app-item-details {
    display: flex;
    flex-direction: column;

    .app-image-wrapper {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;

      .app-image {
        width: 132px;
        height: 132px;
      }
    }

    .app-details {
      flex: 2;
      padding-left: 20px;

      .title {
        font-size: 26px;
        font-weight: 400;
        color: rgba(65,65,65,1);
        line-height: 37px;
      }
    }

    .section {
      display: flex;
      border-bottom: 1px solid $borderColor;
      padding-bottom: 20px;
      padding-top: 20px;
      flex-direction: column;
      margin-bottom: 10px;

      .section-title {
        font-weight: 600;
        margin-bottom: 20px;
      }

      &.section-app-head {
        flex-direction: row;
        padding-top: 0;
      }
    }

    .photo-gallery {
      display: flex;

      .item {
        width:148px;
        height:128px;
        border-radius:5px;
        border:1px solid $borderColor;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
      }
    }
  }
</style>
<script lang="ts">
  import { Vue, Component, Prop, Emit } from 'nuxt-property-decorator'
  import { Application } from '~/services/common'
  import AppToggleBtn from './AppToggleBtn.vue'

  @Component({
    components: {
      AppToggleBtn
    }
  })
  export default class AppItem extends Vue {
    @Prop(Object) item!: Application

    get attributes() {
      const res = [{
        key: '分类',
        value: this.item.application_category ? this.item.application_category.name : ''
      }, {
          key: '版本',
          value: this.item.version
      }, {
          key: '添加次数',
          value: this.item.install_number
      }, {
          key: '上线时间',
          value: this.item.create_time
      }]
      console.log('res:', res)
      return res
    }

    @Emit('onDismiss')
    handleDismissDialog() {}
  }
</script>
