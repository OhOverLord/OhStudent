<template>
  <div id="app">
    <header>
      <router-link class="logo" to="/">OhStudent</router-link>
      <router-link class="login-link" to="/login" active-class="active" v-if="status != 'success'">Login</router-link>
      <div v-else class="dropdown">
        <span class="dropbtn">{{username}}</span>
        <div class="dropdown-content">
          <router-link to="/profile">Profile</router-link>
          <a @click="logout">Logout</a>
        </div>
      </div>
      <router-link class="logo" to="/friends">friends</router-link>
      <router-link class="logo" to="/chat">Chat</router-link>
    </header>
    <router-view @status="setStatus" @username="setUsername"></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      status: localStorage.getItem('status'),
      username: localStorage.getItem('username'),
    }
  },
  components: {
  },
  methods: {
    setStatus(status) {
      this.status = status
    },
    setUsername(username) {
      this.username = username
    },
    logout() {
      this.username = ""
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
    background: #DDBBD9;
}

.logo {
    text-decoration: none;
    color: white;
    padding-top: 10px;
    padding-left: 10px;
    font-size: 1.5em;
    font-family: 'Ubuntu', sans-serif;  
}

.login-link, .dropdown{
    text-decoration: none;
    color: white;
    padding-top: 10px;
    margin-right: 5%;
    font-size: 1.5em;
    font-family: 'Ubuntu', sans-serif;  
}

.active {
    visibility: hidden;
}

.dropbtn {
  cursor: pointer;
  display: block;
  height: 100%;
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    right: 5%;
    background-color: #f1f1f1;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
}

.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {background-color: #ddd;}

.dropdown:hover .dropdown-content {display: block;}

a {
  cursor: pointer;
}

::-webkit-scrollbar {
    width: 0px;
}
 
/* Track */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
    -webkit-border-radius: 10px;
    border-radius: 10px;
}
 
/* Handle */
::-webkit-scrollbar-thumb {
    -webkit-border-radius: 10px;
    border-radius: 10px;
    background: #EAD0DE; 
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
}
::-webkit-scrollbar-thumb:window-inactive {
	background: rgba(255,0,0,0.4); 
}
</style>
