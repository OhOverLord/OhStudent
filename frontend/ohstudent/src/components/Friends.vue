<template>
    <div>
        <div class="friends-container">
            <div class="my-friends-container">
                <h2>Мои друзья</h2>
                <div class="friend" v-for="friend in friends" :key="friend.id" >
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">{{friend.user.first_name}} {{friend.user.last_name}}</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать</button>
                        <button class="remove-friend btn" @click="deleteFriend(friend.user.id)">Удалить</button>
                    </div>
                </div>
            </div>
            <div class="add-friends-container">
                <h2>Найти друга</h2>
                <div class="search-friend-container">
                    <input type="text" class="search-input">
                    <button class="search-btn btn">Искать</button>
                </div>
                <div class="friend" v-for="(person, i) in accounts" :key="i">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">{{person.user.first_name}} {{person.user.last_name}}</span>
                    </div>
                    <div class="buttons">
                        <button class="add-friend btn" @click="addFriend(person.user.id, i)">Добавить</button>
                        <button class="send-message btn" @click="startChat(person.user.id)">Написать</button>
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
                        <button class="add-friend btn" @click="applyFriend(friends.contact.user.id)">Добавить</button>
                        <button class="send-message btn" @click="startChat(friends.contact.user.id)">Написать</button>
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
            friendRequests: []
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
                console.log(this.friends)
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
        addFriend(personId, i) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/add-friend/', {
                person_id: personId
            }).then(response => {
                console.log(response)
            })
            .catch(err => { 
                console.warn(err.response)
            })
            console.log(personId, i)
        },
        deleteFriend(personId) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/delete-friend/', {
                person_id: personId
            }).then(response => {
                console.log(response)
            })
            .catch(err => { 
                console.warn(err.response)
            })
            console.log(personId)
        },
        startChat(personId) {
            console.log(personId)
        },
        applyFriend(personId) {
            jwtInterceptor.post('http://127.0.0.1:8000/chat/apply-friend/', {
                person_id: personId
            }).then(response => {
                console.log(response)
            })
            .catch(err => { 
                console.warn(err.response)
            })
            console.log(personId)
        }
    },
    mounted() {
        this.getAllContacts()
        this.getAllFriends()
        this.getFriendRequests()
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
    border-left: 3px solid #DDBBD9;
}

.search-input {
    width: 60%;
    height: 3em;
    border: 3px solid #DDBBD9;
    box-sizing: border-box;
    border-radius: 8px;
}

.add-friend {
    background: #DDBBD9;
}

.add-friend:hover {
    background: #CFA0CA;
}

.send-message {
    background: #BEBEDA;
}

.send-message:hover {
    background: #A4A4CB;
}

.remove-friend {
    background: #FEAEAE;
}

.remove-friend:hover {
    background: #FE8686;
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

.search-btn {
    background: #DDBBD9;
    width: 30%;
    margin-left: 10px;
    box-sizing: border-box;
}

.search-btn:hover {
    background: #CFA0CA;
}

.fio {
    font-size: 100%;
    font-family: 'Noto Sans JP', sans-serif;
    margin-left: 10px;
    width: 100%;
}

.profile-image {
    width: 70px;
    height: 58px;
    background: #C4C4C4;
    border-radius: 17px;
}

h2 {
    font-family: 'Ubuntu', sans-serif; 
}

.friends-container {
    width: 90%;
    height: 80vh;
    border: 3px solid #DDBBD9;
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
    border-right: 3px solid #DDBBD9;
}

.friend {
    width: 90%;
    height: 87px;
    border-bottom: 3px solid #DDBBD9;
    border-radius: 16px;
    display: flex;
    margin-top: 10px;
    cursor: pointer;
}

.friend:hover {
    border-bottom: 3px solid #CFA0CA;
    background: #F8F2F8;
}

.search-friend-container {
    width: 70%;
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