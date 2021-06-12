<template>
    <div id="app">
        <div class="container">
            <div class="diary-header">
                <div class="current-date">
                    <div class="calendar-icon"></div>
                    <span>{{date.getDate()}} {{monthes[date.getMonth()]}} {{date.getFullYear()}}</span>
                </div>
                <div class="buttons-container">
                    <div class="previous-btn" @click="decrease"></div>
                    <div class="current-month-year">{{monthes[month]}} {{year}}</div>
                    <div class="next-btn" @click="increase"></div>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <td class="days" v-for="d in day" :key="d">{{d}}</td>
                    </tr>
                </thead>
                <tr v-for="week in calendar" :key="week.day">             
                    <td class="day" v-for="(day, index) in week" :class="{'weekend-day': day.weekend, 'current-day': day.current}" :key="index" @click="openTaskWindow(day, $event)"> 
                        <div class="day-index">{{day.index}}</div>
                        <div class="tasks-preview-list" v-if="day.tasks">
                            <div v-for="(task, index) in day.tasks.slice(0, 3)" :key="index">
                                <div v-if="task.status == 'process'" class="task-preview" :class="{'current-day-task': day.current}"></div>
                            </div>
                        </div>
                    </td>
                </tr>  
            </table>
        </div>
        <div class="tasks-tile" v-if="tasksWindow">
            <div class="tasks-tile-header">
                <div class="calendar-icon"></div>
                <div>{{choosenDateTitle}}</div>
            </div>
            <div class="task-tile-body" v-if="!showAddTask">
                <div class="task" v-for="(task, index) in day_index.tasks" :key="index">
                    <div class="task-title-container" v-if="task.status == 'process'">
                        <span class="task-title">{{task.title}}</span>
                        <span class="task-time"><span v-if="task.time_from">{{task.time_from}} - </span><span v-if="task.time_to">{{task.time_to}}</span></span>
                    </div>
                    <div class="task-title-container task-title-container-done" v-else>
                        <span class="task-title">{{task.title}}</span>
                        <span class="task-time"><span v-if="task.time_from">{{task.time_from}} - </span><span v-if="task.time_to">{{task.time_to}}</span></span>
                    </div>
                    <div class="task-buttons">
                        <div class="task-edit-btn task-btn" @click="taskEdit(index)"></div>
                        <div class="task-done-btn task-btn" @click="changeTaskStatus($event, index)"></div>
                    </div>
                </div>
            </div>
            <div class="task-tile-add-body" v-else>
                <div class="inputs-container">
                    <label for="add-task-title">Название задачи</label>
                    <input type="text" class="add-task-title" name="add-task-title" v-model="taskTitle" required>
                    <label for="add-task-title">Время начала</label>
                    <input type="text" class="add-task-time-from" name="add-task-time-from" v-model="taskTimeFrom">
                    <label for="add-task-title">Время окончания</label>
                    <input type="text" class="add-task-time-to" name="add-task-time-to" v-model="taskTimeTo">
                </div>
            </div>
            <button class="task-tile-button" @click="openAddTaskWindow">+ Добавить задачу</button>
            <div class="task-tile-close-btn" @click="closeTasksWindow"></div>
        </div>
    </div>
</template>

<script>
import jwtInterceptor from '@/jwtInterceptor'

export default {
    data() {
        return {
            month: new Date().getMonth(),    
            year: new Date().getFullYear(), 
            dFirstMonth: '1',
            day:["Пн", "Вт","Ср","Чт","Пт","Сб", "Вс"],
            monthes:["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
            date: new Date(),
            tasksWindow: false,
            showAddTask: false,
            choosenDateTitle: '',
            chooseDate: '',
            taskTitle: '',
            taskTimeFrom: '',
            taskTimeTo: '',
            day_index: '',
            tasks: [],
            taskEditShow: false,
            index: ''
        }
    },
    methods: {
        taskEdit(index) {
            this.taskEditShow = true
            this.index = index
            this.taskTitle = this.day_index.tasks[index].title
            this.taskTimeFrom = this.day_index.tasks[index].time_from
            this.taskTimeTo = this.day_index.tasks[index].time_to
            this.showAddTask = !this.showAddTask
        },
        openAddTaskWindow() {
            if(this.taskEditShow) {
                jwtInterceptor.post(`http://127.0.0.1:8000/diary/task-update/`, {
                    id: this.day_index.tasks[this.index].id,
                    title: this.taskTitle,
                    time_from: this.taskTimeFrom,
                    time_to: this.taskTimeTo
                }).then(response => {
                    this.day_index.tasks[this.index] = response.data
                    this.taskEditShow = false
                    this.showAddTask = false
                    this.taskTitle = ''
                    this.taskTimeFrom = ''
                    this.taskTimeTo = ''
                })
                .catch(err => { 
                    console.warn(err)
                })
            }
            else if(this.showAddTask && this.taskTitle != '') {
                jwtInterceptor.post(`http://127.0.0.1:8000/diary/task-create/`, {
                    day: this.day_index.index,
                    month: this.month,
                    year: this.year,
                    title: this.taskTitle,
                    time_from: this.taskTimeFrom,
                    time_to: this.taskTimeTo
                }).then(response => {
                    this.day_index.tasks.push(response.data)
                    this.showAddTask = false
                    this.taskTitle = ''
                    this.taskTimeFrom = ''
                    this.taskTimeTo = ''
                })
                .catch(err => { 
                    console.warn(err)
                })
            }
            else {
                this.showAddTask = !this.showAddTask
            }
        },
        changeTaskStatus(event, index) {
            event.target.parentElement.parentElement.firstChild.classList.toggle('task-title-container-done')
            if(this.day_index.tasks[index].status == 'process')
                var status = 'completed'
            else
                var status = 'process'
            jwtInterceptor.post(`http://127.0.0.1:8000/diary/task-update/`, {
                id: this.day_index.tasks[index].id,
                status: status
            }).then(response => {
                this.day_index.tasks[index] = response.data
            })
            .catch(err => { 
                console.warn(err)
            })
        },
        closeTasksWindow() {
            this.tasksWindow = false
            this.chooseDate.classList.toggle('choosen')
            this.taskEditShow = false
            this.showAddTask = false
        },
        openTaskWindow(day, event) {
            event.stopPropagation()
            this.taskEditShow = false
            this.showAddTask = false
            if(this.chooseDate)
            {
                this.chooseDate.classList.remove('choosen')
                this.tasksWindow = false
                this.chooseDate = ''
            }
            if(!day)
                return
            if(event.target.tagName == 'TD')
                return
            this.tasksWindow = true
            this.choosenDateTitle = `${day.index} ${this.monthes[this.month]} ${this.year}`
            this.day_index = day
            this.chooseDate = event.target.parentElement
            this.chooseDate.classList.toggle('choosen')
        },
        decrease() {
            this.month--;
            if (this.month < 0) {
                this.month = 12;
                this.month--;
                this.year--;
            }
            this.getTaskListPreview()
        },
        increase() {
            this.month++;
            if (this.month > 11) {
                this.month = -1;
                this.month++;
                this.year++;
            }
            this.getTaskListPreview()
        },
        getTaskListPreview() {
            jwtInterceptor.post(`http://127.0.0.1:8000/diary/task-list-preview/`, {
                month: this.month,
                year: this.year
            }).then(response => {
                this.tasks = response.data
            })
            .catch(err => { 
                console.warn(err)
            })
        }
    },
    mounted() {
        this.getTaskListPreview()
    },
    computed: {
        calendar() {
            let days = [];
            let week = 0;
            days[week] = [];
            let dlast = new Date(this.year, this.month + 1, 0).getDate();
            let a = {}
            for (let i = 1; i <= dlast; i++) {
                let cur_tasks = []
                for(let j = 0; j < this.tasks.length; j++)
                    if(this.tasks[j].date.day == i && this.tasks[j].date.month == this.month)
                    {
                        cur_tasks.push(this.tasks[j])
                        continue
                    }
                if (new Date(this.year, this.month, i).getDay() != this.dFirstMonth) {
                        a = {index:i, tasks:cur_tasks};
                        days[week].push(a);
                        if (i == new Date().getDate() && this.year == new Date().getFullYear() && this.month == new Date().getMonth()) { a.current = 'var(--general-color)'};
                        if (new Date(this.year, this.month, i).getDay() == 6 || new Date(this.year, this.month, i).getDay() == 0) { a.weekend = 'var(--error-color)'};
                    }
                    else {
                        week++;
                        days[week] = [];
                        a = {index:i};
                        days[week].push(a);
                        if ((i == new Date().getDate()) && (this.year == new Date().getFullYear()) && (this.month == new Date().getMonth())) { a.current = 'var(--general-color)'};
                        if (new Date(this.year, this.month, i).getDay() == 6 || new Date(this.year, this.month, i).getDay() == 0) { a.weekend = 'var(--error-color)'};
                    }
                }
            if (days[0].length > 0) {
                for (let i = days[0].length; i < 7; i++) {
                    days[0].unshift('');
                }
            }
            return days;
        },
    }
}
</script>

<style scoped>
.task-title-container-done {
    text-decoration: line-through;
}

.day-index {
    height: 50%;
    width: 100%;
}

.task-preview {
    width: 10px;
    height: 10px;
    background-color: var(--general-color);
    border-radius: 10px;
    margin-left: 3px;
}

.current-day-task {
    background-color: white;
}

.tasks-preview-list {
    height: 50%;
    display: flex;
}

.choosen {
    background-color: var(--other-color);
}

.inputs-container {
    width: 70%;
    margin-top: 30px;
}

input {
    width: 100%;
    margin-bottom: 20px;
    padding: 7px;
    border-radius: 8px;
    border: 2px solid var(--general-color);
}

.task-buttons {
    width: 50%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
}

.task-btn {
    width: 20%;
    height: 80%;
    margin-left: 20px;
    border-radius: 10px;
    background-color: var(--other-color);
}

.task-edit-btn {
    background-image: url('~@/assets/pen.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 40%;
    cursor: pointer;
}

.task-done-btn {
    background-image: url('~@/assets/tick.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: 40%;
    cursor: pointer;
}

.task-title-container {
    width: 50%;
    display: flex;
    flex-direction: column;
    padding: 10px;
}

.task-title {
    font-size: 24px;
    font-family: 'Ubuntu', sans-serif;
}

.task-time {
    font-family: 'Ubuntu', sans-serif;
    font-size: 18px;
    color: gray;
}

.task {
    width: 100%;
    height: 4em;
    display: flex;
}

.task-tile-close-btn {
    width: 1.2em;
    height: 1.2em;
    position: absolute;
    top: 10px;
    right: 20px;
    background-image: url('~@/assets/cancel.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    cursor: pointer;
}

.task-tile-button {
    width: 35%;
    height: 2em;
    border: none;
    background-color: var(--general-color);
    border-radius: 6px;
    color: white;
    position: absolute;
    bottom: 10px;
    right: 30px;
    cursor: pointer;
}

.task-tile-body {
    width: 100%;
    height: 75%;
    display: flex;
    flex-direction: column;
    overflow: auto;
}

.task-tile-add-body {
    width: 100%;
    height: 75%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.tasks-tile {
    width: 35em;
    height: 25em;
    position: absolute;
    bottom: 0;
    right: 50px;
    border-radius: 39px;
    border: 3px solid var(--general-color);
    background-color: white;
    padding: 35px;
    display: flex;
    flex-direction: column;
}

.tasks-tile-header {
    height: 3em;
    margin: 10px;
    width: 50%;
    display: flex;
    align-items: flex-end;
    padding: 5px;
    border-bottom: 3px solid var(--general-color);
    border-bottom-left-radius: 10px;
}

.day {
    cursor: pointer;
    width: 100px;
}

.weekend-day {
    color: var(--error-color);
}

.current-day {
    color: white;
    background-color: var(--general-color);
}

.current-month-year {
    font-size: 24px;
    font-family: 'Ubuntu', sans-serif;
}

.container {
    width: 90vw;
    height: 80vh;
    margin: auto;
    margin-top: 50px;
}

.previous-btn {
    height: 100%;
    width: 10%;
    margin-right: 10px;
    background-image: url('~@/assets/less.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    cursor: pointer;
}

.next-btn {
    height: 100%;
    width: 10%;
    margin-left: 10px;
    background-image: url('~@/assets/greater.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    cursor: pointer;
}


.diary-header {
    width: 100%;
    height: 10%;
    display: flex;
    align-items: flex-start;
}

.current-date {
    width: 15em;
    border: 2px solid var(--general-color);
    height: 40%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    font-family: 'Ubuntu', sans-serif;
    padding: 10px;
}

.buttons-container {
    width: 100%;
    height: 60%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.calendar-icon {
    width: 25px;
    height: 25px;
    background-image: url('~@/assets/calendar.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;
    margin-right: 10px;
}

table {
    width: 100%;
    height: 90%;
    padding: 15px;
    border: 3px solid var(--general-color);
}

thead {
    text-align: center;
}

tr, td {
  border: 3px solid #DBDBDB;
}

td {
    padding: 10px;
}

.days {
    border: none;
}
</style>