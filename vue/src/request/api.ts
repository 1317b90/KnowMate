import service from "@/request/index";
import type { foodI, registerI, userI } from '@/interfaces'

// --------配料解析--------配料解析--------配料解析--------配料解析--------配料解析--------配料解析

// ocr识别图片
export async function ocr(image: FormData) {
    return service.post('ocrImage', image, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

// 解析配料
export async function parsing(foodName: String, username: string) {
    return service({
        url: "parsing?foodName=" + foodName + "&username=" + username,
        method: "GET"
    })
}

// 食品评价与饮食建议
export async function feadr(foodListText: String, username: string) {
    return service({
        url: "feadr?foodListText=" + foodListText + "&username=" + username,
        method: "GET",
    })
}
// ---------登陆注册---------登陆注册---------登陆注册---------登陆注册---------登陆注册

// 登陆
export async function login(username: String, password: string) {
    return service({
        url: "login",
        method: "post",
        data: {
            'username': username,
            'password': password
        }
    })
}

// 注册
export async function register(data: registerI) {
    return service({
        url: "register",
        method: "post",
        data: {
            'username': data.username,
            'password': data.password,
            'email': data.email
        }
    })
}


// ---------配料数据操作---------配料数据操作---------配料数据操作---------配料数据操作---------配料数据操作

// 查询配料总页数
export function getFoodTotal() {
    return service({
        url: "foodTotal?",
        method: "GET"
    })
}

// 查询单个配料
export async function getFood(name:String) {
    return service({
        url: "food?name=" + name,
        method: "GET"
    })
}

// 分页查询配料数据
export async function getFoodPage(page: number, pageSize: number) {
    return service({
        url: "foodPage?skip=" + (page * pageSize).toString() + "&limit=" + pageSize.toString(),
        method: "GET"
    })
}

// 增加配料数据
export function addFood(data:foodI) {
    return service({
        url: "addFood",
        method: "POST",
        data:data
    })
}

// 修改配料数据
export function setFood(data:foodI) {
    return service({
        url: "setFood",
        method: "POST",
        data:data
    })
}

// 删除配料数据
export function delFood(name:String) {
    return service({
        url: "delFood?name=" + name,
        method: "GET"
    })
}

// ---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作

// 获取单个用户数据
export async function getUser(username: String) {
    return service({
        url: "user?username=" + username,
        method: "GET"
    })
}

// 查询用户总页数
export function getUserTotal() {
    return service({
        url: "userTotal?",
        method: "GET"
    })
}

// 分页查询配料数据
export async function getUserPage(page: number, pageSize: number) {
    return service({
        url: "userPage?skip=" + (page * pageSize).toString() + "&limit=" + pageSize.toString(),
        method: "GET"
    })
}

// 修改用户数据
export async function setUser(data: userI) {
    return service({
        url: "user",
        method: "post",
        data: data
    })
}

// 删除用户数据
export function delUser(username:String) {
    return service({
        url: "delUser?username=" + username,
        method: "GET"
    })
}


// 增加用户数据
export function addUser(data:userI) {
    return service({
        url: "addUser",
        method: "POST",
        data:data
    })
}