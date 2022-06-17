import { LOGIN } from "./actions.type";

const state = {
  errors: null,
  user: {},
  isAuthenticated: true
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  }
};

const actions = {
  [LOGIN]() {
    return true;
  }
};

export default {
  state,
  actions,
  getters
};
