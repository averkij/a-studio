<template>
  <v-card>
    <div class="blue lighten-5">
      <v-card-title>🔮 Export data</v-card-title>
    </div>
    <v-divider></v-divider>
    <v-card-text>Download book in data format.</v-card-text>
    <v-divider class="mt-10"></v-divider>
    <v-card-actions>
      <v-btn @click="downloadFile('xml')" :loading="isLoading.download[info.langCode]"
        :disabled="isLoading.download[info.langCode]" width="133">
        <v-icon left color="grey">mdi-download</v-icon>XML
      </v-btn>
      <v-btn @click="downloadFile('json')" :loading="isLoading.download[info.langCode]"
        :disabled="isLoading.download[info.langCode]" width="133">
        <v-icon left color="grey">mdi-download</v-icon>JSON
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    name: "DownloadDataPanel",
    props: ["info", "isLoading", "direction"],
    methods: {
      downloadFile(format) {
        this.$emit('downloadFile', format, this.direction)
      }
    },
    computed: {}
  };
</script>
