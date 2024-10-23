const path = require("path");
module.exports = {
  entry: "./src/index.js",
  output: {
    filename: "index.js",
    path: path.resolve(__dirname, "lib"),
    libraryTarget: "commonjs-module",
  },
  optimization: {
    minimize: true,
  },
  externals: {},
};
