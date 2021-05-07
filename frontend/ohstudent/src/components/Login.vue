<template>
    <div>
        <form class="login-container" ref="form" action="/">
            <div class="input-container">
                <label for="email">Email</label>
                <input required v-model="email" type="email" placeholder="foo@example.com" name="email"/>
                <label for="password">Password</label>
                <input required v-model="password" type="password" placeholder="********" name="password"/>
                <router-link class='registration-link' to="/registration">Нет аккаунта...</router-link>
                <ul v-if="errors" class="errors">
                    <li v-for="error in errors" :key="error[0]">{{error[0]}}</li>
                </ul>
            </div>
            <a class="login-btn" @click="login" type="button"><p>Login</p></a>
        </form>
    </div>
</template>

<script>
import { jwtDecrypt } from '@/jwtDecode'
import axios from 'axios'

export default {
    data() {
        return {
            email: '',
            password: 'Admin1234!',
            errors: [],
        }
    },
    methods: {
        async login() {
            const response = await axios.post('http://127.0.0.1:8000/account/login/', {
                user: {
                    email: this.email,
                    password: this.password
                }
            }).catch(err => { 
                if (err.response) { 
                    this.errors = err.response.data.errors
                }
            })
            if (response)
            {
                console.log(response.data.user)
                const user = response.data.user
                localStorage.setItem("token", user.token)
                localStorage.setItem("refresh_token", user.refresh_token)
                localStorage.setItem("first_name", user.first_name)
                localStorage.setItem("last_name", user.last_name)
                localStorage.setItem("username", user.username)
                const jwtDecodedValue = jwtDecrypt(user.token)
                localStorage.setItem("token_exp", jwtDecodedValue.exp)
                localStorage.setItem('status', 'success')
                this.$emit('status', 'success')
                this.$refs.form.submit()
            }
        }
    }
}
</script>

<style scoped>
.login-container {
    border: 3px solid #C5FAD1;
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

.login-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 80%;
    height: 48px;
    background: #C5FAD1;
    border-radius: 9px;
    border: none;
    cursor: pointer;
    color: white;
}

.login-btn p {
    font-family: 'Noto Sans JP', sans-serif;
    margin: 0;
}

.registration-link {
    color: #AAAAAA;
    font-family: 'Noto Sans JP', sans-serif;
}

.errors {
    color: #F68F71;
}
</style>