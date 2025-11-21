// 导入axios库
import axios from "axios";

// 获取当前环境变量，假设为PRODUCT_ENV
const environment = process.env.NODE_ENV;

// 定义基础URL
let baseUrl = "";
let mediaUrl = "";

if (environment === "development") {
  // 动态获取当前访问的hostname，这样无论通过IP还是localhost访问都能正常工作
  const hostname = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
  baseUrl = `http://${hostname}:8000`;
  mediaUrl = `http://${hostname}:8000`;
} else if (environment === "production") {
  baseUrl = "/api/chatbot";
  mediaUrl = "/api/media";
} else {
  throw new Error("未知环境变量");
}

// 定义一个发送POST请求的函数
export async function postRequest(endpoint: string, headers: Record<string, string>, data: object): Promise<any> {
  const response = await axios.post(`${baseUrl}${endpoint}`, data, { headers });
  return response.data; // 返回解析后的数据
}

export async function postRequestArraybuffer(endpoint: string, headers: Record<string, string>, data: object): Promise<any> {
  const response = await axios.post(`${baseUrl}${endpoint}`, data, {
    responseType: 'arraybuffer',
    headers: headers,
  });
  return response.data; // 返回解析后的数据
}

// 定义一个发送Get请求的函数
export async function getRequest(endpoint: string, headers: Record<string, string>): Promise<any> {
  const response = await axios.get(`${baseUrl}${endpoint}`, { headers });
  return response.data; // 返回响应对象
}

export function buildMediaUrl(imageUrl: string) {
    return `${mediaUrl}${imageUrl}`
}