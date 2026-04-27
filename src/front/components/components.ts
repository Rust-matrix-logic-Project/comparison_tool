import { MenuBar } from './menu';

export class Header {
    header: HTMLHeadElement;
    functionName: HTMLDivElement;
    menubar: HTMLElement;
    private themeToggle: HTMLButtonElement;
    private isDark: boolean = true;

    constructor(functionName: string) {
        this.header = document.createElement('header');
        this.header.classList.add('header');

        this.menubar = document.createElement('ul');
        this.menubar.classList.add('menu');

        this.functionName = document.createElement('div');
        this.functionName.classList.add('function-name');
        this.functionName.textContent = functionName;

        this.themeToggle = document.createElement('button');
        this.themeToggle.classList.add('theme-toggle');
        this.themeToggle.textContent = '☀';
        this.themeToggle.title = 'テーマ切替';
        this.themeToggle.addEventListener('click', () => this._toggleTheme());
    }

    setFunctionName(name: string) {
        this.functionName.textContent = name;
    }

    render(footer?: Footer) {
        const container = document.querySelector('.app-container');

        const menu = new MenuBar();
        menu.addItems('File', [
            { label: 'ファイルを開く', action: () => footer?.log('ファイルを開く（未実装）') },
            { label: '保存', action: () => footer?.log('保存（未実装）') },
        ]);
        menu.addItems('View', [
            { label: 'ダークテーマ', action: () => this._setTheme('dark') },
            { label: 'ライトテーマ', action: () => this._setTheme('light') },
            {
                label: 'フッターを表示',
                action: () => {
                    document.querySelector('.footer')?.classList.remove('hidden');
                    document.querySelector('.app-container')?.classList.remove('footer-hidden');
                }
            },
            {
                label: 'グラフを表示',
                action: () => {
                    document.querySelector('.graph-area')?.classList.remove('hidden');
                    document.querySelector('.app-container')?.classList.remove('graph-hidden');
                }
            },
        ]);

        this.menubar.appendChild(menu.build());
        this.header.append(this.menubar, this.functionName, this.themeToggle);
        container?.append(this.header);
    }

    private _toggleTheme() {
        this.isDark = !this.isDark;
        this._setTheme(this.isDark ? 'dark' : 'light');
    }

    private _setTheme(theme: 'dark' | 'light') {
        this.isDark = theme === 'dark';
        document.documentElement.setAttribute('data-theme', theme);
        this.themeToggle.textContent = this.isDark ? '☀' : '🌙';
    }
}


export class Sidebar {
    sidebar: HTMLElement;
    private buttons: { label: string; icon: string; action: () => void }[] = [];

    constructor() {
        this.sidebar = document.createElement('aside');
        this.sidebar.classList.add('sidebar');
    }

    addFunction(label: string, icon: string, action: () => void) {
        this.buttons.push({ label, icon, action });
        return this;
    }

    render() {
        const container = document.querySelector('.app-container');
        this.buttons.forEach(({ label, icon, action }, index) => {
            const btn = document.createElement('button');
            btn.classList.add('sidebar-btn');
            btn.title = label;
            btn.textContent = icon;
            if (index === 0) btn.classList.add('active');
            btn.addEventListener('click', () => {
                document.querySelectorAll('.sidebar-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                action();
            });
            this.sidebar.append(btn);
        });
        container?.append(this.sidebar);
    }
}


export class GraphArea {
    graphArea: HTMLElement;

    constructor() {
        this.graphArea = document.createElement('aside');
        this.graphArea.classList.add('graph-area');

        const header = document.createElement('div');
        header.classList.add('panel-header');
        const title = document.createElement('span');
        title.textContent = 'グラフ';
        const closeBtn = document.createElement('button');
        closeBtn.classList.add('close-btn');
        closeBtn.textContent = '×';
        closeBtn.title = '閉じる';
        closeBtn.addEventListener('click', () => {
            this.graphArea.classList.add('hidden');
            document.querySelector('.app-container')?.classList.add('graph-hidden');
        });
        header.append(title, closeBtn);

        const content = document.createElement('div');
        content.classList.add('graph-content');
        content.textContent = 'NN実装後に有効化';

        this.graphArea.append(header, content);
    }

    render() {
        const container = document.querySelector('.app-container');
        container?.append(this.graphArea);
    }
}


export class Footer {
    footer: HTMLElement;
    logArea: HTMLElement;

    constructor() {
        this.footer = document.createElement('footer');
        this.footer.classList.add('footer');

        const header = document.createElement('div');
        header.classList.add('panel-header');
        const title = document.createElement('span');
        title.textContent = 'ログ';
        const closeBtn = document.createElement('button');
        closeBtn.classList.add('close-btn');
        closeBtn.textContent = '×';
        closeBtn.title = '閉じる';
        closeBtn.addEventListener('click', () => {
            this.footer.classList.add('hidden');
            document.querySelector('.app-container')?.classList.add('footer-hidden');
        });
        header.append(title, closeBtn);

        this.logArea = document.createElement('div');
        this.logArea.classList.add('log-area');

        this.footer.append(header, this.logArea);
    }

    log(message: string) {
        const entry = document.createElement('span');
        entry.classList.add('log-entry');
        const time = new Date().toLocaleTimeString('ja-JP', { hour12: false });
        entry.textContent = `[${time}] ${message}`;
        this.logArea.append(entry);
        this.logArea.scrollTop = this.logArea.scrollHeight;
    }

    error(message: string) {
        const entry = document.createElement('span');
        entry.classList.add('log-entry', 'log-error-entry');
        const time = new Date().toLocaleTimeString('ja-JP', { hour12: false });
        entry.textContent = `[${time}] ERROR: ${message}`;
        this.logArea.append(entry);
        this.logArea.scrollTop = this.logArea.scrollHeight;
    }

    render() {
        const container = document.querySelector('.app-container');
        container?.append(this.footer);
    }
}


export class MainArea {
    private mainArea: HTMLElement;

    constructor() {
        this.mainArea = document.querySelector('.main-area') as HTMLElement;
    }

    setContent(content: HTMLElement) {
        this.mainArea.innerHTML = '';
        this.mainArea.append(content);
    }
}
