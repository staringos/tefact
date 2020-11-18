<template>
  <div class="app-numbers-wrapper">
    <div class="item">
      <h2 class="el-input-number">1</h2>
      <p>安装数</p>
    </div>
    <div class="item">
      <h2 class="el-input-number">1</h2>
      <p>使用人数</p>
    </div>
    <div class="item">
      <h2 class="el-input-number">1</h2>
      <p>页面访问量</p>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.app-numbers-wrapper {
  display: flex;
  flex: 1;

  .item {
    flex: 1;
    justify-content: center;
    align-items: center;
    display: flex;
    flex-direction: column;
  }

  .el-input-number {
    font-weight: 600;
    font-size: 32px;
    text-align: center;
  }
}
</style>
