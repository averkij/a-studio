<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card>
      <v-card-title>
        Alignment settings
      </v-card-title>
      <v-card-text class="mt-5">
        <v-text-field label="Name" v-model="name" v-on:keyup.enter="createAlignment">
        </v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="show=false">
          Close
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" dark width="80px" @click="createAlignment">
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    name: "CreateAlignmentDialog",
    props: {
      value: Boolean
    },
    data() {
      return {
        name: ""
      }
    },
    methods: {
      createAlignment() {
        if (this.name) {
          this.show = false;
          this.$emit('createAlignment', this.name)
        } else {
          alert("Enter alignment name");
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
