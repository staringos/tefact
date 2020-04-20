import webpack from 'webpack'
import path from 'path'
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const nodeExternals = require('webpack-node-externals')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

// https://webpack.js.org/configuration/externals/#externals
const ignore = nodeExternals({
  modulesDir: '../../node_modules',
  importType: 'umd'
})

console.log('ignore:', ignore)

const config: webpack.Configuration = {
  mode: 'development',
  entry: {
    app: ['./src/index.ts']
  },
  resolve: {
    extensions: ['.ts', '.js', '.vue', '.json']
  },
  output: {
    path: path.resolve(process.cwd(), './lib'),
    filename: 'index.js',
    chunkFilename: '[id].js',
    libraryTarget: 'umd',
    libraryExport: 'default',
    library: 'ui',
    umdNamedDefine: true,
    globalObject: 'typeof self !== \'undefined\' ? self : this'
  },
  // target: 'node',
  externals: [ignore, "vue", "vuex"],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      }, {
        test: /\.ts$/,
        loader: 'ts-loader',
        exclude: /node_modules/,
        options: { appendTsSuffixTo: [/\.vue$/] }
      }, {
        test: /\.scss$/,
        use: [
          // fallback to style-loader in development
          process.env.NODE_ENV !== 'production'
            ? 'style-loader'
            : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ]
      }, {
        test: /\.vue$/,
        exclude: /node_modules/,
        loader: 'vue-loader'
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: '[name].css',
      chunkFilename: '[id].css',
    })
  ]
}

export default config
