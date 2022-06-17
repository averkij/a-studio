<template>
  <v-card>
    <div class="blue lighten-5">
      <v-card-title>{{ info.icon }} {{ info.name }} {{title}}</v-card-title>
      <!-- <v-card-text>Your {{ info.name }} files</v-card-text> -->
    </div>
    <v-divider></v-divider>
    <v-card-text>Aligned {{ info.name }} {{title}} in txt format.</v-card-text>
    <v-card-text class="py-0">One <b>{{lineItemName}}</b> per line.</v-card-text>
    <v-divider class="mt-10"></v-divider>
    <v-card-actions>
      <v-btn @click="downloadFile(info.langCode)" :loading="isLoading.download[info.langCode]"
        :disabled="isLoading.download[info.langCode]">
        <v-icon left color="grey">mdi-download</v-icon>Download
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    name: "DownloadPanel",
    props: ["info", "isLoading", "title", "direction", "paragraphs", "lineItemName"],
    methods: {
      downloadFile(langCode) {
        this.$emit('downloadFile', langCode, this.paragraphs, this.direction)
      }
    },
    computed: {}
  };
</script>
