import './global.css';
import {Footer, GraphArea, Header, MainArea, Sidebar} from './components/components.ts';
import { Timer } from './components/timer.ts';
function App(){
    const root = document.querySelector<HTMLDivElement>('#app-container');
    const header = new Header('機能名');
    header.render();
    const sidebar = new Sidebar('機能名')
    sidebar.render()
    const graphArea = new GraphArea('グラフ表示エリア')
    graphArea.render()
    const footer = new Footer('フッター')
    footer.render()
    const timer = new Timer()
    const mainArea = new MainArea(timer.timer, timer.start_timer)
    mainArea.render()
    timer.render()
    if(!root) return;
}
App();
export default App;