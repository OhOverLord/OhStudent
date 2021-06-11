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
                <tr v-for="week in calendar()" :key="week.day">             
                    <td class="day" v-for="(day, index) in week" :class="{'weekend-day': day.weekend, 'current-day': day.current}" :key="index" @click="openTaskWindow(day, $event)"> 
                        <div class="day-index">{{day.index}}</div>
                        <div class="tasks-preview-list">
                            <div class="task-preview" :class="{'current-day-task': day.current}"></div>
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
                <div class="task">
                    <div class="task-title-container">
                        <span class="task-title">Работа</span>
                        <span class="task-time">09.00 - 15.00</span>
                    </div>
                    <div class="task-buttons">
                        <div class="task-edit-btn task-btn"></div>
                        <div class="task-done-btn task-btn"></div>
                    </div>
                </div>
            </div>
            <div class="task-tile-add-body" v-else>
                <div class="inputs-container">
                    <label for="add-task-title">Название задачи</label>
                    <input type="text" class="add-task-title" name="add-task-title">
                    <label for="add-task-title">Время начала</label>
                    <input type="text" class="add-task-time-from" name="add-task-time-from">
                    <label for="add-task-title">Время окончания</label>
                    <input type="text" class="add-task-time-to" name="add-task-time-to">
                </div>
            </div>
            <button class="task-tile-button" @click="openAddTaskWindow">+ Добавить задачу</button>
            <div class="task-tile-close-btn" @click="closeTasksWindow"></div>
        </div>
    </div>
</template>

<script>
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
        }
    },
    methods: {
        openAddTaskWindow() {
            this.showAddTask = !this.showAddTask
        },
        closeTasksWindow() {
            this.tasksWindow = false
            this.chooseDate.classList.toggle('choosen')
        },
        openTaskWindow(day, event) {
            if(!day)
                return
            this.tasksWindow = true
            this.choosenDateTitle = `${day.index} ${this.monthes[this.month]} ${this.year}`
            this.chooseDate = event.target
            this.chooseDate.classList.toggle('choosen')
        },
        calendar() {
            let days = [];
            let week = 0;
            days[week] = [];
            let dlast = new Date(this.year, this.month + 1, 0).getDate();
            let a = {}
            for (let i = 1; i <= dlast; i++) {
                if (new Date(this.year, this.month, i).getDay() != this.dFirstMonth) {
                        a = {index:i};
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
        decrease() {
            this.month--;
            if (this.month < 0) {
                this.month = 12;
                this.month--;
                this.year--;
            }
        },
        increase() {
            this.month++;
            if (this.month > 11) {
                this.month = -1;
                this.month++;
                this.year++;
            }
        },
    }
}
</script>

<style scoped>
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
    width: 100%;
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