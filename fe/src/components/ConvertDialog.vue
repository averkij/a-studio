<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title> Convertation </v-card-title>
      <v-card-text class="mt-5">
        Your file will be converted in txt format.
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="show = false"> Close </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="80px" @click="convert">
          Convert
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "ConvertDialog",
  props: {
    value: Boolean,
  },
  data() {
    return {
      pageNumber: "",
    };
  },
  methods: {
    convert() {
      let num = parseInt(this.pageNumber);
      if (num) {
        this.show = false;
        this.$emit("convert", num);
      } else {
        alert("Enter a valid number");
      }
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
