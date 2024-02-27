let CookieUtils = {
    obj2str: function (cookie) {
        let str = '';
        for (let i = 0; i < cookie.length; i++) {
            str += cookie[i].name;
            str += '=';
            str += cookie[i].value;
            str += '; '
        }
        return str;
    }
};

let TimeUtils = {
    format: (fmt, date) => {
        let ret;
        const opt = {
            "Y+": date.getFullYear().toString(),        // 年
            "m+": (date.getMonth() + 1).toString(),     // 月
            "d+": date.getDate().toString(),            // 日
            "H+": date.getHours().toString(),           // 时
            "M+": date.getMinutes().toString(),         // 分
            "S+": date.getSeconds().toString(),         // 秒
            "s+": date.getMilliseconds().toString()     // 毫秒
        };
        for (let k in opt) {
            ret = new RegExp("(" + k + ")").exec(fmt);
            if (ret) {
                fmt = fmt.replace(ret[1], (ret[1].length === 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
            }
        }
        return fmt;
    }
};