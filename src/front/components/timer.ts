import type { Footer } from './components';

export class Timer {
    container: HTMLElement;
    timer: HTMLElement;
    start_timer: HTMLButtonElement;
    end_timer: HTMLButtonElement;
    private startTimeEl: HTMLElement;
    private csvTable: HTMLElement;
    private intervalId: number | null = null;
    private isTracking: boolean = false;
    private count: number = 0;
    private footer: Footer | null = null;

    constructor(footer?: Footer) {
        this.footer = footer ?? null;

        this.container = document.createElement('div');
        this.container.classList.add('timer-container');

        // Section 1: Start time display
        this.startTimeEl = document.createElement('div');
        this.startTimeEl.classList.add('timer-start-time');
        this.startTimeEl.textContent = '開始時間: --:--:--';

        // Section 2: Timer display + buttons
        const displaySection = document.createElement('div');
        displaySection.classList.add('timer-display-section');

        this.timer = document.createElement('div');
        this.timer.classList.add('timer-count');
        this.timer.textContent = '00:00:00';

        const btnRow = document.createElement('div');
        btnRow.classList.add('timer-buttons');

        this.start_timer = document.createElement('button');
        this.start_timer.classList.add('btn-primary');
        this.start_timer.textContent = '開始';

        this.end_timer = document.createElement('button');
        this.end_timer.classList.add('btn-secondary');
        this.end_timer.textContent = '終了';

        btnRow.append(this.start_timer, this.end_timer);
        displaySection.append(this.timer, btnRow);

        // Section 3: CSV / 当日の記録
        const csvSection = document.createElement('div');
        csvSection.classList.add('timer-csv-section');

        const csvTitle = document.createElement('div');
        csvTitle.classList.add('section-title');
        csvTitle.textContent = '本日の記録';

        this.csvTable = document.createElement('div');
        this.csvTable.classList.add('csv-table');

        csvSection.append(csvTitle, this.csvTable);
        this.container.append(this.startTimeEl, displaySection, csvSection);

        this._setupEvents();
    }

    private _setupEvents() {
        this.start_timer.addEventListener('click', () => {
            if (this.isTracking) {
                alert('既に開始しています');
                return;
            }
            const startTime = new Date();
            this.startTimeEl.textContent = `開始時間: ${startTime.toLocaleTimeString('ja-JP', { hour12: false })}`;
            this.start_timer.textContent = startTime.toLocaleDateString('ja-JP');
            this.isTracking = true;
            this.count = 0;

            fetch('http://localhost:8082/timer/start', { method: 'GET' })
                .then(() => this.footer?.log('タイマー開始'))
                .catch(() => this.footer?.log('タイマー開始（オフライン）'));

            this.intervalId = window.setInterval(() => {
                this.count++;
                this.timer.textContent = this._formatTime(this.count);
            }, 1000);
        });

        this.end_timer.addEventListener('click', () => {
            if (!this.isTracking) {
                alert('開始ボタンが押されていません');
                return;
            }
            if (this.intervalId !== null) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
            const endTime = new Date();
            this.end_timer.textContent = endTime.toLocaleDateString('ja-JP');
            this.isTracking = false;

            this._addCsvRow(this.startTimeEl.textContent?.replace('開始時間: ', '') ?? '', this._formatTime(this.count));

            fetch('http://localhost:8082/timer/stop', { method: 'POST' })
                .then(() => this.footer?.log(`タイマー停止 — 経過: ${this._formatTime(this.count)}`))
                .catch(() => this.footer?.log(`タイマー停止（オフライン）— 経過: ${this._formatTime(this.count)}`));
        });
    }

    private _formatTime(seconds: number): string {
        const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
        const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
        const s = (seconds % 60).toString().padStart(2, '0');
        return `${h}:${m}:${s}`;
    }

    private _addCsvRow(start: string, elapsed: string) {
        const row = document.createElement('div');
        row.classList.add('csv-row');
        row.innerHTML = `<span>${new Date().toLocaleDateString('ja-JP')}</span><span>${start}</span><span>${elapsed}</span>`;
        this.csvTable.append(row);
    }

    render() {
        const container = document.querySelector('.main-area');
        container?.append(this.container);
    }
}
