<template>
    <div class="container">
        <p class="title">Учёт финансов:</p>
        <div class="wallets-container">
            <div class="wallet">
                <span class="balance" v-if="wallets_sum.rubles != null">{{wallets_sum.rubles}}</span>
                <span class="balance" v-if="wallets_sum.dollars != null">{{wallets_sum.dollars}}</span>
                <span class="balance" v-if="wallets_sum.euros != null">{{wallets_sum.euros}}</span>
                <span class="balance-description">В наличии по всем кошелькам</span>
            </div>
            <div class="wallet" v-for="(wallet, i) in wallets" :key="i" @click="chooseWallet(wallet.id)">
                <span class="balance">{{wallet.money}}{{wallet.currency}}</span>
                <span class="balance-description">{{wallet.description}}</span>
                <button class="edit-wallet-btn" @click="showWalletModel(wallet, i)">Редактировать</button>
            </div>
            <div v-if="wallets.length < 3" class="wallet add-wallet" @click="showAddWalletModal = true">
            </div>
        </div>
        <div class="finance-container" :class="{'visible': !visible}">
            <div class="categories-container">
                <span>Категория</span>
                <div class="categories-list">
                    <div class="category" v-for="category in categories" :key="category.id" @click="chooseCategory(category.id)">
                        <span>{{category.title}}</span>
                    </div>
                </div>
                <button class="add-category-btn" @click="showCategoryModal = true">
                    Добавить категорию
                </button>
            </div>
            <div class="spending-container" :class="{'visible': !spendingFormVisible}">
                <div class="spending-list">
                    <div class="spending" v-for="spending in spendings" :key="spending.id">
                        <div>
                            <span class="date">{{spending.date.split('T')[0]}}</span>
                            <span class="description">{{spending.title}}</span>
                        </div>
                        <span class="summ">{{spending.money}}</span>
                    </div>
                </div>
                <div class="add-spending">
                    <div class="inputs-container">
                        <textarea type="text" placeholder="Описание..." class="spending-descrtiption" v-model="spendingTitle"></textarea>
                        <input type="number" class="spending-summ" min="0" v-model="spendingMoney">
                    </div>
                    <button class="add-spending-btn" @click="addSpending">Добавить</button>
                </div>
            </div>
        </div>

        <modal v-if="showAddWalletModal" @close="showAddWalletModal = false">
            <h3 slot="header">Добавить кошелёк:</h3>
            <div slot="body" class="add-wallet-body">
                <label for="money">Количество деняк :(</label>
                <input type="number" class="money" name="money" min="0" v-model="money">
                <label for="description">Описание кошелька:</label>
                <input type="text" name="description" placeholder="работа..." v-model="description">
                <label for="currency">Валюта:</label>
                <select name="currency" v-model="currency">
                    <option value="₽">Рубли</option>
                    <option value="$">Доллары</option>
                    <option value="€">Евро</option>
                </select>
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-add modal-btn" @click="addWallet">Добавить</button>
                <button class="close modal-btn" @click="showAddWalletModal = false">Закрыть</button>
            </div>
        </modal>

        <modal v-if="walletModal" @close="walletModal = false">
            <h3 class="wallet-model-header" slot="header"><span>Редактировать кошелёк:</span> <div class="modal-wallet-close" @click="walletModal = false">X</div></h3>
            <div slot="body" class="add-wallet-body">
                <label for="money">Количество деняк :(</label>
                <input type="number" class="money" name="money" min="0" v-model="money">
                <label for="description">Описание кошелька:</label>
                <input type="text" name="description" placeholder="работа..." v-model="description">
                <label for="currency">Валюта:</label>
                <select name="currency" v-model="currency">
                    <option value="₽">Рубли</option>
                    <option value="$">Доллары</option>
                    <option value="€">Евро</option>
                </select>
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-add modal-btn" @click="editWallet">Редактировать</button>
                <button class="modal-delete modal-btn" @click="deleteWallet">Удалить</button>
            </div>
        </modal>

        <modal v-if="showCategoryModal" @close="showCategoryModal = false">
            <h3 slot="header">Добавить категорию:</h3>
            <div slot="body" class="category-model-body">
                <label for="title">Название:</label>
                <input type="text" name="title" placeholder="Продукты..." v-model="categoryTitle">
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-add modal-btn" @click="addCategory">Добавить</button>
                <button class="close modal-btn" @click="showCategoryModal = false">Закрыть</button>
            </div>
        </modal>
    </div>
</template>

<script>
import modal from '@/components/Modal'
import jwtInterceptor from '@/jwtInterceptor'

export default {
    data() {
        return {
            showAddWalletModal: false,
            walletModal: false,
            wallets: [],
            money: 0,
            description: '',
            currency: '₽',
            current_wallet: '',
            wallets_sum: {},
            visible: false,
            categories: [],
            spendingFormVisible: false,
            categoryTitle: '',
            currentCategory: '',
            showCategoryModal: false,
            choosenWallet: '',
            spendings: [],
            spendingTitle: '',
            spendingMoney: '',
        }
    },
    components: {
        modal,
    },
    mounted() {
        this.getWallets()
        this.getWalletsSum()
    },
    watch: {
        money() {
            if(this.money < 0)
            {
                alert("Баланс не может быть отрицательным... :)")
                this.money = 0
            }
        }
    },
    methods: {
        addWallet() {
            if(this.description != '')
            {
                jwtInterceptor.post('http://127.0.0.1:8000/finance/wallet-create/', {
                    money: this.money,
                    description: this.description,
                    currency: this.currency
                }).then(response => {
                    this.wallets.push(response.data)
                    this.showAddWalletModal = false
                    this.clearWalletFields()
                    this.getWalletsSum()
                })
                .catch(err => { 
                    console.warn(err.response)
                })
            }
            else
                alert("Заполните описание кошелька")
        },
        showWalletModel(wallet, i) {
            this.walletModal = true
            this.money = wallet.money
            this.description = wallet.description
            this.currency = wallet.currency
            this.current_wallet = i
        },
        getWallets() {
            jwtInterceptor.get('http://127.0.0.1:8000/finance/wallet-list/').then(response => {
                this.wallets = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        editWallet() {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/wallet-update/', {
                id: this.wallets[this.current_wallet].id,
                money: this.money,
                description: this.description,
                currency: this.currency
            }).then(response => {
                this.getWallets()
                this.getWalletsSum()
                this.walletModal = false
                this.clearWalletFields()
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        deleteWallet() {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/wallet-delete/', {
                id: this.wallets[this.current_wallet].id,
            }).then(response => {
                this.getWallets()
                this.getWalletsSum()
                this.walletModal = false
                this.clearWalletFields()
                this.visible = false
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        clearWalletFields() {
            this.money = ''
            this.description = ''
            this.currency = ''
        },
        getWalletsSum() {
            jwtInterceptor.get('http://127.0.0.1:8000/finance/wallets-result/').then(response => {
                this.wallets_sum = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        chooseWallet(id) {
            this.visible = true
            this.getCategories(id)
            this.choosenWallet = id
            this.spendingFormVisible = false
        },
        getCategories(wallet) {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/category-list/', {
                wallet: wallet
            }).then(response => {
                this.categories = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        chooseCategory(id) {
            this.spendingFormVisible = true
            this.currentCategory = id
            this.getSpendings(id)
        },
        addCategory() {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/category-create/', {
                title: this.categoryTitle,
                wallet: this.choosenWallet
            }).then(response => {
                this.categories.push(response.data)
                this.showCategoryModal = false
                this.categoryTitle = ''
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        getSpendings(category) {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/consumption-list/', {
                category: category
            }).then(response => {
                this.spendings = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        addSpending() {
            jwtInterceptor.post('http://127.0.0.1:8000/finance/consumption-create/', {
                title: this.spendingTitle,
                money: this.spendingMoney,
                category: this.currentCategory
            }).then(response => {
                this.spendings.push(response.data)
                this.spendingTitle = ''
                this.spendingMoney = ''
            })
            .catch(err => { 
                console.warn(err.response)
            })
        }
    }
}
</script>

<style scoped>
.category-model-body {
    display: flex;
    flex-direction: column;
}

.visible {
    opacity: 0%;
}

.modal-wallet-close {
    color: gray;
    cursor: pointer;
}

.wallet-model-header {
    display: flex;
    justify-content: space-between;
}

.add-wallet-body {
    display: flex;
    flex-direction: column;
}

.balance {
    padding: 15px 15px 0;
}

.balance-description {
    padding-right: 15px;
}

.modal-btn {
  width: 45%;
  height: 50%;
  border-radius: 5px;
  border: none;
  font-size: 90%;
  cursor: pointer;
  color: white;
}

.modal-add {
    background: var(--add-button-color);
}

.modal-add:hover {
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
    justify-content: flex-start;
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
    align-items: flex-start;
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
    cursor: pointer;
}

.category:hover {
    background-color: var(--light-general-color);
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
    font-size: 25px;
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
    height: 10em;
    margin: auto;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}

.wallet {
    width: 249px;
    height: 100%;
    border-radius: 17px;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    margin-right: 45px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    font-family: 'Ubuntu', sans-serif;
    position: relative;
}

.edit-wallet-btn {
    width: 100%;
    position: absolute;
    bottom: 0;
    border-radius: 0 0 13px 13px;
    cursor: pointer;
    border: none;
    background: var(--general-color);
    color: white;
}

.add-wallet {
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

.wallet:hover {
    background-color: var(--light-general-color);
}

.modal-delete {
    background: var(--button-delete-color);
}

.modal-close {
    width: 100%;
    margin-top: 10px;
}

.modal-buttons {
    display: flex;
    justify-content: space-between;
}
</style>