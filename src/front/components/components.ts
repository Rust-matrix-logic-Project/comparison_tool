import { MenuBar } from "./menu";

export class Header{
    header: HTMLHeadElement;
    functionName?: HTMLDivElement; 
    menubar?: HTMLElement;
    constructor(functionName: string){
        // header
        this.header = document.createElement('header');
        this.header.classList.add('header');

        // childElements
        if(this.header){
            // functionName
            this.functionName = document.createElement('div')
            this.functionName.classList.add('function-name')
            this.functionName.textContent = functionName;
            this.functionName.textContent = functionName;
            this.functionName.style.textAlign = 'center'

            // menubar
            this.menubar = document.createElement('ul');
            this.menubar.classList.add('menu')
            this.menubar.style.alignItems = 'left'
            this.menubar.textContent = 'test'
        }
    }
    render(){
        const container = document.querySelector('.app-container');
        const menu = new MenuBar()
        this.menubar?.appendChild(menu.build())
        if(this.menubar){
        this.header?.append(this.menubar);
        }
        if(this.functionName){
        this.header?.append(this.functionName);
        }
        container?.append(this.header)  
    }
    
};

export class Sidebar{
    functionName: HTMLElement; 

    constructor(functionName: string){
        this.functionName = document.createElement('aside');
        this.functionName.classList.add('sidebar')
        this.functionName.textContent = functionName;
        this.functionName.style.textAlign = 'center'
    }
    render(){
        const container = document.querySelector('.app-container');
        container?.append(this.functionName);
    }
    
};

export class GraphArea{
    graphData: HTMLElement; 

    constructor(graphData: string){
        this.graphData = document.createElement('aside');
        this.graphData.classList.add('graph-area')
        this.graphData.textContent = graphData;
        this.graphData.style.textAlign = 'center'
    }
    render(){
        const container = document.querySelector('.app-container');
        container?.append(this.graphData);
    }
    
};


export class Footer{
    fotter: HTMLElement; 

    constructor(fotter: string){
        this.fotter = document.createElement('footer');
        this.fotter.classList.add('footer')
        this.fotter.textContent = fotter;
        this.fotter.style.textAlign = 'center'
    }
    render(){
        const container = document.querySelector('.app-container');
        container?.append(this.fotter);
    }
    
};

export class MainArea{
    mainArea: HTMLElement
    functions: HTMLElement
    actions: HTMLButtonElement
    constructor(functions: HTMLElement, actions: HTMLButtonElement){
        this.mainArea = document.createElement('div');
        this.mainArea.classList.add('.main-area');
        this.functions = functions
        this.actions = actions
    }
    render(){
        const container = document.querySelector('.main-area');
        container?.append(this.mainArea);
        container?.append(this.functions);
        container?.append(this.actions);
    }
}

export class StatisticalArea{
    data: HTMLElement
    constructor(data: HTMLElement){
        this.data = data
    }
}