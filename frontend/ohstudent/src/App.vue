<template>
  <div id="app">
    <header>
      <router-link class="logo" to="/">OhStudent</router-link>
      <router-link class="login-link" to="/login" active-class="active">Login</router-link>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
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

.login-link {
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
</style>
