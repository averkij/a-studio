<template>
  <v-card>
    <v-list class="pa-0">
      <v-list-item-group mandatory color="gray">
        <v-list-item
          v-for="(item, i) in items[info.langCode]"
          :key="i"
          @change="selectAndLoadPreview(info.langCode, item.name, item.guid)"
          @mouseover="hover_index = i"
          @mouseleave="hover_index = -1"
        >
          <v-list-item-icon>
            <v-icon>mdi-text-box-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <div>
              {{ item.name
              }}<v-chip
                v-if="item.has_proxy"
                class="ml-2"
                small
                label
                color="blue"
                text-color="white"
                >translated</v-chip
              >
            </div>
          </v-list-item-content>
          <v-icon
            v-show="hover_index == i"
            class="ml-2"
            @click.stop.prevent="
              (currentItem = item), (showConfirmDeleteDialog = true)
            "
            >mdi-close</v-icon
          >
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <ConfirmDeleteDialog
      v-model="showConfirmDeleteDialog"
      :itemName="currentItem.name"
      @confirmDelete="confirmDelete"
    />
    <v-divider></v-divider>
    <div v-if="uploadEnabled">
      <v-card-title>Upload</v-card-title>
      <v-card-text
        >Upload raw {{ info.name }} document in txt format.</v-card-text
      >
      <v-card-actions>
        <v-file-input
          outlined
          dense
          accept=".txt"
          @change="onFileChange($event, info.langCode)"
        >
        </v-file-input>
      </v-card-actions>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn
          @click="uploadFile(info.langCode)"
          :loading="isLoading.upload[info.langCode]"
          :disabled="isLoading.upload[info.langCode]"
        >
          <v-icon left color="grey">mdi-cloud-upload</v-icon>Upload
        </v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
import ConfirmDeleteDialog from "@/components/ConfirmDeleteDialog";

export default {
  name: "RawPanel",
  props: ["info", "isLoading", "items", "uploadEnabled"],
  data() {
    return {
      hover_index: -1,
      showConfirmDeleteDialog: false,
      currentItem: { name: "" },
    };
  },
  methods: {
    confirmDelete() {
      this.$emit("performDelete", this.currentItem, this.info.langCode);
    },
    onFileChange(event, langCode) {
      this.$emit("onFileChange", event, langCode);
    },
    uploadFile(langCode) {
      this.$emit("uploadFile", langCode);
    },
    selectAndLoadPreview(langCode, item, id) {
      this.$emit("selectAndLoadPreview", langCode, item, id);
    },
  },
  computed: {},
  components: {
    ConfirmDeleteDialog,
  },
};
</script>
