<template>
  <div>
    <v-card class="mt-0">
      <v-card-title>
        {{ LANGUAGES[info.langCode].name }} side ({{ direction }})
      </v-card-title>
      <v-card-text>
        <ol>
          <li>Download or open the text.</li>
          <li>Translate it.</li>
          <li>Upload translation back using the form below.</li>
        </ol>
      </v-card-text>
      <v-card-actions>
        <v-file-input
          outlined
          dense
          accept=".txt"
          @change="onProxyFileChange($event, info.langCode)"
        >
        </v-file-input>
      </v-card-actions>
      <v-divider></v-divider>
      <v-card-actions>
        <!-- download splitted text -->
        <v-btn @click="downloadSplitted(info.langCode, false)"
          ><v-icon left color="grey">mdi-download</v-icon>Download</v-btn
        >

        <!-- open splitted text -->
        <v-btn @click="downloadSplitted(info.langCode, true)"
          ><v-icon left color="grey">mdi-open-in-new</v-icon>Open</v-btn
        >
        <v-spacer></v-spacer>
        <v-btn
          @click="uploadProxyFile(info.langCode)"
          :loading="isLoading.uploadProxy[info.langCode]"
          :disabled="isLoading.uploadProxy[info.langCode]"
        >
          <v-icon left color="grey">mdi-cloud-upload</v-icon>Upload
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { LANGUAGES } from "@/common/language.helper";
export default {
  name: "ProxyPanel",
  props: [
    "info",
    "selected",
    "isLoading",
    "showUploadProxyBtn",
    "side",
    "direction",
  ],
  data() {
    return {
      LANGUAGES,
      showUploadProxyPanel: false,
    };
  },
  methods: {
    onProxyFileChange(event, langCode) {
      this.$emit("onProxyFileChange", event, langCode, this.side);
    },
    uploadProxyFile(langCode) {
      this.$emit("uploadProxyFile", langCode, this.side, this.direction);
    },
    downloadSplitted(langCode, openInBrowser) {
      this.$emit("downloadSplitted", langCode, openInBrowser, this.direction);
    },
  },
};
</script>
