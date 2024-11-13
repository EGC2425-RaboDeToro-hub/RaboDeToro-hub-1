import path from 'path';

module.exports = {
  entry: path.resolve(__dirname, './scripts.js'),
  output: {
    filename: 'email.bundle.js',
    path: path.resolve(__dirname, '../dist'),
  },
  resolve: {
    fallback: {
      "fs": false 
    }
  },
  mode: 'development',
};
