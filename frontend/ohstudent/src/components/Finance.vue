<template>
    <div class="container">
        <p class="title">Учёт финансов:</p>
        <div class="wallets-container">
            <div class="wallet">
                <span class="balance">10000₽</span>
                <span class="balance-description">В наличии по всем кошелькам</span>
            </div>
            <div class="wallet">
                <span class="balance">10000₽</span>
                <span class="balance-description">Зарплата</span>
            </div>
            <div class="wallet add-wallet" @click="showAddWAlletModal = true">
            </div>
        </div>
        <div class="finance-container">
            <div class="categories-container">
                <span>Категория</span>
                <div class="categories-list">
                    <div class="category">
                        <span>Такси</span>
                    </div>
                </div>
                <button class="add-category-btn">
                    Добавить категорию
                </button>
            </div>
            <div class="spending-container">
                <div class="spending-list">
                    <div class="spending">
                        <div>
                            <span class="date">31.03.2021</span>
                            <span class="description">Такси до дома</span>
                        </div>
                        <span class="summ">1000₽</span>
                    </div>

                    <div class="spending">
                        <div>
                            <span class="date">31.03.2021</span>
                            <span class="description">Такси до дома</span>
                        </div>
                        <span class="summ">1000₽</span>
                    </div>

                    <div class="spending">
                        <div>
                            <span class="date">31.03.2021</span>
                            <span class="description">Такси до дома</span>
                        </div>
                        <span class="summ">1000₽</span>
                    </div>

                </div>
                <div class="add-spending">
                    <div class="inputs-container">
                        <textarea type="text" placeholder="Описание..." class="spending-descrtiption"></textarea>
                        <input type="number" class="spending-summ">
                        <select name="wallet">
                            <option>wallet 1</option>
                            <option>wallet 2</option>
                        </select>
                    </div>
                    <button class="add-spending-btn">Добавить</button>
                </div>
            </div>
        </div>
        <modal v-if="showAddWAlletModal" @close="showAddWAlletModal = false">
            <h3 slot="header">Добавить кошелёк:</h3>
            <div slot="body">
                <input type="text" class="share-link" v-model="link" readonly>
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-share modal-btn" @click="share">Добавить</button>
                <button class="close modal-btn" @click="showAddWAlletModal = false">Закрыть</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@/components/Modal'

export default {
    data() {
        return {
            showAddWAlletModal: false,
        }
    },
    components: {
        modal,
    }
}
</script>

<style scoped>
.modal-btn {
  width: 45%;
  height: 50%;
  border-radius: 5px;
  border: none;
  margin-left: 10px;
  font-size: 90%;
  cursor: pointer;
  color: white;
}

.modal-share {
    background: var(--add-button-color);
}

.modal-share:hover {
    background: var(--add-button-color-hover);
}

.add-spending-btn {
    width: 17em;
    height: 20%;
    border-radius: 6px;
    background: var(--general-color); 
    border: none;
    cursor: pointer;
    color: white;
}

.inputs-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

select {
    background: #E4E3E3;
    border-radius: 8px;
}

textarea {
    resize: none;
    width: 40em;
    height: 4em;
    margin-bottom: 10px;
    background: #E4E3E3;
    border-radius: 8px;
}

input {
    margin-bottom: 10px;
    background: #E4E3E3;
    border: none;
    border-radius: 8px;
    box-sizing: border-box;
    padding: 3px;
}

.description {
    margin-left: 10px;
}

.spending {
    width: 49em;
    height: 2em;
    border: 3px solid var(--general-color);
    border-radius: 6px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px;
}

.spending-list {
    width: 100%;
    height: 50%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}

.add-spending {
    width: 90%;
    height: 25%;
    border-radius: 6px;
    border: 2px solid var(--general-color);
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 10px;
    margin-bottom: 10px;
}

.spending-container {
    width: 54em;
    height: 100%;
    margin-left: 25px;
    border-radius: 28px;
    border: 2px solid var(--general-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
}

span {
    font-size: 18px;
    font-family: 'Ubuntu', sans-serif;
}

.add-category-btn {
    width: 17em;
    height: 10%;
    border-radius: 6px;
    background: var(--general-color); 
    border: none;
    cursor: pointer;
    color: white;
}

.category {
    width: 14em;
    height: 10%;
    border: 2px solid var(--general-color);
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    border-radius: 6px;
    margin-top: 10px;
}

.categories-container {
    text-align: center;
    width: 17em;
    height: 100%;
    border: 2px solid var(--general-color);
    box-sizing: border-box;
    border-radius: 28px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.categories-list {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: auto;
}

.finance-container {
    width: 100%;
    height: 30em;
    margin-top: 20px;
    display: flex;
}
.balance {
    font-size: 36px;
    display: block;
}

.balance-description {
    font-size: 14px;
}

.container {
    margin: auto;
    width: 90vw;
}
.title {
    font-size: 36px;
    margin-bottom: 16px;
    font-family: 'Ubuntu', sans-serif;
}

.wallets-container {
    width: 90vw;
    height: 10em;
    margin: auto;
    display: flex;
    justify-content: flex-start;
}

.wallet {
    width: 17em;
    height: 100%;
    border-radius: 17px;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    margin-right: 45px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    padding: 30px;
    font-family: 'Ubuntu', sans-serif;
}

.add-wallet {
    width: 17em;
    background: var(--general-color);
    background-image: url('~@/assets/plus.svg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 20%;
    cursor: pointer;
}

.add-wallet:hover {
    background-color: var(--light-general-color);
}
</style>