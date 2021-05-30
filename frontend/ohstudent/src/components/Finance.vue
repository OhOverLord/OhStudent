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
            <div class="wallet add-wallet">

            </div>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
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
}

.wallets-container {
    width: 90vw;
    height: 25vh;
    margin: auto;
    display: flex;
    justify-content: flex-start;
}

.wallet {
    width: 17em;
    height: 100%;
    border-radius: 17px;
    border: 3px solid #EAD0DE;
    box-sizing: border-box;
    margin-right: 45px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    padding: 30px;
}

.add-wallet {
    width: 17em;
    background: #EAD0DE;
    background-image: url('~@/assets/plus.svg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 20%;
}
</style>