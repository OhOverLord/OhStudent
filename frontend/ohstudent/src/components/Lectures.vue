<template>
    <div class="container">
        <div class="lectures-container">
            <div class="search-container">
                <input type="text" class="search" v-model="search">
            </div>
            <div class="lectures-and-folders-container" v-if="!folders">
                <div class="folders-container" @mouseover="showFolders" id="folder">
                    <div class="folder-icon"></div>
                </div>
                <div class="lectures-list-container" id="lectures-list-container">
                    <div class="lecture-tile new-lecture" @click="newLecture">
                        <div class="new-lecture-img"></div>
                    </div>
                    <div class="lecture-tile" v-for="(lecture, i) in filteredLectures" :key="lecture.id" @click="chooseLecture(lecture, i)">
                        <div class="lecture-tile-header">
                            <span class="tile-title">{{lecture.title}}</span>
                            <span class="tile-date">{{lecture.created_at.split('T')[0]}}</span>
                        </div>
                        <div class="lecture-tile-body">
                            <span class="lecture-tile-description" v-if="lecture.description.length < 40">
                                {{lecture.description.replace(/<\/?[^>]+(>|$)/g, "")}}
                            </span>
                            <span class="lecture-tile-description" v-else>
                                {{lecture.description.substr(0, 40).replace(/<\/?[^>]+(>|$)/g, "")}}...
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="lectures-and-folders-container">
                <div class="folders-list">
                    <div class="folder-tile" @click="addFolderModal">
                        <div class="folder-tile-icon add-icon"></div>
                        <div class="folder-tile-title">Добавить папку</div>
                    </div>

                    <div class="folder-tile all-lectures-folder-tile" @click="allLectures($event)">
                        <div class="folder-tile-icon"></div>
                        <div class="folder-tile-title">Все лекции</div>
                    </div>

                    <div class="folder-tile" v-for="folder in folders_list" :key="folder.id" 
                    @contextmenu.prevent="chooseFolderToEdit(folder)"
                    @click="chooseFolder(folder, $event)"
                    >
                        <div class="folder-tile-icon"></div>
                        <div class="folder-tile-title">{{folder.title}}</div>
                    </div>
                </div>
                <div class="lecture-icon-container" @mouseover="showLectures">
                    <div class="lecture-icon"></div>
                </div>
            </div>
        </div>
        <div class="lecture-container" :class="{'visible': visible}">
            <div class="lecture-header">
                <input type="text" class="lecture-title" v-model="lectureTitle" maxlength="30">
                <div class="buttons-container">
                    <div class="share-btn btn" @click="showShare"></div>
                    <div class="save-btn btn" @click="save" v-if="!loading"></div>
                    <clip-loader v-else :loading="loading" :color="color" :size="size"></clip-loader>
                    <div class="delete-btn btn" @click="showDeleteModal = true"></div>
                </div>
            </div>
            <div class="lecture-body">
                <ckeditor class="lecture-input" v-model="editorData" :config="editorConfig"></ckeditor>
            </div>
        </div>

        <!-- <div class="folder-container" :class="{'visible': !visible}">
            <div class="folder-header">
                <input type="text" class="folder-title" v-model="folder_title">
            </div>
            <div class="folder-body">

            </div>
        </div> -->

        <modal v-if="showDeleteModal" @close="showDeleteModal = false">
            <h3 slot="header">Вы точно хотите удалить?</h3>
            <div class="modal-buttons" slot="footer">
                <button class="modal-delete modal-btn" @click="share">Удалить</button>
                <button class="close modal-btn" @click="showDeleteModal = false">Закрыть</button>
            </div>
        </modal>

        <modal v-if="showDeleteModal" @close="showDeleteModal = false">
            <h3 slot="header">Вы точно хотите удалить?</h3>
            <div class="modal-buttons" slot="footer">
                <button class="modal-delete modal-btn" @click="_delete">Удалить</button>
                <button class="close modal-btn" @click="showDeleteModal = false">Закрыть</button>
            </div>
        </modal>

        <modal v-if="showShareModal" @close="showShareModal = false">
            <h3 slot="header">Поделиться:</h3>
            <div slot="body">
                <input type="text" class="share-link" v-model="link" readonly>
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-share modal-btn" @click="share">Поделиться</button>
                <button class="close modal-btn" @click="showShareModal = false">Закрыть</button>
            </div>
        </modal>

        <modal v-if="editFolderModal" @close="editFolderModal = false">
            <h3 slot="header">Папка:</h3>
            <div slot="body">
                <input type="text" class="share-link" v-model="folder_title">
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-share modal-btn" @click="editFolder">Изменить</button>
                <button class="modal-delete modal-btn" @click="deleteFolder">Удалить</button>
                <button class="close modal-btn" @click="editFolderModal = false">Закрыть</button>
            </div>
        </modal>

        <modal v-if="showAddFolderModal" @close="showAddFolderModal = false">
            <h3 slot="header">Новая папка:</h3>
            <div slot="body">
                <input type="text" class="share-link" v-model="folder_title">
            </div>
            <div class="modal-buttons" slot="footer">
                <button class="modal-share modal-btn" @click="addFolder">Добавить папку</button>
                <button class="close modal-btn" @click="showAddFolderModal = false">Закрыть</button>
            </div>
        </modal>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
import modal from '@/components/Modal'
import _ from 'lodash';

export default {
    data() {
        return {
            editorData: '',
            editorConfig: {
                height: '29rem',
                resize_enabled: false,
            },
            data: '',
            lectureTitle: '',
            lectureCreatedAt: '',
            lectures: [],
            visible: true,
            choose: false,
            lecture: {},
            color: '#9ED1AE',
            size: '30px',
            loading:false,
            index: '',
            showDeleteModal: false,
            showShareModal: false,
            link: '',
            search: '',
            folders: false,
            folders_list: [],
            folder_title: '',
            folder: {},
            editFolderModal: false,
            showAddFolderModal: false,
        };
    },
    methods: {
        chooseLecture(lecture, index) {
            this.editorData = lecture.description
            this.lectureTitle = lecture.title
            this.lectureCreatedAt = lecture.created_at.split('T')[0]
            this.visible = false
            this.choose = true
            this.lecture = lecture
            this.index = index
            console.log(this.lecture)
        },
        get_folders() {
            jwtInterceptor.get('http://127.0.0.1:8000/lectures/folder-list/').then(response => {
                this.folders_list = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        newLecture() {
            this.editorData = ''
            this.lectureTitle = ''
            this.lectureCreatedAt = new Date().toJSON().slice(0,10).replace(/-/g,'-');
            this.visible = false
            this.choose = false
        },
        save() {
            if(!this.choose)
            {
                if(this.lectureTitle != '' && this.editorData != '')
                {
                    jwtInterceptor.post('http://127.0.0.1:8000/lectures/create/', {
                        title: this.lectureTitle,
                        description: this.editorData,
                        folder: this.folder.id
                    }).then(response => {
                        this.lectures.unshift(response.data)
                        this.choose = true
                        this.lecture = response.data
                    })
                    .catch(err => { 
                        console.warn(err.response)
                    })
                }
                else
                    return
            }
            else
                this.update()
            this.loading = false
        },
        update() {
            jwtInterceptor.post(`http://127.0.0.1:8000/lectures/update/`, {
                title: this.lectureTitle,
                description: this.editorData,
                id: this.lecture.id
            }).then(response => {
                this.lecture.title = this.lectureTitle
                this.lecture.description = this.editorData
            })
            .catch(err => { 
                console.warn(err)
            })
        },
        _delete() {
            if(this.choose) {
                console.log(this.index)
                jwtInterceptor.post(`http://127.0.0.1:8000/lectures/delete/`, {
                    id: this.lecture.id
                }).then(response => {
                    console.log(response)
                    this.lectures.splice(this.index, 1)
                })
                .catch(err => { 
                    console.warn(err)
                })
            }
            this.visible = true
            this.showDeleteModal = false
        },
        share() {
            jwtInterceptor.post('http://127.0.0.1:8000/lectures/share/', {
                id: this.lecture.id
            }).then(() => {
                alert("Ссылка скопирована")
            })
            .catch(err => {
                console.warn(err.response)
            })
            this.showShareModal = false
        },
        showShare() {
            this.showShareModal = true
            this.link = `http://localhost:8080${this.lecture.absolute_url}`
        },
        showFolders() {
            this.folders = true
        },
        showLectures() {
            this.folders = false
        },
        chooseFolderToEdit(folder) {
            this.folder = folder
            this.visible = true
            this.folder_title = this.folder.title
            this.editFolderModal = true
        },
        chooseFolder(folder, event) {
            event.stopPropagation()
            this.folder = folder
            this.getLectures(folder.id)
            this.folders = false
            event.target.style.backgroundColor = "black";
            console.log(event.target)
        },
        allLectures(event) {
            this.getLectures()
            this.folders = false
        },
        editFolder() {
            jwtInterceptor.post('http://127.0.0.1:8000/lectures/folder-update/', {
                id: this.folder.id,
                title: this.folder_title
            }).then(response => {
                let index;
                for(let i=0; i<this.folders_list.length; i++)
                {
                    if( this.folder.id === this.folders_list[i].id )
                    {
                        index = i
                    }
                }
                this.editFolderModal = false
                this.folders_list[index] = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        },
        deleteFolder() {
            jwtInterceptor.post('http://127.0.0.1:8000/lectures/folder-delete/', {
                id: this.folder.id,
            }).then(response => {
                let index;
                for(let i=0; i<this.folders_list.length; i++)
                {
                    if( this.folder.id === this.folders_list[i].id )
                    {
                        index = i
                    }
                }
                this.editFolderModal = false
                this.folders_list.splice(index, 1)
            })
            .catch(err => { 
                console.warn(err)
            })
        },
        addFolderModal() {
            this.showAddFolderModal = true
        },
        addFolder() {
            jwtInterceptor.post('http://127.0.0.1:8000/lectures/folder-create/', {
                title: this.folder_title
            }).then(response => {
                this.folders_list.push(response.data)
                this.showAddFolderModal = false
                this.folder_title = ''
            })
            .catch(err => { 
                console.warn(err)
            })
        },
        getLectures(folder = null) {
            jwtInterceptor.post('http://127.0.0.1:8000/lectures/lectures-list/', {
                folder:folder
            }).then(response => {
                this.lectures = response.data
            })
            .catch(err => { 
                console.warn(err.response)
            })
        }
    },
    mounted() {
        this.getLectures()
        this.get_folders()
    },
    components: {
        ClipLoader,
        modal
    },
    watch: {
        editorData() {
            this.loading = true
            this.debounced()
        },
        lectureTitle() {
            this.loading = true
            this.debounced()
        }
    },
    created() {
        this.debounced = _.debounce(this.save, 500)
    },
    computed: {
        filteredLectures(){
            const value = this.search.toLowerCase();
            return this.lectures.filter(function(lecture){
                return lecture.title.toLowerCase().indexOf(value) > -1
            })
        },
    }
}
</script>

<style>
.modal-delete {
    background-color: var(--button-delete-color);
    margin-bottom: 10px;
}
/* .folder-container {
    width: 55em;
    height: 39em;
    border-bottom: none;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.folder-body {
    width: 100%;
    height: 100%;
    background-color: gray;
} */

.all-lectures-folder-tile {
    background-color: var(--light-general-color) !important;
}

.folder-tile-title {
    margin-left: 10px;
    font-family: 'Ubuntu', sans-serif;
}

.folder-tile-icon {
    background-image: url('~@/assets/folder.png');
    width: 28px;
    height: 27px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.add-icon {
    background-image: url('~@/assets/add-folder.png');
}

.folder-tile {
    width: 25em;
    height: 2em;
    display: flex;
    align-items: center;
    padding: 10px;
    border: 3px solid var(--general-color);
    background-color: white;
    margin-top: 10px;
    cursor: pointer;
}

.folder-tile:hover {
    box-shadow: 8px 4px 16px 5px rgba(0,0,0,0.3);
}

.folders-list {
    height: 100%;
    width: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: auto;
}

.lecture-icon-container {
    height: 100%;
    width: 10%;
    border-left: 2px solid var(--general-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

.lecture-icon {
    background-image: url('~@/assets/document.png');
    width: 65%;
    height: 10%;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.folder-icon {
    background-image: url('~@/assets/folder.png');
    width: 65%;
    height: 10%;
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.share-link {
    width: 100%;
}

.lecture-title {
    width: 30%;
}

.folder-title {
    width: 30%;
    font-size: 100%;
}

.buttons-container {
    width: 20%;
    height: 2em;
    display: flex;
    justify-content: space-between;
    border-left: 3px solid var(--general-color);
    border-right: 3px solid var(--general-color);
}

.btn {
    width: 20%;
    height: 100%;
    border-radius: 30%;
    cursor: pointer;
    background-position: center;
    background-repeat: no-repeat;
    background-size: 50%;
}

.share-btn {
    background-image: url('~@/assets/share.svg');
}

.share-btn:hover {
    background-color: var(--light-general-color);
}

.save-btn {
    background-image: url('~@/assets/floppy-disk.svg');
}

.save-btn:hover {
    background-color: var(--light-general-color);
}

.delete-btn {
    background-image: url('~@/assets/delete.svg');
}

.delete-btn:hover {
    background-color: var(--button-delete-color);
}

.modal-delete {
    background: var(--button-delete-color);
}

.modal-delete:hover {
    background: var(--button-delete-color-hover);
}

.modal-share {
    background: var(--add-button-color);
}

.modal-share:hover {
    background: var(--add-button-color-hover);
}


.modal-btn {
  width: 45%;
  height: 50%;
  border-radius: 5px;
  border: none;
  font-size: 90%;
  cursor: pointer;
  color: white;
  margin-left: 10px;
}

.close {
    background-color: var(--button-color);
}

.new-lecture-img {
    width: 50%;
    height: 50%;
    background-image: url('~@/assets/plus.svg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
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
    width: 35em;
    height: 39em;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.lecture-container {
    width: 55em;
    height: 39em;
    border-bottom: none;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
}

.search-container {
    width: 100%;
    height: 10%;
    border-bottom: 3px solid var(--general-color);
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.search {
    width: 90%;
    height: 50%;
    border: 2px solid var(--general-color);
    box-sizing: border-box;
    font-family: 'Ubuntu', sans-serif;
}

.lectures-list-container {
    width: 90%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: auto;
}

/* .lectures-animation {
    overflow: hidden;
    animation-duration: 3s;
    animation-name: expansion;
    animation-timing-function: linear;
} */

.lectures-and-folders-container {
    width: 100%;
    height: 90%;
    background: var(--other-color);
    display: flex;
}

.folders-container {
    width: 10%;
    height: 100%;
    border-right: 2px solid var(--general-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

/* .folder-animation {
    animation-duration: 3s;
    animation-name: expansion;
    animation-timing-function: linear;
} */

/* @keyframes expansion {
  from {
    width: 10%;
  }

  to {
    width: 200%;
  }
}

@keyframes compression {
  from {
    width: 90%;
  }

  to {
    width: 10%;
  }
} */

.lecture-tile {
    width: 90%;
    min-height: 17%;
    border: 3px solid var(--general-color);
    margin-top: 10px;
    background: white;
    font-family: 'Ubuntu', sans-serif;
}

.new-lecture {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--light-general-color);
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
    width: 100%;
    height: 5em;
    padding-left: 10px;
    padding-right: 10px;
    align-items: center;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
}

/* .folder-header {
    width: 100%;
    height: 3.5em;
    border: 3px solid var(--general-color);
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
} */

/* .lecture-body {
    width: 100%;
    height: 100%;
} */

.visible {
    display: none;
}
</style>