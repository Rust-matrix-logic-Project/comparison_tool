export class Timer{
    timer: HTMLElement;
    start_timer: HTMLButtonElement;
    end_timer: HTMLButtonElement;
    constructor(){
        this.timer = document.createElement('div');
        this.timer.classList.add('timer');
        this.timer.id = 'timer'
        
        
        this.timer.style.textAlign = 'center'

        this.start_timer = document.createElement('button');
        this.start_timer.classList.add('start');
        this.start_timer.id = 'start'
        this.start_timer.textContent = '開始'

        this.end_timer = document.createElement('button');
        this.end_timer.classList.add('end');
        this.end_timer.id = 'end'
        this.end_timer.textContent = '終了'
    }

    render(){
        const container = document.querySelector('.main-area');
        container?.append(this.timer)
        let count = 0;

        let isTracking: boolean = false;
        
        this.start_timer.addEventListener("click", () => {
            if(isTracking === true){
                alert('既に開始しています')
                return
            }
            fetch('http://localhost:8082/timer/start', {method:"GET"})
            .then(() => {const date = new Date(); this.start_timer.textContent = date.toLocaleDateString();})
            isTracking = !isTracking
            setInterval(() => {
            count++;
            this.timer.textContent = count.toString()}, 1000)
        })
        container?.append(this.start_timer)

        this.end_timer.addEventListener("click", () => {
            if(isTracking === false){
                alert('開始ボタンが押されていません')
                return
            }
            fetch('http://localhost:8082/timer/stop', {method:"POST"})
            .then(() => {const date = new Date(); this.end_timer.textContent = date.toLocaleDateString();})
            isTracking = !isTracking
        })
        container?.append(this.end_timer)
    }
}