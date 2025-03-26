const images = [
    {
        "imageUrl": '1.bmp',
        "foodTags": ["饮用水", "牛奶", "白砂糖", "全脂乳粉", "乳清蛋白粉", "果葡糖浆", "浓缩苹果汁", "浓缩草莓汁",
            "羧甲基纤维素钠", "乳酸", "柠檬酸", "柠檬酸钠", "甜蜜素", "安赛蜜", "阿斯巴甜", "纽甜", "红曲红", "食用香精"]
    },
    {
        "imageUrl": '2.jpeg',
        "foodTags": ["大米", "白砂糖", "植物油", "米粉", "淀粉", "食用盐", "明胶", "呈味核苷酸二钠", "味精"]
    },
    {
        "imageUrl": '3.jpg',
        "foodTags": ["饮用水", "全脂乳粉", "白砂糖", "乳清蛋白粉", "果葡糖浆", "浓缩苹果汁", "羧甲基纤维素钠",
            "黄原胶", "乳酸", "柠檬酸", "柠檬酸钠", "单双甘油脂肪酸酯", "海藻酸丙二醇酯", "琥珀酸单甘油酯",
            "双乙酰酒石酸单双甘油酯", "三氯蔗糖", "安赛蜜", "纽甜", "食品用香精"]
    },
    {
        "imageUrl": '4.jpeg',
        "foodTags": ["小麦粉", "植物油", "生活饮用水", "丙三醇", "食用盐", "大豆膳食纤维粉", "白砂糖", "味精",
            "辣椒", "香辛料", "单硬脂酸甘油酯", "呈味核苷酸二钠", "辣椒红", "环已基氨基磺酸钠", "三氯蔗糖",
            "特丁基对苯二酚", "纽甜", "食用香精香料"]
    },
    {
        "imageUrl": '5.png',
        "foodTags": ["生牛乳", "白砂糖", "果葡糖浆", "嗜热链球菌", "保加利亚乳杆菌", "嗜酸乳杆菌", "乳双歧杆菌",
            "干酪乳杆菌", "聚葡萄糖", "低聚异麦芽糖", "乙酰化双淀粉已二酸酯", "羟丙基二淀粉磷酸酯", "明胶",
            "果胶", "琼脂"]
    }
]

export const requirePath = (imgPath: string) => {
    return new URL(`../assets/testImages/${imgPath}`, import.meta.url).href;
}

export function randomImage() {
    const randomIndex = Math.floor(Math.random() * images.length)
    return images[randomIndex]
}

export function getImage(index: number) {
    return images[index-1]
}

export function suppleFormat(foodTags: string[]) {
    return foodTags.map((tag, index) => ({
        id: index,
        name: tag,
        editing: false
    }));
}