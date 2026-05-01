import { StatisticalArea } from "./components";
export class Timer{
    timer: HTMLElement;
    operation_area: HTMLElement;
    start_timer: HTMLButtonElement;
    end_timer: HTMLButtonElement;
    timer_click: number;
    low_area:HTMLElement;
    log_area: HTMLElement;
    button_log: HTMLElement;
    csv_area: HTMLElement;
    left_area: HTMLElement;
    right_area: HTMLElement;
    
    constructor(){
        this.left_area = document.createElement('div')
        this.left_area.classList.add('left-area')
        this.right_area = document.createElement('div')
        this.right_area.classList.add('right-area')

        this.timer = document.createElement('div');
        this.timer.classList.add('timer');
        this.timer.id = 'timer'
        this.timer.textContent = '00:00:00'
        this.timer.style.textAlign = 'center'

        this.low_area = document.createElement('div')
        this.low_area.classList.add('low-area')

        this.log_area = document.createElement('div')
        this.log_area.classList.add('log-area')
        this.log_area.style.flexDirection = 'column'
        
        this.operation_area = document.createElement('div')
        this.operation_area.classList.add('operation_area')
        this.operation_area.id = 'operation_area'

        this.start_timer = document.createElement('button');
        this.start_timer.classList.add('start');
        this.start_timer.id = 'start'
        this.start_timer.textContent = 'start'
        this.start_timer.style.whiteSpace = 'nowrap'

        this.end_timer = document.createElement('button');
        this.end_timer.classList.add('end');
        this.end_timer.id = 'end'
        this.end_timer.textContent = 'stop'
        this.end_timer.style.whiteSpace = 'nowrap'

        this.button_log = document.createElement('div')
        this.button_log.classList.add('button-log')
        this.button_log.style.whiteSpace = "pre-wrap"
        this.button_log.id = 'button-log'

        this.csv_area = document.createElement('div')
        this.csv_area.classList.add('csv-area')

        this.timer_click = 0
    }
    private _button_log(button: String){
        const date = new Date().toLocaleString("en-US", {dateStyle:'full', timeStyle: 'short', hour12: false})
        if(this.button_log){
            this.button_log.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            })
        }
        this.button_log.append(`${date} ${button}`+ "\n")
    }
    render(){
        const container = document.querySelector('.main-area');
        let count = 0;
        const damyElement = document.createElement('div')
        damyElement.textContent = '統計エリア'
        this.csv_area.textContent = 'CSVエリア'
        const Statistical = new StatisticalArea(damyElement);
        let isTracking: boolean = false;

        this.start_timer.addEventListener("click", () => {
            if(isTracking === true){
                alert('既に開始しています')
                return
            }
            clearInterval(this.timer_click)
            count = 0

            fetch('http://localhost:8082/timer/start', {method:"GET"})
            isTracking = !isTracking
            this.timer_click = setInterval(() => {
            count++;
            const h = Math.floor(count / 3600)
            const m = Math.floor((count % 3600) / 60)
            const s = count % 60
            this.timer.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0')}, 1000)

            this._button_log('start')

        })
        this.operation_area?.append(this.start_timer)

        this.end_timer.addEventListener("click", () => {
            if(isTracking === false){
                alert('開始ボタンが押されていません')
                return
            }
            fetch('http://localhost:8082/timer/stop', {method:"POST"})
            isTracking = !isTracking
            clearInterval(this.timer_click)
            this._button_log(`stop`)
        })

        this.log_area.append(this.button_log)

        this.operation_area.append(this.start_timer)
        this.operation_area.append(this.end_timer)
        this.log_area.append(Statistical.data)
        this.left_area.append(this.operation_area, this.log_area)
        this.low_area.append(this.left_area)
        this.right_area.append(this.csv_area)
        this.low_area.append(this.right_area)
        container?.append(this.low_area)
    }
}