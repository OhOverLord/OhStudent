<template>
  <div id="app">
    <header>
      <router-link class="logo" to="/">OhStudent</router-link>
      <router-link class="login-link" to="/login" active-class="active" v-if="status != 'success'">Login</router-link>
      <div v-else class="dropdown">
        <span class="dropbtn">{{username}}</span>
        <div class="dropdown-content">
          <router-link to="/profile">Профиль</router-link>
          <router-link to="/friends">Друзья</router-link>
          <router-link to="/chat">Чат</router-link>
          <a :href="finance_link">Финансы</a>
          <a :href="diary_link">Ежедневник</a>
          <a @click="logout">Выйти</a>
        </div>
      </div>
    </header>
    <router-view @status="setStatus" @username="setUsername"></router-view>
  </div>
</template>

<script>
import { HOST_URL } from "@/settings";

export default {
  name: 'App',
  data() {
    return {
      status: localStorage.getItem('status'),
      username: localStorage.getItem('username'),
      finance_link: `http://localhost:8080/finance`,
      diary_link: `http://localhost:8080/diary`
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
    },
    checkPony() {
    let ponies = ['pinkypie', 'applejack', 'rainbowdash', 'twilightsparkle']
    console.log(this.username.toLowerCase().replace(/\s/g, ''))
    for(let pony of ponies)
      if(this.username.toLowerCase().replace(/\s/g, '') == pony)
      {
        this.changeTheme()
        return
      }
    },
    changeTheme() {
      document.documentElement.style.setProperty('--general-color', '#DDBBD9');
      document.documentElement.style.setProperty('--light-general-color', '#F8F2F8');
      document.documentElement.style.setProperty('--other-color', '#E5E5EA');
      document.documentElement.style.setProperty('--background-color', '#F0F0F0');
      document.documentElement.style.setProperty('--button-delete-color', '#FEAEAE');
      document.documentElement.style.setProperty('--button-delete-color-hover', '#FE8686');
      document.documentElement.style.setProperty('--add-button-color', '#FE8686');
      document.documentElement.style.setProperty('--add-button-color-hover', '#DDBBD9');
      document.documentElement.style.setProperty('--button-color', '#BEBEDA');
      document.documentElement.style.setProperty('--button-color-hover', '#A4A4CB');
      document.documentElement.style.setProperty('--error-color', '#F68F71');
    }
  },
  mounted() {
    this.first_name = localStorage.getItem('first_name')
    this.checkPony()
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
    background: var(--general-color);
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
    background: var(--general-color); 
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
}
::-webkit-scrollbar-thumb:window-inactive {
	background: rgba(255,0,0,0.4); 
}

:root {
  --general-color: #9ED1AE;
  --light-general-color: #D5EBDC;
  --other-color: #E5E5EA;
  --background-color: #F0F0F0;
  --button-delete-color: #FEAEAE;
  --button-delete-color-hover: #FE8686;
  --add-button-color: #9ED1AE;
  --add-button-color-hover: #9ED1AE;
  --button-color: #BEBEDA;
  --button-color-hover: #A4A4CB;
  --error-color: #F68F71;
  }
</style>
