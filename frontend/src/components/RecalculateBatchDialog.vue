<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-tabs v-model="tab" background-color="transparent" color="basil" grow>
        <v-tab> Resolve </v-tab>
        <v-tab> Recalculate </v-tab>
      </v-tabs>

      <div style="background: green; height: 250px">
        <v-tabs-items v-model="tab" style="height: 100%">

          <v-tab-item style="height: 100%">
            <v-card class="d-flex flex-column" style="height: 100%">
            <v-card-title class="justify-center pt-5 text-subtitle-1 px-10"
              >Batch {{ batch_id + 1 }}. Resolve all found conflicts.</v-card-title
            >
            
            <v-spacer></v-spacer>

            <v-card-actions>
              <v-btn color="primary" text @click="show = false"> Close </v-btn>
              <v-spacer></v-spacer>
              <v-btn color="success" :disabled="inProgress" :loading="inProgress" @click="resolveConflictsBatch">
                Resolve
              </v-btn>
            </v-card-actions>
            </v-card>
          </v-tab-item>

          <v-tab-item style="height: 100%">
            <v-card class="d-flex flex-column" style="height: 100%">
            <v-card-title class="justify-center pt-5 text-subtitle-1 px-10"
              >Batch {{ batch_id + 1 }}. Select the shift for the second
              text.</v-card-title
            >
            <v-card-actions class="px-15 mt-5 d-flex justify-space-between">
              <v-btn fab outlined color="gray" @click="shift -= stepSize">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <div class="text-h4">
                {{ shift }}
              </div>
              <v-btn fab outlined color="gray" @click="shift += stepSize">
                <v-icon>mdi-arrow-right</v-icon>
              </v-btn>
            </v-card-actions>
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-btn color="primary" text @click="show = false"> Close </v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" :disabled="inProgress" :loading="inProgress" @click="recalculateBatch">
                Recalculate
              </v-btn>
            </v-card-actions>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "RecalculateBatchDialog",
  props: {
    value: Boolean,
    batch_id: Number,
    inProgress: Boolean
  },
  data() {
    return {
      tab: null,
      shift: 0,
      stepSize: 20,
    };
  },
  methods: {
    recalculateBatch() {
      this.show = false;
      this.$emit("recalculateBatch", this.batch_id, this.shift);
    },
    resolveConflictsBatch() {
      this.show = false;
      this.$emit("resolveConflictsBatch", this.batch_id);
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
};
</script>
