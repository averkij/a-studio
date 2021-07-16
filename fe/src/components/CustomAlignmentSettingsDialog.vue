<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <div style="background: green; height: 300px">
        <v-card class="d-flex flex-column" style="height: 100%">
          <v-card-title class="justify-center pt-5 text-h6 px-10"
            >Set custom settings</v-card-title
          >

          <div class="px-6 text-center mt-10">
            Align batches from
            <span class="font-weight-bold">{{ range[0] + 1 }}</span> to
            <span class="font-weight-bold">{{ range[1] + 1 }}</span>
          </div>
          <v-card-actions class="px-6 mt-3">
            <v-range-slider
              v-model="range"
              :max="totalBatches - 1"
              min="0"
              hide-details
            ></v-range-slider>
          </v-card-actions>

          <v-spacer></v-spacer>

          <v-card-actions>
            <v-btn color="primary" text @click="show = false"> Close </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" class="px-10" @click="applySettings">
              Apply
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "CustomAlignmentSettingsDialog",
  props: {
    value: Boolean,
    totalBatches: Number,
  },
  data() {
    return {
      range: [0, this.totalBatches - 1],
    };
  },
  methods: {
    applySettings() {
      this.show = false;
      let newSettings = { start: this.range[0], end: this.range[1] };
      this.$emit("applySettings", newSettings);
    },
    init() {
      this.range = [0, this.totalBatches - 1];
    }
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  mounted() {
    this.range = [0, this.totalBatches - 1];
  },
};
</script>
