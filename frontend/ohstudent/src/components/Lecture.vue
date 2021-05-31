<template>
    <div>
        <div v-if="!errors">
            <h2>{{lecture.title}}</h2>
            <p>{{lecture.description}}</p>
        </div>
        <div v-else>
            <p>Такой лекции не существует ;(</p>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'

export default {
    data() {
        return {
            lecture: {},
            errors: false
        }
    },
    mounted() {
        jwtInterceptor.post('http://127.0.0.1:8000/lectures/public-lecture-detail/', {
            id: this.$route.params.id
        }).then(response => {
            this.lecture = response.data
            console.log(response.data)
        })
        .catch(err => {
            this.err = true
        })
    }
}
</script>

<style scoped>

</style>