interface MenuItem {
    label: string;
    action: () => void;
}

export class MenuBar {
    private menuEl: HTMLElement;
    private activeDropdown: HTMLElement | null = null;

    constructor() {
        this.menuEl = document.createElement('ul');
        this.menuEl.classList.add('menu-list');

        document.addEventListener('click', (e) => {
            if (!this.menuEl.contains(e.target as Node)) {
                this._closeAll();
            }
        });
    }

    addItems(label: string, items: MenuItem[]) {
        const li = document.createElement('li');
        li.classList.add('menu-item');

        const btn = document.createElement('button');
        btn.classList.add('menu-btn');
        btn.textContent = label;

        const dropdown = document.createElement('ul');
        dropdown.classList.add('menu-dropdown');

        items.forEach(item => {
            const itemLi = document.createElement('li');
            const itemBtn = document.createElement('button');
            itemBtn.classList.add('menu-dropdown-item');
            itemBtn.textContent = item.label;
            itemBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                item.action();
                this._closeAll();
            });
            itemLi.append(itemBtn);
            dropdown.append(itemLi);
        });

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (this.activeDropdown === dropdown) {
                this._closeAll();
            } else {
                this._closeAll();
                dropdown.classList.add('open');
                this.activeDropdown = dropdown;
            }
        });

        li.append(btn, dropdown);
        this.menuEl.append(li);
        return this;
    }

    private _closeAll() {
        this.menuEl.querySelectorAll('.menu-dropdown').forEach(d => d.classList.remove('open'));
        this.activeDropdown = null;
    }

    build() {
        return this.menuEl;
    }
}
