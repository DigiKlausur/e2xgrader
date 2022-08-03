const path = require("path");
module.exports = {
  entry: {
    "student_exam/main": "./src/student-exam-extension.js",
  },
  output: {
    path: path.resolve(__dirname, "../../e2xgrader/nbextensions/tree"),
    filename: "[name].js",
    libraryTarget: "amd",
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
        test: /\.js$/,
        include: path.resolve(__dirname, "src"),
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env"],
          plugins: ["transform-class-properties"],
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
