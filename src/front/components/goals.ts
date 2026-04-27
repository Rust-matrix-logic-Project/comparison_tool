import type { Footer } from './components';

interface GoalData {
    key?: string;
    goal: string;
    status: 'todo' | 'doing' | 'done';
    limit?: string;
}

export class Goals {
    container: HTMLElement;
    private listEl: HTMLElement;
    private inputs: HTMLInputElement[] = [];
    private statusSelect: HTMLSelectElement;
    private selectedKey: string | null = null;
    private footer: Footer | null = null;

    constructor(footer?: Footer) {
        this.footer = footer ?? null;

        this.container = document.createElement('div');
        this.container.classList.add('goals-container');

        // Section 1: Task list
        const listSection = document.createElement('div');
        listSection.classList.add('goals-list-section');

        const listTitle = document.createElement('div');
        listTitle.classList.add('section-title');
        listTitle.textContent = '進行中タスク';

        this.listEl = document.createElement('div');
        this.listEl.classList.add('goals-list');

        listSection.append(listTitle, this.listEl);

        // Section 2: Form
        const formSection = document.createElement('div');
        formSection.classList.add('goals-form');

        const formTitle = document.createElement('div');
        formTitle.classList.add('section-title');
        formTitle.textContent = '目標登録';
        formSection.append(formTitle);

        const goalLabels = ['第一目標', '第二目標', '第三目標', '第四目標'];
        goalLabels.forEach((label) => {
            const row = document.createElement('div');
            row.classList.add('form-row');
            const lbl = document.createElement('label');
            lbl.textContent = label;
            const input = document.createElement('input');
            input.type = 'text';
            input.classList.add('goal-input');
            input.placeholder = `${label}を入力`;
            this.inputs.push(input);
            row.append(lbl, input);
            formSection.append(row);
        });

        // Status + limit row
        this.statusSelect = document.createElement('select');
        this.statusSelect.classList.add('goal-select');
        (['todo', 'doing', 'done'] as const).forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = s;
            this.statusSelect.append(opt);
        });

        const statusRow = document.createElement('div');
        statusRow.classList.add('form-row');
        const statusLabel = document.createElement('label');
        statusLabel.textContent = 'ステータス';
        statusRow.append(statusLabel, this.statusSelect);
        formSection.append(statusRow);

        // Buttons
        const btnRow = document.createElement('div');
        btnRow.classList.add('form-buttons');

        const registerBtn = document.createElement('button');
        registerBtn.classList.add('btn-primary');
        registerBtn.textContent = '登録';
        registerBtn.addEventListener('click', () => this._register());

        const updateBtn = document.createElement('button');
        updateBtn.classList.add('btn-secondary');
        updateBtn.textContent = 'ステータス更新';
        updateBtn.addEventListener('click', () => this._update());

        btnRow.append(registerBtn, updateBtn);
        formSection.append(btnRow);

        this.container.append(listSection, formSection);

        this._loadGoals();
    }

    private _register() {
        const goals = this.inputs.map(i => i.value.trim()).filter(v => v);
        if (goals.length === 0) {
            alert('目標を1つ以上入力してください');
            return;
        }
        const month = new Date().toISOString().slice(0, 7);

        fetch('http://localhost:8082/goals/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ goal: goals, month }),
        })
            .then(() => {
                this.footer?.log(`目標を登録しました: ${goals.join(', ')}`);
                this._loadGoals();
                this.inputs.forEach(i => (i.value = ''));
            })
            .catch(() => {
                this.footer?.log('目標を登録しました（オフライン・ローカル表示）');
                goals.forEach(g => this._addGoalItem({ goal: g, status: this.statusSelect.value as GoalData['status'] }));
                this.inputs.forEach(i => (i.value = ''));
            });
    }

    private _update() {
        if (!this.selectedKey) {
            alert('リストからタスクを選択してください');
            return;
        }
        const month = new Date().toISOString().slice(0, 7);
        const status = this.statusSelect.value;

        fetch('http://localhost:8082/goals/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: this.selectedKey, status, month }),
        })
            .then(() => {
                this.footer?.log(`ステータス更新: ${this.selectedKey} → ${status}`);
                this._loadGoals();
            })
            .catch(() => {
                this.footer?.error('バックエンドに接続できません');
            });
    }

    private _loadGoals() {
        const month = new Date().toISOString().slice(0, 7);
        fetch(`http://localhost:8082/goals/data?month=${month}`)
            .then(r => r.json())
            .then((data: GoalData[]) => {
                this.listEl.innerHTML = '';
                data.forEach(g => this._addGoalItem(g));
            })
            .catch(() => {
                if (this.listEl.childElementCount === 0) {
                    this._loadDemoData();
                }
            });
    }

    private _loadDemoData() {
        const demo: GoalData[] = [
            { key: '1', goal: 'タイマー機能実装', status: 'done' },
            { key: '2', goal: 'Goals画面実装', status: 'doing' },
            { key: '3', goal: 'NN機能実装', status: 'todo' },
        ];
        demo.forEach(g => this._addGoalItem(g));
    }

    private _addGoalItem(data: GoalData) {
        const item = document.createElement('div');
        item.classList.add('goal-item');
        if (data.key) item.dataset.key = data.key;

        const tag = document.createElement('span');
        tag.classList.add('goal-status', `status-${data.status}`);
        tag.textContent = data.status;

        const text = document.createElement('span');
        text.textContent = data.goal;

        item.append(tag, text);

        item.addEventListener('click', () => {
            document.querySelectorAll('.goal-item').forEach(el => el.classList.remove('selected'));
            item.classList.add('selected');
            this.selectedKey = data.key ?? null;
            this.statusSelect.value = data.status;
        });

        this.listEl.append(item);
    }

    render() {
        const container = document.querySelector('.main-area');
        container?.append(this.container);
    }
}
