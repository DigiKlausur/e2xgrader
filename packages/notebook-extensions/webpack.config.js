const path = require("path");
module.exports = {
  entry: {
    "student/main": "./src/student-extension.js",
    "student_exam/main": "./src/student-exam-extension.js",
    "teacher/main": "./src/teacher-extension.js",
  },
  output: {
    path: path.resolve(__dirname, "../../e2xgrader/nbextensions/notebook"),
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
