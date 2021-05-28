<template>
    <div class="container">
        <div class="lectures-container">
            <div class="search-container">
                <input type="text" class="search">
            </div>
            <div class="lectures-list-container">
                <div class="lecture-tile">
                    <div class="lecture-tile-header">
                        <span class="tile-title">Лекция по истории</span>
                        <span class="tile-date">29.03.2021</span>
                    </div>
                    <div class="lecture-tile-body">
                        <span class="lecture-tile-description">
                            Первоначальное значение слова «история» восходит к
                            древнегреческому термину, означавшему...
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <div class="lecture-container">
            <div class="lecture-header">
                <input type="text" class="lecture-title" value="Лекция по истории">
                <span class="lecture-date">29.03.2021</span>
            </div>
            <div class="lecture-body">
                <ckeditor class="lecture-input" v-model="editorData" :config="editorConfig"></ckeditor>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            editorData: '<p>Записывайте лекцию здесь :)</p>',
            editorConfig: {
                height: '29rem',
                resize_enabled: false,
            },
            data: '',
        };
    }
}
</script>

<style scoped>
.buttons-container {
    width: 30%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
}

.share-button {
    background: var(--add-button-color);
}

.container {
    width: 98vw;
    height: 85vh;
    margin: auto;
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
}

.lectures-container {
    width: 20%;
    height: 39em;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.lecture-container {
    width: 79%;
    height: 39em;
    border-bottom: none;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.search-container {
    width: 100%;
    padding: 10px;
    border-bottom: 3px solid var(--general-color);
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.search {
    width: 90%;
    border: 2px solid var(--general-color);
    box-sizing: border-box;
    font-family: 'Ubuntu', sans-serif;
}

.lectures-list-container {
    width: 100%;
    height: 100%;
    background: var(--other-color);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}

.lecture-tile {
    width: 90%;
    min-height: 17%;
    border: 3px solid var(--general-color);
    margin-top: 10px;
    background: white;
    font-family: 'Ubuntu', sans-serif;
}

.lecture-tile:hover {
    box-shadow: 8px 4px 16px 5px rgba(0,0,0,0.3);
    cursor: pointer;
}

.lecture-tile-header {
    width: 100%;
    border-bottom: 3px solid var(--general-color);
    box-sizing: border-box;
    display: flex;
    justify-content: space-between;
    padding: 5px;
    font-weight: bold;
}

.lecture-tile-body {
    padding: 5px;
}

.lecture-header {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    width: 100%;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
}

.lecture-body {
    width: 100%;
    height: 100%;
}

</style>