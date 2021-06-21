<template>
  <v-card width="400" class="mx-auto mt-5">
    <v-form>
      <v-card-title>Привет, 你好, Szia, Hallo, Ahoj!</v-card-title>
      <v-card-text>
        <v-text-field
          label="Username"
          prepend-icon="mdi-account-circle"
          v-model="username"
          @keydown.enter.prevent="onSubmit(username)"
        />
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <!-- <v-btn color="success">Register</v-btn>
          <v-spacer></v-spacer> -->
        <v-btn @click="onSubmit(username)" color="info">Login</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
import { LOGIN } from "@/store/actions.type";

export default {
  data() {
    return {
      username: null
    };
  },
  methods: {
    onSubmit: function(username) {
      this.$store
        .dispatch(LOGIN, {
          username
        })
        .then(() =>
          this.$router.push({
            path: `/user/${username}`
          })
        );
    }
  }
};
</script>
