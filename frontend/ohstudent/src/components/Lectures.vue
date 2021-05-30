<template>
    <div class="container">
        <div class="lectures-container">
            <div class="search-container">
                <input type="text" class="search">
            </div>
            <div class="lectures-list-container">
                <div class="lecture-tile new-lecture" @click="newLecture">
                    <div class="new-lecture-img"></div>
                </div>
                <div class="lecture-tile" v-for="lecture in lectures" :key="lecture.id" @click="chooseLecture(lecture)">
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
        <div class="lecture-container" :class="{'visible': visible}">
            <div class="lecture-header">
                <input type="text" class="lecture-title" v-model="lectureTitle" maxlength="30">
                <div class="buttons-container">
                    <div class="share-btn btn"></div>
                    <div class="save-btn btn" @click="save" v-if="!loading"></div>
                    <clip-loader v-else :loading="loading" :color="color" :size="size"></clip-loader>
                    <div class="delete-btn btn"></div>
                </div>
            </div>
            <div class="lecture-body">
                <ckeditor class="lecture-input" v-model="editorData" :config="editorConfig"></ckeditor>
            </div>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'
import ClipLoader from 'vue-spinner/src/ClipLoader.vue'
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
            loading:false
        };
    },
    methods: {
        chooseLecture(lecture) {
            this.editorData = lecture.description
            this.lectureTitle = lecture.title
            this.lectureCreatedAt = lecture.created_at.split('T')[0]
            this.visible = false
            this.choose = true
            this.lecture = lecture
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
                        description: this.editorData
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
                console.log(response)
                this.lecture.title = this.lectureTitle
                this.lecture.description = this.editorData
            })
            .catch(err => { 
                console.warn(err)
            })
        }
    },
    mounted() {
        jwtInterceptor.get('http://127.0.0.1:8000/lectures/lectures-list/').then(response => {
            this.lectures = response.data
        })
        .catch(err => { 
            console.warn(err.response)
        })
    },
    components: {
        ClipLoader,
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
}
</script>

<style scoped>
.lecture-title {
    width: 30%;
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

.new-lecture-img {
    width: 50%;
    height: 50%;
    background-image: url('~@/assets/plus.svg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
}

.visible {
    visibility: hidden;
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

.lecture-body {
    width: 100%;
    height: 100%;
}

</style>