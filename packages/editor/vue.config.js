// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require("path");
// eslint-disable-next-line @typescript-eslint/no-var-requires
const nodeExternals = require("webpack-node-externals");

const isLib = process.env.BD === "lib";
const isProd = process.env.NODE_ENV === "production";

// function addStyleResource(rule) {
//   rule
//     .use("style-resource")
//     .loader("style-resources-loader")
//     .options({
//       patterns: [path.resolve(__dirname, "./src/assets/styles/index.scss")]
//     });
// }

module.exports = {
  configureWebpack(config) {
    config.externals = isProd && isLib ? [nodeExternals()] : {};
    console.log("config:", config.watchOptions);
    // watchOptions: {
    //   included: /node_modules/
    // }
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "~@/assets/styles/index.scss";`
      }
    }
  }
};
