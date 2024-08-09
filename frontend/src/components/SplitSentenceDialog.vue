<template>
  <v-dialog v-model="show" max-width="800px">
    <v-card>
      <v-card-title> Split sentence </v-card-title>
      <v-card-text
        >Following sentence will be splitted into two. Lines numeration will be
        handled everywhere in the alignment.</v-card-text
      >
      <!-- <v-row class="ma-0 mt-0 px-7">
        <v-col class="text-overline"> Sentence to split:</v-col>
      </v-row> -->
      <v-row class="ma-0 mt-0 px-7">
        <v-col> {{ text }}</v-col>
      </v-row>
      <v-row class="ma-0 mt-0 px-7">
        <v-col>
          <v-textarea rows="3" label="Part 1" v-model="part1"> </v-textarea>
          <v-textarea rows="3" label="Part 2" v-model="part2"> </v-textarea>
        </v-col>
      </v-row>

      <v-card-actions>
        <v-btn color="primary" text @click="show = false"> Close </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="120px" @click="split"> Split </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "SplitSentence",
  props: {
    value: Boolean,
    text: String,
  },
  data() {
    return {
      part1: "",
      part2: "",
    };
  },
  methods: {
    split() {
      this.$emit("splitSentence", this.part1, this.part2);
    },
    init() {
      setTimeout(() => {
        let splitted = this.text.split(".");
        if (splitted.length > 1) {
          this.part1 = splitted[0] + ".";
          if (
            splitted[1].endsWith(":") ||
            splitted[1].endsWith("!") ||
            splitted[1].endsWith("?") ||
            splitted[1].endsWith(";")
          ) {
            this.part2 = splitted[1];
          } else {
            if (splitted[1].length > 1) {
              this.part2 = splitted[1] + ".";
            }
          }
        }
      }, 100);
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
