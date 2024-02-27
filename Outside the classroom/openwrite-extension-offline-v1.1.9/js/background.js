function isEmpty(obj) {
    return typeof obj == 'undefined' || obj == null || obj === '';
}

let JSON_HEADER = {'content-type': 'application/json'};

let X_FORM_HEADER = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'};

/**
 * listen web page message
 */
chrome.runtime.onMessageExternal.addListener(
    function (request, sender, sendResponse) {
        let sendResponsePlus = {
            error: (message) => {
                sendResponse({ok: false, message: message})
            },
            success: (data) => {
                sendResponse({ok: true, data: data});
            },
            send: (data) => {
                sendResponse(data);
            }
        };
        try {
            eval(request.js);
            let func = request.func.split('.');
            let main = MAIN;
            while (func.length > 1) {
                main = main[func.shift()];
            }
            main[func.shift()](sendResponsePlus, request.args);
        } catch (e) {
            sendResponsePlus.error('Unknown Error');
        }
    });


chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        if (/article\/(.*?)\/delete/.exec(details.url)) {
            let id = /article\/(.*?)\/delete/.exec(details.url)[1];
            details.requestHeaders.push({name: 'Referer', value: `https://aijishu.com/a/${id}`});
        } else {
            details.requestHeaders.push({name: 'Referer', value: 'https://aijishu.com/write'});
        }
        details.requestHeaders.push({name: 'Origin', value: 'https://aijishu.com'});
        return {requestHeaders: details.requestHeaders};
    },
    {urls: ["https://aijishu.com/api/*"]},
    ["blocking", "requestHeaders", "extraHeaders"]
);

chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        if (details.initiator.indexOf('chrome-extension://') !== -1) {
            if (/article\/(.*?)\/delete/.exec(details.url)) {
                let id = /article\/(.*?)\/delete/.exec(details.url)[1];
                details.requestHeaders.push({ name: 'Referer', value: `https://segmentfault.com/a/${id}` });
            } else if (details.url.indexOf('articles/add') != -1) {
                details.requestHeaders.push({ name: 'Referer', value: 'https://segmentfault.com/write?freshman=1' });
            }
        }
        return { requestHeaders: details.requestHeaders };
    },
    { urls: ["https://segmentfault.com/api/*"] },
    ["blocking", "requestHeaders", "extraHeaders"]
);

// 掘金请求头设置
chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        if (details.initiator.indexOf('chrome-extension://') !== -1) {
            details.requestHeaders.push({
                name: 'Referer', value: 'https://juejin.cn/editor/drafts/6857487746525888520'
            })
            details.requestHeaders.push({
                name: 'Origin', value: 'https://juejin.cn'
            })
            return { requestHeaders: details.requestHeaders }
        }
    },
    { urls: ['https://api.juejin.cn/*'] },
    ["blocking", "requestHeaders", "extraHeaders"]
);

// 头条请求头设置
chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        details.requestHeaders.push({
            name: 'Referer', value: 'http://mp.toutiao.com/profile_v4/graphic/publish'
        })
        details.requestHeaders.push({
            name: 'Origin', value: 'http://mp.toutiao.com'
        })
        return { requestHeaders: details.requestHeaders }
    },
    { urls: ["http://mp.toutiao.com/mp/*"] },
    ["blocking", "requestHeaders", "extraHeaders"]
)

// 微博请求头设置
chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        details.requestHeaders.push({
            name: 'Referer', value: 'https://card.weibo.com/article/v3/editor'
        })
        details.requestHeaders.push({
            name: 'Origin', value: 'https://card.weibo.com'
        })
        return { requestHeaders: details.requestHeaders }
    },
    { urls: ["https://card.weibo.com/article/v3/*"] },
    ["blocking", "requestHeaders", "extraHeaders"]
)

// 百家号请求头配置
chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        details.requestHeaders.push({
            name: 'Referer', value: 'https://baijiahao.baidu.com/builder/rc/edit?type=news'
        })
        details.requestHeaders.push({
            name: 'Origin', value: 'https://baijiahao.baidu.com'
        })
        return { requestHeaders: details.requestHeaders }
    },
    { urls: ["https://baijiahao.baidu.com/builder/author/article/*"] },
    ["blocking", "requestHeaders", "extraHeaders"]
)

// B站头部配置
chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        details.requestHeaders.push({
            name: 'Referer', value: 'https://member.bilibili.com/article-text/home?'
        })
        details.requestHeaders.push({
            name: 'Origin', value: 'https://member.bilibili.com'
        })
        return { requestHeaders: details.requestHeaders }
    },
    { urls: ["https://api.bilibili.com/x/article/*"] },
    ["blocking", "requestHeaders", "extraHeaders"]
)