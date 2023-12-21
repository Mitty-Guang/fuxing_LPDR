const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  publicPath: './',
  outputDir: 'dist',
  assetsDir: 'static',
  devServer: {
        proxy: {
            "/image": {
                target: "https://niupic.com/api",
                pathRewrite: { "^/image": "" },
            },
        }
    }
})
