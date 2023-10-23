<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title> Split conflict </v-card-title>
      <v-card-text class="mt-5">
        <div>Confirm that following pairs are correct alignments:</div>
        <div class="mt-6 text-subtitle-2">
          <div>[ {{ linesFrom[2] }} ]</div>
          <div>[ {{ linesTo[2] }} ]</div>
          <div class="mt-4">[ {{ linesFrom[3] }} ]</div>
          <div>[ {{ linesTo[3] }} ]</div>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="show = false"> Cancel </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="80px" @click="handle"> Ok </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "SplitConflictDialog",
  props: {
    value: Boolean,
    linesFrom: Array,
    linesTo: Array,
  },
  data() {
    return {};
  },
  methods: {
    handle() {
      this.show = false;
      this.$emit("splitConflict", this.linesFrom[0], this.linesTo[0]);
    },
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
};
</script>
