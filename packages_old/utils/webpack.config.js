const path = require("path");
module.exports = {
  entry: {
    index: "./src/index.js",
  },
  output: {
    path: path.resolve(__dirname, "lib"),
    filename: "[name].js",
    libraryTarget: "commonjs-module",
  },
  externals: [/^base\/js*/, /^notebook\/js*/],
  optimization: {
    minimize: false,
  },
};
