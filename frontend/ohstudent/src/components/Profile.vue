<template>
    <div>
        <div class="profile-container">
            <div class="profile-image"></div>
            <div class="information-container">
                <div class="username">
                    <span>Username: </span>
                    <input type="text" v-model="username">
                </div>
                <div class="email">
                    <span>Email: </span>
                    <span>{{email}}</span>
                </div>
                <div class="first_name">
                    <span>Имя: </span>
                    <input type="text" v-model="first_name">
                </div>
                <div class="last_name">
                    <span>Фамилия: </span>
                    <input type="text" v-model="last_name">
                </div>
                <div class="change-pass" :class="{hide: hide}">
                    <input type="password" v-model="password" placeholder="Новый пароль">
                    <input type="password" v-model="password2" placeholder="Подтверждение пароля">
                    <ul v-if="errors" class="errors">
                        <li v-for="error in errors" :key="error[0]">{{error[0]}}</li>
                    </ul>
                </div>
                <a href="#" class="change-pass-link" @click="changePassShow" :class="{hide: !hide}">Сменить пароль</a>
            </div>
            <button class="save-btn" :class="{disabled: disabled}" :disabled="disabled" @click="save">Сохранить</button>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'

export default {
    data() {
        return {
            username: '',
            email: '',
            first_name: '',
            last_name: '',
            password: '',
            password2: '',
            disabled: true,
            hide: true,
            errors: []
        }
    },
    watch: {
        username(newEl, oldEl) {
            if(oldEl != '')
                this.disabled = false
        },
        first_name(newEl, oldEl) {
            if(oldEl != '')
                this.disabled = false
        },
        last_name(newEl, oldEl) {
            if(oldEl != '')
                this.disabled = false
        },
        password2(newEl, oldEl) {
            if(this.password == this.password2)
                {
                    this.disabled = false
                    this.errors = []
                }
                else
                {
                    this.errors[0] = ["Пароли не совпадают"]
                    this.disabled = true
                }
        },
        password(newEl, oldEl) {
            if(this.password == this.password2)
                {
                    this.disabled = false
                    this.errors = []
                }
                else
                {
                    this.errors[0] = ["Пароли не совпадают"]
                    this.disabled = true
                }
        },
    },
    mounted() {
        jwtInterceptor.get('http://127.0.0.1:8000/account/user/').then(response => {
            this.username = response.data.user.username,
            this.email = response.data.user.email,
            this.first_name = response.data.user.first_name,
            this.last_name = response.data.user.last_name
        })
        .catch(err => (console.log(err.response)));
    },
    methods: {
        save() {
            let user = {
                username: this.username,
                first_name: this.first_name,
                last_name: this.last_name
            }
            if(this.password2 != '')
                user['password'] = this.password;
            jwtInterceptor.patch('http://127.0.0.1:8000/account/user/', {
                user: user
            }).then(() => {
                this.disabled = true
                localStorage.setItem('username', this.username)
                this.$emit('username', this.username)
                if(this.password2 != '')
                    this.hide = !this.hide
                })
            .catch(err => { 
                if (err.response) { 
                    this.errors = err.response.data.errors
                }
            })
        },
        changePassShow() {
            this.hide = !this.hide
        }
    }
}
</script>

<style scoped>

.change-pass {
    margin-top: 5%;
    width: 50%;
    display: flex;
    flex-direction: column;
}

.change-pass > input {
    margin-top: 10px;
}

input {
    height: 100%;
    border: 1px solid #ccc;
    box-sizing: border-box;
    border-radius: 8px;
}

.change-pass-link {
    color: #AAAAAA;
    margin-top: 20px;
}

.profile-container {
    width: 30%;
    height: 80vh;
    border: 3px solid #EAD0DE;
    border-radius: 38px;
    margin: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.profile-image {
    width: 30%;
    height: 20%;
    background-color:#C4C4C4;
    border-radius: 10%;
}

.information-container {
    width: 100%;
    height: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.save-btn {
    width: 80%;
    height: 30px;
    background: #EAD0DE;
    border-radius: 9px;
    border: none;
    cursor: pointer;
    color: white;
    font-size: 100%;
    margin-top: 10%;
    font-family: 'Noto Sans JP', sans-serif;
}

.disabled {
    background: #E6E6E6;
}

.username, .email, .first_name, .last_name {
    border-bottom: 3px solid #EAD0DE;
    width: 80%;
    height: 10%;
    text-align: center;
    margin-top: 5%;
}

.hide {
    display: none;
}

.errors {
    color: #F68F71;
}
</style>