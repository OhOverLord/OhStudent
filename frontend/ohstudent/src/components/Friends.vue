<template>
    <div>
        <div class="friends-container">
            <h2>Мои друзья</h2>
            <div class="my-friends-container">
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Николай Иванов</span>
                    </div>
                    <div class="buttons">
                        <button class="send-message btn">Написать сообщение</button>
                        <button class="remove-friend btn">Удалить из друзей</button>
                    </div>
                </div>
            </div>
            <h2>Добавить друга</h2>
            <div class="add-friends-container">
                <div class="search-friend-container">
                    <input type="text" class="search-input">
                    <button class="search-btn btn">Искать</button>
                </div>
                <div class="friend">
                    <div class="person">
                        <div class="profile-image"></div>
                        <span class="fio">Иван Петров</span>
                    </div>
                    <div class="buttons">
                        <button class="add-friend btn">Добавить в друзья</button>
                        <button class="send-message btn">Написать сообщение</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.search-input {
    width: 60%;
    height: 36px;
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
    height: 36px;
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
}

.search-btn:hover {
    background: #CFA0CA;
}

.fio {
    font-size: 130%;
    font-family: 'Noto Sans JP', sans-serif;
    margin-left: 10px;
}

.profile-image {
    width: 62px;
    height: 58px;
    background: #C4C4C4;
    border-radius: 17px;
}

h2 {
    font-family: 'Ubuntu', sans-serif; 
}

.friends-container {
    width: 70%;
    height: 80vh;
    border: 3px solid #DDBBD9;
    margin: auto;
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 30px;
}

.my-friends-container {
    width: 100%;
    height: 100%;
    border-bottom: 3px solid #DDBBD9;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}

.friend {
    width: 70%;
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
    height: 87px;
    border: 3px solid #DDBBD9;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.search-friend-container:hover {
    border: 3px solid #CFA0CA;
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