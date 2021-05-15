<template>
    <div class="container">
        <div class="chat-list-container">
            <div class="search-container">
                <input type="text" class="search-chat">
                <button class="search-button">Искать</button>
            </div>
            <div class="message-list-container">
                <div v-for="chat in chats" :key="chat.id" class="message-container" @click="openChat(chat.id, chat.participants[0].user.first_name + ' ' + chat.participants[0].user.last_name)">
                    <div class="profile-image"></div>
                    <div class="message">
                        <div class="fio">
                            {{chat.participants[0].user.first_name}}
                            {{chat.participants[0].user.last_name}}
                        </div>
                    </div>
                </div>
            </div>
            <router-link class="add-friend-btn" to="/friends">Добавить друга</router-link>
        </div>
        <div class="chat-container" :class="{'visible': visible}">
            <div class="chat-header">
                <div class="profile-image"></div>
                <div class="person-info">
                    <span>{{fio}}</span><br>
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
      fio: '',
    }
  },
  methods: {
    openChat(chatId, fio) {
        this.chatId = chatId
        this.visible = false
        this.connect(chatId, 'fetchMessages')
        this.fio = fio
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
        const path = `ws://127.0.0.1:8000/ws/chat/${chatUrl}/`;
        this.socketRef = new WebSocket(path);
        this.socketRef.onopen = () => {
            console.log("WebSocket open");
            if(func_name == 'fetchMessages')
            {
                console.log('lol')
                this.fetchMessages(localStorage.getItem('username'), chatUrl)
            }
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
        console.log(response)
    })
    .catch(err => { 
            if (err.response.status === 500) { 
                this.$router.push('/login');
            }
        })
  }
}
</script>

<style lang="scss" scoped>
.visible {
    opacity: 0%;
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
    background: #EAD0DE; 
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
}
::-webkit-scrollbar-thumb:window-inactive {
	background: rgba(255,0,0,0.4); 
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
	background: #EAD0DE;
	align-self: flex-end;
		
	&:before {
		right: -7px;
        width: 20px;
        background-color: #EAD0DE;
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
	background: #E5E5EA;
	color: black;
    align-self: flex-start;
		
	&:before {
        left: -7px;
        width: 20px;
        background-color: #E5E5EA;
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
    background: #EAD0DE;
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
    background: #E4E3E3;
    border-radius: 8px;
}

.message-input-container {
    width: 100%;
    height: 10%;
    border-top: 3px solid #EAD0DE;
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
    border-bottom: 3px solid #EAD0DE;
    display: flex;
}

.person-info {
    margin-top: 10px;
}

.fio {
    border-bottom: 3px solid #EAD0DE;
    font-family: 'Noto Sans JP', sans-serif;
}

.message-short-text {
    width: 100%;
    height: 40%;
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 80%;
}

.profile-image {
    width: 50px;
    height: 50px;
    background: #C4C4C4;
    border-radius: 17px;
    margin: 10px;
}

.message {
    width: 60%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-family: 'Noto Sans JP', sans-serif;
}

.add-friend-btn {
    display: block;
    text-align: center;
    text-decoration: none;
    width: 100%;
    background: #EAD0DE;
    border: none;
    cursor: pointer;
    color: white;
    font-size: 100%;
    font-family: 'Noto Sans JP', sans-serif;
}

.search-chat {
    width: 70%;
    border: 2px solid #EAD0DE;
}

.search-button {
    margin-left: 10px;
    border: none;
    cursor: pointer;
    background: #EAD0DE;
    color: white;
    font-family: 'Noto Sans JP', sans-serif;
}

.message-list-container {
    width: 100%;
    height: 100%;
    background: #F0F0F0;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: auto;
}

.message-container {
    width: 90%;
    border: 3px solid #EAD0DE;
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
    border-bottom: 3px solid #EAD0DE;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-list-container {
    width: 403px;
    height: 85vh;
    display: flex;
    flex-direction: column;
    border: 3px solid #EAD0DE;
}

.chat-container {
    margin-left: 10px;
    width: 100%;
    height: 85vh;
    display: flex;
    flex-direction: column;
    border: 3px solid #EAD0DE;
}

.container {
    display: flex;
    margin: 10px;
}
</style>