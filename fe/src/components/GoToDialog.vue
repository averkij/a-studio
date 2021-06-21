<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title>
        Go to page
      </v-card-title>
      <v-card-text class="mt-5">
        <v-text-field label="Page number" v-model="pageNumber">
        </v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="show=false">
          Close
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="80px" @click="goToPage">
          Go
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: "GoToDialog",
    props: {
      value: Boolean
    },
    data() {
      return {
        pageNumber: ""
      }
    },
    methods: {
      goToPage() {
        let num = parseInt(this.pageNumber)
        if (num) {
          this.show = false;
          this.$emit('goToPage', num)
        } else {
          alert("Enter a valid number");
        }
      }
    },
    computed: {
      show: {
        get() {
          return this.value
        },
        set(value) {
          this.$emit('input', value)
        }
      }
    }
  }
</script>
