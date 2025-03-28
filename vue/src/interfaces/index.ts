export interface foodI {
    id?: number
    name: string
    type?: string | undefined | null //配料类型
    intro?: string | undefined | null //配料简介
    effect?: string | undefined | null //配料作用
    harmType?: string | undefined | null //对人体有害或有益
    harmReason?: string | undefined | null // 有害或有益的原因
    risk?: string | undefined | null // 不适宜人群
    ruler?: Array<{ url: string, title: string }> // 法律法规
    error?: string
    createtime?: string | null,
    modiftime?: string | null,
}


export interface foodTagsI {
    id: number
    name: string
    editing: boolean
}


export interface registerI {
    username: string,
    password: string,
    password2: string,
    email: string,
}


export interface userI {
    age: string | null,
    gender: string | null,
    height: number | null,
    weight: number | null,
    allergy: string[],
    allergyOther: string | null,
    disease: string[],
    diseaseOther: string | null,
    goals: string | null,
    need: string[],
    needOther: string | null

    username: string,
    email?: string | null,
    createtime?: string | null,
    password?: string | null,

    muslim?: boolean | null
}


export interface logI {
    id: number,
    time?: string,
    type?: string,
    username?: string,
    ip?: string,
    input?: string,
    output?: string,
    state?: boolean
}

export enum ModelRoleEnum {
    USER = 'user',
    ASSISTANT = 'assistant',
    ERROR = 'error',
    MODEL_CHANGE = 'model-change'
}

export interface chatItemI {
    avatar?: string;
    name?: string;
    datetime?: string;
    content: string;
    role: ModelRoleEnum;
    isHide?: boolean;
}

export interface FetchCancelI {
    controller: {
        close: () => void;
    };
}

export interface SSEOptionsI {
    success?: (data: any) => void;
    fail?: () => void;
    complete?: (success: boolean, message?: string) => void;
}

