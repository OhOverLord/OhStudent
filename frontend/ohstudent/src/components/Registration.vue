<template>
    <div>
        <form class="login-container">
            <div class="input-container">
                <label for="email">Email</label>
                <input required v-model="email" type="email" placeholder="foo@example.com" name="email"/>
                <label for="fio">Имя и фамилия</label>
                <input required v-model="fio" type="text" placeholder="Иванов Иван" name="fio"/>
                <label for="username">Имя пользователя</label>
                <input required v-model="username" type="text" placeholder="example" name="username"/>
                <label for="password">Password</label>
                <input required v-model="password" type="password" placeholder="********" name="password"/>
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
    height: 442px;
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

input {
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