<template>
  <div class="header-bar-node">
    <div class="left-area">
      <SlotArea :preview="preview" />
    </div>
    <div class="title-area">{{title}}</div>
    <div class="right-area">
      <SlotArea :preview="preview" />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.header-bar-node {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  background-color: white;
  border-bottom: 1px solid $borderColor;
  box-sizing: border-box;
  height: 50px;
  width: 100%;
  align-items: center;
  padding: 5px;

  .left-area, .right-area {
    max-width: 200px;
    width: 100px;
    height: 40px;
  }

  .title-area {
    flex: 1;
    text-align: center;
  }
}
</style>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import SlotArea from "../components/SlotArea.vue"

@Component({
  components: { SlotArea }
})
export default class AppItem extends Vue {
  title = "首页"
  @Prop() preview
}
</script>
