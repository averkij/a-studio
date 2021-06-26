<template>
  <div>
    <v-alert
      type="info"
      border="left"
      colored-border
      color="blue"
      class="mt-6"
      elevation="2"
      v-if="
        !splitted |
          !splitted[info.langCode] |
          (splitted[info.langCode].lines.length == 0)
      "
    >
      Select file to preview.
    </v-alert>
    <v-card v-else>
      <div class="blue lighten-5">
        <v-card-title>
          {{ selected[info.langCode] }}
        </v-card-title>
        <v-card-text
          >{{
            splitted[info.langCode].meta.lines_count | separator
          }}
          lines</v-card-text
        >
      </div>
      <v-divider></v-divider>
      <div v-for="(line, i) in splitted[info.langCode].lines" :key="i">
        <PreviewItem :item="line"></PreviewItem>
        <v-divider></v-divider>
      </div>
      <div class="text-center pa-3">
        <v-pagination
          v-model="splitted[info.langCode].meta.page"
          :length="splitted[info.langCode].meta.total_pages"
          total-visible="7"
          @input="
            onPreviewPageChange(
              splitted[info.langCode].meta.page,
              info.langCode
            )
          "
        >
        </v-pagination>
      </div>
      <v-divider></v-divider>
      <v-card-actions>
        <!-- download splitted text -->
        <v-btn @click="downloadSplitted(info.langCode, false)"
          ><v-icon left color="grey">mdi-download</v-icon>Download</v-btn
        >
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import PreviewItem from "@/components/PreviewItem";
export default {
  name: "SplittedPanel",
  props: ["info", "splitted", "selected", "isLoading"],
  methods: {
    onPreviewPageChange(page, langCode) {
      this.$emit("onPreviewPageChange", page, langCode);
    },
    downloadSplitted(langCode, openInBrowser) {
      this.$emit("downloadSplitted", langCode, openInBrowser);
    },
  },
  components: {
    PreviewItem,
  }
};
</script>
