<template>
    <div>
        <div class="friends-container">
            <div class="my-friends-container">
                <h2>Мои друзья</h2>
                <div class="friend" v-for="(friend, i) in friends" :key="i" >
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">{{friend.user.first_name}} {{friend.user.last_name}}</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn" @click="startChat(friend.user.username)">Написать</button>
                        <button class="remove-friend btn" @click="deleteFriend(i, friend.user.id)">Удалить</button>
                    </div>
                </div>
            </div>
            <div class="add-friends-container">
                <h2>Найти друга</h2>
                <div class="search-friend-container">
                    <input type="text" class="search-input" v-model="search">
                </div>
                <div class="friend" v-for="(person, i) in filteredAccounts" :key="i">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">{{person.user.first_name}} {{person.user.last_name}}</span>
                    </div>
                    <div class="buttons">
                        <button class="add-friend btn" @click="addFriend(person.user.id, i)">Добавить</button>
                        <button class="send-message btn" @click="startChat(person.user.username)">Написать</button>
                    </div>
                </div>
            </div>
            <div class="friend-requests">
                <h2>Заявки в друзья</h2>
                <div class="friend" v-for="(friends, i) in friendRequests" :key="i">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">{{friends.contact.user.first_name}} {{friends.contact.user.last_name}}</span>
                    </div>
                    <div class="buttons">
                        <button class="add-friend btn" @click="applyFriend(i, friends.contact.user.id)">Добавить</button>
                        <button class="send-message btn" @click="startChat(friends.contact.user.username)">Написать</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'

export default {
    data() {
        return {
            accounts: [],
            friends: [],
            friendRequests: [],
            search: '',
        }
    },
    methods: {
        getAllContacts() {
            jwtInterceptor.get('http://127.0.0.1:8000/chat/contact-list/').then(response => {
                this.accounts = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        getAllFriends() {
            jwtInterceptor.get('http://127.0.0.1:8000/chat/friends-list/').then(response => {
                for(let pairs of response.data)
                    if(pairs.contact.user.username != localStorage.getItem('username'))
                        this.friends.push(pairs.contact)
                    else
                        this.friends.push(pairs.friend)
            })
            .catch(err => { 
                console.warn(err)
            })
        },
        getFriendRequests() {
            jwtInterceptor.get('http://127.0.0.1:8000/chat/friend-requests-list/').then(response => {
                this.friendRequests = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        addFriend(personId, index) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/add-friend/', {
                person_id: personId
            }).then(response => {
                this.accounts.find((o, i) => {
                    if (o.user.id === this.filteredAccounts[index].user.id) {
                        this.accounts.splice(i, 1)
                        return true;
                    }
                })
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        deleteFriend(i, personId) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/delete-friend/', {
                person_id: personId
            }).then(response => {
                this.friends.splice(i, 1)
                this.accounts.push(response.data)
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        startChat(username) {
            let interclutor = username
            let currentUser = localStorage.getItem('username')
            jwtInterceptor.post('http://127.0.0.1:8000/chat/create/', {
                    messages: [],
                    participants: [interclutor, currentUser]
            }).then(response => {
                this.$router.push(`/chat/${response.data.id}`)
            })
            .catch(err => { 
                if (err.response) { 
                    this.errors = err.response.data.errors
                }
            })
        },
        applyFriend(i, personId) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/apply-friend/', {
                person_id: personId
            }).then(response => {
                this.friendRequests.splice(i, 1)
                this.friends.push(response.data)
                console.log(response.data)
            })
            .catch(err => { 
                console.warn(err)
            })
            console.log(personId)
        }
    },
    mounted() {
        this.getAllContacts()
        this.getAllFriends()
        this.getFriendRequests()
    },
    computed: {
        filteredAccounts(){
            const value = this.search.toLowerCase();
            return this.accounts.filter(function(account){
                return account.user.first_name.toLowerCase().indexOf(value) > -1 ||
                        account.user.last_name.toLowerCase().indexOf(value) > -1 ||
                        (account.user.first_name.toLowerCase() + ' ' + account.user.last_name.toLowerCase()).indexOf(value) > -1
            })
        },
    }
}
</script>

<style scoped>
.friend-requests {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
    border-left: 3px solid var(--general-color);
}

.search-input {
    width: 100%;
    height: 3em;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    border-radius: 8px;
}

.add-friend {
    background: var(--add-button-color);
}

.add-friend:hover {
    background: var(--add-button-color-hover);
}

.send-message {
    background: var(--button-color);
}

.send-message:hover {
    background: var(--button-color-hover);
}

.remove-friend {
    background: var(--button-delete-color);
}

.remove-friend:hover {
    background: var(--button-delete-color-hover);
}

.person {
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.buttons {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.btn {
    width: 45%;
    height: 2.5em;
    color: white;
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 100%;
    border-radius: 8px;
    cursor: pointer;
    border: none;
}

.fio {
    font-size: 100%;
    font-family: 'Noto Sans JP', sans-serif;
    margin-left: 10px;
    width: 100%;
}

/* .profile-image {
    width: 70px;
    height: 58px;
    background: #C4C4C4;
    border-radius: 17px;
} */

h2 {
    font-family: 'Ubuntu', sans-serif; 
}

.friends-container {
    width: 90%;
    height: 80vh;
    border: 3px solid var(--general-color);
    margin: auto;
    margin-top: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 30px;
}

.my-friends-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
    border-right: 3px solid var(--general-color);
}

.friend {
    width: 90%;
    height: 87px;
    border-bottom: 3px solid var(--general-color);
    border-radius: 16px;
    display: flex;
    margin-top: 10px;
    cursor: pointer;
}

.friend:hover {
    border-bottom: 3px solid var(--general-color);
    background: var(--light-general-color);
}

.search-friend-container {
    width: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.add-friends-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}
</style>