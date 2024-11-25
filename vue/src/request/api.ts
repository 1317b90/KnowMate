import service from "@/request/index";
import type { foodI, userI } from '@/interfaces'

// --------配料解析--------配料解析--------配料解析--------配料解析--------配料解析--------配料解析

// ocr识别图片
export async function ocr(image: FormData) {
    return service.post('ocrImg', image, {
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


// ---------配料数据操作---------配料数据操作---------配料数据操作---------配料数据操作---------配料数据操作

// 查询配料总页数
export function getFoodTotal() {
    return service({
        url: "food/total?",
        method: "GET"
    })
}

// 查询单个配料
export async function getFood(name: String) {
    return service({
        url: "food?name=" + name,
        method: "GET"
    })
}

// 分页查询配料数据
export async function getFoodPage(page: number, pageSize: number) {
    return service({
        url: "food/page?skip=" + (page * pageSize).toString() + "&limit=" + pageSize.toString(),
        method: "GET"
    })
}

// 增加配料数据
export function addFood(data: foodI) {
    return service({
        url: "food",
        method: "POST",
        data: data
    })
}

// 修改配料数据
export function setFood(data: foodI) {
    return service({
        url: "food",
        method: "PUT",
        data: data
    })
}

// 删除配料数据
export function delFood(name: String) {
    return service({
        url: "food?name=" + name,
        method: "DEL"
    })
}

// ---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作---------用户表操作

// 登陆
export async function login(username: String, password: string) {
    return service({
        url: "user/login",
        method: "post",
        data: {
            'username': username,
            'password': password
        }
    })
}


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
        url: "user/total?",
        method: "GET"
    })
}

// 分页查询配料数据
export async function getUserPage(page: number, pageSize: number) {
    return service({
        url: "user/page?skip=" + (page * pageSize).toString() + "&limit=" + pageSize.toString(),
        method: "GET"
    })
}

// 修改用户数据
export async function setUser(data: userI) {
    return service({
        url: "user",
        method: "PUT",
        data: data
    })
}

// 删除用户数据
export function delUser(username: String) {
    return service({
        url: "user?username=" + username,
        method: "DEL"
    })
}

// 增加用户数据
export function addUser(data: userI) {
    return service({
        url: "user",
        method: "POST",
        data: data
    })
}

// ---------记录表操作---------记录表操作---------记录表操作---------记录表操作---------记录表操作

// 查询记录总页数
export function getLogTotal() {
    return service({
        url: "log/otal?",
        method: "GET"
    })
}

// 分页查询记录数据
export async function getLogPage(page: number, pageSize: number) {
    return service({
        url: "log/page?skip=" + (page * pageSize).toString() + "&limit=" + pageSize.toString(),
        method: "GET"
    })
}
