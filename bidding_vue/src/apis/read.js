import service from "../utils/request";


export function GetAll(){
    return service.request({
        url:"/",
        method:"get"
    });
}

export function GetInfoPost(postparams){
    return service.request({
        method:"post",
        url:postparams.url,
        data:{
            key:postparams.key,
            secretKey: 0
        }
    })
}