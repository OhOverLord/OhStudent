<template>
  <div id="app">
    <header>
      <router-link class="logo" to="/">OhStudent</router-link>
      <router-link class="login-link" to="/login" active-class="active" v-if="status != 'success'">Login</router-link>
      <a @click="logout" v-else class="logout" >Logout</a>
    </header>
    <router-view @status="setStatus"></router-view>
    {{first_name}}
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      status: localStorage.getItem('status'),
      first_name: localStorage.getItem('first_name'),
    }
  },
  components: {
  },
  methods: {
    setStatus(status) {
      this.status = status
    },
    logout() {
      localStorage.clear()
      this.status = '';
      this.$router.push('/login')
    }
  },
  mounted() {
    this.first_name = localStorage.getItem('first_name')
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100;400&display=swap');

body {
  margin: 0; 
  font-family: Arial, Helvetica, sans-serif;
}

header {
    display: flex;
    justify-content: space-between;
    margin: 0;
    width: 100vw;
    height: 50px;
    background: #EAD0DE;
}

.logo {
    text-decoration: none;
    color: white;
    padding-top: 10px;
    padding-left: 10px;
    font-size: 1.5em;
    font-family: 'Ubuntu', sans-serif;  
}

.login-link, .logout{
    text-decoration: none;
    color: white;
    padding-top: 10px;
    margin-right: 5%;
    font-size: 1.5em;
    font-family: 'Ubuntu', sans-serif;  
}

.logout {
  cursor: pointer;
}

.active {
    visibility: hidden;
}
</style>
