var path = require('path');

module.exports = {
  entry: path.resolve(__dirname, '../src/app.js'),
  output: {
    path: path.resolve(__dirname, '../build'),
    filename: 'app.js',
    resolve: {
      extensions: ['', '.js', '.jsx']
    },
  },

  module: {
    loaders: [
      {
        test: /src\/.+.js$/,
        exclude: /node_modules/,
        loader: 'babel',
        query:
        {
          presets:['react', 'es2015']
        }
      }
    ]
  }
};