<template>
    <div>
        <form class="login-container" @submit.prevent="register">
            <div class="input-container">
                <label for="email">Email</label>
                <input required v-model="email" type="email" placeholder="foo@example.com" name="email"/>
                <label for="fio">Имя и фамилия</label>
                <input required v-model="fio" type="text" placeholder="Иван Иванов" name="fio"/>
                <label for="username">Имя пользователя</label>
                <input required v-model="username" type="text" placeholder="example" name="username"/>
                <label for="password">Пароль</label>
                <input required v-model="password" type="password" placeholder="********" name="password"/>
                <label for="confirmPassword">Подтверждение пароля</label>
                <input required v-model="confirmPassword" type="password" placeholder="********" name="confirmPassword"/>
                <ul v-if="errors" class="errors">
                    <li v-for="error in errors" :key="error[0]">{{error[0]}}</li>
                </ul>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            email: '',
            fio: '',
            username: '',
            password: '',
            confirmPassword: '',
            errors: [],
        }
    },
    methods: {
        async register() {
            this.errors = []
            if(this.password != this.confirmPassword)
                this.errors.push(["Пароли не совпадают"])
            if(this.fio.split(' ').length > 2)
                this.errors.push(["Неправильно заполнены имя и фамилия"])
            if(this.errors.length == 0){
                const response = await axios.post('http://127.0.0.1:8000/account/register/', {
                    user: {
                        email: this.email,
                        username: this.username,
                        first_name: this.fio.split(' ')[0],
                        last_name: this.fio.split(' ')[1],
                        password: this.password
                    }
                }).catch(err => {
                    if (err.response)
                        this.errors = err.response.data.errors
                })
                if (response) {
                    this.$router.push('/login')
                } else {
                    console.log('Error!')
                }
            }
        },
    }
}
</script>

<style scoped>
.login-container {
    border: 3px solid #EAD0DE;
    width: 50%;
    height: 550px;
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
    margin-top: 3%;
    font-family: 'Noto Sans JP', sans-serif;
}

.registration-link {
    color: #AAAAAA;
    font-family: 'Noto Sans JP', sans-serif;
}

.errors {
    color: #F68F71;
}
</style>