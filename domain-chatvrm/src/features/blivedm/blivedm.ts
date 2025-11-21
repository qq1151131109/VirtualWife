// 获取当前环境变量，假设为PRODUCT_ENV
const environment = process.env.NODE_ENV;

// 定义基础URL
let baseUrl = "";
if (environment === "development") {
  baseUrl = ":8000";
} else if (environment === "production") {
  baseUrl = "/api/chatbot";
} else {
  throw new Error("未知环境变量");
}


export async function connect(): Promise<WebSocket> {
    const hostname = window.location.hostname;
    const socket = new WebSocket(`ws://${hostname}${baseUrl}/ws/`);
    socket.onopen = () => {
        console.log('WebSocket connection established.');
        socket.send('connection success');
    };
    // 移除自动重连逻辑，由外部管理
    socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
    };
    return socket;
}
