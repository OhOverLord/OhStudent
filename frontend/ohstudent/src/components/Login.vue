<template>
    <div>
        <form class="login-container">
            <div class="input-container">
                <label for="email">Email</label>
                <input required v-model="email" type="email" placeholder="foo@example.com" name="email"/>
                <label for="password">Password</label>
                <input required v-model="password" type="password" placeholder="********" name="password"/>
                <router-link class='registration-link' to="/registration">Нет аккаунта...</router-link>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.login-container {
    border: 3px solid #EAD0DE;
    width: 50%;
    height: 322px;
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin: auto;
    border-radius: 31px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: 'Noto Sans JP', sans-serif;
}

input[type=email], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  border: 1px solid #ccc;
  box-sizing: border-box;
  border-radius: 8px;
}

.input-container {
    width: 80%;
}

button {
    width: 80%;
    height: 48px;
    background: #EAD0DE;
    border-radius: 9px;
    border: none;
    cursor: pointer;
    color: white;
    font-size: 100%;
    margin-top: 5%;
    font-family: 'Noto Sans JP', sans-serif;
}

.registration-link {
    color: #AAAAAA;
    font-family: 'Noto Sans JP', sans-serif;
}
</style>