import './global.css';
import { Footer, GraphArea, Header, MainArea, Sidebar } from './components/components.ts';
import { Timer } from './components/timer.ts';
import { Goals } from './components/goals.ts';

function App() {
    // Render order matches grid placement: header → sidebar → graph → footer → main-area content
    const footer = new Footer();
    const header = new Header('Timer');
    header.render(footer);

    const sidebar = new Sidebar();
    const graphArea = new GraphArea();
    graphArea.render();
    footer.render();

    const mainArea = new MainArea();
    const timer = new Timer(footer);
    const goals = new Goals(footer);

    sidebar
        .addFunction('タイマー', '⏱', () => {
            mainArea.setContent(timer.container);
            header.setFunctionName('Timer');
            footer.log('Timerビューに切り替えました');
        })
        .addFunction('目標管理', '🎯', () => {
            mainArea.setContent(goals.container);
            header.setFunctionName('Goals');
            footer.log('Goalsビューに切り替えました');
        });

    sidebar.render();

    // Default view: Timer
    mainArea.setContent(timer.container);
    footer.log('アプリケーションを起動しました');
}

App();
export default App;
