<template>
    <div>
        <div v-if="!errors">
            <h2 style="text-align:center;">{{lecture.title}}</h2>
            <ckeditor v-model="editorData" :config="editorConfig"></ckeditor>
            <p>Создано: {{lecture.created_at.split('T')[0]}}</p>
            <p>Редактировано: {{lecture.updated_at.split('T')[0]}}</p>
            <p>Пользователь: {{lecture.user.first_name}} {{lecture.user.last_name}} ({{lecture.user.username}})</p>
        </div>
        <div v-else>
            <p>Такой лекции не существует ;(</p>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'
import { HOST_URL } from "@/settings";

export default {
    data() {
        return {
            lecture: {},
            errors: false,
            editorData: '',
            editorConfig: {
                height: '29rem',
                resize_enabled: false,
                readOnly: true,
            },
        }
    },
    mounted() {
        jwtInterceptor.post(`${HOST_URL}/lectures/public-lecture-detail/`, {
            id: this.$route.params.id
        }).then(response => {
            this.lecture = response.data
            this.editorData = this.lecture.description
            console.log(response.data)
        })
        .catch(err => {
            this.errors = true
        })
    }
}
</script>

<style scoped>

</style>