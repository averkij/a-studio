module.exports = {
  transpileDependencies: ["vuetify"],
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
