<template>
    <div class="container">
        <div class="chat-list-container">
            <div class="search-container">
                <input type="text" class="search-chat" v-model="search">
            </div>
            <div class="message-list-container">
                <div v-for="chat in filteredChats" :key="chat.id" class="message-container" @click="openChat(chat.id)">
                    <div class="message">
                        <div class="fio" 
                        v-if="chat.participants[0].user.first_name != first_name
                              && chat.participants[0].user.last_name != last_name">
                            {{chat.participants[0].user.first_name}}
                            {{chat.participants[0].user.last_name}}
                        </div>
                        <div v-else class="fio">
                            {{chat.participants[1].user.first_name}}
                            {{chat.participants[1].user.last_name}}
                        </div>
                    </div>
                </div>
            </div>
            <router-link class="add-friend-btn" to="/friends">Добавить друга</router-link>
        </div>
        <div class="chat-container" :class="{'visible': visible}">
            <div class="chat-header">
                <!-- <div class="profile-image"></div> -->
                <div class="person-info">
                    <span>{{interclutor_fio}}</span><br>
                    <span class="status">Online</span>
                </div>
            </div>
            <div class="chat" id="chat">
                <p v-for="message in messages" :key="message.id" :class="{ 'from-me': username == message.author, 'from-them': username != message.author }">{{message.content}}</p>
            </div>
            <div class="message-input-container">
                <input v-model="messageText" v-on:keyup.enter="newMessage" type="text" class="message-input" placeholder="Написать сообщение...">
                <button class="send-message-btn" @click="newMessage">Отправить</button>
            </div>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'

export default {
  props: ['id'],
  data() {
    return {
      connection: null,
      chats: [],
      messages: [],
      socketRef: Object,
      username: localStorage.getItem('username'),
      messageText: '',
      chatId: '',
      visible: true,
      interclutor_fio: '',
      first_name: localStorage.getItem('first_name'),
      last_name: localStorage.getItem('last_name'),
      search: '',
    }
  },
  methods: {
    openChat(chatId) {
        this.chatId = chatId
        this.connect(chatId, 'fetchMessages')
    },
    newMessage() {
        if(this.messageText != '')
        {
            this.newChatMessage({
                from: localStorage.getItem('username'),
                content: this.messageText,
                chatId: this.chatId
            })
            this.messageText = ''
        }
        else {alert('Напишите сообщение... :)')}
    },
    connect(chatUrl, func_name) {
        jwtInterceptor.get(`http://127.0.0.1:8000/chat/${chatUrl}/`).then(response => {
            let participants = response.data.participants
            if (participants[0].user.first_name != this.first_name && participants[0].user.last_name != this.last_name)
                this.interclutor_fio = participants[0].user.first_name + ' ' + participants[0].user.last_name
            else
                this.interclutor_fio = participants[1].user.first_name + ' ' + participants[1].user.last_name
            this.visible = false
        })
        .catch(err => { 
            this.visible = true
            console.warn(err.response)
        })
        const path = `ws://127.0.0.1:8000/ws/chat/${chatUrl}/`;
        this.socketRef = new WebSocket(path);
        this.socketRef.onopen = () => {
            console.log("WebSocket open");
            if(func_name == 'fetchMessages')
                this.fetchMessages(localStorage.getItem('username'), chatUrl)
        };
        this.socketRef.onmessage = e => {
            this.socketNewMessage(e.data);
        };
        this.socketRef.onerror = e => {
            console.log(e.message);
        };
        this.socketRef.onclose = () => {
            console.log("WebSocket closed let's reopen");
            this.connect();
        };
    },
    fetchMessages(username, chatId) {
        this.sendMessage({
            command: "fetch_messages",
            username: username,
            chatId: chatId
        });
    },
    newChatMessage(message) {
        this.sendMessage({
            command: "new_message",
            from: message.from,
            message: message.content,
            chatId: message.chatId
        });
    },
    sendMessage(data) {
        try {
            this.socketRef.send(JSON.stringify({ ...data }));
        } catch (err) {
            console.log(err.message);
        }
    },
    socketNewMessage(data) {
        const parsedData = JSON.parse(data);
        const command = parsedData.command;
        console.log(parsedData)
        if (command === "messages") {
            this.messages = parsedData.messages;
        }
        if (command === "new_message") {
            this.messages.push(parsedData.message);
            console.log(parsedData.message)
        }
    },
    disconnect() {
        this.socketRef.close();
    },
    scrollToEnd() {
      var container = this.$el.querySelector("#chat");
      container.scrollTop = container.scrollHeight;
    },
  },
  updated() {
    this.scrollToEnd();
  },
  mounted() {
    jwtInterceptor.get('http://127.0.0.1:8000/chat/').then(response => {
        this.chats = response.data
        console.log(response.data)
    })
    .catch(err => { 
        console.warn(err.response)
    })
    if(this.$route.params.id)
    {
        this.openChat(this.$route.params.id)
        console.log(this.$route.params.id)
    }
  },
  computed: {
      filteredChats(){
            // const value = this.search.toLowerCase();
            // return this.chats.filter(function(chat){
            //     if (chat.participants[0].user.first_name == this.first_name && chat.participants[0].user.last_name == this.last_name)
            //         return chat.participants[0].user.first_name.toLowerCase().indexOf(value) > -1 ||
            //             chat.participants[0].user.last_name.toLowerCase().indexOf(value) > -1 ||
            //             (chat.participants[0].user.first_name.toLowerCase() + ' ' + chat.participants[0].user.last_name.toLowerCase()).indexOf(value) > -1
            //     else
            //         return chat.participants[1].user.first_name.toLowerCase().indexOf(value) > -1 ||
            //             chat.participants[1].user.last_name.toLowerCase().indexOf(value) > -1 ||
            //             (chat.participants[1].user.first_name.toLowerCase() + ' ' + chat.participants[1].user.last_name.toLowerCase()).indexOf(value) > -1
            // })
            const value = this.search.toLowerCase();
            const first_name = this.first_name
            const last_name = this.last_name
            let user_id = 0
            return this.chats.filter(function(chat) {
                console.log(chat.participants[0].user.first_name, first_name)
                if (chat.participants[0].user.first_name == first_name && chat.participants[0].user.last_name == last_name)
                    user_id = 1
                return chat.participants[user_id].user.first_name.toLowerCase().indexOf(value) > -1 ||
                        chat.participants[user_id].user.last_name.toLowerCase().indexOf(value) > -1 ||
                        (chat.participants[user_id].user.first_name.toLowerCase() + ' ' + chat.participants[0].user.last_name.toLowerCase()).indexOf(value) > -1
            })
        },
  }
}
</script>

<style lang="scss" scoped>
.visible {
    opacity: 0%;
}

p {
  max-width: 255px;
  word-wrap: break-word;
  line-height: 24px;
  position: relative;
  padding: 10px 20px;
  border-radius: 25px;
  
  &:before, &:after {
    content: "";
    position: absolute;
    bottom: 0;
    height: 25px;
  }
}

.from-me {
	color: white; 
	background: var(--general-color);
	align-self: flex-end;
		
	&:before {
		right: -7px;
        width: 20px;
        background-color: var(--general-color);
		border-bottom-left-radius: 16px 14px;
	}

	&:after {
		right: -26px;
        width: 26px;
        background-color: white;
		border-bottom-left-radius: 10px;
	}
}
.from-them {
	background: var(--other-color);
	color: black;
    align-self: flex-start;
		
	&:before {
        left: -7px;
        width: 20px;
        background-color: var(--other-color);
        border-bottom-right-radius: 16px 14px;
	}

	&:after {
        left: -26px;
        width: 26px;
        background-color: white;
        border-bottom-right-radius: 10px;
	}
}

.chat {
    width: 80%;
    height: 100%;
	font-size: 15px;
	font-weight: normal;
    max-width: 80%;
    display: flex;
    flex-direction: column;
    margin: auto;
    overflow: hidden;
}

.chat:hover {
    overflow-y:scroll;
    overflow-x: hidden;
}

.send-message-btn {
    height: 50%;
    background: var(--general-color);
    border: none;
    cursor: pointer;
    color: white;
    font-size: 100%;
    font-family: 'Noto Sans JP', sans-serif;
    border-radius: 5px;
    margin-left: 10px;
}

.message-input {
    width: 70%;
    height: 50%;
    border: none;
    background: var(--other-color);
    border-radius: 8px;
}

.message-input-container {
    width: 100%;
    height: 10%;
    border-top: 3px solid var(--general-color);
    display: flex;
    justify-content: center;
    align-items: center;
}

span {
    font-family: 'Noto Sans JP', sans-serif;
}

.status {
    color: gray;
}

.chat-header {
    width: 100%;
    height: 11%;
    border-bottom: 3px solid var(--general-color);
    display: flex;
}

.person-info {
    margin: 10px;
}

.fio {
    border-bottom: 3px solid var(--general-color);
    font-family: 'Noto Sans JP', sans-serif;
    width: 100%;
}

.message-short-text {
    width: 100%;
    height: 40%;
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 80%;
}

// .profile-image {
//     width: 50px;
//     height: 50px;
//     background: #C4C4C4;
//     border-radius: 17px;
//     margin: 10px;
// }

.message {
    width: 80%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-family: 'Noto Sans JP', sans-serif;
    padding: 10px;
}

.add-friend-btn {
    display: block;
    text-align: center;
    text-decoration: none;
    width: 100%;
    background: var(--general-color);
    border: none;
    cursor: pointer;
    color: white;
    font-size: 100%;
    font-family: 'Noto Sans JP', sans-serif;
}

.search-chat {
    width: 90%;
    border: 2px solid var(--general-color);
}

.message-list-container {
    width: 100%;
    height: 100%;
    background: var(--background-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: auto;
}

.message-container {
    width: 90%;
    border: 3px solid var(--general-color);
    margin-top: 5px;
    height: 13%;
    background: white;
    display: flex;
}

.message-container:hover {
    box-shadow: 8px 4px 16px 5px rgba(0,0,0,0.3);
    cursor: pointer;
}

.search-container {
    width: 100%;
    height: 40px;
    border-bottom: 3px solid var(--general-color);
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-list-container {
    width: 403px;
    height: 85vh;
    display: flex;
    flex-direction: column;
    border: 3px solid var(--general-color);
}

.chat-container {
    margin-left: 10px;
    width: 100%;
    height: 85vh;
    display: flex;
    flex-direction: column;
    border: 3px solid var(--general-color);
}

.container {
    display: flex;
    margin: 10px;
}
</style>