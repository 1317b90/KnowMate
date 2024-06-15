const images=[
    {
        "imageUrl":'1.bmp',
        "foodTags":[
            { "id": 1, "name": "全脂乳粉", "editing": false},
            { "id": 2, "name": "牛奶", "editing": false},
            { "id": 3, "name": "白砂糖", "editing": false},
            { "id": 4, "name": "饮用水", "editing": false},
            { "id": 5, "name": "乳清蛋白粉", "editing": false},
            { "id": 6, "name": "果葡糖浆", "editing": false},
            { "id": 7, "name": "浓缩苹果汁", "editing": false},
            { "id": 8, "name": "浓缩草莓汁", "editing": false},
            { "id": 9, "name": "羧甲基纤维素钠", "editing": false},
            { "id": 10, "name": "乳酸", "editing": false},
            { "id": 11, "name": "柠檬酸", "editing": false},
            { "id": 12, "name": "柠檬酸钠", "editing": false},
            { "id": 13, "name": "甜蜜素", "editing": false},
            { "id": 14, "name": "安赛蜜", "editing": false},
            { "id": 15, "name": "阿斯巴甜", "editing": false},
            { "id": 16, "name": "纽甜", "editing": false},
            { "id": 17, "name": "红曲红", "editing": false},
            { "id": 18, "name": "食用香精", "editing": false}
        ]
    },
    {
        "imageUrl":'3.jpg',
        "foodTags":[
            { "id": 1, "name": "全脂乳粉", "editing": false},
            { "id": 2, "name": "饮用水", "editing": false},
            { "id": 3, "name": "白砂糖", "editing": false},
            { "id": 4, "name": "乳清蛋白粉", "editing": false},
            { "id": 5, "name": "果葡糖浆", "editing": false},
            { "id": 6, "name": "浓缩苹果汁", "editing": false},
            { "id": 7, "name": "羧甲基纤维素钠", "editing": false},
            { "id": 8, "name": "黄原胶", "editing": false},
            { "id": 9, "name": "乳酸", "editing": false},
            { "id": 10, "name": "柠檬酸", "editing": false},
            { "id": 11, "name": "柠檬酸钠", "editing": false},
            { "id": 12, "name": "单双甘油脂肪酸酯", "editing": false},
            { "id": 13, "name": "海藻酸丙二醇酯", "editing": false},
            { "id": 14, "name": "琥珀酸单甘油酯", "editing": false},
            { "id": 15, "name": "双乙酰酒石酸单双甘油酯", "editing": false},
            { "id": 16, "name": "三氯蔗糖", "editing": false},
            { "id": 17, "name": "安赛蜜", "editing": false},
            { "id": 18, "name": "纽甜", "editing": false},
            { "id": 19, "name": "食品用香精", "editing": false},
        ]
    },
    {
        "imageUrl":'4.jpeg',
        "foodTags":[
            { "id": 1, "name": "小麦粉", "editing": false},
            { "id": 2, "name": "植物油", "editing": false},
            { "id": 3, "name": "生活饮用水", "editing": false},
            { "id": 4, "name": "丙三醇", "editing": false},
            { "id": 5, "name": "食用盐", "editing": false},
            { "id": 6, "name": "大豆膳食纤维粉", "editing": false},
            { "id": 7, "name": "白砂糖", "editing": false},
            { "id": 8, "name": "味精", "editing": false},
            { "id": 9, "name": "辣椒", "editing": false},
            { "id": 10, "name": "香辛料", "editing": false},
            { "id": 11, "name": "单硬脂酸甘油酯", "editing": false},
            { "id": 12, "name": "呈味核苷酸二钠", "editing": false},
            { "id": 13, "name": "辣椒红", "editing": false},
            { "id": 14, "name": "环已基氨基磺酸钠", "editing": false},
            { "id": 15, "name": "三氯蔗糖", "editing": false},
            { "id": 16, "name": "特丁基对苯二酚", "editing": false},
            { "id": 17, "name": "纽甜", "editing": false},
            { "id": 18, "name": "食用香精香料", "editing": false},
        ]
    },
    {
        "imageUrl":'5.png',
        "foodTags":[
            { "id": 1, "name": "生牛乳", "editing": false},
            { "id": 2, "name": "白砂糖", "editing": false},
            { "id": 3, "name": "果葡糖浆", "editing": false},
            { "id": 4, "name": "嗜热链球菌", "editing": false},
            { "id": 5, "name": "保加利亚乳杆菌", "editing": false},
            { "id": 6, "name": "嗜酸乳杆菌", "editing": false},
            { "id": 7, "name": "乳双歧杆菌", "editing": false},
            { "id": 8, "name": "干酪乳杆菌", "editing": false},
            { "id": 9, "name": "聚葡萄糖", "editing": false},
            { "id": 10, "name": "低聚异麦芽糖", "editing": false},
            { "id": 11, "name": "乙酰化双淀粉已二酸酯", "editing": false},
            { "id": 12, "name": "羟丙基二淀粉磷酸酯", "editing": false},
            { "id": 13, "name": "明胶", "editing": false},
            { "id": 14, "name": "果胶", "editing": false},
            { "id": 15, "name": "琼脂", "editing": false},
        ]
    }
]

export const requirePath = (imgPath: string) => {
    return new URL(`../assets/testImages/${imgPath}`, import.meta.url).href;
}

export function randomImage(){
    const randomIndex = Math.floor(Math.random() * images.length)
    return images[randomIndex]
}