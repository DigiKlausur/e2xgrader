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
  externals: [
    "jquery",
    "require",
    "underscore",
    /^base\/js*/,
    /^notebook\/js*/,
  ],
  optimization: {
    minimize: true,
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
