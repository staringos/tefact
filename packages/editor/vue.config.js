// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require("path");
// eslint-disable-next-line @typescript-eslint/no-var-requires
const nodeExternals = require("webpack-node-externals");
// eslint-disable-next-line @typescript-eslint/no-var-requires
const webpack = require("webpack");

function resolve(dir) {
  return path.join(__dirname, dir);
}

const isLib = process.env.BD === "lib";
const isProd = process.env.NODE_ENV === "production";

const plugins = [
  new webpack.IgnorePlugin({
    resourceRegExp: /^\.\/locale$/,
    contextRegExp: /moment$/
  })
];

if (isLib) {
  plugins.push(
    new webpack.optimize.LimitChunkCountPlugin({
      maxChunks: 1
    })
  );
}

module.exports = {
  publicPath: "/",
  outputDir: isLib ? "lib" : "dist",
  productionSourceMap: true,
  filenameHashing: false,
  lintOnSave: process.env.NODE_ENV !== "production",
  chainWebpack: config => {
    config.plugins.delete("prefetch");
    if (isLib) {
      config.entry("main").clear();
      config.entry("main").add("./src/index.ts");
    }

    config.resolve.alias.set("@", resolve("src"));
  },
  configureWebpack: {
    plugins,
    externals: isProd && isLib ? [nodeExternals()] : {}
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "~@/assets/styles/index.scss";`
      }
    }
  }
};
