export class MenuBar {
    list = document.createElement('li')
    constructor(){
        this.list.className = 'menu-list'
    }

    addItems(label: string, action: () => void){
        const li = document.createElement('li')
        const btn = document.createElement('button')
        li.textContent = label
        btn.addEventListener('click', action)
        li.appendChild(btn)
        this.list.appendChild(li)
        return this
    }

    build(){ return this.list }
}