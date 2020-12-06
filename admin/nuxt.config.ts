// import { Configuration } from '@nuxt/types'
// import LodashModuleReplacementPlugin from 'lodash-webpack-plugin'
import Sass from 'sass'
import Fiber from 'fibers'

const script = [
  { src: 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js' }
]

const isDev = process.env.NODE_ENV !== 'production'

if (!isDev) {
  script.push({
    src: 'https://hm.baidu.com/hm.js?4d0b59a36bbb65c0522de6a7e6d026f2'
  })
}

const customSass = {
  implementation: Sass,
  sassOptions: {
    fiber: Fiber,
  }
};

const config = {
  dev: isDev,
  srcDir: 'src/',
  server: {
    port: 8800,
    host: '0.0.0.0'
  },
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    title: 'Tefact - 企业级低代码平台',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script
  },

  env: {
    ARRPLAT_BASE_URL: isDev ? 'http://localhost:5500' : 'http://saasapi.tefact.com/',
    BUCKET_NAME: 'arrplat',
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    '~/assets/styles/index.scss',
    '~/assets/css/index.css'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '~plugins/ElementUI',
    '~plugins/GlobalComponent',
    '~plugins/ArrplatUI',
    '~plugins/Clipboard',
    '~plugins/Baidu',
    { src: '~/plugins/AxiosToken.ts', ssr: false },
    { src: '~/plugins/PersistedState.ts', ssr: false },
    { src: '~/plugins/Route.ts', ssr: false },
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/nuxt-tailwindcss
    '@nuxt/typescript-build'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/style-resources', '@nuxtjs/sentry',
  ],
  /*
  ** Build configuration
  */
  build: {
    analyze: true,
    loaders: {
      scss: customSass
    },
    transpile: [
      'vuex-module-decorators', /^element-ui/
    ],
    // plugins: [
    //   new LodashModuleReplacementPlugin()
    // ],
    babel: {
      plugins: [
        ["component",
          {
            "libraryName": "element-ui",
            "styleLibraryName": "theme-chalk"
          }
        ]
      ],
    },
    styleResources: {
      scss: ['./src/assets/styles/variables.scss']
    },
    /*
    ** You can extend webpack config here
    */
    extend(config: any, ctx: any) {
      config.devtool = ctx.isClient ? 'eval-source-map' : 'inline-source-map'

      config.node = {
        fs: 'empty',
      }

      // https://segmentfault.com/a/1190000011100006
      config.resolve.symlinks = false;

    }
  },
} as any

if (!isDev) {
  config.sentry = {
    dsn: 'https://926a3edc432c40c08eb09edf20a4d3c1@o483948.ingest.sentry.io/5536565', // Enter your project's DSN here
    config: {}, // Additional config
    lazy: true
  }
}

export default config
