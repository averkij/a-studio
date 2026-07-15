module.exports = {
  transpileDependencies: ["vuetify"],
  publicPath: '/lingtrain_aligner/', //subpath for deploy
  css: {
    loaderOptions: {
      sass: {
        implementation: require('sass'),
        sassOptions: {
          quietDeps: true
        }
      },
      scss: {
        implementation: require('sass'),
        sassOptions: {
          quietDeps: true
        }
      },
    },
  },
};
