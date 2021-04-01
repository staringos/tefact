<div align="center">
  <img src="./docs/assets/images/logo-banner.png">
</div>
<div align="center">
  <a href="https://staringos.com">Website</a> | 
  <a href="http://saas.staringos.com">Usage</a> | 
  <a href="https://staringos.com/docs">Documents</a> | 
  <a href="https://staringos.com/docs/join-us">Community</a> | 
  <a href="https://staringos.com/docs/join-us">Support</a>
</div>

<br />

<div align="center">

[![license](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/Tefact/tefact-saas)
[![Actions Status](https://github.com/tefact/tefact-saas/workflows/deploy/badge.svg)](https://github.com/tefact/tefact-saas/actions)
[![Release Version](https://img.shields.io/badge/release-0.0.1-green.svg)](https://github.com/Tefact/tefact-saas/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Tefact/tefact-saas/pulls)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Tefact/tefact-saas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Tefact/tefact-saas/alerts/)

</div>

# Tefact Engine

Make your `Website`、`Mobile Page` and `Form` without code.

[中文文档](./README-CN.md)

## Getting Start

Install dependency

```shell script
yarn add @tefact/editor
```

Import styles to your css or less file:

```vue
import "@tefact/editor/lib/index.css"
```

Import Editor to you

```vue
<template>
  <Editor
      :value="target"
      :editorSetting="editorSetting"
  ></Editor>
</template>
<script lang="ts">
import Vue from "vue";
import Editor, { getDefaultFeature } from "@tefact/editor";

export default Vue.extends({
  data() {
    return {
      target: getDefaultFeature("page"),
      editorSetting: {}
    }
  },
  components: {
    Editor
  }
})
</script>
```

## Core Concept

### Target

Target is an object that we edit for. It can be a H5 Page / Form Page or website Page. It's a JSON data structure for descript how a Page for Form looks like.

You can use `getDefaultFeature` in `@tefact/editor` to generate default target data. And save it to somewhere, it can be used directly to `@tefact/feature-form` or `@tefact/feature-page`

### Editor

`@tefact/editor` is a Edit view for feature page or form. 

#### Parameters

- Target: the edit target
- editorSetting: Setting of editor

#### Event

- addTarget: Add target within the editor
- editTarget: after editor target basic information
- share: toggle target share
- save: When save target
- back: When editor within the editor back toggle

### Page

`@tefact/feature-page` is a view component for those `target` has a `featureType = page`. To preview a page, you can do:

```vue
<template>
  <Page :value="target"></Page>
</template>
<script lang="ts">
import Vue from "vue";
import Page, { DFFAULT } from "@tefact/feature-page";

export default Vue.extends({
  data() {
    return {
      target: DFFAULT
    }
  },
  components: {
    Page
  }
})
</script>
```

### Form

Same like `page`, `@tefact/feature-form` is use for preview or display those target has a `featureType = form`, you can do:

```vue
<template>
  <Form :value="target"></Form>
</template>
<script lang="ts">
import Vue from "vue";
import Form, { DFFAULT } from "@tefact/feature-page";

export default Vue.extends({
  data() {
    return {
      target: DFFAULT
    }
  },
  components: {
    Form
  }
})
</script>
```
